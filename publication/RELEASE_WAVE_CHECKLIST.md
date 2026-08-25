# Website Release Wave Checklist

## Before the wave

- [ ] Decide the exact teams/conference in this public wave.
- [ ] Confirm every PDF has passed primer production QA.
- [ ] Confirm PDF filenames exactly match `publication/teams_manifest.csv`.
- [ ] Do not place later-wave PDFs in the public GitHub repository.

## Publish

- [ ] Upload/copy only this wave's PDFs into the correct `pdfs/<conference>/` folders.
- [ ] Activate the conference or individual teams in `assets/release-state.js`.
- [ ] Run `python tools/validate_publication.py` or verify equivalent checks manually.
- [ ] Require `WEBSITE PUBLICATION GATE: PASSED`.
- [ ] Commit the PDFs and release-state change together.

## After GitHub Pages deploys

- [ ] Open `https://cfb.drwhittier.com/` in a fresh/private browser window.
- [ ] Confirm the overall available count is correct.
- [ ] Confirm the conference count is correct.
- [ ] Open at least two newly released PDFs from the homepage.
- [ ] Confirm unreleased teams still show `Coming soon`.
- [ ] Confirm HTTPS remains enforced.
- [ ] Then publicize the wave.
