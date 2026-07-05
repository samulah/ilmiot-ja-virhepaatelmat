# Full SEO Audit — ilmiöt.fi

**URL audited:** https://www.ilmiöt.fi/ (served as `https://www.xn--ilmit-mua.fi/`)
**Date:** 2026-07-05 (re-audit; supersedes the 2026-06-21 run)
**Scope:** 70 indexable URLs (68 phenomenon articles + homepage + about); `random.html` correctly `noindex`
**Method:** Live fetch (curl over HTTP/2+3) + full local source analysis. No field data (CrUX/Playwright unavailable in this environment); Performance assessed from architecture + live response behaviour.

---

## Executive Summary

**Overall SEO Health Score: 84 / 100 (live)** — unchanged from the 2026-06-21 audit.

### ⚠️ Headline finding: the score hasn't moved because the improvements were never deployed.

The live site is still the **19 June build**. Every fix from the last audit is sitting in the repo — some committed to `main`, some only in the working tree — but **none of it is on the server.** Google, Bing and the AI crawlers still see the pre-fix version. Deploying is the single highest-leverage action available and costs no new development.

| State | What's there | Deployed? |
|---|---|---|
| **Live server (19 Jun build)** | Base site: full schema, security headers, sitemap, llms.txt, redirects | ✅ live |
| **Committed to `main`, NOT deployed** | `Organization.logo` + `Article.image` (ImageObject), author `@id`→`#ilmiomies`, mermaid lazy-load via `IntersectionObserver` + init-ordering fix | ❌ pending deploy |
| **Working tree only (uncommitted, NOT deployed)** | Full-text search (`index.html` + generated `search-index.js` + `scripts/build_search_index.py`) | ❌ uncommitted + pending deploy |
| **Not done anywhere** | IDN→punycode host, `chart.js` `defer`, per-article OG images, thin/YMYL page strengthening, branded 404, deep-linkable search + `SearchAction` | ❌ open |

**Verification:** live `gaslighting.html` has 0 `ImageObject` and eager mermaid; local has 2 `ImageObject` + `IntersectionObserver`. Live `robots.txt`/`sitemap.xml`/canonicals all still use raw-Unicode `www.ilmiöt.fi`. Homepage `last-modified: 19 Jun 2026`; live homepage has no reference to `search-index.js`.

**Business type:** Publisher / educational reference ("tietopankki"). Finnish-language glossary of **68** societal phenomena across 8 categories (power, propaganda, cognitive bias, bureaucracy, project-management laws, growth/finance, scams, sales/pressure tactics). Single-language (fi), non-local, non-ecommerce.

### Top 5 issues (live)
1. **Deploy gap (highest leverage).** ~2 weeks of committed + staged SEO work is not on the server. Deploying immediately lifts Schema and Performance and makes the search feature real.
2. **IDN host inconsistency — still open everywhere.** All 71 local pages, `sitemap.xml` (70 `<loc>`), `robots.txt` and `llms.txt` (69 URLs) use raw-Unicode `www.ilmiöt.fi`; the site is served on punycode `xn--ilmit-mua.fi`. Non-ASCII in sitemap `<loc>` violates the sitemaps.org spec. Not blocking (Google normalises IDNs) but should be standardised. *(High)*
3. **`chart.js` render-blocking on 3 finance pages** — `<script src=…chart.umd.min.js>` with no `defer` (live *and* local). *(Medium perf)*
4. **Generic OG image site-wide** — all 68 articles share `/og/brand.png`; per-article `/og/<slug>.png` returns 404. *(Medium)*
5. **23 thin pages (<320 words incl. chrome)** — glossary format, but the thinnest (`paskuuttaminen` 241w, `conways-laki`, `hofstadterin-laki`, `brooksin-laki`…) are light; scam/finance pages remain uncited (borderline-YMYL). *(Medium)*

### Top 5 quick wins
1. **Deploy the committed + staged changes** → schema logo/image live, mermaid lazy-loads, search goes live.
2. **Standardise the host to punycode** across canonicals, `og:url`, JSON-LD `url`/`@id`, `sitemap.xml`, `robots.txt` Sitemap line, `llms.txt` (mechanical find-replace).
3. **Add `defer` to `chart.js`** on the 3 finance pages.
4. **Commit + `defer` the search script**, and make search deep-linkable (`/?q=…`) so you can add a `SearchAction` (sitelinks search box).
5. **Trim ~21 over-length `<title>` tags** (>65 chars truncate in SERPs).

---

## Deployment & Delta vs 2026-06-21

