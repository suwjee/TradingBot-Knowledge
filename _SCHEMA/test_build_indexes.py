"""Regression checks for fixture-source review classification."""
from __future__ import annotations

from contextlib import redirect_stderr
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch

from _SCHEMA import build_indexes


VAULT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_SOURCE = Path("07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FixtureSourceReviewTests(unittest.TestCase):
    """Exercise the builder against isolated, source-mismatched Vault copies."""

    def copied_vault(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        target = Path(temporary.name) / "vault"

        def ignore(directory: str, names: list[str]) -> set[str]:
            relative = Path(directory).resolve().relative_to(VAULT_ROOT)
            blocked = {".git", "_GENERATED", "__pycache__"}
            if relative.parts[:2] == ("08_DATA", "Raw"):
                blocked.update(name for name in names if name.endswith(".json"))
            return blocked.intersection(names)

        shutil.copytree(VAULT_ROOT, target, ignore=ignore)
        return temporary, target

    @staticmethod
    def fixture_notes(root: Path) -> list[Path]:
        return sorted(
            path
            for path in (root / "07_VALIDATION/Fixtures").rglob("*.md")
            if "source_fixture_sha256:" in path.read_text(encoding="utf-8-sig")
        )

    @staticmethod
    def fixture_hashes(notes: list[Path]) -> dict[Path, str]:
        return {
            path: next(
                line.split(": ", 1)[1]
                for line in path.read_text(encoding="utf-8-sig").splitlines()
                if line.startswith("source_fixture_sha256:")
            )
            for path in notes
        }

    @staticmethod
    def mark_pending_manual_review(notes: list[Path]) -> None:
        for path in notes:
            content = path.read_text(encoding="utf-8-sig")
            path.write_text(
                content.replace(
                    "source_fixture_sha256:",
                    "source_fixture_review: \"pending-manual-review\"\nsource_fixture_sha256:",
                    1,
                ),
                encoding="utf-8",
            )

    @staticmethod
    def replace_frontmatter_value(path: Path, field: str, value: str) -> None:
        content = path.read_text(encoding="utf-8-sig")
        updated, count = re.subn(
            rf"(?m)^{re.escape(field)}: .+$",
            f"{field}: {value}",
            content,
            count=1,
        )
        if count != 1:
            raise AssertionError(f"Missing frontmatter field: {field}")
        path.write_text(updated, encoding="utf-8")

    @staticmethod
    def mutate_fixture_source_and_manifest(root: Path) -> None:
        fixture_source = root / FIXTURE_SOURCE
        fixture_source.write_text(
            fixture_source.read_text(encoding="utf-8-sig")
            + "\n<!-- isolated fixture-source mutation for verification -->\n",
            encoding="utf-8",
        )
        manifest_path = root / "_INDEX/source-hashes.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        evidence = next(
            row
            for row in manifest["supporting_files"]
            if row["path"] == FIXTURE_SOURCE.as_posix()
        )
        evidence["sha256"] = sha256(fixture_source)
        evidence["bytes"] = fixture_source.stat().st_size
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def run_builder(root: Path) -> tuple[int, str]:
        stderr = io.StringIO()
        with patch.object(build_indexes, "ROOT", root), redirect_stderr(stderr):
            result = build_indexes.build(check=True, mode="knowledge")
        return result, stderr.getvalue()

    def test_undeclared_fixture_source_hash_mismatch_is_an_error(self) -> None:
        temporary, root = self.copied_vault()
        self.addCleanup(temporary.cleanup)
        self.mutate_fixture_source_and_manifest(root)

        result, stderr = self.run_builder(root)

        self.assertEqual(1, result)
        self.assertIn("Fixture source SHA mismatch", stderr)

    def test_declared_fixture_source_hash_mismatch_is_known_pending_without_sha_rewrite(self) -> None:
        temporary, root = self.copied_vault()
        self.addCleanup(temporary.cleanup)
        notes = self.fixture_notes(root)
        original_hashes = self.fixture_hashes(notes)
        self.assertEqual(22, len(notes))
        self.mark_pending_manual_review(notes)
        self.mutate_fixture_source_and_manifest(root)

        result, stderr = self.run_builder(root)

        self.assertEqual(0, result)
        self.assertIn("KNOWN_PENDING", stderr)
        self.assertEqual(original_hashes, self.fixture_hashes(notes))

    def test_matching_declared_fixture_source_has_no_known_pending_result(self) -> None:
        temporary, root = self.copied_vault()
        self.addCleanup(temporary.cleanup)
        notes = self.fixture_notes(root)
        self.mark_pending_manual_review(notes)

        result, stderr = self.run_builder(root)

        self.assertEqual(0, result)
        self.assertNotIn("KNOWN_PENDING", stderr)

    def test_declared_fixture_source_hash_mismatch_keeps_line_check_strict(self) -> None:
        temporary, root = self.copied_vault()
        self.addCleanup(temporary.cleanup)
        notes = self.fixture_notes(root)
        self.mark_pending_manual_review(notes)
        self.replace_frontmatter_value(notes[0], "source_fixture_line", "999999")
        self.mutate_fixture_source_and_manifest(root)

        result, stderr = self.run_builder(root)

        self.assertEqual(1, result)
        self.assertIn("KNOWN_PENDING", stderr)
        self.assertIn("Fixture source line out of range", stderr)

    def test_declared_fixture_source_hash_mismatch_keeps_heading_check_strict(self) -> None:
        temporary, root = self.copied_vault()
        self.addCleanup(temporary.cleanup)
        notes = self.fixture_notes(root)
        self.mark_pending_manual_review(notes)
        self.replace_frontmatter_value(notes[0], "source_fixture_line", "1")
        self.mutate_fixture_source_and_manifest(root)

        result, stderr = self.run_builder(root)

        self.assertEqual(1, result)
        self.assertIn("KNOWN_PENDING", stderr)
        self.assertIn("Fixture source heading mismatch", stderr)

    def test_order_a_cannot_lose_accepted_regression_metadata(self) -> None:
        temporary, root = self.copied_vault()
        self.addCleanup(temporary.cleanup)
        self.replace_frontmatter_value(
            root / "04_ALGORITHMS/Order/Order-A.md",
            "valid_for_regression_baseline",
            "false",
        )

        result, stderr = self.run_builder(root)

        self.assertEqual(1, result)
        self.assertIn(
            "Accepted Order_A metadata mismatch: algorithm.order.a.valid_for_regression_baseline",
            stderr,
        )

    def test_source_fixture_review_only_accepts_pending_manual_review(self) -> None:
        temporary, root = self.copied_vault()
        self.addCleanup(temporary.cleanup)
        note = self.fixture_notes(root)[0]
        content = note.read_text(encoding="utf-8-sig")
        note.write_text(
            content.replace(
                "source_fixture_sha256:",
                "source_fixture_review: \"verified\"\nsource_fixture_sha256:",
                1,
            ),
            encoding="utf-8",
        )

        result, stderr = self.run_builder(root)

        self.assertEqual(1, result)
        self.assertIn("'pending-manual-review' was expected", stderr)

    def test_machine_owned_generated_markdown_is_not_a_canonical_note(self) -> None:
        temporary, root = self.copied_vault()
        self.addCleanup(temporary.cleanup)
        generated = root / "_GENERATED/Fixture-Catalog-Full.md"
        generated.parent.mkdir()
        generated.write_text("machine-owned generated artifact\n", encoding="utf-8")

        result, stderr = self.run_builder(root)

        self.assertEqual(0, result)
        self.assertNotIn("_GENERATED/Fixture-Catalog-Full.md", stderr)


if __name__ == "__main__":
    unittest.main()
