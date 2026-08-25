# 2026 College Football Preseason Primer Website – Publication Readiness QA

**Source site:** `cfb-primer-site-v3`  
**Prepared state:** `v4-publication-ready`  
**Result:** **PASSED**

## Scope

The existing website design was preserved. This update adds staged-publication infrastructure and validation only; it does not redesign the site.

## Appearance preservation

- Original v3 `assets/styles.css` SHA-256: `03965b2ffd6f52a6f7bf3d6bc69cd87353a8c3525d8932d5ed1f5050cd77729e`
- v4 `assets/styles.css`: **byte-for-byte identical**
- Original v3 `index.html` SHA-256: `d50c86d3b73cea33cdc6dfc435d08f9b1c3290978b5d0ca22854110c3cf07ef8`
- v4 adds one invisible script include for `assets/release-state.js`; after removing that line, the HTML matches the original v3 hash exactly.
- Existing team display labels, conference-card layout, filters, copy, colors, spacing, and CSS were not changed.

## Staged release behavior

Publication state is now isolated in `assets/release-state.js`.

- Full conference: flip one conference boolean to `true`.
- Custom wave: add individual team display names under `teams`.
- Unreleased teams continue to show `Coming soon`.
- Team/conference/overall counts continue to update automatically.
- Unreleased PDFs should never be uploaded to the public repository, because direct URLs would still be public even without a homepage link.

## Canonical team/path audit

- 68/68 project teams represented.
- Conference counts: ACC 17, Big Ten 18, Big 12 16, SEC 16, Notre Dame 1.
- Exact PDF path manifest created for all 68 teams.
- Website filename convention aligned to production: spaces become underscores while meaningful punctuation is retained.
- Existing display label `Pitt` is preserved, but its link maps to canonical `Pittsburgh_2026_Preseason_Primer.pdf`.
- `Texas A&M` maps to `Texas_A&M_2026_Preseason_Primer.pdf`.

## Validator

`python tools/validate_publication.py`

Initial site state result:

- Released: 0/68
- 29 checks passed
- 0 checks failed
- `WEBSITE PUBLICATION GATE: PASSED`

The gate checks manifest integrity, release-state validity, exact filenames/paths, released-PDF presence, accidental exposure of unreleased PDFs, unexpected PDFs, the custom domain, and appearance-baseline hashes.

## Publish-wave utility test

A complete simulated SEC release was run in a disposable copy using 16 dummy PDF fixtures.

- SEC expected: 16
- SEC copied: 16
- SEC activated: 16/16
- Other conferences remained 0 available
- Publication validator after activation: **PASSED**
- `Texas_A&M_2026_Preseason_Primer.pdf` path validated successfully

No dummy PDFs are included in the actual v4 package.

## Deployment settings

No DNS or GitHub Pages setting changes are required.

- Domain remains `cfb.drwhittier.com`
- CNAME remains unchanged
- Existing HTTPS configuration is untouched
- `assets/styles.css` remains unchanged

## Recommended use

Prepare/review this v4 repository now, before the first PDF release. When a wave is ready, upload only that wave's PDFs, activate the conference or teams in `assets/release-state.js`, require `WEBSITE PUBLICATION GATE: PASSED`, deploy, verify live links, then publicize the wave.