| Prior action item | Status now |
|---|---|
| Mermaid lazy-load (`IntersectionObserver`) | ✅ committed — ❌ not deployed |
| Mermaid init-ordering fix | ✅ committed — ❌ not deployed |
| `Organization.logo` + `Article.image` + author `@id` | ✅ committed — ❌ not deployed |
| IDN → punycode standardisation | ❌ not started (0/71 pages) |
| Per-article OG images | ❌ not started (`/og/<slug>.png` = 404) |
| Thin / YMYL page strengthening | ❌ not started |
| `chart.js` `defer` | ❌ not started (live + local) |
| **NEW:** full-text search (`search-index.js`) | 🆕 built, uncommitted, not deployed |

---

## Technical SEO — 87/100

**Strong (live-verified):**
- HTTPS everywhere; `Strict-Transport-Security: max-age=31536000; includeSubDomains` on every page.
- Full security-header suite site-wide: `X-Content-Type-Options`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy`, `Permissions-Policy`, and a real `Content-Security-Policy`. Well above typical.
- **Brotli compression** active (`content-encoding: br`): homepage 46 KB → 7.9 KB, article 47 KB → 12.6 KB, `style.css` → 2.5 KB.
- Clean redirects, all single-hop 301: `http→https`, `http/https apex → www`.
- Proper **404 status** on unknown URLs.
- LiteSpeed with **HTTP/2 + HTTP/3 (QUIC)** advertised via `alt-svc`; homepage TTFB ~0.10 s.
- `robots.txt` allows all + explicitly allow-lists GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot.
- `sitemap.xml` complete: 70 `<loc>` = every indexable page.

**Issues:**
- **IDN inconsistency (High/Medium):** raw `ö` host in every machine-readable URL vs served punycode. Non-ASCII in sitemap `<loc>` is spec-non-compliant; some validators reject it. Standardise on `https://www.xn--ilmit-mua.fi/`.
- **Default (unbranded) 404 page (Low):** returns correct 404 status (good for crawlers) but is the stock LiteSpeed page — a branded 404 linking home/categories would keep users on-site.
- **CSP over-broad (Low):** `style-src` allows `fonts.googleapis.com` and `font-src` `fonts.gstatic.com`, but fonts are self-hosted (`/fonts/*.woff2`) and no page references Google Fonts. Drop the unused external font origins. `script-src` uses `'unsafe-inline'` (pragmatic for the inline mermaid/search init; acceptable for a no-input static site).

---

## Content Quality — 76/100

**Strong:**
- Original, clearly-written Finnish; consistent four-part structure (what it is / mechanism / how to spot / examples).
- E-E-A-T basics: dedicated `tietoa.html` (purpose, author, selection method, sourcing statement); per-article byline `Kirjoittanut Ilmiömies · Päivitetty …` with `rel="author"`.
- Good citability: definitions name origins/classic cases.

**Issues:**
- **23 thin pages (<320 words incl. nav/breadcrumb/footer chrome; real body shorter).** Thinnest: `paskuuttaminen` 241, `yhdeksanyhdeksan` 258, `conways-laki` 262, `starve-the-beast` 264, `hofstadterin-laki` 275, `performatiivinen-lasnaolo` 276, `tekninen-velka` 282, `bikeshedding` 286, `scope-creep` 287, `brooksin-laki` 292. Mostly the project/software-law cluster. Expand with a concrete example + a short "miten tunnistat" list.
- **Pseudonymous authorship on borderline-YMYL topics (Medium):** "Ilmiömies" has no external identity/credentials. Fine for general explainers, but scams (`pig-butchering`, `ponzi-pyramidi`, `ennakkomaksuhuijaus`) and finance (`korkoa-korolle`, `negatiivinen-korkoa`, `korkokierre`) should carry explicit citations/sources.

---

## On-Page SEO — 89/100

**Strong (verified across all 68 articles):**
- **0 duplicate `<title>` and 0 duplicate meta descriptions** — 68/68 unique.
- **Exactly one `<h1>` per page** — 0 exceptions.
- Meta-description length healthy (median 151, none <70 chars).
- Strong internal linking (~6–8 related phenomena + breadcrumb + home + about per article); clean descriptive slug URLs.

**Issues (minor):**
- **21 titles >65 chars** (median 58, max 85) — will truncate in Google SERPs. The brand suffix `— Ilmiöitä` usually truncates (acceptable), but trim the longest so the meaningful phrase survives.
- 7 meta descriptions >160 chars (slight truncation).
- Homepage `og:title` == `og:site_name` (cosmetic).
- Breadcrumb category node (position 2) has no `item` URL (categories are homepage anchors) — could point to `index.html#<category>`.

---

## Schema & Structured Data — 85/100 live (→ ~92 after deploy)

