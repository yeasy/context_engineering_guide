from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


ROOT = Path(__file__).resolve().parent
DEFAULT_DOC_DIR = ROOT / "sample_docs"
DEFAULT_EVAL_SET = ROOT / "eval_set.jsonl"
MIN_QUERY_TERM_COVERAGE = 0.2


@dataclass(frozen=True)
class Chunk:
    id: str
    title: str
    content: str
    source: str
    department: str


@dataclass(frozen=True)
class RetrievalResult:
    chunk: Chunk
    bm25_score: float
    dense_score: float

    @property
    def score(self) -> float:
        return self.bm25_score + 0.6 * self.dense_score


def tokenize(text: str) -> List[str]:
    """Tokenize mixed Chinese and English text without external libraries."""
    raw_tokens = re.findall(r"[\u4e00-\u9fff]+|[A-Za-z0-9_]+", text.lower())
    tokens: List[str] = []

    for token in raw_tokens:
        if re.fullmatch(r"[\u4e00-\u9fff]+", token):
            tokens.extend(token)
            tokens.extend(token[i : i + 2] for i in range(max(0, len(token) - 1)))
            tokens.extend(token[i : i + 3] for i in range(max(0, len(token) - 2)))
        else:
            tokens.append(token)

    return tokens


def parse_front_matter(text: str) -> tuple[Dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    raw_meta = text[4:end]
    body = text[end + 5 :]
    metadata: Dict[str, str] = {}

    for line in raw_meta.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()

    return metadata, body


def extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def split_markdown(path: Path, max_chars: int = 360, overlap_chars: int = 80) -> List[Chunk]:
    metadata, body = parse_front_matter(path.read_text(encoding="utf-8"))
    title = extract_title(body, path.stem)
    department = metadata.get("department", "all")
    paragraphs = [block.strip() for block in re.split(r"\n\s*\n", body) if block.strip()]

    chunks: List[Chunk] = []
    current = ""

    def emit(text: str) -> None:
        text = text.strip()
        if not text:
            return
        chunk_number = len(chunks) + 1
        chunks.append(
            Chunk(
                id=f"{path.stem}#{chunk_number}",
                title=title,
                content=text,
                source=path.name,
                department=department,
            )
        )

    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= max_chars:
            current = candidate
            continue

        emit(current)
        prefix = current[-overlap_chars:] if overlap_chars and current else ""
        current = f"{prefix}\n\n{paragraph}".strip()

    emit(current)
    return chunks


def load_chunks(doc_dir: Path) -> List[Chunk]:
    chunks: List[Chunk] = []
    for path in sorted(doc_dir.glob("*.md")):
        chunks.extend(split_markdown(path))
    return chunks


class HybridRetriever:
    def __init__(self, chunks: Sequence[Chunk]):
        if not chunks:
            raise ValueError("At least one chunk is required.")

        self.chunks = list(chunks)
        self.chunk_tokens = [tokenize(chunk.content) for chunk in self.chunks]
        self.term_counts = [Counter(tokens) for tokens in self.chunk_tokens]
        self.doc_lengths = [len(tokens) for tokens in self.chunk_tokens]
        self.avg_doc_length = sum(self.doc_lengths) / len(self.doc_lengths)
        self.idf = self._build_idf(self.chunk_tokens)

    @staticmethod
    def _build_idf(tokenized_chunks: Sequence[Sequence[str]]) -> Dict[str, float]:
        document_count = len(tokenized_chunks)
        document_frequency: Counter[str] = Counter()
        for tokens in tokenized_chunks:
            document_frequency.update(set(tokens))

        return {
            term: math.log(1 + (document_count - freq + 0.5) / (freq + 0.5))
            for term, freq in document_frequency.items()
        }

    def _bm25(self, query_tokens: Sequence[str], index: int) -> float:
        k1 = 1.5
        b = 0.75
        score = 0.0
        counts = self.term_counts[index]
        doc_length = self.doc_lengths[index]

        for term in query_tokens:
            term_frequency = counts.get(term, 0)
            if term_frequency == 0:
                continue
            denominator = term_frequency + k1 * (
                1 - b + b * doc_length / self.avg_doc_length
            )
            score += self.idf.get(term, 0.0) * term_frequency * (k1 + 1) / denominator

        return score

    def _dense_proxy(self, query_tokens: Sequence[str], index: int) -> float:
        query_counts = Counter(query_tokens)
        doc_counts = self.term_counts[index]
        shared_terms = set(query_counts) & set(doc_counts)
        dot_product = sum(query_counts[term] * doc_counts[term] for term in shared_terms)
        query_norm = math.sqrt(sum(value * value for value in query_counts.values()))
        doc_norm = math.sqrt(sum(value * value for value in doc_counts.values()))
        if query_norm == 0 or doc_norm == 0:
            return 0.0
        return dot_product / (query_norm * doc_norm)

    @staticmethod
    def _can_read(chunk: Chunk, department: str) -> bool:
        return chunk.department in {"all", department}

    def search(self, query: str, department: str = "all", top_k: int = 4) -> List[RetrievalResult]:
        query_tokens = tokenize(query)
        query_term_set = set(query_tokens)
        scored: List[RetrievalResult] = []

        for index, chunk in enumerate(self.chunks):
            if not self._can_read(chunk, department):
                continue
            query_coverage = (
                len(query_term_set & set(self.chunk_tokens[index])) / len(query_term_set)
                if query_term_set else 0
            )
            if query_coverage < MIN_QUERY_TERM_COVERAGE:
                continue
            result = RetrievalResult(
                chunk=chunk,
                bm25_score=self._bm25(query_tokens, index),
                dense_score=self._dense_proxy(query_tokens, index),
            )
            if result.score > 0:
                scored.append(result)

        return sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]


