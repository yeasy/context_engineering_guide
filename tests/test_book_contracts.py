from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

import check_project_rules as rules


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "appendix" / "volatile_facts.md"


class VolatileFactsTests(unittest.TestCase):
    def write_ledger(
        self,
        directory: str,
        *,
        verified: str = "2026-07-10",
        expires: str = "2026-08-09",
        ttl: int = 30,
        status: str = "current",
    ) -> Path:
        path = Path(directory) / "facts.md"
        path.write_text(
            "# Facts\n\n"
            f"> `verified_at`: {verified} · `expires_at`: {expires} · `ttl_days`: {ttl}\n\n"
            f"<!-- volatile-status: id=models status={status} -->\n",
            encoding="utf-8",
        )
        return path

    def check(self, path: Path, today: date) -> list[str]:
        self.assertTrue(
            hasattr(rules, "check_volatile_facts"),
            "check_project_rules.py must define check_volatile_facts()",
        )
        return rules.check_volatile_facts(path, today)

    def test_valid_30_day_ledger_is_current_through_expiry(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_ledger(directory)
            self.assertEqual(self.check(path, date(2026, 7, 10)), [])
            self.assertEqual(self.check(path, date(2026, 8, 9)), [])

    def test_future_verification_and_expired_ledgers_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            future = self.write_ledger(directory, verified="2026-07-11", expires="2026-08-10")
            self.assertTrue(any("future" in issue for issue in self.check(future, date(2026, 7, 10))))
            expired = self.write_ledger(directory, verified="2026-06-09", expires="2026-07-09")
            self.assertTrue(any("expired" in issue for issue in self.check(expired, date(2026, 7, 10))))

    def test_ttl_must_be_exactly_30_days(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_ledger(directory, expires="2026-09-08", ttl=60)
            issues = self.check(path, date(2026, 7, 10))
            self.assertTrue(any("30 days" in issue for issue in issues), issues)

    def test_open_conflict_fails_and_resolved_conflict_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            open_path = self.write_ledger(directory, status="open-conflict")
            self.assertTrue(any("unresolved conflict" in issue for issue in self.check(open_path, date(2026, 7, 10))))
            resolved = self.write_ledger(directory, status="resolved-conflict")
            self.assertEqual(self.check(resolved, date(2026, 7, 10)), [])

    def test_repository_snapshot_tracks_current_catalog_and_resolved_openai_transition(self):
        text = LEDGER.read_text(encoding="utf-8")
        for marker in (
            "`verified_at`: 2026-07-10",
            "`expires_at`: 2026-08-09",
            "`ttl_days`: 30",
            "id=openai-models status=current",
            "id=openai-gpt-5-6-availability status=resolved-conflict",
            "GPT-5.6 Sol",
            "GPT-5.6 Terra",
            "GPT-5.6 Luna",
            "GPT-5.3-Codex",
            "Claude Fable 5",
            "Claude Sonnet 5",
            "Gemini 3.5 Flash",
            "https://developers.openai.com/api/docs/models",
            "https://developers.openai.com/api/docs/models/gpt-5.6-sol",
            "https://developers.openai.com/api/docs/models/gpt-5.6-terra",
            "https://developers.openai.com/api/docs/models/gpt-5.6-luna",
            "https://developers.openai.com/api/docs/changelog",
            "https://openai.com/index/previewing-gpt-5-6-sol/",
            "2026-06-26",
            "2026-07-09",
            "https://www.anthropic.com/news/redeploying-fable-5",
            "https://www.anthropic.com/news/claude-sonnet-5",
            "https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash",
        ):
            self.assertIn(marker, text)
        current_snapshot = text.split("## E.1 当前模型快照", 1)[1].split("## E.2 冲突记录", 1)[0]
        for current_source in (
            "https://developers.openai.com/api/docs/models",
            "https://developers.openai.com/api/docs/models/gpt-5.6-sol",
            "https://developers.openai.com/api/docs/models/gpt-5.6-terra",
            "https://developers.openai.com/api/docs/models/gpt-5.6-luna",
        ):
            self.assertIn(current_source, current_snapshot)
        for stale_claim in ("推荐生产旗舰模型 GPT-5.5", "受信合作方开放的 preview"):
            self.assertNotIn(stale_claim, current_snapshot)
        conflict_record = text.split("## E.2 冲突记录", 1)[1].split("## E.3 其他快变事实入口", 1)[0]
        for transition_evidence in (
            "id=openai-gpt-5-6-availability status=resolved-conflict",
            "https://openai.com/index/previewing-gpt-5-6-sol/",
            "https://developers.openai.com/api/docs/changelog",
            "2026-06-26",
            "2026-07-09",
            "后续",
            "取代",
        ):
            self.assertIn(transition_evidence, conflict_record)
        self.assertEqual(self.check(LEDGER, date(2026, 7, 10)), [])

    def test_mythos_access_is_current_across_chapters_and_keeps_restoration_history(self):
        current_surfaces = {
            "2.1": (ROOT / "02_llm_basics" / "2.1_how_llm_works.md").read_text(encoding="utf-8"),
            "2.4": (ROOT / "02_llm_basics" / "2.4_model_comparison.md").read_text(encoding="utf-8"),
        }
        ledger = LEDGER.read_text(encoding="utf-8")
        current_surfaces["ledger current snapshot"] = ledger.split(
            "## E.1 当前模型快照", 1
        )[1].split("## E.2 冲突记录", 1)[0]

        for label, text in current_surfaces.items():
            with self.subTest(surface=label):
                for marker in ("Mythos 5", "非普遍可用", "Project Glasswing", "获批客户"):
                    self.assertIn(marker, text)
                self.assertRegex(text, r"(有限|邀请|受限).{0,8}(开放|可用)")
                self.assertNotIn("已恢复正常提供", text)

        conflict_record = ledger.split("## E.2 冲突记录", 1)[1].split(
            "## E.3 其他快变事实入口", 1
        )[0]
        for marker in ("2026-07-01", "一组美国机构", "当前模型文档"):
            self.assertIn(marker, conflict_record)

    def test_main_checker_enforces_volatile_facts(self):
        source = (ROOT / "check_project_rules.py").read_text(encoding="utf-8")
        self.assertIn("issues.extend(check_volatile_facts())", source)


class LongHorizonContractTests(unittest.TestCase):
    def test_control_contract_has_all_six_fields(self):
        text = (ROOT / "10_advanced" / "10.8_long_horizon_tasks.md").read_text(encoding="utf-8").lower()
        for field in ("trigger", "goal", "verification", "stop", "memory", "human gate"):
            self.assertIn(field, text)

    def test_context_harness_external_loop_chapter_and_navigation_exist(self):
        chapter = ROOT / "10_advanced" / "10.9_context_harness_external_loop.md"
        self.assertTrue(chapter.is_file())
        text = chapter.read_text(encoding="utf-8")
        for marker in ("Context", "Harness", "External Loop", "控制契约", "人类门控"):
            self.assertIn(marker, text)
        summary = (ROOT / "SUMMARY.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        advanced = (ROOT / "10_advanced" / "README.md").read_text(encoding="utf-8")
        relative = "10_advanced/10.9_context_harness_external_loop.md"
        self.assertIn(relative, summary)
        self.assertIn(relative, readme)
        self.assertIn("10.9_context_harness_external_loop.md", advanced)

    def test_model_comparison_routes_volatile_claims_to_ledger(self):
        text = (ROOT / "02_llm_basics" / "2.4_model_comparison.md").read_text(encoding="utf-8")
        self.assertIn("../appendix/volatile_facts.md", text)
        for marker in ("GPT-5.6 Sol", "GPT-5.6 Terra", "GPT-5.6 Luna", "GPT-5.3-Codex", "Claude Sonnet 5", "Gemini 3.5 Flash"):
            self.assertIn(marker, text)
        for stale_claim in ("推荐生产旗舰 GPT-5.5", "受限 preview GPT-5.6"):
            self.assertNotIn(stale_claim, text)


if __name__ == "__main__":
    unittest.main()
