# Full SEO Audit — ilmiöt.fi

**URL audited:** https://www.ilmiöt.fi/ (served as `https://www.xn--ilmit-mua.fi/`)
**Date:** 2026-06-21
**Crawl scope:** 70 indexable pages (68 phenomenon articles + homepage + about page); `random.html` correctly `noindex`
**Method:** Live fetch + local source analysis (inline, no field data — Playwright/CrUX unavailable in this environment)

---

## Executive Summary

**Overall SEO Health Score: 84 / 100** — strong.

**Business type detected:** Publisher / educational reference site ("tietopankki"). Finnish-language glossary of 68 societal phenomena (power structures, propaganda, cognitive biases, bureaucracy, project-management laws, growth dynamics, scams, sales/pressure tactics). Single-language (fi), non-local, non-ecommerce.

This is a well-engineered static site: clean security posture, complete and consistent structured data, real internal linking, an About page with authorship, and deliberate AI-search readiness (llms.txt + AI-crawler allow-list). The weak spots are narrow and fixable: an IDN URL inconsistency, a heavy third-party diagram library on most pages, generic social images, and a handful of thin pages.

### Top 5 issues
1. **IDN URL inconsistency** — canonical, `og:url`, schema `@id`/`url`, `sitemap.xml`, `robots.txt` and `llms.txt` all declare the raw-Unicode host `www.ilmiöt.fi`, while the site is served on punycode `xn--ilmit-mua.fi`. Non-ASCII in `<loc>` is non-compliant with the sitemap spec. *(Medium)*
2. **`mermaid.min.js` on 55 pages from jsDelivr** — large client-side render library + `chart.js` on 3 pages; the heaviest CWV/INP factor on an otherwise featherweight site. *(Medium-High perf)*
3. **Mermaid init ordering looks broken** — `mermaid.initialize()` is an immediate inline script placed *after* the `defer`-loaded bundle, so `mermaid` is likely undefined when it runs. Verify diagrams actually render. *(Medium — correctness)*
4. **Generic OG image site-wide** — all 68 articles share `/og/brand.png` with generic `og:image:alt`; no per-article social/AI preview. *(Medium)*
5. **13 thin pages (<300 words incl. chrome)** — glossary format, but the shortest (e.g. `paskuuttaminen`, `conways-laki`, `hofstadterin-laki`) are light on examples. *(Medium)*

### Top 5 quick wins
1. Add `logo` (ImageObject) to the `Organization` schema and `image` to the `Article` schema → unlocks Article rich-result eligibility.
2. Add per-article `og:image` + descriptive `og:image:alt` (instead of the shared `/og/brand.png`).
3. Add `defer` to the `chart.js` tag on the 3 finance pages.
4. Add `potentialAction` (SearchAction) to the `WebSite` schema — you already have an on-site search box.
5. Give the author `Person` a `description`/`sameAs` (even just the About page) and consider a real attributed identity for the finance/scam pages (borderline-YMYL).

---

## Technical SEO — 88/100

**Strong:**
- HTTPS everywhere; `Strict-Transport-Security: max-age=31536000; includeSubDomains`.
- Full security-header suite: `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, and a real `Content-Security-Policy`. Well above typical.
- Canonicalization correct: `http→https` 301, apex `→ www` 301.
- `robots.txt` allows all + explicitly allows GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot.
- `sitemap.xml` complete: 70 `<loc>` entries = every indexable page; `random.html` excluded and `noindex, follow`.
- LiteSpeed with HTTP/2 + HTTP/3 (QUIC) advertised.
- `viewport` meta on every page; responsive CSS.

**Issues:**
- **IDN inconsistency (Medium):** every machine-readable URL uses raw `ö` (`www.ilmiöt.fi`) instead of punycode. Google normalizes IDNs, so this is not blocking indexation, but: (a) non-ASCII characters in sitemap `<loc>` violate the sitemaps.org / RFC 3986 requirement and some validators/crawlers reject them; (b) consistency between the served host (punycode) and declared canonical is cleaner. **Standardize on `https://www.xn--ilmit-mua.fi/` in canonical, `og:url`, schema `url`/`@id`, `sitemap.xml`, `robots.txt` Sitemap line, and `llms.txt`.**
- No `<meta name="robots">` on indexable pages (fine — defaults to index,follow).

---

## Content Quality — 76/100

**Strong:**
- Original, clearly-written Finnish; consistent four-part structure (what it is / mechanism / how to spot it / examples).
- E-E-A-T basics present: dedicated `tietoa.html` About page explaining purpose, author, selection method, and sourcing ("perustuu julkisiin lähteisiin ja vakiintuneeseen käsitteistöön"); per-article byline `Kirjoittanut Ilmiömies · Päivitetty …` with `rel="author"`.
- Good citability: definitions name origins/classic cases (e.g. gaslighting → 1944 film *Gaslight*).

