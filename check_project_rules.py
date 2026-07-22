import os
import re
import sys
import argparse
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import unquote, urlparse


VOLATILE_FACTS = Path("appendix/volatile_facts.md")

ROOT = Path(__file__).resolve().parent
SKIP_DIRS = {
    ".agent",
    ".git",
    ".mdpress",
    "_book",
    "_site",
    "dist",
    "node_modules",
}
LINK_RE = re.compile(r"(!?)\[[^\]]*\]\(([^)\s]+(?:\s+\"[^\"]*\")?)\)")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


VOLATILE_FACTS = Path("appendix/volatile_facts.md")


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def strip_fenced_blocks(text: str) -> str:
    output: list[str] = []
    in_fence = False
    fence_marker = ""
    fence_len = 0
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)
            char = marker[0]
            length = len(marker)
            if not in_fence:
                in_fence = True
                fence_marker = char
                fence_len = length
            elif char == fence_marker and length >= fence_len:
                in_fence = False
            output.append("")
            continue
        output.append("" if in_fence else line)
    return "\n".join(output)


def check_fences(path: Path, text: str) -> list[str]:
    issues: list[str] = []
    stack: list[tuple[str, int, int]] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        match = FENCE_RE.match(line)
        if not match:
            continue
        marker = match.group(1)
        char = marker[0]
        length = len(marker)
        if not stack:
            stack.append((char, length, line_no))
            continue
        open_char, open_len, _ = stack[-1]
        if char == open_char and length >= open_len:
            stack.pop()
        else:
            stack.append((char, length, line_no))
    for _, _, line_no in stack:
        issues.append(f"{path.relative_to(ROOT)}:{line_no}: unclosed fenced code block")
    return issues


def is_local_target(target: str) -> bool:
    parsed = urlparse(target)
    return not parsed.scheme and not parsed.netloc and not target.startswith("#")


def normalize_target(raw_target: str) -> str:
    target = raw_target.strip()
    if " " in target and target.count('"') >= 2:
        target = target.split(" ", 1)[0]
    return unquote(target.split("#", 1)[0])


def check_links(path: Path, text: str) -> list[str]:
    issues: list[str] = []
    body = strip_fenced_blocks(text)
    for match in LINK_RE.finditer(body):
        raw_target = match.group(2).strip()
        target = normalize_target(raw_target)
        if not target or not is_local_target(raw_target):
            continue
        target_path = (path.parent / target).resolve()
        try:
            target_path.relative_to(ROOT)
        except ValueError:
            continue
        if not target_path.exists():
            line_no = body[: match.start()].count("\n") + 1
            issues.append(
                f"{path.relative_to(ROOT)}:{line_no}: missing local link target: {raw_target}"
            )
    return issues


def check_summary_links() -> list[str]:
    summary = ROOT / "SUMMARY.md"
    if not summary.exists():
        return []
    return check_links(summary, summary.read_text(encoding="utf-8", errors="ignore"))


def check_volatile_facts(filepath=VOLATILE_FACTS, today=None):
    """Validate the dated snapshot that contains deliberately volatile claims."""
    path = Path(filepath)
    current_date = today or date.today()
    issues = []

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{path} [Volatile facts] Cannot read ledger: {exc}"]

    metadata = re.search(
        r"`verified_at`:\s*(\d{4}-\d{2}-\d{2})\s*·\s*"
        r"`expires_at`:\s*(\d{4}-\d{2}-\d{2})\s*·\s*"
        r"`ttl_days`:\s*(\d+)",
        content,
    )
    if metadata is None:
        return [
            f"{path} [Volatile facts] Missing verified_at, expires_at, or ttl_days metadata."
        ]

    try:
        verified_at = datetime.strptime(metadata.group(1), "%Y-%m-%d").date()
        expires_at = datetime.strptime(metadata.group(2), "%Y-%m-%d").date()
        ttl_days = int(metadata.group(3))
    except ValueError as exc:
        return [f"{path} [Volatile facts] Invalid metadata: {exc}"]

    if ttl_days != 30 or expires_at - verified_at != timedelta(days=30):
        issues.append(
            f"{path} [Volatile facts] Snapshot TTL must be exactly 30 days."
        )
    if verified_at > current_date:
        issues.append(
            f"{path} [Volatile facts] verified_at is in the future: {verified_at}."
        )
    if current_date > expires_at:
        issues.append(
            f"{path} [Volatile facts] Snapshot expired on {expires_at}."
        )

    statuses = re.findall(
        r"<!--\s*volatile-status:\s+id=[^\s]+\s+status=([^\s]+)\s*-->",
        content,
    )
    if not statuses:
        issues.append(f"{path} [Volatile facts] Missing volatile-status marker.")
    for status in statuses:
        if status == "open-conflict":
            issues.append(f"{path} [Volatile facts] Ledger has an unresolved conflict.")
        elif status not in {"current", "resolved-conflict"}:
            issues.append(
                f"{path} [Volatile facts] Unsupported volatile-status: {status}."
            )

    return issues


