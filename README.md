# 2026 College Football Preseason Primer website

Static one-page catalog for the PDF-first primer project at **cfb.drwhittier.com**.

The current site appearance is intentionally frozen. Publication tooling is designed to support staged releases without redesigning the page.

## Public identity

- Creator: **DRWhittier**
- Site: **cfb.drwhittier.com**
- X: **@GatorBait7**

No personal email address, analytics, cookies, third-party fonts, or third-party scripts are included.

## Staged publication model

Team primers are released in waves. A wave may be a full conference or a custom set of teams.

**Important:** this GitHub Pages repository is public. A PDF uploaded here is publicly reachable by URL even if the homepage still says “Coming soon.” Therefore, do **not** upload unreleased PDFs to the repository. Upload only the PDFs that are intended to become public in the current wave.

Publication state is controlled in `assets/release-state.js`.

### Release an entire conference

1. Upload that conference's completed PDFs into its existing folder under `pdfs/`.
2. Open `assets/release-state.js`.
3. Change that conference from `false` to `true`. Example:

```js
"SEC": true
```

4. Commit the PDFs and the release-state change together.
5. Run/confirm the publication validator.

The homepage automatically updates all team links, conference counts, and the overall available count.

### Release a custom team wave

Keep the conference set to `false`, then add only the released display names under `teams`. Example:

```js
"teams": {
  "Florida": true,
  "Georgia": true,
  "Vanderbilt": true
}
```

Upload only those PDFs and commit them with the release-state change.

### Canonical filenames

Exact expected filenames/paths are listed in:

- `publication/teams_manifest.csv`
- `publication/teams_manifest.json`
- `publication/EXPECTED_PDF_PATHS.txt`

Website PDF filenames are aligned to the production renderer convention: spaces become underscores and meaningful punctuation is retained. Examples:

- `Pittsburgh_2026_Preseason_Primer.pdf` (site display remains **Pitt**)
- `Texas_A&M_2026_Preseason_Primer.pdf`
- `West_Virginia_2026_Preseason_Primer.pdf`

## Publication tools

`python tools/validate_publication.py`

Checks:

- all 68 manifest entries and conference membership
- publication-state validity
- every released team has the exact expected PDF
- no unreleased team PDF has accidentally been uploaded
- no unexpected PDF exists in the team folders
- website links resolve to the exact canonical paths
- the existing CSS and visible HTML remain unchanged from the v3 appearance baseline

`python tools/publish_wave.py --conference SEC --source <folder>`

Copies the expected PDFs for one conference from a local source folder, activates that conference, and runs the validator.

Custom wave example:

```bash
python tools/publish_wave.py --teams Florida Georgia Vanderbilt --source <folder>
```

Use `--dry-run` to check a wave without changing files.

For a GitHub-web-only workflow, you do not need the Python tools: upload the intended public PDFs and edit `assets/release-state.js` manually.

## Conference reviews

Conference reviews remain independently controlled in `assets/site.js` with the existing `reviewAvailable` setting. Their expected PDF paths are already defined there.

## GitHub Pages deployment

Current production configuration:

- custom domain: `cfb.drwhittier.com`
- GitHub Pages: deploy from `main` / root
- DNS: CNAME `cfb` → `granite777.github.io`
- HTTPS: enabled / enforced

No Pages or DNS configuration change is required to publish team PDFs.

## Privacy and identity checklist

- Keep Porkbun WHOIS/RDAP privacy enabled.
- Keep the GitHub account/profile free of unwanted identifying information.
- Keep public Git commit metadata free of personal email addresses.
- Keep the site free of analytics unless intentionally added later.
- Keep personal email/phone/address data off the site.
- PDF metadata Author: `DRWhittier`.
- Check PDFs for embedded local file paths or unwanted document properties.
- Keep X as the only contact link unless a project email is intentionally added later.
- Avoid wildcard DNS records.

## Canonical PDF publication block

Immediately before Sources:

**About this primer**

**DRWhittier · cfb.drwhittier.com · X: @GatorBait7 · Version 1.0 – [date]**

© 2026 DRWhittier. Original analysis, commentary, selection, and arrangement.

`cfb.drwhittier.com` and `@GatorBait7` are clickable. Copyright is on its own line. Do not restore the former “Independent preseason analysis covering every Power 4 team + Notre Dame.” sentence.
