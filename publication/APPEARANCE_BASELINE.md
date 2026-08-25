# Appearance baseline

The website's visual design is intentionally unchanged from `cfb-primer-site-v3`.

Original v3 SHA-256:

- `index.html`: `d50c86d3b73cea33cdc6dfc435d08f9b1c3290978b5d0ca22854110c3cf07ef8`
- `assets/styles.css`: `03965b2ffd6f52a6f7bf3d6bc69cd87353a8c3525d8932d5ed1f5050cd77729e`

The publication-ready version adds only one invisible script include to `index.html`: `assets/release-state.js`. The validator removes that line before comparing the visible HTML to the v3 baseline.

`assets/styles.css` must remain byte-for-byte unchanged unless an intentional design revision is separately approved.