def check_volatile_facts(filepath=VOLATILE_FACTS, today=None):
    """Validate the dated snapshot that contains deliberately volatile claims."""
    path = Path(filepath)
    current_date = today or date.today()
    issues = []

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{path} [Volatile facts] Cannot read ledger: {exc}"]

    metadata = re.search(
        r"`verified_at`:\s*(\d{4}-\d{2}-\d{2})\s*·\s*"
        r"`expires_at`:\s*(\d{4}-\d{2}-\d{2})\s*·\s*"
        r"`ttl_days`:\s*(\d+)",
        content,
    )
    if metadata is None:
        return [
            f"{path} [Volatile facts] Missing verified_at, expires_at, or ttl_days metadata."
        ]

    try:
        verified_at = datetime.strptime(metadata.group(1), "%Y-%m-%d").date()
        expires_at = datetime.strptime(metadata.group(2), "%Y-%m-%d").date()
        ttl_days = int(metadata.group(3))
    except ValueError as exc:
        return [f"{path} [Volatile facts] Invalid metadata: {exc}"]

    if ttl_days != 30 or expires_at - verified_at != timedelta(days=30):
        issues.append(
            f"{path} [Volatile facts] Snapshot TTL must be exactly 30 days."
        )
    if verified_at > current_date:
        issues.append(
            f"{path} [Volatile facts] verified_at is in the future: {verified_at}."
        )
    if current_date > expires_at:
        issues.append(
            f"{path} [Volatile facts] Snapshot expired on {expires_at}."
        )

    statuses = re.findall(
        r"<!--\s*volatile-status:\s+id=[^\s]+\s+status=([^\s]+)\s*-->",
        content,
    )
    if not statuses:
        issues.append(f"{path} [Volatile facts] Missing volatile-status marker.")
    for status in statuses:
        if status == "open-conflict":
            issues.append(f"{path} [Volatile facts] Ledger has an unresolved conflict.")
        elif status not in {"current", "resolved-conflict"}:
            issues.append(
                f"{path} [Volatile facts] Unsupported volatile-status: {status}."
            )

    return issues

def check_trailing_newline(content, filepath, issues):
    if not content.endswith('\n') or content.endswith('\n\n'):
        issues.append(f"{filepath} [Rule 1.4] File must end with exactly one newline.")