def split_sentences(text: str) -> List[str]:
    text = "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("#")
    )
    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[。！？.!?])\s*", text)
        if sentence.strip()
    ]


def assemble_context(results: Sequence[RetrievalResult], max_chars: int = 900) -> str:
    parts: List[str] = []
    used_chars = 0

    for result in results:
        snippet = (
            f"[{result.chunk.id} | {result.chunk.title} | {result.chunk.source}]\n"
            f"{result.chunk.content}"
        )
        if used_chars + len(snippet) > max_chars:
            continue
        parts.append(snippet)
        used_chars += len(snippet)

    return "\n\n".join(parts)


def answer_from_context(query: str, results: Sequence[RetrievalResult]) -> str:
    if not results:
        return "未找到有权限访问且与问题相关的资料。"

    query_terms = set(tokenize(query))
    candidates: List[tuple[int, float, str, str]] = []

    for result in results:
        for sentence in split_sentences(result.chunk.content):
            overlap = len(query_terms & set(tokenize(sentence)))
            if overlap:
                candidates.append((overlap, result.score, sentence, result.chunk.id))

    if not candidates:
        return "检索到了候选资料，但未找到足够明确的句子回答该问题。"

    candidates.sort(reverse=True)
    selected: List[str] = []
    sources: List[str] = []

    for _, _, sentence, source_id in candidates:
        if sentence in selected:
            continue
        selected.append(sentence)
        sources.append(source_id)
        if len(selected) == 2:
            break

    citation = " ".join(f"[来源: {source}]" for source in dict.fromkeys(sources))
    return f"{'；'.join(selected)} {citation}"


def run_query(query: str, department: str = "all", top_k: int = 4) -> Dict[str, object]:
    retriever = HybridRetriever(load_chunks(DEFAULT_DOC_DIR))
    results = retriever.search(query, department=department, top_k=top_k)
    return {
        "query": query,
        "department": department,
        "answer": answer_from_context(query, results),
        "context": assemble_context(results),
        "results": [
            {
                "id": result.chunk.id,
                "source": result.chunk.source,
                "title": result.chunk.title,
                "score": round(result.score, 4),
                "bm25_score": round(result.bm25_score, 4),
                "dense_score": round(result.dense_score, 4),
            }
            for result in results
        ],
    }


