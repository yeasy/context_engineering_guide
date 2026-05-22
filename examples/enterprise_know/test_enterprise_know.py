import unittest
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent))

from enterprise_know import DEFAULT_DOC_DIR, HybridRetriever, evaluate, load_chunks, run_query


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

    def test_query_returns_cited_answer(self):
        result = run_query("VPN 登录失败怎么办？")
        self.assertIn("来源", result["answer"])
        self.assertIn("it_support", result["answer"])

    def test_eval_set_passes(self):
        report = evaluate()
        self.assertTrue(report["passed"], report)
        self.assertEqual(report["source_hit_rate"], 1.0)
        self.assertEqual(report["answer_term_hit_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
