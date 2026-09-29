from __future__ import annotations
from contextlib import redirect_stdout, redirect_stderr
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from _SCHEMA import build_indexes

DRAFT = Path(__file__).resolve().parents[1]
TEST_RUNS = Path(os.environ.get("TRADINGBOT_SCHEMA_TEST_ROOT",
                              str(Path(tempfile.gettempdir()) / "tradingbot-vault-schema-tests")))
REL = "06_SOURCE/Code/engine/pipeline/probe.py"
CODE = b'"""Synthetic metadata compatibility evidence; no trading rules."""\n__version__ = "1.0.0"\ndef probe(value):\n    return value\n'

def pin(path):
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

def write_note(path, fields, body="Synthetic metadata compatibility test.\n"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\n" + "\n".join(key + ": " + json.dumps(value) for key, value in fields.items())
                    + "\n---\n" + body, encoding="utf-8")

class CurrentVaultValidationTests(unittest.TestCase):
    def setUp(self):
        TEST_RUNS.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=TEST_RUNS)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(DRAFT, self.root / "_SCHEMA")
        source = self.root / REL
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(CODE)
        common = {"status": "active", "authority": "executable", "related_entities": [],
                  "source_reference": [REL + "#L1"]}
        def add(ident, kind, path, **extra):
            write_note(self.root / path, {"id": ident, "type": kind, "title": ident, **common, **extra})
        add("system.authority", "system", "00_SYSTEM/AUTHORITY_MODEL.md",
            status="canonical", authority="normative", source_reference=[])
        add("source.probe", "source", "06_SOURCE/Modules/probe.md", source_path=REL,
            mirror=REL, sha256=pin(source)["sha256"],
            implements=["algorithm.order.b", "algorithm.orderaudit"])
        add("algorithm.order.b", "algorithm", "04_ALGORITHMS/Order/Order-B.md",
            implemented_by=["source.probe"])
        add("algorithm.orderaudit", "algorithm", "04_ALGORITHMS/Order/OrderAudit.md",
            implemented_by=["source.probe"])
        for kind in ("workflow", "version", "decision"):
            add(kind + ".current", kind, kind + "/Current.md")
        refs = []
        for direction in ("Bullish", "Bearish"):
            name = direction + "_Current.md"
            local = "06_SOURCE/Code/engine/algorithms/" + name
            path = self.root / local
            path.parent.mkdir(parents=True, exist_ok=True)
            fence = bytes([96]) * 4
            path.write_bytes(b"# Synthetic reference for metadata tests\n"
                             b"<!-- EXACT-SOURCE-BEGIN:pipeline/probe.py -->\n" + fence + b"python\n"
                             + CODE + fence + b"\n<!-- EXACT-SOURCE-END:pipeline/probe.py -->\n")
            refs.append({"id": direction.lower() + "_current", "name": name,
                         "direction": direction, "repository_relative_path": "engine/algorithms/" + name,
                         "local_path": local, "version": "1.0.0", **pin(path)})
        registry = self.root / "06_SOURCE/References/registry.json"
        write_json(registry, {"schema_version": 1, "references": refs})
        self.manifest = {"schema_version": 1, "files": [{"source": REL, "mirror": REL, **pin(source)}],
                         "algorithm_references": [{"source": r["local_path"], "direction": r["direction"],
                                                   "sha256": r["sha256"], "bytes": r["bytes"]} for r in refs],
                         "supporting_files": [{"path": "06_SOURCE/References/registry.json", **pin(registry)}]}
        self.manifest_path = self.root / "_INDEX/source-hashes.json"
        write_json(self.manifest_path, self.manifest)
        write_json(self.root / "_INDEX/sync-status.json",
                   {"scope": "synthetic_compatibility_test", "review_state": "reviewed-source-reference-exact"})
        (self.root / "08_DATA/Raw").mkdir(parents=True, exist_ok=True)
        (self.root / "07_VALIDATION/Fixtures").mkdir(parents=True, exist_ok=True)

    def run_build(self, check=False, mode="full-data"):
        output, errors = io.StringIO(), io.StringIO()
        with patch.object(build_indexes, "ROOT", self.root), redirect_stdout(output), redirect_stderr(errors):
            result = build_indexes.build(check=check, mode=mode)
        return result, output.getvalue() + errors.getvalue()

    def assert_bad(self, expected):
        result, output = self.run_build()
        self.assertEqual(1, result, output)
        self.assertIn(expected, output)
        self.assertFalse((self.root / "_INDEX/entities.json").exists())

    def test_alias_collision_across_canonical_names_is_rejected(self):
        left = self.root / "04_ALGORITHMS/Order/Order-B.md"
        right = self.root / "04_ALGORITHMS/Order/OrderAudit.md"
        fields = build_indexes.frontmatter(left)
        write_note(left, {**fields, "name": "Signal", "aliases": ["Shared"]})
        fields = build_indexes.frontmatter(right)
        write_note(right, {**fields, "name": "Other", "aliases": ["SHARED"]})
        self.assert_bad("Ambiguous entity name")

    def test_alias_cannot_shadow_a_stable_id(self):
        path = self.root / "04_ALGORITHMS/Order/Order-B.md"
        fields = build_indexes.frontmatter(path)
        write_note(path, {**fields, "aliases": ["algorithm.orderaudit"]})
        self.assert_bad("Ambiguous entity name")

    def test_aliases_need_string_array_metadata(self):
        path = self.root / "04_ALGORITHMS/Order/Order-B.md"
        fields = build_indexes.frontmatter(path)
        write_note(path, {**fields, "aliases": "Signal"})
        self.assert_bad("aliases")

    def test_recursive_source_symbol_inventory_includes_control_block_functions(self):
        path = self.root / "nested.py"
        path.write_text("class Container:\n"
                        "    def owner(self):\n"
                        "        for number in (1,):\n"
                        "            def nested(value):\n"
                        "                return value\n"
                        "            if number:\n"
                        "                def deeper(value):\n"
                        "                    return nested(value)\n", encoding="utf-8")
        result = build_indexes._ast_structure(path, "nested.py")
        found = {row["qualified_name"] for row in result.get("symbols", [])}
        self.assertEqual(found, {"Container", "Container.owner", "Container.owner.nested",
                                 "Container.owner.deeper"})

    def test_generated_entities_pin_complete_note_bytes(self):
        result, output = self.run_build()
        self.assertEqual(result, 0, output)
        rows = json.loads((self.root / "_INDEX/entities.json").read_text())["entities"]
        for row in rows.values():
            data = (self.root / row["file"]).read_bytes()
            self.assertEqual(row.get("content_sha256"), hashlib.sha256(data).hexdigest())
            self.assertEqual(row.get("content_bytes"), len(data))

    def test_empty_stores_current_order_metadata_and_new_note_types_are_valid(self):
        result, output = self.run_build()
        self.assertEqual(0, result, output)
        entities = json.loads((self.root / "_INDEX/entities.json").read_text())["entities"]
        self.assertEqual("active", entities["algorithm.order.b"]["status"])
        self.assertEqual("executable", entities["algorithm.orderaudit"]["authority"])
        for kind in ("workflow", "version", "decision"):
            self.assertIn(kind + ".current", entities)
        self.assertEqual([], list((self.root / "08_DATA/Raw").iterdir()))

    def test_whole_file_and_zero_byte_package_source_are_valid(self):
        package_relative = "06_SOURCE/Code/engine/__init__.py"
        package = self.root / package_relative
        package.write_bytes(b"")
        self.manifest["files"].append({"source": package_relative, "mirror": package_relative, **pin(package)})
        registry_path = self.root / "06_SOURCE/References/registry.json"
        registry = json.loads(registry_path.read_text())
        for row, mirror in zip(registry["references"], self.manifest["algorithm_references"]):
            reference = self.root / row["local_path"]
            reference.write_bytes(reference.read_bytes() +
                b'<!-- EXACT-SOURCE-BEGIN:__init__.py -->\n````python\n````\n<!-- EXACT-SOURCE-END:__init__.py -->\n')
            row.update(pin(reference))
            mirror.update(pin(reference))
        write_json(registry_path, registry)
        self.manifest["supporting_files"][0].update(pin(registry_path))
        write_json(self.manifest_path, self.manifest)
        write_note(self.root / "06_SOURCE/Modules/package.md", {
            "id": "source.package", "type": "source", "status": "active", "authority": "executable",
            "title": "Zero-byte package", "related_entities": [], "source_reference": [package_relative],
            "source_path": package_relative, "mirror": package_relative, "sha256": pin(package)["sha256"]})
        result, output = self.run_build()
        self.assertEqual(0, result, output)

    def test_full_schema_owned_metadata_is_retained_in_entity_index(self):
        path = self.root / "04_ALGORITHMS/Order/Order-B.md"
        fields = build_indexes.frontmatter(path)
        body = path.read_text().split("\n---\n", 1)[1]
        fields.update({"valid_for_reasoning": True, "version": "current", "evidence_basis": "Source"})
        write_note(path, fields, body)
        result, output = self.run_build()
        self.assertEqual(0, result, output)
        row = json.loads((self.root / "_INDEX/entities.json").read_text())["entities"][fields["id"]]
        self.assertEqual(fields, {key: value for key, value in row.items()
                                  if key not in {"file", "content_sha256", "content_bytes"}})
        self.assertEqual(pin(path)["sha256"], row["content_sha256"])
        self.assertEqual(pin(path)["bytes"], row["content_bytes"])

    def test_declared_current_contract_enforces_identity_and_status_generically(self):
        self.manifest["current_contract"] = {"entities": {
            "algorithm.orderaudit": {"status": "pending"}}, "empty_entity_types": ["data", "case"]}
        write_json(self.manifest_path, self.manifest)
        self.assert_bad("Current contract metadata mismatch: algorithm.orderaudit:status")

    def test_declared_current_inventory_rejects_missing_and_extra_concepts(self):
        self.manifest["current_contract"] = {"closed_entity_inventory": True,
                                             "entities": {"system.missing": {"status": "active"}}}
        write_json(self.manifest_path, self.manifest)
        self.assert_bad("Current entity inventory differs")

    def test_duplicate_id_is_rejected(self):
        write_note(self.root / "duplicate.md", {
            "id": "system.authority", "type": "system", "status": "active", "authority": "executable",
            "title": "Duplicate", "related_entities": [], "source_reference": []})
        self.assert_bad("Duplicate ID")

    def test_duplicate_frontmatter_field_is_rejected(self):
        path = self.root / "00_SYSTEM/AUTHORITY_MODEL.md"
        path.write_text(path.read_text().replace('type: "system"', 'type: "system"\ntype: "system"'))
        self.assert_bad("Duplicate frontmatter")

    def test_duplicate_json_key_is_rejected(self):
        text = self.manifest_path.read_text()
        self.manifest_path.write_text(text.replace('"schema_version": 1', '"schema_version": 1, "schema_version": 1'))
        self.assert_bad("Duplicate JSON key")

    def test_duplicate_nested_json_key_is_rejected(self):
        text = self.manifest_path.read_text()
        self.manifest_path.write_text(text.replace('"bytes": ' + str(len(CODE)),
                                                  '"bytes": ' + str(len(CODE)) + ', "bytes": ' + str(len(CODE)), 1))
        self.assert_bad("Duplicate JSON key")

    def test_duplicate_sync_status_json_key_is_rejected(self):
        (self.root / "_INDEX/sync-status.json").write_text(
            '{"review_state":"current","review_state":"current"}\n')
        self.assert_bad("Duplicate JSON key")

    def test_obsolete_quarantine_and_historical_metadata_are_rejected(self):
        path = self.root / "04_ALGORITHMS/Order/Order-B.md"
        original = path.read_text()
        fields = {
            "implementation_validity": "known-invalid",
            "affected_by_known_invalid_order_route": False,
            "rewrite_required": True,
        }
        for key, value in fields.items():
            with self.subTest(field=key):
                path.write_text(original.replace("\n---\n", "\n" + key + ": " + json.dumps(value) + "\n---\n", 1))
                self.assert_bad("schema")
        for status in ("pending-fix", "deprecated", "superseded", "archived"):
            with self.subTest(status=status):
                path.write_text(original.replace('status: "active"', 'status: ' + json.dumps(status)))
                self.assert_bad("schema")
        path.write_text(original.replace('authority: "executable"', 'authority: "historical"'))
        self.assert_bad("schema")

    def test_all_supported_metadata_id_arrays_reject_dangling_targets(self):
        path = self.root / "00_SYSTEM/AUTHORITY_MODEL.md"
        original = path.read_text()
        values = {
            "used_by_fixtures": ["case.deleted_fixture"],
            "validated_by": ["test.missing"],
            "consumed_by_algorithms": ["algorithm.missing"],
            "produces_behaviors": ["behavior.missing"],
        }
        for key, value in values.items():
            with self.subTest(field=key):
                path.write_text(original.replace("\n---\n", "\n" + key + ": " + json.dumps(value) + "\n---\n", 1))
                self.assert_bad("Unresolved metadata link")

    def test_all_supported_metadata_id_scalars_reject_dangling_targets(self):
        path = self.root / "00_SYSTEM/AUTHORITY_MODEL.md"
        original = path.read_text()
        values = {"algorithm": "algorithm.missing", "validation_rule": "test.missing",
                  "chronology_model": "market.missing", "hash_reference": "data.missing",
                  "parent_dataset": "data.dataset_deadbeef"}
        for key, value in values.items():
            with self.subTest(field=key):
                path.write_text(original.replace("\n---\n", "\n" + key + ": " + json.dumps(value) + "\n---\n", 1))
                self.assert_bad("Unresolved metadata link")

    def test_metadata_link_types_are_validated(self):
        path = self.root / "00_SYSTEM/AUTHORITY_MODEL.md"
        original = path.read_text()
        for key, value in {"chronology_model": "algorithm.order.b", "hash_reference": "source.probe"}.items():
            with self.subTest(field=key):
                path.write_text(original.replace("\n---\n", "\n" + key + ": " + json.dumps(value) + "\n---\n", 1))
                self.assert_bad("Metadata link target type")

    def test_obsolete_external_source_metadata_is_rejected(self):
        path = self.root / "00_SYSTEM/AUTHORITY_MODEL.md"
        original = path.read_text()
        missing = "06_SOURCE/Code/engine/pipeline/missing.py"
        for fields in (
            {"external_source_paths": [missing], "external_source_hashes": {missing: "a" * 64}},
            {"external_source_paths": [REL], "external_source_hashes": {REL: "b" * 64}},
        ):
            with self.subTest(fields=fields):
                additions = "".join("\n" + key + ": " + json.dumps(value) for key, value in fields.items())
                path.write_text(original.replace("\n---\n", additions + "\n---\n", 1))
                self.assert_bad("schema")

    def test_source_module_and_symbol_metadata_are_validated(self):
        path = self.root / "00_SYSTEM/AUTHORITY_MODEL.md"
        original = path.read_text()
        path.write_text(original.replace("\n---\n", '\nsource_module: "06_SOURCE/Code/engine/pipeline/missing.py"\n---\n', 1))
        self.assert_bad("Missing source reference")
        path.write_text(original.replace("\n---\n", '\nsource_module: ' + json.dumps(REL)
                                         + '\nsource_function: "missing_function"\n---\n', 1))
        self.assert_bad("Unknown source function")

    def test_valid_optional_metadata_links_and_source_symbol_are_accepted(self):
        common = {"status": "active", "authority": "executable", "related_entities": [],
                  "source_reference": [REL + "#L1"]}
        for ident, kind, extra in (
            ("market.chronology", "market", {}),
            ("data.policy", "data", {"data_kind": "policy"}),
            ("test.policy", "test", {}),
            ("behavior.sample", "behavior", {"implemented_by": ["source.probe"]}),
        ):
            write_note(self.root / (kind + "/Metadata.md"),
                       {"id": ident, "type": kind, "title": ident, **common, **extra})
        path = self.root / "00_SYSTEM/AUTHORITY_MODEL.md"
        fields = build_indexes.frontmatter(path)
        fields.update({"algorithm": "algorithm.order.b", "validation_rule": "test.policy",
                       "chronology_model": "market.chronology", "hash_reference": "data.policy",
                       "consumed_by_algorithms": ["algorithm.order.b"], "produces_behaviors": ["behavior.sample"],
                       "validated_by": ["test.policy"], "used_by_fixtures": [],
                       "source_module": REL, "source_function": "probe"})
        write_note(path, fields)
        result, output = self.run_build()
        self.assertEqual(0, result, output)

    def test_invalid_relation_element_is_rejected_without_crashing(self):
        path = self.root / "04_ALGORITHMS/Order/Order-B.md"
        path.write_text(path.read_text().replace('["source.probe"]', '[{"id":"source.probe"}]'))
        self.assert_bad("schema")

    def test_dangling_markdown_link_is_rejected(self):
        path = self.root / "00_SYSTEM/AUTHORITY_MODEL.md"
        path.write_text(path.read_text() + "\n[missing](Missing.md)\n")
        self.assert_bad("Broken Markdown link")

    def test_source_anchor_out_of_range_is_rejected(self):
        path = self.root / "04_ALGORITHMS/Order/Order-B.md"
        path.write_text(path.read_text().replace("#L1", "#L9999"))
        self.assert_bad("Invalid source line")

    def test_stale_evidence_hash_is_rejected(self):
        (self.root / REL).write_bytes(CODE + b"\n")
        self.assert_bad("Evidence SHA/size mismatch")

    def test_missing_noninitializer_module_note_is_rejected(self):
        (self.root / "06_SOURCE/Modules/probe.md").unlink()
        self.assert_bad("Missing physical module note")

    def test_unsafe_manifest_path_is_rejected(self):
        self.manifest["files"][0]["source"] = "../outside.py"
        write_json(self.manifest_path, self.manifest)
        self.assert_bad("Non-normalized path")

    def test_reference_reconstruction_mismatch_is_rejected_even_after_repin(self):
        refs = self.manifest["algorithm_references"]
        path = self.root / refs[0]["source"]
        path.write_bytes(path.read_bytes().replace(b"return value\n", b"return None\n"))
        refs[0].update(pin(path))
        registry_path = self.root / "06_SOURCE/References/registry.json"
        registry = json.loads(registry_path.read_text())
        registry["references"][0].update(pin(path))
        write_json(registry_path, registry)
        self.manifest["supporting_files"][0].update(pin(registry_path))
        write_json(self.manifest_path, self.manifest)
        self.assert_bad("Embedded source mismatch")

    def test_relation_target_is_rejected(self):
        path = self.root / "04_ALGORITHMS/Order/Order-B.md"
        path.write_text(path.read_text().replace('"source.probe"', '"source.missing"'))
        self.assert_bad("Unresolved relation")

    def test_unregistered_raw_file_is_rejected(self):
        (self.root / "08_DATA/Raw/unregistered.json").write_text("[]")
        self.assert_bad("Unregistered RAW")

    def test_check_compares_generated_bytes_without_writing(self):
        result, output = self.run_build()
        self.assertEqual(0, result, output)
        generated = self.root / "_GENERATED/knowledge-model.json"
        generated.write_text('{"stale": true}\n')
        before = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result, output = self.run_build(check=True)
        after = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(1, result, output)
        self.assertIn("Stale generated file", output)
        self.assertEqual(before, after)

    def test_external_managed_validation_artifact_is_not_compared_or_rewritten(self):
        result, output = self.run_build()
        self.assertEqual(0, result, output)
        validation = self.root / "_GENERATED/current_validation.json"
        validation.write_text('{"status":"BOUNDED_VALIDATION"}\n')
        result, output = self.run_build(check=True)
        self.assertEqual(0, result, output)
        self.assertEqual('{"status":"BOUNDED_VALIDATION"}\n', validation.read_text())

if __name__ == "__main__":
    unittest.main()