def iter_jsonl(path: Path) -> Iterable[Dict[str, object]]:
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc


def evaluate(path: Path = DEFAULT_EVAL_SET) -> Dict[str, object]:
    cases = list(iter_jsonl(path))
    retriever = HybridRetriever(load_chunks(DEFAULT_DOC_DIR))
    reports: List[Dict[str, object]] = []

    for case in cases:
        query = str(case["query"])
        department = str(case.get("department", "all"))
        case_type = str(case.get("case_type", "positive"))
        expected_behavior = str(case.get("expected_behavior", "answer"))
        expected_sources = [str(item) for item in case.get("expected_sources", [])]
        forbidden_sources = [str(item) for item in case.get("forbidden_sources", [])]
        required_terms = [str(item) for item in case.get("required_terms", [])]
        results = retriever.search(query, department=department, top_k=4)
        answer = answer_from_context(query, results)
        result_ids = [result.chunk.id for result in results]

        source_hit = (
            all(
                any(result_id.startswith(expected) for result_id in result_ids)
                for expected in expected_sources
            )
            if expected_sources
            else not result_ids
        )
        missing_terms = [term for term in required_terms if term not in answer]
        term_hit = not missing_terms
        forbidden_hits = [
            source
            for source in forbidden_sources
            if any(result_id.startswith(source) for result_id in result_ids)
        ]
        behavior_hit = (
            not result_ids if expected_behavior == "abstain" else bool(result_ids)
        )

        failures: List[str] = []
        if not source_hit:
            failures.append("expected source not retrieved")
        if missing_terms:
            failures.append(f"missing required terms: {', '.join(missing_terms)}")
        if forbidden_hits:
            failures.append(f"forbidden source retrieved: {', '.join(forbidden_hits)}")
        if not behavior_hit:
            failures.append(
                "expected abstention but retrieved sources"
                if expected_behavior == "abstain"
                else "expected answer but no supported result"
            )
        passed = source_hit and term_hit and not forbidden_hits and behavior_hit

        reports.append(
            {
                "case_type": case_type,
                "query": query,
                "expected_behavior": expected_behavior,
                "source_hit": source_hit,
                "term_hit": term_hit,
                "missing_terms": missing_terms,
                "expected_sources": expected_sources,
                "actual_sources": result_ids,
                "failure_reason": "; ".join(failures) if failures else None,
                "passed": passed,
                "answer": answer,
                "results": result_ids,
            }
        )

    total = len(reports)
    source_hit_rate = (
        sum(1 for item in reports if item["source_hit"]) / total if total else 0.0
    )
    answer_term_hit_rate = (
        sum(1 for item in reports if item["term_hit"]) / total if total else 0.0
    )

    return {
        "case_count": total,
        "source_hit_rate": round(source_hit_rate, 4),
        "answer_term_hit_rate": round(answer_term_hit_rate, 4),
        "passed": bool(reports) and all(bool(item["passed"]) for item in reports),
        "cases": reports,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="EnterpriseKnow local RAG lab.")
    parser.add_argument("--query", help="Question to ask the local knowledge base.")
    parser.add_argument("--department", default="all", help="Department ACL to apply.")
    parser.add_argument("--top-k", type=int, default=4)
    parser.add_argument("--eval", action="store_true", help="Run the bundled eval set.")
    parser.add_argument(
        "--eval-set",
        type=Path,
        default=DEFAULT_EVAL_SET,
        help="JSONL eval set to use with --eval.",
    )
    args = parser.parse_args()

    if args.eval:
        report = evaluate(args.eval_set)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        raise SystemExit(0 if report["passed"] else 1)

    query = args.query or "差旅报销需要在多久内提交？"
    print(
        json.dumps(
            run_query(query, department=args.department, top_k=args.top_k),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
