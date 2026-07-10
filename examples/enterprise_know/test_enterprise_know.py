import json
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent))

from enterprise_know import DEFAULT_DOC_DIR, HybridRetriever, evaluate, load_chunks, run_query


ROOT = Path(__file__).resolve().parent


class EnterpriseKnowTest(unittest.TestCase):
    def setUp(self):
        self.retriever = HybridRetriever(load_chunks(DEFAULT_DOC_DIR))

    def test_retrieves_hr_policy(self):
        results = self.retriever.search("差旅报销需要多久内提交？", department="all")
        self.assertTrue(results)
        self.assertTrue(results[0].chunk.id.startswith("hr_travel"))

    def test_department_acl_filters_restricted_docs(self):
        blocked = self.retriever.search("生产数据库访问需要什么审批？", department="hr")
        allowed = self.retriever.search("生产数据库访问需要什么审批？", department="engineering")

        self.assertFalse(any(result.chunk.id.startswith("security_access") for result in blocked))
        self.assertTrue(any(result.chunk.id.startswith("security_access") for result in allowed))

    def test_acl_query_does_not_fall_back_to_unrelated_accessible_docs(self):
        result = run_query("生产数据库访问需要什么审批？", department="hr")

        self.assertIn("未找到有权限访问且与问题相关的资料", result["answer"])
        self.assertEqual([], result["results"])

    def test_query_returns_cited_answer(self):
        result = run_query("VPN 登录失败怎么办？")
        self.assertIn("来源", result["answer"])
        self.assertIn("it_support", result["answer"])

    def test_eval_set_passes(self):
        report = evaluate()
        self.assertTrue(report["passed"], report)
        self.assertEqual(report["source_hit_rate"], 1.0)
        self.assertEqual(report["answer_term_hit_rate"], 1.0)
        self.assertGreaterEqual(report["case_count"], 8)
        for case in report["cases"]:
            self.assertIn("missing_terms", case)
            self.assertIn("expected_sources", case)
            self.assertIn("actual_sources", case)
            self.assertIn("failure_reason", case)
            self.assertTrue(case["passed"], case)

    def test_eval_set_covers_failure_and_safety_cases(self):
        case_types = {
            json.loads(line)["case_type"]
            for line in (ROOT / "eval_set.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        self.assertTrue(
            {"positive", "negative", "unauthorized", "conflicting-source", "missing-info", "irrelevant"}
            <= case_types
        )

    def test_failed_case_explains_missing_terms_and_source_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "failing.jsonl"
            path.write_text(
                json.dumps(
                    {
                        "case_type": "positive",
                        "query": "差旅报销需要在多久内提交？",
                        "department": "all",
                        "expected_behavior": "answer",
                        "expected_sources": ["nonexistent_policy"],
                        "required_terms": ["90 天"],
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            case = evaluate(path)["cases"][0]

        self.assertFalse(case["passed"])
        self.assertEqual(["90 天"], case["missing_terms"])
        self.assertEqual(["nonexistent_policy"], case["expected_sources"])
        self.assertTrue(case["actual_sources"])
        self.assertIn("expected source", case["failure_reason"])
        self.assertIn("missing required terms", case["failure_reason"])

    def test_eval_cli_returns_nonzero_when_a_case_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "failing.jsonl"
            path.write_text(
                '{"case_type":"positive","query":"天气","expected_behavior":"answer",'
                '"expected_sources":["weather"],"required_terms":["晴"]}\n',
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "enterprise_know.py"),
                    "--eval",
                    "--eval-set",
                    str(path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn('"passed": false', result.stdout)


if __name__ == "__main__":
    unittest.main()
