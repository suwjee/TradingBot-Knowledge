"""Validate Vault frontmatter and evidence, then rebuild derived indexes.

Requires jsonschema for schema checks. Reads only files inside this Vault;
writes _INDEX/*.json only when every validation succeeds.
Run with: python -B _SCHEMA/build_indexes.py
"""
from __future__ import annotations

from pathlib import Path
import argparse
import ast
import bisect
import hashlib
import json
import re
import sys

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REL_KEYS = (
    "calculated_by", "implemented_by", "depends_on", "produces", "implements",
    "affects", "parent_of", "child_of", "relates_to", "supports", "orchestrates",
)
SCHEMA_TYPES = {"behavior", "algorithm", "source", "test", "case", "data"}
STOPALL_GATES = {
    "behavior.stopall.type1": "sequence-group-stop",
    "behavior.stopall.type2": "stopall-stop",
    "behavior.stopall.type3": "opposite-s-group-stop",
}


def frontmatter(path: Path) -> dict | None:
    raw = path.read_text(encoding="utf-8-sig")
    if not raw.startswith("---\n"):
        return None
    end = raw.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"Unclosed frontmatter: {path}")
    data: dict = {}
    for line in raw[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Bad frontmatter line: {path}: {line}")
        key, value = line.split(":", 1)
        if not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            raise ValueError(f"Invalid key {key!r}: {path}")
        if key in data:
            raise ValueError(f"Duplicate key {key}: {path}")
        data[key] = json.loads(value.strip())
    return data


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def safe_path(root: Path, relative: str) -> Path:
    if (not isinstance(relative, str) or not relative or "\\" in relative
            or ":" in relative or any(part in {"", ".", ".."} for part in relative.split("/"))):
        raise ValueError(f"Non-normalized path: {relative!r}")
    full = (root / relative).resolve()
    if not full.is_relative_to(root.resolve()):
        raise ValueError(f"Path outside root: {relative!r}")
    return full


def build(check: bool = False, mode: str = "full-data") -> int:
    if mode not in {"knowledge", "full-data"}:
        raise ValueError("Validation mode must be knowledge or full-data")
    errors: list[str] = []
    digest_cache: dict[Path, str] = {}
    candles_cache: dict[Path, list] = {}
    symbol_cache: dict[Path, set[str]] = {}

    def cached_sha(path: Path) -> str:
        resolved = path.resolve()
        if resolved not in digest_cache:
            digest_cache[resolved] = sha(resolved)
        return digest_cache[resolved]

    def validate_window(path: Path, first: int, last: int, rows: int, expected_sha: str) -> bool:
        resolved = path.resolve()
        if resolved not in candles_cache:
            candles_cache[resolved] = json.loads(resolved.read_bytes())
        candles = candles_cache[resolved]
        times = [row["time"] for row in candles]
        start = bisect.bisect_left(times, first)
        end = bisect.bisect_right(times, last)
        selected = candles[start:end]
        if len(selected) != rows or not selected or selected[0]["time"] != first or selected[-1]["time"] != last:
            return False
        packed = json.dumps(selected, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(packed).hexdigest() == expected_sha

    def source_symbols(path: Path) -> set[str]:
        resolved = path.resolve()
        if resolved not in symbol_cache:
            tree = ast.parse(resolved.read_text(encoding="utf-8-sig"))
            names = set()
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    names.add(node.name)
                elif isinstance(node, ast.ClassDef):
                    for child in node.body:
                        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            names.add(f"{node.name}.{child.name}")
            symbol_cache[resolved] = names
        return symbol_cache[resolved]
    schemas: dict[str, Draft202012Validator] = {}
    for name in ["note", *sorted(SCHEMA_TYPES)]:
        try:
            schema = json.loads((ROOT / "_SCHEMA" / f"{name}.schema.json").read_text(encoding="utf-8-sig"))
            Draft202012Validator.check_schema(schema)
            schemas[name] = Draft202012Validator(schema)
        except Exception as exc:
            errors.append(f"Invalid schema {name}: {exc}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    notes: dict[str, dict] = {}
    files: dict[str, str] = {}
    module_paths: set[str] = set()
    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        if (".obsidian" in path.parts or "Code" in path.parts
                or rel.startswith("07_VALIDATION/Fixtures/Sources/") or path.stat().st_size == 0):
            continue
        try:
            data = frontmatter(path)
            if data is None:
                raise ValueError("Populated Markdown missing frontmatter")
            for name in ("note", data.get("type")):
                if name not in schemas:
                    continue
                for err in schemas[name].iter_errors(data):
                    errors.append(f"{rel}: {name} schema: {err.message}")
            ident = data.get("id")
            if not isinstance(ident, str):
                raise ValueError("Missing or invalid ID")
            if ident in notes:
                raise ValueError(f"Duplicate ID {ident}: already in {files[ident]}")
            if ident.split(".", 1)[0] != data.get("type"):
                raise ValueError(f"ID/type prefix mismatch: {ident} / {data.get('type')}")
            if ident == "algorithm.orderaudit":
                errors.append("OrderAudit must not be indexed as a knowledge concept")
            if ident == "algorithm.order.a":
                required = {"status": "canonical", "authority": "normative",
                            "implementation_validity": "accepted", "valid_for_reasoning": True,
                            "valid_for_validation": True}
                for field, expected in required.items():
                    if data.get(field) != expected:
                        errors.append(f"Accepted Order_A metadata mismatch: {ident}.{field}")
            if ident in {"algorithm.order.b", "algorithm.order.c"}:
                required = {"status": "pending-fix", "authority": "non-canonical",
                            "implementation_validity": "known-invalid", "valid_for_reasoning": False,
                            "valid_for_validation": False, "valid_for_regression_baseline": False,
                            "rewrite_required": True}
                for field, expected in required.items():
                    if data.get(field) != expected:
                        errors.append(f"Quarantine metadata mismatch: {ident}.{field}")
            if rel.startswith("06_SOURCE/Modules/"):
                if "source_path" not in data:
                    raise ValueError("Physical module note missing source_path")
            if "source_path" in data:
                source = data["source_path"]
                source_file = safe_path(ROOT, source)
                mirror = safe_path(ROOT, data.get("mirror"))
                if not source_file.is_file() or not mirror.is_file():
                    errors.append(f"Missing source/mirror for {ident}")
                elif sha(source_file) != data.get("sha256") or sha(mirror) != data.get("sha256"):
                    errors.append(f"Module SHA mismatch: {ident}")
                if source in module_paths:
                    errors.append(f"Duplicate module source_path: {source}")
                module_paths.add(source)
            for ref in [*data.get("source_refs", []), *data.get("source_reference", [])]:
                source, sep, anchor = ref.partition("#L")
                actual = safe_path(ROOT, source)
                if not actual.is_file():
                    errors.append(f"Missing source ref: {ident}: {ref}")
                elif sep and (not anchor.isdigit() or int(anchor) < 1
                              or int(anchor) > len(actual.read_text(encoding="utf-8-sig").splitlines())):
                    errors.append(f"Invalid source line: {ident}: {ref}")
            if data.get("type") == "case":
                body = path.read_text(encoding="utf-8-sig")
                claim = re.search(r"[*]{2}Status:[*]{2} (Active|Pending|Historical); [*]{2}authority:[*]{2} (Canonical|Pending|Historical)[.]", body)
                if (claim is None or claim.group(1) != data["fixture_status"]
                        or claim.group(2) != data["fixture_authority"]):
                    errors.append(f"Fixture frontmatter/body status contradiction: {ident}")
                if data["fixture_status"] == "Pending" and re.search(r"(?m)^- Status: \*\*Active ", body):
                    errors.append(f"Pending fixture has active scenario label: {ident}")
                if data.get("algorithm") in {"algorithm.order.b", "algorithm.order.c"}:
                    if data.get("fixture_authority") == "Canonical" or data.get("valid_for_regression_baseline") is not False:
                        errors.append(f"Known-invalid Order fixture is an approved baseline: {ident}")
                order_identity = data["order_identity"]
                first_index, break_index = data["first_index"], data["break_index"]
                if isinstance(order_identity, list):
                    if [first_index, break_index] != order_identity:
                        errors.append(f"Fixture physical Order index mismatch: {ident}")
                elif first_index != "unknown" or break_index != "unknown":
                    errors.append(f"Fixture indexes without physical Order evidence: {ident}")
                fixture_ref = data["source_fixture"]
                fixture = safe_path(ROOT, fixture_ref)
                if not fixture.is_file():
                    errors.append(f"Missing Vault fixture source: {ident}: {fixture_ref}")
                elif cached_sha(fixture) != data["source_fixture_sha256"]:
                    errors.append(f"Fixture source SHA mismatch: {ident}")
                else:
                    fixture_lines = fixture.read_text(encoding="utf-8-sig").splitlines()
                    fixture_line = data["source_fixture_line"]
                    if fixture_line > len(fixture_lines):
                        errors.append(f"Fixture source line out of range: {ident}")
                    else:
                        section = re.fullmatch(r"case\.fixture_([0-9]+)_([0-9]+)", ident)
                        if section and not fixture_lines[fixture_line - 1].startswith(
                            f"### {section.group(1)}.{section.group(2)} "
                        ):
                            errors.append(f"Fixture source heading mismatch: {ident}")
                dataset = safe_path(ROOT, data["dataset"])
                allowed_data_roots = (ROOT / "08_DATA/Raw",)
                if not any(dataset.resolve().is_relative_to(root.resolve()) for root in allowed_data_roots):
                    errors.append(f"Fixture dataset outside RAW roots: {ident}: {dataset}")
                elif mode == "full-data" and not dataset.is_file():
                    errors.append(f"Missing fixture dataset: {ident}: {dataset}")
                elif mode == "full-data" and cached_sha(dataset) != data["dataset_sha256"]:
                    errors.append(f"Fixture dataset SHA mismatch: {ident}")
                if mode == "full-data" and data.get("dataset_window_sha256"):
                    if not validate_window(dataset, data["dataset_window_first_epoch"],
                                           data["dataset_window_last_epoch"],
                                           data["dataset_window_row_count"],
                                           data["dataset_window_sha256"]):
                        errors.append(f"Fixture RAW window mismatch: {ident}")
                source_module = data["source_module"]
                if source_module != "unknown":
                    module = safe_path(ROOT, source_module)
                    if not module.is_file():
                        errors.append(f"Missing fixture source module: {ident}: {source_module}")
                    elif data["source_function"] != "unknown" and data["source_function"] not in source_symbols(module):
                        errors.append(f"Unknown fixture source function: {ident}: {data['source_function']}")
            if data.get("type") == "data" and data.get("data_kind") == "dataset":
                allowed_data_roots = (ROOT / "08_DATA/Raw",)
                raw_locations = data["raw_locations"]
                if data["raw_path"] not in raw_locations:
                    errors.append(f"Primary RAW missing from locations: {ident}")
                if data["name"] != Path(data["raw_path"]).name:
                    errors.append(f"Dataset name/path mismatch: {ident}")
                if ident != f"data.dataset_{data['raw_sha256'][:8]}":
                    errors.append(f"Dataset ID/hash mismatch: {ident}")
                for location in raw_locations:
                    raw_file = safe_path(ROOT, location)
                    if not any(raw_file.resolve().is_relative_to(root.resolve()) for root in allowed_data_roots):
                        errors.append(f"Dataset RAW outside approved roots: {ident}: {location}")
                    elif mode == "full-data" and not raw_file.is_file():
                        errors.append(f"Dataset RAW missing: {ident}: {location}")
                    elif mode == "full-data" and cached_sha(raw_file) != data["raw_sha256"]:
                        errors.append(f"Dataset RAW SHA mismatch: {ident}: {location}")
                    elif mode == "full-data" and raw_file.stat().st_size != data["raw_bytes"]:
                        errors.append(f"Dataset RAW byte count mismatch: {ident}: {location}")
            if data.get("type") == "data" and data.get("data_kind") == "window":
                raw_file = safe_path(ROOT, data["raw_path"])
                if not raw_file.resolve().is_relative_to((ROOT / "08_DATA/Raw").resolve()):
                    errors.append(f"RAW window outside Vault: {ident}")
                elif mode == "full-data" and (not raw_file.is_file() or cached_sha(raw_file) != data["retained_raw_sha256"]):
                    errors.append(f"RAW window parent mismatch: {ident}")
                elif mode == "full-data" and not validate_window(raw_file, data["first_epoch"], data["last_epoch"],
                                         data["row_count"], data["raw_sha256"]):
                    errors.append(f"RAW window content mismatch: {ident}")
            external_paths = data.get("external_source_paths", [])
            external_hashes = data.get("external_source_hashes", {})
            if external_paths and set(external_paths) != set(external_hashes):
                errors.append(f"External source/hash inventory mismatch: {ident}")
            for source in external_paths:
                actual = safe_path(ROOT, source)
                if not actual.is_file():
                    errors.append(f"Missing external source: {ident}: {source}")
                elif sha(actual) != external_hashes.get(source):
                    errors.append(f"External source hash changed: {ident}: {source}")
            if ident in STOPALL_GATES and data.get("source_gate_type") != STOPALL_GATES[ident]:
                errors.append(f"Wrong StopAll gate mapping: {ident}")
            notes[ident] = data
            files[ident] = rel
        except Exception as exc:
            errors.append(f"{rel}: {exc}")

    edges = []
    source_entities = {data["source_path"]: ident for ident, data in notes.items() if "source_path" in data}
    datasets_by_hash: dict[str, str] = {}
    for ident, data in notes.items():
        if data["type"] != "data" or data.get("data_kind") != "dataset":
            continue
        raw_hash = data["raw_sha256"]
        if raw_hash in datasets_by_hash:
            errors.append(f"Duplicate dataset content hash: {ident} / {datasets_by_hash[raw_hash]}")
        datasets_by_hash[raw_hash] = ident
        expected = {data["hash_reference"], data["chronology_model"], "test.regression_policy",
                    *data["consumed_by_algorithms"], *data["produces_behaviors"],
                    *data["used_by_fixtures"], *data["validated_by"]}
        missing = expected - set(data["related_entities"])
        if missing:
            errors.append(f"Missing dataset relations: {ident}: {sorted(missing)}")
        for fixture_id in data["used_by_fixtures"]:
            fixture = notes.get(fixture_id)
            if fixture is None or fixture.get("type") != "case" or fixture.get("dataset_sha256") != raw_hash:
                errors.append(f"Dataset/fixture hash relationship mismatch: {ident} -> {fixture_id}")
    for ident, data in notes.items():
        if data["type"] != "case":
            continue
        if data["dataset_sha256"] not in datasets_by_hash:
            errors.append(f"Fixture dataset has no data entity: {ident}")
        expected = {data["validation_rule"]}
        if data["behavior"] != "unknown":
            expected.add(f"behavior.{data['behavior'].lower()}")
        if data["algorithm"] != "unknown":
            expected.add(data["algorithm"])
        if data["source_module"] != "unknown":
            expected.add(source_entities.get(data["source_module"], "unknown-source-entity"))
        missing = expected - set(data["related_entities"])
        if missing:
            errors.append(f"Missing fixture relations: {ident}: {sorted(missing)}")
    for ident, data in notes.items():
        for key in (*REL_KEYS, "related_entities"):
            for target in data.get(key, []):
                if target not in notes:
                    errors.append(f"Unresolved {key}: {ident} -> {target}")
                    continue
                edge_key = "relates_to" if key == "related_entities" else key
                source_type = data["type"]
                target_type = notes[target]["type"]
                if edge_key in {"implemented_by"} and target_type != "source":
                    errors.append(f"implemented_by target not Source: {ident} -> {target}")
                if edge_key == "calculated_by" and target_type != "algorithm":
                    errors.append(f"calculated_by target not Algorithm: {ident} -> {target}")
                if edge_key in {"implements", "supports", "orchestrates"} and (source_type != "source" or target_type != "algorithm"):
                    errors.append(f"Wrong {edge_key} types: {ident} -> {target}")
                if edge_key == "depends_on" and ident == target:
                    errors.append(f"Self dependency: {ident}")
                if (data["authority"] == "normative" and notes[target]["authority"] == "non-canonical"
                        and edge_key not in {"relates_to", "affects"}):
                    errors.append(f"Normative edge into non-canonical knowledge: {ident} {edge_key} {target}")
                edges.append({"from": ident, "type": edge_key, "to": target})
    pairs = {(row["from"], row["type"], row["to"]) for row in edges}
    if len(pairs) != len(edges):
        errors.append(f"Duplicate relations: {len(edges) - len(pairs)}")
    for source, key, target in pairs:
        if key == "implemented_by" and notes[source]["type"] == "algorithm" and (target, "implements", source) not in pairs:
            errors.append(f"Missing inverse implements: {source} -> {target}")
        if key == "implements" and (target, "implemented_by", source) not in pairs:
            errors.append(f"Missing inverse implemented_by: {source} -> {target}")
        if key == "calculated_by" and notes[source]["type"] == "behavior" and (target, "produces", source) not in pairs:
            errors.append(f"Missing inverse produces: {source} -> {target}")

    try:
        manifest = json.loads((ROOT / "_INDEX/source-hashes.json").read_text(encoding="utf-8-sig"))
        mirror_expected: set[str] = set()
        source_expected: set[str] = set()
        for row in manifest["files"]:
            source = safe_path(ROOT, row["source"])
            mirror = safe_path(ROOT, row["mirror"])
            mirror_expected.add(row["mirror"])
            source_expected.add(row["source"])
            if not source.is_file() or not mirror.is_file():
                errors.append(f"Missing mirror/source: {row['source']}")
            elif sha(source) != row["sha256"] or sha(mirror) != row["sha256"] or source.stat().st_size != row["bytes"]:
                errors.append(f"SHA/size mismatch: {row['source']}")
        mirror_actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / "06_SOURCE/Code").rglob("*.py")}
        if mirror_actual != mirror_expected:
            errors.append(f"Mirror inventory mismatch: missing={sorted(mirror_expected-mirror_actual)} extra={sorted(mirror_actual-mirror_expected)}")
        if not module_paths.issubset(source_expected):
            errors.append(f"Module notes missing from manifest: {sorted(module_paths-source_expected)}")
        refs = manifest.get("algorithm_references", [])
        for row in refs:
            source = safe_path(ROOT, row["source"])
            if not source.is_file() or sha(source) != row["sha256"] or source.stat().st_size != row["bytes"]:
                errors.append(f"Reference changed: {row['source']}")
        for row in manifest.get("supporting_files", []):
            if mode == "knowledge" and row["path"].startswith("08_DATA/Raw/"):
                continue
            support = safe_path(ROOT, row["path"])
            if not support.is_file() or sha(support) != row["sha256"] or support.stat().st_size != row["bytes"]:
                errors.append(f"Supporting evidence changed: {row['path']}")
        code_expected = mirror_expected | {row["source"] for row in refs if row["source"].startswith("06_SOURCE/Code/")} | {
            row["path"] for row in manifest.get("supporting_files", []) if row["path"].startswith("06_SOURCE/Code/")
        }
        code_actual = {path.relative_to(ROOT).as_posix() for path in (ROOT / "06_SOURCE/Code").rglob("*")
                       if path.is_file() and path.suffix in {".py", ".js", ".md"}}
        if code_actual != code_expected:
            errors.append(f"Code evidence inventory mismatch: missing={sorted(code_expected-code_actual)} extra={sorted(code_actual-code_expected)}")
    except Exception as exc:
        errors.append(f"Hash manifest validation failed: {exc}")
        manifest = {"files": [], "algorithm_references": []}

    registered_references = 0
    try:
        registry = json.loads((ROOT / "06_SOURCE/References/registry.json").read_text(encoding="utf-8-sig"))
        references = registry["references"]
        registered_references = len(references)
        if {row["id"] for row in references} != {"bullish_hpzr6", "bearish_hpzr6"}:
            errors.append("Directional reference registry must identify both HPZR6 directions")
        for row in references:
            relative = row["repository_relative_path"]
            if (not relative.startswith("engine/algorithms/") or "\\" in relative or ":" in relative
                    or any(part in {"", ".", ".."} for part in relative.split("/"))
                    or Path(relative).name != row["name"]):
                errors.append(f"Unsafe reference registry path: {relative}")
            if not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) or row["bytes"] < 1:
                errors.append(f"Invalid reference identity: {row['id']}")
            if not row["known_invalid_sections"] or not row["inactive_sections"]:
                errors.append(f"Missing reference quarantine scope: {row['id']}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"Invalid directional reference registry: {exc}")

    if errors:
        print("\n".join(sorted(errors)), file=sys.stderr)
        print(f"FAILED: {len(errors)} errors", file=sys.stderr)
        return 1

    entity_rows = {ident: {"file": files[ident], "type": data["type"], "status": data["status"],
                            "authority": data["authority"], "title": data["title"],
                            "valid_for_reasoning": data.get("valid_for_reasoning"),
                            "implementation_validity": data.get("implementation_validity", "unreviewed"),
                            "affected_by_known_invalid_order_route": data.get("affected_by_known_invalid_order_route", False)}
                   for ident, data in sorted(notes.items())}
    source_map = {ident: sorted(set(data.get("implemented_by", [])))
                  for ident, data in sorted(notes.items()) if data["type"] == "algorithm"}
    sorted_edges = sorted(edges, key=lambda row: (row["from"], row["type"], row["to"]))
    outputs = {
        "entities.json": {"generated_from": "canonical Markdown frontmatter", "entities": entity_rows},
        "relations.json": {"generated_from": "canonical Markdown frontmatter", "relations": sorted_edges},
        "files.json": {"generated_from": "canonical Markdown frontmatter", "files": dict(sorted(files.items()))},
        "source-map.json": {"generated_from": "canonical Markdown frontmatter", "algorithm_to_source": source_map},
        "knowledge-graph.json": {"generated_from": "canonical Markdown frontmatter",
                                 "nodes": [{"id": ident, **row} for ident, row in entity_rows.items()], "edges": sorted_edges},
    }
    for name, obj in outputs.items():
        path = ROOT / "_INDEX" / name
        rendered = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
        if check:
            if not path.is_file() or path.read_text(encoding="utf-8-sig") != rendered:
                errors.append(f"Stale index: {name}")
        else:
            path.write_text(rendered, encoding="utf-8")
    if errors:
        print("\n".join(sorted(errors)), file=sys.stderr)
        return 1
    print(f"OK: {len(notes)} entities, {len(edges)} relations, {len(manifest['files'])} source snapshots, {registered_references} optional references, {len(manifest.get('supporting_files', []))} supporting files")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate without writing indexes")
    parser.add_argument("--mode", choices=("knowledge", "full-data"), default="full-data")
    args = parser.parse_args()
    raise SystemExit(build(args.check, args.mode))