**Issues:**
- **Pseudonymous authorship (Medium):** "Ilmiömies" has no real identity, credentials, or external profile. Fine for general explainers, but several topics border on YMYL — scams (`pig-butchering`, `ponzi-pyramidi`, `ennakkomaksuhuijaus`) and finance (`korkoa-korolle`, `negatiivinen-korkoa`, `korkokierre`). For those, add explicit sourcing/citations and stronger trust signals.
- **Thin pages (Medium):** 68 articles range 240–669 visible words (median 341, incl. nav/breadcrumb/footer chrome — real body is shorter). 13 are <300 words. Glossary format tolerates this, but expanding the thinnest with a concrete example + "how to recognise" list would help both ranking and AI citation.

---

## On-Page SEO — 90/100

**Strong:**
- Unique, descriptive, well-sized `<title>` per page (e.g. *"Gaslighting — todellisuuden järjestelmällinen kiistäminen — Ilmiöitä"*).
- Unique meta descriptions per page.
- Exactly one `<h1>` per page; logical `h2`/`h3` structure; homepage `h2`s map to the 8 categories.
- Strong internal linking: each article links to ~6–8 related phenomena plus breadcrumb + home + about (sample `gaslighting.html`: 13 internal `.html` links).
- Clean, descriptive slug URLs.

**Issues (minor):**
- `og:site_name` and `og:title` are identical on the homepage. Cosmetic.
- Breadcrumb category node (position 2) has no `item` URL because categories are homepage anchors — could point to `index.html#<category>`.

---

## Schema & Structured Data — 85/100

**Implemented (all valid JSON-LD, `@graph` + `@id` referencing):**
- Homepage: `WebSite`, `Organization`, `CollectionPage` with `mainEntity` `ItemList` (68 `ListItem`s).
- Every article: `BreadcrumbList`, `Article` (headline, description, inLanguage, articleSection, isPartOf, publisher, about→`DefinedTerm`/`DefinedTermSet`, author `Person`, `datePublished`, `dateModified`).
- About page: `AboutPage`.

**Gaps (Medium/Low):**
- `Organization` has **no `logo`** (ImageObject) — required for several Google rich results.
- `Article` has **no `image`** property (relies on `og:image` only) — Article rich-result eligibility wants it.
- Author `Person` lacks `description`/`sameAs`/`jobTitle`.
- `WebSite` lacks `potentialAction` (SearchAction) — you have an on-site search; adding it enables the sitelinks search box.

---

## Performance (CWV) — 78/100

*No field data (CrUX) or lab run available in this environment; assessed from architecture + assets.*

**Strong:**
- Static HTML on LiteSpeed, HTTP/2 + QUIC; small documents.
- Inline critical CSS on homepage; small external `style.css` (~10 KB) on articles.
- Self-hosted `woff2` fonts with `font-display: swap` (no render-blocking webfont, no FOIT).
- No analytics/ad/tag-manager third parties.

**Issues:**
- **`mermaid@11` from jsDelivr on 55 pages (Medium-High):** large client-side diagram renderer; main contributor to JS download + parse/execute (INP/TBT risk), plus a third-party CDN dependency. Consider pre-rendering diagrams to static inline SVG at build time, or lazy-loading mermaid only when a `.mermaid` block is near the viewport (`IntersectionObserver`).
- **`chart.js@4` on 3 finance pages loaded without `defer`/`async`** (render-blocking). Add `defer`.
- **Init ordering (see correctness note):** `mermaid.initialize()` runs inline before the deferred bundle — verify diagrams render at all.

**Already handled well:** CLS is guarded — `style.css` reserves `.mermaid { min-height: 220px }` and chart `<canvas>` elements carry an explicit `height` attribute, so diagrams/charts don't shift layout on render. (Residual: a mermaid diagram taller than 220px can still shift slightly.)

---

## Images — 80/100

- Favicon is SVG with descriptive `alt`. Almost no raster `<img>` content (diagrams are SVG/mermaid), so no alt-text debt.
- **Single shared OG image** `/og/brand.png` (1200×630, 200 OK) across all 68 articles, with generic `og:image:alt`. Per-article OG images would lift social + AI preview CTR. The repo already contains `scripts/generate_og_images.py` — only `brand.png` is deployed.

---

## AI Search Readiness (GEO) — 90/100

**Strong — this is a highlight:**
- `robots.txt` explicitly allows GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot.
- `llms.txt` present, comprehensive: summary, 8 categories, all phenomena with absolute URLs, author, and an explicit reuse note ("Sisältö on vapaasti viitattavissa").
- `DefinedTerm` / `DefinedTermSet` schema — ideal machine-readable definitions for AI answer engines.
- Definitional, self-contained, citable passages; named origins/cases.

**Opportunities (Low):**
- Per-passage anchors / FAQ blocks for direct citation.
- Fix the IDN host in `llms.txt` URLs for consistency with the served domain.

---

## Score Summary

| Category | Weight | Score | Weighted |
|---|---:|---:|---:|
| Technical SEO | 22% | 88 | 19.4 |
| Content Quality | 23% | 76 | 17.5 |
| On-Page SEO | 20% | 90 | 18.0 |
| Schema | 10% | 85 | 8.5 |
| Performance (CWV) | 10% | 80 | 8.0 |
| AI Search Readiness | 10% | 90 | 9.0 |
| Images | 5% | 80 | 4.0 |
| **Total** | **100%** | | **84** |

See `ACTION-PLAN.md` for the prioritized fix list.
