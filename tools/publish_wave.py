#!/usr/bin/env python3
"""Copy and activate one staged release wave, then validate it.

Examples:
  python tools/publish_wave.py --conference SEC --source C:\\PrimerPDFs
  python tools/publish_wave.py --teams Florida Georgia Vanderbilt --source C:\\PrimerPDFs
  python tools/publish_wave.py --conference "Big Ten" --source ./final-pdfs --dry-run

If --source is omitted, PDFs must already be in their exact repository destinations.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "publication" / "teams_manifest.json"
STATE = ROOT / "assets" / "release-state.js"
VALIDATOR = ROOT / "tools" / "validate_publication.py"


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["teams"]


def load_state():
    text=STATE.read_text(encoding="utf-8")
    m=re.fullmatch(r"\s*window\.CFB_RELEASE_STATE\s*=\s*(\{.*\})\s*;\s*",text,flags=re.S)
    if not m: raise SystemExit("release-state.js is not in the expected format")
    return json.loads(m.group(1))


def write_state(state):
    STATE.write_text("window.CFB_RELEASE_STATE = "+json.dumps(state,indent=2)+";\n",encoding="utf-8")


def normalize(s):
    return re.sub(r"[^a-z0-9]+","",s.lower())


def find_source_pdf(source: Path, filename: str):
    matches=[p for p in source.rglob(filename) if p.is_file()]
    if len(matches)==1: return matches[0]
    if not matches: raise FileNotFoundError(filename)
    raise RuntimeError(f"Multiple source files named {filename}: {matches}")


def main():
    ap=argparse.ArgumentParser()
    group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--conference", help="Conference name or slug, e.g. SEC, Big Ten, big-12")
    group.add_argument("--teams", nargs="+", help="Display or canonical team names")
    ap.add_argument("--source", type=Path, help="Folder containing completed PDFs; searched recursively")
    ap.add_argument("--dry-run", action="store_true")
    args=ap.parse_args()

    teams=load_manifest()
    conf_alias={normalize(t["conference"]):t["conference"] for t in teams}
    conf_alias.update({normalize(t["conference_slug"]):t["conference"] for t in teams})

    if args.conference:
        key=normalize(args.conference)
        if key not in conf_alias:
            raise SystemExit(f"Unknown conference: {args.conference}")
        conference=conf_alias[key]
        selected=[t for t in teams if t["conference"]==conference]
        mode=("conference",conference)
    else:
        lookup={}
        for t in teams:
            lookup[normalize(t["display_name"])]=t
            lookup[normalize(t["canonical_name"])]=t
        selected=[]
        seen=set()
        unknown=[]
        for name in args.teams:
            t=lookup.get(normalize(name))
            if not t:
                unknown.append(name); continue
            if t["display_name"] not in seen:
                selected.append(t); seen.add(t["display_name"])
        if unknown: raise SystemExit("Unknown team(s): "+", ".join(unknown))
        mode=("teams",None)

    if not selected: raise SystemExit("No teams selected")

    # Resolve every source/destination before changing anything.
    copy_plan=[]
    missing=[]
    for t in selected:
        dst=ROOT/t["pdf_path"]
        if args.source:
            try: src=find_source_pdf(args.source.resolve(),t["pdf_filename"])
            except FileNotFoundError: missing.append(t["pdf_filename"]); continue
            copy_plan.append((src,dst))
        elif not dst.is_file():
            missing.append(t["pdf_path"])
    if missing:
        print("Cannot publish; missing expected PDFs:")
        for x in missing: print(" -",x)
        return 1

    print("Release wave:")
    for t in selected: print(f" - {t['display_name']} -> {t['pdf_path']}")
    if args.dry_run:
        print("\nDRY RUN: no files or release state changed.")
        return 0

    state_before=STATE.read_bytes()
    created=[]
    replaced_backups=[]
    try:
        for src,dst in copy_plan:
            dst.parent.mkdir(parents=True,exist_ok=True)
            if dst.exists():
                backup=dst.with_suffix(dst.suffix+".publish-wave-backup")
                shutil.copy2(dst,backup); replaced_backups.append((dst,backup))
            else:
                created.append(dst)
            shutil.copy2(src,dst)

        state=load_state()
        if mode[0]=="conference":
            state["conferences"][mode[1]]=True
        else:
            for t in selected: state["teams"][t["display_name"]]=True
        write_state(state)

        result=subprocess.run([sys.executable,str(VALIDATOR)],cwd=ROOT)
        if result.returncode != 0:
            raise RuntimeError("publication validator failed")

        for _,backup in replaced_backups:
            backup.unlink(missing_ok=True)
        print("\nWave prepared successfully. Commit the PDFs and assets/release-state.js together.")
        return 0
    except Exception as e:
        STATE.write_bytes(state_before)
        for p in created: p.unlink(missing_ok=True)
        for dst,backup in replaced_backups:
            if backup.exists(): shutil.move(str(backup),str(dst))
        print(f"\nPublish aborted and local changes rolled back: {e}",file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
