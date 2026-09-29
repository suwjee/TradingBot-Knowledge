"""Validate current Vault metadata/evidence and deterministically derive retrieval indexes.

Production and source evidence are read only. build(check=True) never writes.
Semantic rules are provided by current notes/source; this tool has no trading-rule gates.
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
from urllib.parse import unquote, urlsplit
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REL_KEYS = ("calculated_by", "implemented_by", "depends_on", "produces", "implements",
            "affects", "parent_of", "child_of", "relates_to", "supports", "orchestrates")
SCHEMA_TYPES = {"behavior", "algorithm", "source", "test", "case", "data"}
ID_PATTERN = re.compile(r"^[a-z][a-z0-9]*(\.[a-z0-9_]+)+$")
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
SCHEMA_URI = "https://json-schema.org/draft/2020-12/schema"
METADATA_ARRAY_LINKS = {
    "consumed_by_algorithms": {"algorithm"},
    "produces_behaviors": {"behavior"},
    "used_by_fixtures": {"case"},
    "validated_by": {"test"},
}
METADATA_SCALAR_LINKS = {
    "algorithm": {"algorithm"},
    "validation_rule": {"test"},
    "chronology_model": {"core", "market"},
    "hash_reference": {"data"},
    "parent_dataset": {"data"},
}

def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result

def loads(value):
    def invalid_constant(token):
        raise ValueError(f"Invalid JSON constant: {token}")
    return json.loads(value, object_pairs_hook=_pairs, parse_constant=invalid_constant)

def _read_json(path):
    return loads(path.read_text(encoding="utf-8-sig"))

def frontmatter(path):
    raw = path.read_text(encoding="utf-8-sig")
    if not raw.startswith("---\n"):
        return None
    boundary = raw.find("\n---\n", 4)
    if boundary < 0:
        raise ValueError(f"Unclosed frontmatter: {path}")
    fields = {}
    for line in raw[4:boundary].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {path}: {line}")
        key, value = line.split(":", 1)
        if not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            raise ValueError(f"Invalid frontmatter field: {key}")
        if key in fields:
            raise ValueError(f"Duplicate frontmatter field: {key}")
        fields[key] = loads(value.strip())
    return fields

def safe_path(root, relative):
    if (not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative
            or any(part in {"", ".", ".."} for part in relative.split("/"))):
        raise ValueError(f"Non-normalized path: {relative!r}")
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path outside root: {relative}")
    return path

def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()

def _without_code(text):
    fence = chr(96)
    text = re.sub(r"(?ms)^[ \t]*(" + fence + r"{3,}|~{3,})[^\n]*\n.*?^[ \t]*\1[ \t]*$", "", text)
    return re.sub(fence + r"[^" + fence + r"]*" + fence, "", text)

def _heading_ids(path):
    seen = {}
    ids = set()
    for line in _without_code(path.read_text(encoding="utf-8-sig")).splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            heading = re.sub(r"<[^>]*>", "", match[1]).strip().lower()
            slug = re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")
            count = seen.get(slug, 0)
            seen[slug] = count + 1
            ids.add(slug + (f"-{count}" if count else ""))
    return ids

def _validate_anchor(path, anchor, label):
    if not anchor:
        return
    match = re.fullmatch(r"L([1-9][0-9]*)(?:-L?([1-9][0-9]*))?", anchor, re.IGNORECASE)
    if match:
        start = int(match[1])
        end = int(match[2] or start)
        if start > end or end > len(path.read_text(encoding="utf-8-sig").splitlines()):
            raise ValueError(f"Invalid source line: {label}")
    elif path.suffix.lower() == ".md" and unquote(anchor).lower() in _heading_ids(path):
        return
    else:
        raise ValueError(f"Invalid Markdown anchor: {label}")

def _validate_code_ref(root, value):
    relative, _, anchor = value.partition("#")
    if not relative.startswith("06_SOURCE/Code/"):
        raise ValueError(f"Source reference outside Code: {value}")
    path = safe_path(root, relative)
    if not path.is_file():
        raise ValueError(f"Missing source reference: {value}")
    _validate_anchor(path, anchor, value)

def _source_symbols(path):
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=path.name)
    return {row["qualified_name"] for row in _symbol_details(tree)}

def _symbol_details(tree):
    """Retain lexical owners even when definitions occur inside control blocks."""
    symbols = []
    def visit(node, prefix=""):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = prefix + node.name
            symbols.append({"qualified_name": name, "name": node.name,
                            "kind": "class" if isinstance(node, ast.ClassDef) else "function",
                            "line": node.lineno, "end_line": node.end_lineno})
            prefix = name + "."
        for child in ast.iter_child_nodes(node):
            visit(child, prefix)
    visit(tree)
    return symbols

def _validate_links(root, note_path, text, notes, files):
    text = _without_code(text)
    targets = re.findall(r"!?\[[^\]]*\]\((<[^>]+>|[^)\n]+)\)", text)
    definitions = re.findall(r"(?m)^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)", text)
    for raw_target in [*targets, *definitions]:
        target = raw_target.strip()
        if target.startswith("<"):
            target = target[1:target.index(">")]
        else:
            target = re.split(r'\s+["\']', target, maxsplit=1)[0]
        target = unquote(target)
        parsed = urlsplit(target)
        if parsed.scheme in {"http", "https", "mailto"}:
            continue
        if parsed.scheme or parsed.netloc or "\\" in target:
            raise ValueError(f"Unsafe Markdown link: {target}")
        relative, _, anchor = target.partition("#")
        path = (note_path.parent / relative).resolve() if relative else note_path.resolve()
        if not path.is_relative_to(root.resolve()) or not path.exists():
            raise ValueError(f"Broken Markdown link: {target}")
        if anchor:
            if not path.is_file():
                raise ValueError(f"Invalid Markdown anchor: {target}")
            _validate_anchor(path, anchor, target)
    for target in re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", text):
        value, _, anchor = target.partition("#")
        if value in notes:
            path = safe_path(root, files[value])
        else:
            path = (note_path.parent / value).resolve()
            if not path.suffix:
                path = path.with_suffix(".md")
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError(f"Broken Wiki link: {target}")
        _validate_anchor(path, anchor, target)

def _ast_structure(path, relative):
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=relative)
    functions = []
    classes = []
    imports = []
    constants = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append({"name": node.name, "line": node.lineno, "end_line": node.end_lineno,
                              "parameters": [arg.arg for arg in [*node.args.posonlyargs, *node.args.args,
                                                               *node.args.kwonlyargs]]})
        elif isinstance(node, ast.ClassDef):
            classes.append({"name": node.name, "line": node.lineno, "end_line": node.end_lineno,
                            "decorators": [ast.unparse(item) for item in node.decorator_list],
                            "fields": [{"name": item.target.id,
                                        "annotation": ast.unparse(item.annotation), "line": item.lineno}
                                       for item in node.body if isinstance(item, ast.AnnAssign)
                                       and isinstance(item.target, ast.Name)],
                            "methods": [{"name": item.name, "line": item.lineno, "end_line": item.end_lineno}
                                        for item in node.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))]})
        elif isinstance(node, ast.Import):
            imports.extend({"module": item.name, "line": node.lineno} for item in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append({"module": "." * node.level + (node.module or ""),
                            "names": [item.name for item in node.names], "line": node.lineno})
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for item in targets:
                if isinstance(item, ast.Name) and (item.id.isupper() or item.id == "__version__"):
                    constants.append({"name": item.id, "line": node.lineno})
    return {"path": relative, "functions": functions, "classes": classes,
            "symbols": _symbol_details(tree),
            "imports": imports, "constants": constants}

def _embedded_sources(data):
    fence = bytes([96])
    pattern = (rb"<!-- EXACT-SOURCE-BEGIN:([^>\r\n]+) -->\r?\n("
               + re.escape(fence) + rb"{3,})python[^\r\n]*\r?\n(.*?)^\2[ \t]*\r?\n"
               + rb"<!-- EXACT-SOURCE-END:\1 -->")
    sources = {}
    matches = list(re.finditer(pattern, data, re.MULTILINE | re.DOTALL))
    starts = re.findall(rb"<!-- EXACT-SOURCE-BEGIN:([^>\r\n]+) -->", data)
    if len(matches) != len(starts):
        raise ValueError("Malformed embedded source block")
    for match in matches:
        relative = match[1].decode("utf-8")
        if relative in sources:
            raise ValueError(f"Duplicate embedded source: {relative}")
        sources[relative] = match[3]
    return sources

def build(check=False, mode="full-data"):
    if mode not in {"knowledge", "full-data"}:
        raise ValueError("Validation mode must be knowledge or full-data")
    root = ROOT.resolve()
    errors = []
    schemas = {}
    for name in ["note", *sorted(SCHEMA_TYPES)]:
        try:
            schema = _read_json(root / "_SCHEMA" / (name + ".schema.json"))
            if schema.get("$schema") != SCHEMA_URI:
                raise ValueError("Unsupported schema dialect")
            Draft202012Validator.check_schema(schema)
            schemas[name] = Draft202012Validator(schema)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            errors.append(f"Schema {name}: {exc}")
    notes, files, bodies = {}, {}, {}
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root).as_posix()
        parts = path.relative_to(root).parts
        if any(part in {".git", ".obsidian", "_GENERATED", "Code"} for part in parts) or path.stat().st_size == 0:
            continue
        try:
            safe_path(root, relative)
            fields = frontmatter(path)
            if fields is None:
                raise ValueError("Populated Markdown missing frontmatter")
            note_invalid = False
            for name in ("note", fields.get("type")):
                if name in schemas:
                    for failure in schemas[name].iter_errors(fields):
                        location = ".".join(str(part) for part in failure.absolute_path) or "<root>"
                        errors.append(f"{relative}: {name} schema at {location}: {failure.message}")
                        note_invalid = True
            if note_invalid:
                raise ValueError("Invalid note frontmatter")
            ident = fields.get("id")
            if not isinstance(ident, str) or not ID_PATTERN.fullmatch(ident):
                raise ValueError("Invalid stable ID")
            if ident in notes:
                raise ValueError(f"Duplicate ID: {ident}")
            if ident.split(".", 1)[0] != fields.get("type"):
                raise ValueError(f"ID/type prefix mismatch: {ident}")
            for ref in [*fields.get("source_reference", []), *fields.get("source_refs", [])]:
                _validate_code_ref(root, ref)
            if relative.startswith("06_SOURCE/Modules/") and not fields.get("source_path"):
                raise ValueError(f"Physical module note missing source_path: {ident}")
            if "source_path" in fields:
                for key in ("source_path", "mirror"):
                    source = safe_path(root, fields[key])
                    if not source.is_file() or sha(source) != fields["sha256"]:
                        raise ValueError(f"Module note SHA mismatch: {ident}")
            notes[ident], files[ident], bodies[ident] = fields, relative, path.read_text(encoding="utf-8-sig")
        except (OSError, ValueError, TypeError, KeyError) as exc:
            errors.append(f"{relative}: {exc}")
    labels = {}
    for ident, fields in sorted(notes.items()):
        for label in [ident, fields.get("name", fields["title"]), *fields.get("aliases", [])]:
            key = label.strip().casefold()
            if not key:
                errors.append(f"Empty entity name: {ident}")
            elif key in labels and labels[key] != ident:
                errors.append(f"Ambiguous entity name: {label}: {labels[key]} / {ident}")
            else:
                labels[key] = ident
    edges = []
    for ident, fields in sorted(notes.items()):
        for key in (*REL_KEYS, "related_entities"):
            values = fields.get(key, [])
            if not isinstance(values, list):
                errors.append(f"Relation field is not an array: {ident}.{key}")
                continue
            for target in values:
                if target not in notes:
                    errors.append(f"Unresolved relation: {ident}.{key} -> {target}")
                    continue
                if key == "implemented_by" and notes[target]["type"] != "source":
                    errors.append(f"implemented_by target is not source: {ident} -> {target}")
                if key == "calculated_by" and notes[target]["type"] != "algorithm":
                    errors.append(f"calculated_by target is not algorithm: {ident} -> {target}")
                if key == "depends_on" and ident == target:
                    errors.append(f"Self dependency: {ident}")
                edges.append({"from": ident, "type": "relates_to" if key == "related_entities" else key,
                              "to": target})
    edge_keys = {(item["from"], item["type"], item["to"]) for item in edges}
    if len(edge_keys) != len(edges):
        errors.append("Duplicate relations")
    symbol_cache = {}
    for ident, fields in sorted(notes.items()):
        for key, allowed_types in {**METADATA_ARRAY_LINKS, **METADATA_SCALAR_LINKS}.items():
            if key not in fields:
                continue
            targets = fields[key] if key in METADATA_ARRAY_LINKS else [fields[key]]
            for target in targets:
                if target == "unknown" and key == "algorithm":
                    continue
                if target not in notes:
                    errors.append(f"Unresolved metadata link: {ident}.{key} -> {target}")
                elif notes[target]["type"] not in allowed_types:
                    errors.append(f"Metadata link target type: {ident}.{key} -> {target}")
                elif key == "parent_dataset" and notes[target].get("data_kind") != "dataset":
                    errors.append(f"Metadata link target type: {ident}.{key} needs a physical dataset")
        try:
            source_module = fields.get("source_module")
            source_function = fields.get("source_function")
            if source_module and source_module != "unknown":
                _validate_code_ref(root, source_module)
                module_path = safe_path(root, source_module)
                if source_function and source_function != "unknown":
                    if module_path not in symbol_cache:
                        symbol_cache[module_path] = _source_symbols(module_path)
                    if source_function not in symbol_cache[module_path]:
                        raise ValueError(f"Unknown source function: {ident}: {source_function}")
            elif source_function and source_function != "unknown":
                raise ValueError(f"Source function has no physical source module: {ident}")
        except (OSError, ValueError, TypeError, KeyError, SyntaxError) as exc:
            errors.append(f"{ident}: {exc}")
    manifest = {"files": [], "algorithm_references": [], "supporting_files": []}
    pins = {}
    structures = []
    try:
        sync_status_path = root / "_INDEX/sync-status.json"
        if sync_status_path.is_file():
            sync_status = _read_json(sync_status_path)
            if not isinstance(sync_status, dict) or not isinstance(sync_status.get("review_state"), str):
                raise ValueError("Invalid sync status structure")
        manifest = _read_json(root / "_INDEX/source-hashes.json")
        for key in ("files", "algorithm_references", "supporting_files"):
            values = manifest.get(key, [])
            if not isinstance(values, list) or (key != "supporting_files" and key not in manifest):
                raise ValueError(f"Missing/invalid manifest array: {key}")
            for row in values:
                names = [row["source"], row["mirror"]] if key == "files" else [row.get("mirror", row.get("source", row.get("path")))]
                for value in names:
                    safe_path(root, value)
                if key == "files" and not all(value.startswith("06_SOURCE/Code/") for value in names):
                    raise ValueError("Source snapshot outside Code")
                for relative in dict.fromkeys(names):
                    path = safe_path(root, relative)
                    if (not HASH_PATTERN.fullmatch(row["sha256"]) or not isinstance(row["bytes"], int)
                            or isinstance(row["bytes"], bool) or row["bytes"] < 0):
                        raise ValueError(f"Invalid evidence identity: {relative}")
                    if relative in pins:
                        raise ValueError(f"Duplicate manifest path: {relative}")
                    pins[relative] = row
                    if mode == "knowledge" and relative.startswith("08_DATA/Raw/"):
                        continue
                    if not path.is_file() or path.stat().st_size != row["bytes"] or sha(path) != row["sha256"]:
                        errors.append(f"Evidence SHA/size mismatch: {relative}")
                    elif row.get("line_count") is not None and row["line_count"] != len(path.read_text(encoding="utf-8-sig").splitlines()):
                        errors.append(f"Evidence line count mismatch: {relative}")
        code_root = root / "06_SOURCE/Code"
        physical_code = {path.relative_to(root).as_posix() for path in code_root.rglob("*") if path.is_file()} if code_root.is_dir() else set()
        pinned_code = {relative for relative in pins if relative.startswith("06_SOURCE/Code/")}
        if physical_code != pinned_code:
            errors.append(f"Code inventory mismatch: missing={sorted(pinned_code-physical_code)} extra={sorted(physical_code-pinned_code)}")
        module_notes = [fields["source_path"] for fields in notes.values() if fields.get("source_path")]
        if len(module_notes) != len(set(module_notes)):
            errors.append("Duplicate module source_path")
        for relative in sorted(pinned_code):
            path = safe_path(root, relative)
            if path.suffix == ".py" and path.is_file():
                structures.append(_ast_structure(path, relative))
                if path.name != "__init__.py" and relative not in module_notes:
                    errors.append(f"Missing physical module note: {relative}")
        for relative in module_notes:
            if relative not in pins:
                errors.append(f"Module note source missing from manifest: {relative}")
    except (OSError, ValueError, TypeError, KeyError, SyntaxError) as exc:
        errors.append(f"Manifest/evidence validation: {exc}")

    registry = {"references": []}
    reconstructions = []
    try:
        registry_path = root / "06_SOURCE/References/registry.json"
        registry = _read_json(registry_path)
        if registry.get("schema_version") != 1 or not isinstance(registry.get("references"), list):
            raise ValueError("Unsupported reference registry")
        if "06_SOURCE/References/registry.json" not in pins:
            raise ValueError("Reference registry not pinned in manifest")
        refs = registry["references"]
        if len(refs) != 2 or {row["direction"] for row in refs} != {"Bullish", "Bearish"}:
            raise ValueError("Registry must contain exactly both current directions")
        if len({row["id"] for row in refs}) != len(refs):
            raise ValueError("Duplicate reference ID")
        required_sources = {relative.removeprefix("06_SOURCE/Code/engine/")
                            for relative in pins if relative.startswith("06_SOURCE/Code/engine/")
                            and relative.endswith(".py")}
        registered_local = set()
        for row in refs:
            origin = row["repository_relative_path"]
            safe_path(root, origin)
            if not origin.startswith("engine/algorithms/") or Path(origin).name != row["name"]:
                raise ValueError(f"Unsafe reference registry path: {origin}")
            local = row["local_path"]
            path = safe_path(root, local)
            if not local.startswith("06_SOURCE/Code/engine/algorithms/") or path.name != row["name"]:
                raise ValueError(f"Unsafe local reference path: {local}")
            registered_local.add(local)
            if not path.is_file() or sha(path) != row["sha256"] or path.stat().st_size != row["bytes"]:
                raise ValueError(f"Reference identity mismatch: {row['id']}")
            pin_row = pins.get(local)
            if pin_row is None or pin_row["sha256"] != row["sha256"] or pin_row["bytes"] != row["bytes"]:
                raise ValueError(f"Reference manifest mismatch: {row['id']}")
            sources = _embedded_sources(path.read_bytes())
            if set(sources) != required_sources:
                errors.append(f"Embedded source inventory mismatch: {row['id']}: missing={sorted(required_sources-set(sources))} extra={sorted(set(sources)-required_sources)}")
            for relative, payload in sources.items():
                source = safe_path(root, "06_SOURCE/Code/engine/" + relative)
                matches = source.is_file() and source.read_bytes() == payload
                if not matches:
                    errors.append(f"Embedded source mismatch: {row['id']}:{relative}")
                reconstructions.append({"reference_id": row["id"], "source": relative,
                                        "sha256": hashlib.sha256(payload).hexdigest(),
                                        "bytes": len(payload), "exact": matches})
        manifest_refs = {row.get("mirror", row["source"]) for row in manifest.get("algorithm_references", [])}
        if manifest_refs != registered_local:
            errors.append("Reference manifest/registry inventory mismatch")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors.append(f"Reference validation: {exc}")
    for ident, fields in notes.items():
        try:
            _validate_links(root, safe_path(root, files[ident]), bodies[ident], notes, files)
            for value in fields.get("algorithm_reference", []):
                if value not in {row["id"] for row in registry["references"]}:
                    _validate_code_ref(root, value)
            for value in fields.get("mirror_links", []):
                if value not in notes:
                    relative, _, anchor = value.partition("#")
                    path = safe_path(root, relative)
                    if not path.is_file():
                        raise ValueError(f"Missing mirror link: {value}")
                    _validate_anchor(path, anchor, value)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            errors.append(f"{ident}: {exc}")
    datasets = {ident: fields for ident, fields in notes.items()
                if fields["type"] == "data" and fields.get("data_kind") == "dataset"}
    windows = {ident: fields for ident, fields in notes.items()
               if fields["type"] == "data" and fields.get("data_kind") == "window"}
    cases = {ident: fields for ident, fields in notes.items() if fields["type"] == "case"}
    registered_raw = set()
    candle_cache = {}
    def raw_path(value):
        path = safe_path(root, value)
        if not path.is_relative_to((root / "08_DATA/Raw").resolve()):
            raise ValueError(f"Dataset outside Raw: {value}")
        return path
    def verify_window(path, fields, hash_field="raw_sha256", first_field="first_epoch", last_field="last_epoch", count_field="row_count"):
        if path not in candle_cache:
            candle_cache[path] = loads(path.read_bytes())
        candles = candle_cache[path]
        if not isinstance(candles, list) or not all(isinstance(row, dict) and isinstance(row.get("time"), int) for row in candles):
            raise ValueError(f"Invalid RAW array: {path.name}")
        times = [row["time"] for row in candles]
        if any(left >= right for left, right in zip(times, times[1:])):
            raise ValueError(f"Invalid RAW chronology: {path.name}")
        selected = candles[bisect.bisect_left(times, fields[first_field]):bisect.bisect_right(times, fields[last_field])]
        if (not selected or len(selected) != fields[count_field] or selected[0]["time"] != fields[first_field]
                or selected[-1]["time"] != fields[last_field]
                or hashlib.sha256(json.dumps(selected, separators=(",", ":")).encode()).hexdigest() != fields[hash_field]):
            raise ValueError(f"RAW window mismatch: {path.name}")
    for ident, fields in datasets.items():
        try:
            locations = fields["raw_locations"]
            if fields["raw_path"] not in locations:
                raise ValueError("Primary RAW not in locations")
            for relative in locations:
                path = raw_path(relative)
                registered_raw.add(relative)
                if mode == "full-data" and (not path.is_file() or sha(path) != fields["raw_sha256"] or path.stat().st_size != fields["raw_bytes"]):
                    raise ValueError(f"Dataset SHA/size mismatch: {relative}")
        except (OSError, ValueError, TypeError, KeyError) as exc:
            errors.append(f"{ident}: {exc}")
    for ident, fields in windows.items():
        try:
            path = raw_path(fields["raw_path"])
            if fields["parent_dataset"] not in datasets:
                raise ValueError("Window parent dataset missing")
            if mode == "full-data":
                if sha(path) != fields["retained_raw_sha256"]:
                    raise ValueError("Window parent SHA mismatch")
                verify_window(path, fields)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            errors.append(f"{ident}: {exc}")
    for ident, fields in cases.items():
        try:
            dataset = raw_path(fields["dataset"])
            if not any(fields["dataset_sha256"] == item["raw_sha256"] for item in datasets.values()):
                raise ValueError("Fixture dataset entity missing")
            source = safe_path(root, fields["source_fixture"])
            if not source.is_file() or sha(source) != fields["source_fixture_sha256"]:
                raise ValueError("Fixture source SHA mismatch")
            line = fields["source_fixture_line"]
            lines = source.read_text(encoding="utf-8-sig").splitlines()
            if not 1 <= line <= len(lines) or lines[line - 1] != "### " + fields["title"]:
                raise ValueError("Fixture source line/heading mismatch")
            if mode == "full-data" and (not dataset.is_file() or sha(dataset) != fields["dataset_sha256"]):
                raise ValueError("Fixture dataset SHA mismatch")
            if mode == "full-data" and fields.get("dataset_window_sha256"):
                verify_window(dataset, fields, "dataset_window_sha256", "dataset_window_first_epoch",
                              "dataset_window_last_epoch", "dataset_window_row_count")
        except (OSError, ValueError, TypeError, KeyError) as exc:
            errors.append(f"{ident}: {exc}")
    if mode == "full-data":
        raw_root = root / "08_DATA/Raw"
        for path in raw_root.rglob("*.json") if raw_root.is_dir() else []:
            relative = path.relative_to(root).as_posix()
            if path.name.endswith(".meta.json"):
                if relative not in pins:
                    errors.append(f"Unregistered RAW sidecar: {relative}")
            elif relative not in registered_raw:
                errors.append(f"Unregistered RAW file: {relative}")
    contract = manifest.get("current_contract")
    if contract is not None:
        try:
            if not isinstance(contract, dict):
                raise ValueError("Current contract must be an object")
            declared = contract.get("entities", {})
            if not isinstance(declared, dict):
                raise ValueError("Current entity contract must be an object")
            if contract.get("closed_entity_inventory") and set(declared) != set(notes):
                errors.append("Current entity inventory differs from its declared contract")
            for ident, constraints in declared.items():
                if ident not in notes or not isinstance(constraints, dict):
                    errors.append(f"Missing current contract entity: {ident}")
                    continue
                for field, value in constraints.items():
                    if json.dumps(notes[ident].get(field), sort_keys=True) != json.dumps(value, sort_keys=True):
                        errors.append(f"Current contract metadata mismatch: {ident}:{field}")
            for kind in contract.get("empty_entity_types", []):
                if any(fields["type"] == kind for fields in notes.values()):
                    errors.append(f"Current contract requires empty entity type: {kind}")
            for selector in contract.get("empty_entity_filters", []):
                if not isinstance(selector, dict) or not selector:
                    raise ValueError("Empty entity filter must be a nonempty metadata object")
                if any(all(json.dumps(fields.get(key), sort_keys=True) == json.dumps(value, sort_keys=True)
                           for key, value in selector.items()) for fields in notes.values()):
                    errors.append(f"Current contract requires empty entity filter: {selector}")
        except (ValueError, TypeError, KeyError) as exc:
            errors.append(f"Current contract validation: {exc}")
    if errors:
        print("\n".join(sorted(set(errors))), file=sys.stderr)
        print(f"FAILED: {len(set(errors))} errors", file=sys.stderr)
        return 1
    rows = {ident: {"file": files[ident], **fields,
                    "content_sha256": sha(safe_path(root, files[ident])),
                    "content_bytes": safe_path(root, files[ident]).stat().st_size}
            for ident, fields in sorted(notes.items())}
    edges.sort(key=lambda item: (item["from"], item["type"], item["to"]))
    label = "current Markdown frontmatter"
    source_map = {ident: sorted(fields.get("implemented_by", []))
                  for ident, fields in sorted(notes.items()) if fields["type"] == "algorithm"}
    outputs = {
        "_INDEX/entities.json": {"generated_from": label, "entities": rows},
        "_INDEX/relations.json": {"generated_from": label, "relations": edges},
        "_INDEX/files.json": {"generated_from": label, "files": dict(sorted(files.items()))},
        "_INDEX/source-map.json": {"generated_from": label, "algorithm_to_source": source_map},
        "_INDEX/knowledge-graph.json": {"generated_from": label,
                                      "nodes": [{"id": ident, **row} for ident, row in rows.items()], "edges": edges},
        "_GENERATED/source-structure.json": {"schema_version": 1, "generated_from": "captured current Python AST",
                                           "modules": structures, "reference_reconstructions": reconstructions},
        "_GENERATED/knowledge-model.json": {"schema_version": 1, "generated_from": label,
                                            "entities": [{"id": ident, "file": files[ident], **fields}
                                                         for ident, fields in sorted(notes.items())],
                                            "relations": edges, "dataset_count": len(datasets),
                                            "fixture_count": len(cases), "window_count": len(windows),
                                            "raw_store_status": "EMPTY_BY_DESIGN" if not datasets and not windows else "REGISTERED",
                                            "fixture_store_status": "EMPTY_BY_DESIGN" if not cases else "REGISTERED"},
    }
    for relative, data in outputs.items():
        path = safe_path(root, relative)
        rendered = (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
        if check:
            if not path.is_file() or path.read_bytes() != rendered:
                errors.append(f"Stale generated file: {relative}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(rendered)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"OK: {len(notes)} entities, {len(edges)} relations, {len(structures)} Python sources, {len(registry['references'])} local references; datasets={len(datasets)}, fixtures={len(cases)}, windows={len(windows)}")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate generated bytes without writing")
    parser.add_argument("--mode", choices=("knowledge", "full-data"), default="full-data")
    args = parser.parse_args()
    raise SystemExit(build(check=args.check, mode=args.mode))