def check_file(filepath, issues):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    check_trailing_newline(content, filepath, issues)

    # Pre-process lines to identify code blocks
    in_code_block = False
    code_block_level = 0
    in_code_block_lines = []

    for line in lines:
        stripped = line.strip()
        match = re.match(r'^(`{3,})', stripped)
        if match:
            level = len(match.group(1))
            if not in_code_block:
                in_code_block = True
                code_block_level = level
                in_code_block_lines.append(True)
            elif level == code_block_level:
                in_code_block = False
                code_block_level = 0
                in_code_block_lines.append(True)
            else:
                in_code_block_lines.append(in_code_block)
        else:
            in_code_block_lines.append(in_code_block)

    pattern_quotes = r'"[^"]*?[\u4e00-\u9fa5]+[^"]*?"'
    header_pattern = re.compile(r'^(#{1,6})\s+(.*)')

    last_level = 0

    for i, line in enumerate(lines):
        if in_code_block_lines[i]:
            continue

        # Rule 3.3
        top_level = Path(filepath).parts[0]
        if '参考资料' in line and top_level.startswith('0') and re.search(r'https?://|\]\(', line):
            issues.append(f"{filepath}:{i+1} [Rule 3.3] Reference links should be centralized in appendix.")

        # Rule 1.6: Chinese Quotes
        if re.search(pattern_quotes, line) and not '<' in line:
            issues.append(f"{filepath}:{i+1} [Rule 1.6] Chinese content should use Chinese curly quotes.")

        # Rule 1.1: Bold spacing
        clean_line = line.replace('\\*\\*', '\x00')
        parts = clean_line.split('**')
        # Check all odd indices (text inside ** **)
        for idx in range(1, len(parts), 2):
            # If the length of parts is even, the last split means an unclosed '**', skip it.
            if idx == len(parts) - 1 and len(parts) % 2 == 0:
                continue
            inside_text = parts[idx]
            if inside_text and (inside_text[0] in ' \t' or inside_text[-1] in ' \t'):
                issues.append(f"{filepath}:{i+1} [Rule 1.1] Spaces inside bold markers.")
                break

        match = header_pattern.match(line)
        if match:
            level = len(match.group(1))
            text = match.group(2)

            # Rule 1.2 Header Spacing
            if i + 1 < len(lines):
                if lines[i+1].strip() != '':
                    if header_pattern.match(lines[i+1]) is None:
                        issues.append(f"{filepath}:{i+1} [Rule 1.2] Missing blank line after header.")
                elif i + 2 < len(lines) and lines[i+2].strip() == '':
                    issues.append(f"{filepath}:{i+1} [Rule 1.2] Multiple blank lines after header.")

            # Rule 1.3 Hierarchy
            if last_level > 0 and level - last_level > 1:
                 issues.append(f"{filepath}:{i+1} [Rule 1.3] Header level skipped from H{last_level} to H{level}.")
            last_level = level

            # Rule 2.3 English terms in parens
            if re.search(r'\([a-zA-Z\s]+\)', text) and not re.search(r'(API|LLM|AI|RAG)', text):
                 issues.append(f"{filepath}:{i+1} [Rule 2.3] Header contains English parentheses: {text}")

    # Rule 2.2 File Header Levels
    first_header = None
    for line in lines:
        match = re.search(r'^(#{1,6})\s', line)
        if match:
            first_header = match.group(1)
            break

    basename = os.path.basename(filepath)
    if first_header:
        if basename.lower() == 'readme.md' and len(first_header) != 1:
            issues.append(f"{filepath} [Rule 2.2] First header in README must be H1.")
        elif re.match(r'^\d+\.\d+', basename) and len(first_header) != 2:
            issues.append(f"{filepath} [Rule 2.2] First header in section file must be H2.")

def main():
    parser = argparse.ArgumentParser(description='Check project markdown rules.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show all scanned files')
    args = parser.parse_args()

    os.chdir(Path(__file__).resolve().parent)
    repo_dir = '.'
    issues = []
    scanned_files = 0

    issues.extend(check_volatile_facts())

    # 围栏闭合、本地链接可达、SUMMARY 覆盖——12 个兄弟仓库都有，本仓库此前缺失
    md_files = iter_markdown_files()
    for md in md_files:
        md_text = md.read_text(encoding='utf-8', errors='ignore')
        issues.extend(check_fences(md, md_text))
        issues.extend(check_links(md, md_text))
    issues.extend(check_summary_links())

    for root, dirs, files in os.walk(repo_dir):
        if any(skip in root.split(os.sep) for skip in ['.git', '.obsidian', '_images', '__pycache__', '.agent', 'node_modules', '_book']):
            continue
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                if args.verbose:
                    print(f"Scanning {path}...")
                check_file(path, issues)
                scanned_files += 1

    if issues:
        print(f"Found {len(issues)} rule violations across {scanned_files} files:")
        for issue in issues:
            print(issue)
        sys.exit(1)
    else:
        print(f"All {scanned_files} files passed checks!")
        sys.exit(0)

if __name__ == '__main__':
    main()