**Live (all valid JSON-LD, `@graph` + `@id` referencing):**
- Homepage: `WebSite`, `Organization`, `CollectionPage` → `mainEntity` `ItemList` (68 `ListItem`s).
- Every article: `BreadcrumbList`, `Article`, `DefinedTerm`/`DefinedTermSet`, author `Person`.
- About page: `AboutPage`.

**Committed but not yet live** (present in local source, absent on server):
- `Organization.logo` (favicon.svg ImageObject) on homepage + articles + about.
- `Article.image` (brand.png ImageObject, 1200×630) on all 68 articles.
- Author `Person` `@id`-linked to canonical `#ilmiomies` + `description`.

**Still open (Low):**
- No `SearchAction` — currently defensible (search is client-side, no `?q=` endpoint). Becomes a real win once search is made deep-linkable (see Performance/AI).
- Author `Person` lacks `sameAs`/`jobTitle` (pseudonymous — acceptable).

---

## Performance (CWV) — 80/100 (→ ~86 after deploy + chart.js fix)

*No CrUX/lab field data available; assessed from architecture + live behaviour.*

**Strong:**
- Static HTML on LiteSpeed, HTTP/2 + QUIC, Brotli; ~0.10 s homepage TTFB; tiny transfer sizes.
- Inline critical CSS on homepage; small external `style.css` on articles.
- Self-hosted `woff2` fonts (DM Sans + Spectral) with `font-display: swap` — no render-blocking webfont, no FOIT, no third-party font origin actually used.
- No analytics / ad / tag-manager third parties.
- CLS guarded: `style.css` reserves `.mermaid { min-height }` and charts carry explicit `height`.

**Issues:**
- **`chart.js@4` render-blocking on 3 finance pages** (`korkoa-korolle`, `korkokierre`, `negatiivinen-korkoa`) — no `defer`/`async`, live *and* local. Add `defer`. *(Medium)*
- **Mermaid eager on 55 pages live** — `<script defer src=…mermaid.min.js>` downloads on every article view. The lazy-load (`IntersectionObserver`, only downloads near a diagram) is **committed but not deployed** — deploy removes this cost. *(Medium; resolved by deploy)*
- **Search script loads synchronously (once live):** `<script src="search-index.js">` (157 KB uncompressed, ~35 KB Brotli) with no `defer`, at end of `<body>`. Not render-blocking for content, but blocks the parser and delays DOMContentLoaded. `defer` it, or lazy-load on first focus of the search box. *(Low)*

---

## Images — 80/100

- SVG favicon; almost no raster `<img>` content (diagrams are mermaid/SVG) → negligible alt-text debt.
- **Single shared OG image** `/og/brand.png` (1200×630, 200 OK, 29 KB) across all 68 articles; `/og/<slug>.png` = 404. Per-article OG images would lift social + AI-preview CTR. `scripts/generate_og_images.py` reportedly exists in-repo — wire it into the build and set per-page `og:image` + descriptive `og:image:alt`.

---

## AI Search Readiness (GEO) — 90/100

**Strong — a highlight:**
- `robots.txt` explicitly allows GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot.
- `llms.txt` comprehensive: summary, 8 categories, all phenomena with absolute URLs, author, explicit reuse note.
- `DefinedTerm`/`DefinedTermSet` schema — ideal machine-readable definitions for AI answer engines.
- Definitional, self-contained, citable passages naming origins/cases.

**Opportunities (Low):**
- Fix the IDN host in `llms.txt` URLs for consistency with the served domain.
- Per-passage anchors / short FAQ blocks on top phenomena for direct citation.
- Deep-linkable search (`/?q=`) → enables both `SearchAction` and cleaner AI navigation.

---

## Score Summary

| Category | Weight | Live | Weighted | Projected¹ |
|---|---:|---:|---:|---:|
| Technical SEO | 22% | 87 | 19.1 | 90 |
| Content Quality | 23% | 76 | 17.5 | 76 |
| On-Page SEO | 20% | 89 | 17.8 | 90 |
| Schema | 10% | 85 | 8.5 | 92 |
| Performance (CWV) | 10% | 80 | 8.0 | 86 |
| AI Search Readiness | 10% | 90 | 9.0 | 90 |
| Images | 5% | 80 | 4.0 | 80 |
| **Total** | **100%** | | **84** | **~86–87** |

¹ Projected = after deploying the committed + staged changes and doing the two mechanical fixes (IDN→punycode, chart.js `defer`). Reaches ~89–90 with per-article OG images + thin/YMYL strengthening.

See `ACTION-PLAN.md` for the prioritised fix list.
