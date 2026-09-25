"""Validate Vault frontmatter and evidence, then rebuild derived indexes.

Requires jsonschema. Reads production source/references only; writes _INDEX/*.json only
when every validation succeeds. Run with: python -B _SCHEMA/build_indexes.py
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import sys

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
PROD = Path(r"D:\My-Projects\TradingBot")
REL_KEYS = (
    "calculated_by", "implemented_by", "depends_on", "produces", "implements",
    "affects", "parent_of", "child_of", "relates_to", "supports", "orchestrates",
)
SCHEMA_TYPES = {"behavior", "algorithm", "source", "test", "case"}
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


def build() -> int:
    errors: list[str] = []
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
        if ".obsidian" in path.parts or "Code" in path.parts or path.stat().st_size == 0:
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
            if rel.startswith("06_SOURCE/Modules/"):
                if "source_path" not in data:
                    raise ValueError("Physical module note missing source_path")
            if "source_path" in data:
                source = data["source_path"]
                source_file = safe_path(PROD, source)
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
                actual = safe_path(PROD, source)
                if not actual.is_file():
                    errors.append(f"Missing source ref: {ident}: {ref}")
                elif sep and (not anchor.isdigit() or int(anchor) < 1
                              or int(anchor) > len(actual.read_text(encoding="utf-8-sig").splitlines())):
                    errors.append(f"Invalid source line: {ident}: {ref}")
            external_paths = data.get("external_source_paths", [])
            external_hashes = data.get("external_source_hashes", {})
            if external_paths and set(external_paths) != set(external_hashes):
                errors.append(f"External source/hash inventory mismatch: {ident}")
            for source in external_paths:
                actual = safe_path(PROD, source)
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
            source = safe_path(PROD, row["source"])
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
        if len(module_paths) != 9:
            errors.append(f"Expected 9 physical module notes; found {len(module_paths)}")
        refs = manifest.get("algorithm_references", [])
        if len(refs) != 2:
            errors.append(f"Expected two directional reference hashes; found {len(refs)}")
        for row in refs:
            source = safe_path(PROD, row["source"])
            if not source.is_file() or sha(source) != row["sha256"]:
                errors.append(f"Reference changed: {row['source']}")
    except Exception as exc:
        errors.append(f"Hash manifest validation failed: {exc}")
        manifest = {"files": [], "algorithm_references": []}

    if errors:
        print("\n".join(sorted(errors)), file=sys.stderr)
        print(f"FAILED: {len(errors)} errors", file=sys.stderr)
        return 1

    entity_rows = {ident: {"file": files[ident], "type": data["type"], "status": data["status"],
                            "authority": data["authority"], "title": data["title"]}
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
        (ROOT / "_INDEX" / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OK: {len(notes)} entities, {len(edges)} relations, {len(manifest['files'])} verified mirrored files, {len(manifest.get('algorithm_references', []))} reference hashes")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
