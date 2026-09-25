from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
PROD=Path(r"D:\My-Projects\TradingBot")
REL_KEYS=("calculated_by","implemented_by","depends_on","produces","implements","affects","parent_of","child_of","relates_to")
TYPES={"system","core","market","behavior","algorithm","source","mirror","test","case"}
STATUS={"canonical","active","draft","proposed","pending-fix","deprecated","superseded","archived"}
AUTH={"normative","executable","empirical","historical","non-canonical"}
def frontmatter(path):
    raw=path.read_text(encoding="utf-8-sig")
    if not raw.startswith("---\n"):return None
    end=raw.find("\n---\n",4)
    if end<0:raise ValueError(f"Unclosed frontmatter: {path}")
    data={}
    for line in raw[4:end].splitlines():
        if not line.strip():continue
        if ":" not in line:raise ValueError(f"Bad frontmatter line: {path}: {line}")
        key,value=line.split(":",1)
        if key in data:raise ValueError(f"Duplicate key {key}: {path}")
        data[key]=json.loads(value.strip())
    return data
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        while chunk:=f.read(1024*1024):h.update(chunk)
    return h.hexdigest()
def build():
    notes={}
    files={}
    errors=[]
    for path in sorted(ROOT.rglob("*.md")):
        rel=path.relative_to(ROOT).as_posix()
        if ".obsidian" in path.parts or "Code" in path.parts:continue
        if path.stat().st_size==0:continue
        try:d=frontmatter(path)
        except Exception as e:errors.append(str(e));continue
        if d is None:errors.append(f"Populated Markdown missing frontmatter: {rel}");continue
        ident=d.get("id")
        if ident in notes:errors.append(f"Duplicate ID {ident}: {rel}")
        if not isinstance(ident,str) or not re.fullmatch(r"[a-z][a-z0-9]*(\.[a-z0-9_]+)+",ident or ""):errors.append(f"Invalid ID: {rel}")
        if d.get("type") not in TYPES:errors.append(f"Invalid type: {rel}")
        if d.get("status") not in STATUS:errors.append(f"Invalid status: {rel}")
        if d.get("authority") not in AUTH:errors.append(f"Invalid authority: {rel}")
        if d.get("status")=="pending-fix" and d.get("authority")=="normative":errors.append(f"Pending-fix normative: {rel}")
        for key in REL_KEYS:
            if key in d and (not isinstance(d[key],list) or not all(isinstance(x,str) for x in d[key])):errors.append(f"Invalid relation array {key}: {rel}")
        if d.get("type")=="behavior" and ("calculated_by" not in d or "implemented_by" not in d):errors.append(f"Behavior missing mapping: {rel}")
        if d.get("type")=="algorithm" and "implemented_by" not in d:errors.append(f"Algorithm missing source mapping: {rel}")
        for ref in d.get("source_refs",[]):
            src,_,anchor=ref.partition("#L")
            actual=PROD/src
            if not actual.is_file():errors.append(f"Missing source ref: {ident}: {ref}")
            elif anchor and (not anchor.isdigit() or int(anchor)<1 or int(anchor)>sum(1 for _ in actual.open(encoding="utf-8"))):errors.append(f"Invalid source line: {ident}: {ref}")
        notes[ident]=d
        files[ident]=rel
    edges=[]
    for ident,d in notes.items():
        for key in REL_KEYS:
            for target in d.get(key,[]):
                if target not in notes:errors.append(f"Unresolved {key}: {ident} -> {target}")
                edges.append({"from":ident,"type":key,"to":target})
    manifest=json.loads((ROOT/"_INDEX/source-hashes.json").read_text(encoding="utf-8-sig"))
    for row in manifest["files"]:
        src=PROD/row["source"];mirror=ROOT/row["mirror"]
        if not src.is_file() or not mirror.is_file():errors.append(f"Missing mirror/source: {row['source']}");continue
        if sha(src)!=row["sha256"] or sha(mirror)!=row["sha256"]:errors.append(f"SHA mismatch: {row['source']}")
    for row in manifest.get("algorithm_references",[]):
        if sha(PROD/row["source"])!=row["sha256"]:errors.append(f"Reference changed: {row['source']}")
    if errors:
        print("\n".join(errors),file=sys.stderr)
        print(f"FAILED: {len(errors)} errors",file=sys.stderr)
        return 1
    entity_rows={i:{"file":files[i],"type":d["type"],"status":d["status"],"authority":d["authority"],"title":d["title"]} for i,d in sorted(notes.items())}
    source_map={}
    for ident,d in notes.items():
        if d["type"]=="algorithm":source_map[ident]=sorted(set(d.get("implemented_by",[])))
    outputs={
      "entities.json":{"generated_from":"canonical Markdown frontmatter","entities":entity_rows},
      "relations.json":{"generated_from":"canonical Markdown frontmatter","relations":sorted(edges,key=lambda x:(x["from"],x["type"],x["to"]))},
      "files.json":{"generated_from":"canonical Markdown frontmatter","files":dict(sorted(files.items()))},
      "source-map.json":{"generated_from":"canonical Markdown frontmatter","algorithm_to_source":dict(sorted(source_map.items()))},
      "knowledge-graph.json":{"generated_from":"canonical Markdown frontmatter","nodes":[{"id":i,**x} for i,x in entity_rows.items()],"edges":sorted(edges,key=lambda x:(x["from"],x["type"],x["to"]))}
    }
    for name,obj in outputs.items():(ROOT/"_INDEX"/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"OK: {len(notes)} entities, {len(edges)} relations, {len(manifest['files'])} verified mirrored files, {len(manifest.get('algorithm_references',[]))} reference hashes")
    return 0
if __name__=="__main__":raise SystemExit(build())

