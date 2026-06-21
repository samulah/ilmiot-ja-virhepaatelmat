# SEO Action Plan — ilmiöt.fi

Generated 2026-06-21. Health score: **84/100**. Priority: Critical > High > Medium > Low.

## Critical (blocks indexing / penalties)
*None.* The site is fully crawlable and indexable.

## High (fix within 1 week)
1. ✅ **DONE (2026-06-21, not yet deployed).** Mermaid now lazy-loads via `IntersectionObserver` (200px margin) on all 55 pages — the library downloads only when a diagram nears the viewport. `scripts/seo_patch_v2.py`.
2. ✅ **DONE (2026-06-21, not yet deployed).** Init ordering fixed: `load → onload → mermaid.initialize({startOnLoad:false}) → mermaid.run()` (was an immediate inline init before the `defer`-loaded bundle → threw, brand theme lost). **Pending: confirm render in a browser after deploy** (scroll to a diagram, check gold/cream styling + clean console).

## Medium (fix within 1 month)
3. **Standardize the host to punycode.** Replace `https://www.ilmiöt.fi/` with `https://www.xn--ilmit-mua.fi/` in: every page's `<link rel="canonical">` and `og:url`/`twitter` URLs, all JSON-LD `url`/`@id`, `sitemap.xml` `<loc>`, the `robots.txt` `Sitemap:` line, and `llms.txt`. Non-ASCII in sitemap `<loc>` is spec-non-compliant; consistency with the served host is cleaner.
4. **(Already done — CLS guarded.)** `style.css` reserves `.mermaid { min-height: 220px }` and charts use a `height` attribute. Optional polish: reserve height proportional to each diagram's real size so diagrams taller than 220px don't shift.
5. ✅ **DONE (2026-06-21, not yet deployed):**
   - `Organization.logo` (favicon.svg ImageObject) → homepage + 68 articles + about page.
   - `Article.image` (brand.png ImageObject, 1200×630) → 68 articles.
   - author `Person`: `@id`-linked to canonical `#ilmiomies` + `description` → 68 articles.
   - `SearchAction` **intentionally skipped** — on-site search is client-side only (no `?q=` endpoint), so a SearchAction target would be non-functional. `sameAs` omitted (pseudonymous author, no external profiles).
6. **Per-article OG images.** Generate unique 1200×630 images (the repo's `scripts/generate_og_images.py` already exists) and set per-page `og:image` + descriptive `og:image:alt`, instead of the shared `/og/brand.png`.
7. **Strengthen thin / borderline-YMYL pages.** Expand the 13 sub-300-word articles (start with `paskuuttaminen`, `conways-laki`, `hofstadterin-laki`, `yhdeksanyhdeksan`, `starve-the-beast`) with a concrete example + "how to recognise" list. For scam/finance topics (`pig-butchering`, `ponzi-pyramidi`, `ennakkomaksuhuijaus`, `korkoa-korolle`, `negatiivinen-korkoa`, `korkokierre`) add explicit citations/sources to lift trust.

## Low (backlog)
8. Add `defer` to the `chart.js` tag on the 3 finance pages (currently render-blocking).
9. Differentiate homepage `og:title` from `og:site_name`.
10. Point breadcrumb category node (position 2) to `index.html#<category>`.
11. Add per-passage anchors / FAQ blocks to top phenomena for direct AI citation.
12. Verify the site is added to Google Search Console + Bing Webmaster Tools (using the punycode property) and the sitemap submitted, so you get real indexation + CWV field data.

---
*Note: this overwrites the prior 2026-06-19 audit output of the same skill. No measurements used Playwright/CrUX — those tools were unavailable in this run; Performance is assessed from architecture and assets.*
