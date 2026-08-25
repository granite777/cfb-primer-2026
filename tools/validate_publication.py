#!/usr/bin/env python3
"""Validate staged publication state for cfb.drwhittier.com.

Stdlib-only; run from anywhere inside this repository.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "publication" / "teams_manifest.json"
STATE_PATH = ROOT / "assets" / "release-state.js"
SITE_JS = ROOT / "assets" / "site.js"
INDEX = ROOT / "index.html"
CSS = ROOT / "assets" / "styles.css"
CNAME = ROOT / "CNAME"

V3_INDEX_SHA256 = "d50c86d3b73cea33cdc6dfc435d08f9b1c3290978b5d0ca22854110c3cf07ef8"
V3_CSS_SHA256 = "03965b2ffd6f52a6f7bf3d6bc69cd87353a8c3525d8932d5ed1f5050cd77729e"
RELEASE_SCRIPT_LINE = '  <script src="assets/release-state.js"></script>\n'


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_state() -> dict:
    text = STATE_PATH.read_text(encoding="utf-8")
    m = re.fullmatch(r"\s*window\.CFB_RELEASE_STATE\s*=\s*(\{.*\})\s*;\s*", text, flags=re.S)
    if not m:
        raise ValueError("assets/release-state.js is not in the expected machine-readable format")
    return json.loads(m.group(1))


def file_safe(name: str) -> str:
    # Match the production renderer's stable naming convention: spaces -> underscores.
    return name.replace(" ", "_")


def main() -> int:
    checks: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, ok, detail))

    # Core files.
    required = [MANIFEST_PATH, STATE_PATH, SITE_JS, INDEX, CSS, CNAME]
    for p in required:
        check(f"required file: {p.relative_to(ROOT)}", p.exists(), "present" if p.exists() else "missing")
    if not all(p.exists() for p in required):
        return finish(checks)

    manifest_doc = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    teams = manifest_doc.get("teams", [])
    check("manifest team count", len(teams) == 68, f"{len(teams)} / 68")

    display_names = [t["display_name"] for t in teams]
    canonical_names = [t["canonical_name"] for t in teams]
    paths = [t["pdf_path"] for t in teams]
    check("manifest display names unique", len(set(display_names)) == 68)
    check("manifest canonical names unique", len(set(canonical_names)) == 68)
    check("manifest PDF paths unique", len(set(paths)) == 68)

    expected_conf_counts = {"ACC":17, "Big Ten":18, "Big 12":16, "SEC":16, "Notre Dame":1}
    actual_conf_counts = {c: sum(1 for t in teams if t["conference"] == c) for c in expected_conf_counts}
    check("conference membership counts", actual_conf_counts == expected_conf_counts, str(actual_conf_counts))

    # Validate manifest filename derivation. Pitt is the deliberate display/canonical exception.
    filename_errors=[]
    for t in teams:
        expected = f"{file_safe(t['canonical_name'])}_2026_Preseason_Primer.pdf"
        if t["pdf_filename"] != expected or t["pdf_path"] != f"pdfs/{t['conference_slug']}/{expected}":
            filename_errors.append(t["display_name"])
    check("canonical filename/path derivation", not filename_errors, ", ".join(filename_errors))

    # State.
    try:
        state = load_state()
        check("release state parse", True)
    except Exception as e:
        check("release state parse", False, str(e))
        return finish(checks)

    conf_state = state.get("conferences", {})
    team_state = state.get("teams", {})
    check("release conference keys", set(conf_state) == set(expected_conf_counts), str(sorted(conf_state)))
    check("release conference values boolean", all(isinstance(v, bool) for v in conf_state.values()))
    unknown_team_keys = sorted(set(team_state) - set(display_names))
    check("team override names valid", not unknown_team_keys, ", ".join(unknown_team_keys))
    check("team override values boolean", all(isinstance(v, bool) for v in team_state.values()))

    # site.js still holds the exact 68 displayed team names.
    site_text = SITE_JS.read_text(encoding="utf-8")
    team_array_blocks = re.findall(r"teams:\s*\[(.*?)\]", site_text, flags=re.S)
    site_team_names=[]
    for block in team_array_blocks:
        site_team_names.extend(re.findall(r'"([^"]+)"', block))
    check("site.js displayed team count", len(site_team_names) == 68, f"{len(site_team_names)} / 68")
    check("site.js vs manifest displayed teams", set(site_team_names) == set(display_names),
          f"missing={sorted(set(display_names)-set(site_team_names))}; extra={sorted(set(site_team_names)-set(display_names))}")
    check("Pitt canonical filename override", '"Pitt": "Pittsburgh"' in site_text)
    check("Texas A&M filename punctuation retained", 'team.replace(/\\s+/g, "_")' in site_text)
    check("site uses staged release helper", "isTeamAvailable(conf, team)" in site_text)

    # index script order and appearance baseline.
    index_text = INDEX.read_text(encoding="utf-8")
    rel_pos = index_text.find('assets/release-state.js')
    app_pos = index_text.find('assets/site.js')
    check("release-state script loaded before site.js", rel_pos >= 0 and app_pos > rel_pos)
    normalized_index = index_text.replace(RELEASE_SCRIPT_LINE, "", 1).encode("utf-8")
    check("visible index HTML unchanged from v3", sha256_bytes(normalized_index) == V3_INDEX_SHA256,
          sha256_bytes(normalized_index))
    check("CSS byte-identical to v3", sha256_file(CSS) == V3_CSS_SHA256, sha256_file(CSS))
    check("CNAME", CNAME.read_text(encoding="utf-8").strip() == "cfb.drwhittier.com",
          CNAME.read_text(encoding="utf-8").strip())

    # Publication/file state.
    by_display={t["display_name"]: t for t in teams}
    released=[]
    unreleased=[]
    for t in teams:
        live = bool(conf_state.get(t["conference"], False) or team_state.get(t["display_name"], False))
        (released if live else unreleased).append(t)

    missing_released=[]
    leaked_unreleased=[]
    for t in released:
        if not (ROOT/t["pdf_path"]).is_file():
            missing_released.append(t["pdf_path"])
    for t in unreleased:
        if (ROOT/t["pdf_path"]).is_file():
            leaked_unreleased.append(t["pdf_path"])
    check("released teams have PDFs", not missing_released, "; ".join(missing_released))
    check("no unreleased PDFs exposed", not leaked_unreleased, "; ".join(leaked_unreleased))

    team_pdf_dirs = [ROOT/"pdfs"/s for s in ["acc","big-ten","big-12","sec","notre-dame"]]
    actual_pdfs=[]
    for d in team_pdf_dirs:
        if d.exists(): actual_pdfs.extend(p.relative_to(ROOT).as_posix() for p in d.glob("*.pdf"))
    unexpected=sorted(set(actual_pdfs)-set(paths))
    check("no unexpected team PDFs", not unexpected, "; ".join(unexpected))

    # Report counts, including custom waves.
    released_by_conf={c: sum(1 for t in released if t["conference"]==c) for c in expected_conf_counts}
    print("\nPublication state")
    print(f"  Released team primers: {len(released)} / 68")
    for c in expected_conf_counts:
        print(f"  {c}: {released_by_conf[c]} / {expected_conf_counts[c]}")

    return finish(checks)


def finish(checks: list[tuple[str,bool,str]]) -> int:
    print("\nValidation checks")
    failed=0
    for name, ok, detail in checks:
        status="PASS" if ok else "FAIL"
        if not ok: failed += 1
        suffix=f" — {detail}" if detail else ""
        print(f"  [{status}] {name}{suffix}")
    print()
    if failed:
        print(f"WEBSITE PUBLICATION GATE: FAILED ({failed} check{'s' if failed != 1 else ''})")
        return 1
    print(f"WEBSITE PUBLICATION GATE: PASSED ({len(checks)} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
