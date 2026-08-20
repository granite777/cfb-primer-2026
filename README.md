# 2026 College Football Preseason Primer website

Static one-page catalog for the PDF-first primer project.

## Public identity

- Creator: **DRWhittier**
- Site: **cfb.drwhittier.com**
- X: **@GatorBait7**

No personal email address, analytics, cookies, third-party fonts, or third-party scripts are included.

## Publish a team PDF

1. Copy the completed PDF to the expected conference folder under `pdfs/`.
   Example: `pdfs/sec/Vanderbilt_2026_Preseason_Primer.pdf`
2. Open `assets/site.js`.
3. Add the team to the `availability` object:

```js
const availability = {
  "Vanderbilt": true,
};
```

4. Commit/publish. The site automatically updates the team link, conference count, and overall count.

## Conference reviews

Copy the conference-review PDF into `pdfs/conference-reviews/` using the filename already listed in `assets/site.js`, then change that conference's `reviewAvailable` value from `false` to `true`.

## GitHub Pages deployment

1. Create a repository for this site.
2. Upload the contents of this folder to the repository root.
3. In GitHub: **Settings → Pages → Deploy from a branch → main / root**.
4. In GitHub Pages settings, set the custom domain to `cfb.drwhittier.com` **before** adding the Porkbun DNS record.
5. At Porkbun, add a `CNAME` record for host `cfb` pointing to `<YOUR-GITHUB-USERNAME>.github.io`.
6. Return to GitHub Pages after DNS resolves and enable **Enforce HTTPS**.

### Privacy note before choosing the GitHub account

The Pages repository, commit history, and DNS target may make the GitHub account behind the site discoverable. If the existing GitHub username/profile reveals a full name or other identity you do not want associated with the project, use a separate/pseudonymous GitHub account such as a DRWhittier-branded account before publishing.

For commits from a local computer, also make sure Git's public author name/email do not expose a personal email address. A pseudonymous author name and GitHub's no-reply email are appropriate for this project.

## Privacy and identity checklist

Before launch:

- Confirm Porkbun WHOIS/RDAP is set to **Use Privacy Service**, not Make Public.
- Confirm the GitHub account/profile does not expose unwanted identifying information.
- Confirm public Git commit metadata does not contain a personal email address.
- Keep the site free of analytics unless intentionally added later.
- Keep the site free of personal email/phone/address data.
- Check PDF metadata and set Author/Creator to `DRWhittier` (or blank), not a full personal name.
- Check PDFs for embedded local file paths or document properties.
- Keep X as the only contact link unless a project email is intentionally added later.
- Confirm HTTPS is enforced after the custom domain is active.
- Avoid wildcard DNS records for the domain/subdomain.

## PDF publication credit

Recommended block immediately before Sources:

**About this primer**  
Created by **DRWhittier** as part of the *2026 College Football Preseason Primer* project. Independent analysis combining publicly available statistics, roster information, advanced metrics, and editorial evaluation.  

**cfb.drwhittier.com · X: @GatorBait7**  
**Version 1.0 – August XX, 2026**  

© 2026 DRWhittier. Original analysis, commentary, selection, and arrangement.
