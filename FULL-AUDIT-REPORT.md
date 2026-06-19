# SEO Full Audit Report — ilmiöt.fi

**Audit target:** https://www.ilmiöt.fi (`https://www.xn--ilmit-mua.fi`)
**Audit date:** 2026-06-19
**Auditor:** Claude Code SEO Audit
**Branch:** seo
**Previous audit:** 2026-06-16 (live 28/100, local build 74/100)

---

## Executive Summary

### SEO Health Score

| State | Score | Notes |
|-------|-------|-------|
| **Live site (deployed today)** | **28 / 100** | Pre-SEO version. None of the local SEO work is live. |
| **Local build (before this session's fixes)** | **72 / 100** | Strong content + schema, undermined by a domain-canonical defect and a script-breaking CSP. |
| **Local build (after C1–C2 + H1, H3, H4, M1–M2 this session)** | **~83 / 100** | All fixes below applied locally. |
| **After deploy (C3)** | **~85 / 100** (projected) | Remaining big lever: H2 internal "related phenomena" linking (deferred). |

> **Update 2026-06-19 (session 2):** Applied locally —
> **C1** domain canonical → www.ilmiöt.fi (895 URLs);
> **C2** CSP `'unsafe-inline'`;
> **H1** `.htaccess` 301 to canonical host (`www.xn--ilmit-mua.fi`);
> **H3** all 68 meta descriptions rewritten to clean full sentences;
> **H4** `author` = **Ilmiömies** + `datePublished`/`dateModified` in Article schema, visible byline + footer on every page, new **`tietoa.html`** About page (AboutPage + Person schema);
> **De-Kendom** — every "Kendom" reference removed; publisher Organization is now "Ilmiöitä";
> **M1** `random.html` `noindex`; **M2** 3 too-short titles lengthened.
> **Deferred:** **H2** related-phenomena internal-link blocks (per request); **C3** deploy (still not live); **M4** GSC/Bing (needs your accounts).

### Business Type
Finnish-language educational reference site. **68 in-depth articles** on social/power phenomena across 8 categories (power structures, propaganda & information ops, cognitive biases, bureaucracy, project-management laws, growth dynamics, scams & fraud, sales-pressure tactics). Non-commercial, informational intent. YMYL-adjacent (manipulation, fraud, cognitive bias). Server: **LiteSpeed**, HTTP/2 + HTTP/3, TTFB ~0.25 s.

### Top 5 Critical / High Issues
1. **🔴 Domain canonical mismatch.** You're auditing `ilmiöt.fi`, but every canonical, `og:url`, `og:image`, the sitemap, `robots.txt` and `llms.txt` point to `kendom.fi/ilmiöt/`. If deployed as-is, `ilmiöt.fi` tells Google "the real version lives on kendom.fi" and hands all ranking authority to the other domain.
2. **🔴 Nothing is deployed.** Live `last-modified` is 2026-06-16 13:23 — *before* the SEO files were written (17:09). The live homepage still has no meta description, no canonical, no OG tags. The 74→ improvement exists only in this repo.
3. **🔴 CSP breaks the site on deploy.** `.htaccess` sets `script-src 'self' cdn.jsdelivr.net` with **no `'unsafe-inline'` and no nonce**, but the site has **196 inline `<script>` blocks** (Mermaid init, Chart.js config, the `random.html` redirect). Deploying `.htaccess` as-is silently kills every diagram, chart, and the random-phenomenon feature.
4. **🟠 No host canonicalization.** `https://ilmiöt.fi/` and `https://www.ilmiöt.fi/` both return 200 with no redirect between them → duplicate content on two hostnames.
5. **🟠 Weak internal linking.** 2–5 internal links per page and **zero "related phenomena" blocks** across 68 thematically linked articles — a large topical-authority and crawl-depth miss.

### Top 5 Quick Wins
1. Search-replace `kendom.fi/ilmiöt` → `www.ilmiöt.fi` across all HTML, `sitemap.xml`, `robots.txt`, `llms.txt` (one scripted pass).
2. Add `'unsafe-inline'` to the CSP `script-src` (or nonce the inline scripts) before deploying `.htaccess`.
3. Add a 301 from non-www → www (or vice versa) at the host/`.htaccess` level.
4. Rewrite the 60 truncated meta descriptions into clean, full Finnish sentences (≤160 chars).
5. Add `<meta name="robots" content="noindex">` + canonical to `random.html`.

---

## Technical SEO

### Crawlability
- ✅ `robots.txt` present, `Allow: /` for all bots, explicit allows for GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot.
- ✅ Clean, static, human-readable URLs (`/paskuuttaminen.html`).
- ✅ XML sitemap with 69 URLs, `lastmod`, `priority`, `changefreq`.
- 🔴 **`robots.txt` `Sitemap:` line points to `https://kendom.fi/ilmiöt/sitemap.xml`** — wrong host for an `ilmiöt.fi` audit.
- 🔴 **Sitemap `<loc>` entries are all `kendom.fi`** — submitting it to GSC for ilmiöt.fi fails cross-host validation.

### Indexability
- 🔴 **Canonical mismatch (69/69 pages → `kendom.fi/ilmiöt/`).** This is the single most consequential issue. On `ilmiöt.fi`, these canonicals deindex the domain in favour of kendom.fi.
- 🟠 **www vs non-www both 200, no redirect.** Pick one host and 301 the other.
- 🟡 `random.html` has no canonical, no meta-robots, no description — a client-side JS redirect that can be indexed as a thin soft-redirect page. Add `noindex`.
- ✅ HTTP→HTTPS 301 redirect is in place.

### Security
- ✅ HTTPS with valid TLS, HTTP/2 + HTTP/3 (`alt-svc` advertised).
- 🔴 **Security headers not live.** `.htaccess` defines HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy, CSP — none are in the live response (undeployed). LiteSpeed honours `.htaccess`, so these will apply once deployed **after the CSP is fixed**.
- 🔴 **CSP/inline-script conflict (see Critical #3).** 196 inline scripts will be blocked.

### Core Web Vitals (lab estimate — no field data)
- ✅ TTFB ~0.25 s, LiteSpeed + HTTP/3, homepage HTML ~27 KB, no content `<img>` tags.
- 🟡 Google Fonts loaded from `fonts.googleapis.com` (preconnected). Mermaid (`@11`, deferred) and Chart.js (`@4`) render client-side — watch for **CLS** as diagrams paint in, and **INP** on diagram-heavy pages.
- ℹ️ No CrUX/GSC field data available in this run; CWV scored on lab signals only.

---

## Content Quality

### E-E-A-T
- ✅ **Experience/Expertise:** genuinely deep, original Finnish explanations; 3,200–4,400 words on sampled pages; Mermaid diagrams; cross-references to mechanisms.
- 🟠 **Authoritativeness:** no author byline, no organisation/credentials block, no "about" page. For YMYL-adjacent topics (fraud, manipulation, cognitive bias) this caps trust signals.
- 🟠 **Trust:** no `datePublished`/`dateModified` visible to users; no contact/about; `Article` schema lacks `author` and `datePublished`.

### Depth & Uniqueness
- ✅ Long-form, unique, non-templated prose per phenomenon. No within-site duplicate content (each page distinct).
- ✅ 1 `<h1>` per content page (68/68 phenomenon pages + index); only `random.html` has 0 (expected).

### AI Citation Readiness
- ✅ Definitional lead sentences + `DefinedTerm` schema → ideal passage-level citability for AI Overviews / ChatGPT / Perplexity.
- ✅ `llms.txt` present and well-structured.
- 🔴 `llms.txt` URLs all point to `kendom.fi/ilmiöt/` — same domain defect; AI engines would cite kendom.fi, not ilmiöt.fi.

---

## On-Page SEO

### Title Tags
- Format is `"<Phenomenon> — Ilmiöitä"`.
- Distribution (of 70): **5 under 30 chars**, 38 in the 30–60 sweet spot, **27 over 60 chars**.
- 🟡 Short titles (e.g. `Paskuuttaminen — Ilmiöitä`, 25 chars) waste SERP real estate; consider a descriptive modifier (`Paskuuttaminen — mitä se tarkoittaa? | Ilmiöitä`).
- 🟡 27 long titles risk SERP truncation.

### Meta Descriptions
- ✅ Present on 69/69 content pages, mostly 109–160 chars.
- 🟠 **60 of 69 end mid-sentence with no terminal punctuation** — they are mechanically cut from the first ~110 characters of body text (e.g. paskuuttaminen ends "…asteittaista heikentämistä niin").
- 🟡 3 descriptions repeat the term ("X: X tarkoittaa…"). Rewrite into clean, benefit-led sentences.

### Heading Structure
- ✅ Single H1 per page; logical H2/H3 hierarchy in sampled pages.

### Internal Linking
- 🟠 **Only 2–5 internal links per page; zero "related phenomena" sections.** With 68 tightly related articles in 8 categories, automated "Liittyvät ilmiöt" blocks (3–6 links each) would sharply improve crawl depth, topical clustering, and AI co-citation. Highest-leverage on-page opportunity.

---

## Schema & Structured Data

Comprehensive JSON-LD coverage (counts across the site):

| @type | Count | Where |
|-------|-------|-------|
| Article | 68 | each phenomenon page |
| DefinedTerm | 68 | each phenomenon page |
| DefinedTermSet | 68 | each phenomenon page |
| BreadcrumbList | 68 | each phenomenon page |
| CollectionPage | 69 | all content pages |
| Organization | 69 | all content pages |
| ListItem | 272 | breadcrumb / list items |
| WebSite | 1 | homepage |
| ItemList | 1 | homepage |

- ✅ Excellent breadth — among the strongest parts of the build.
- 🔴 All schema `url`/`@id` values reference `kendom.fi` (domain defect).
- 🟡 `Article` schema has no `author` or `datePublished` (ties to the E-E-A-T gap).
- 🟡 Pages carry both `Article` and `CollectionPage` — `CollectionPage` is questionable on a single-article page; consider dropping it there.

---

## Performance

- ✅ Fast origin: LiteSpeed, HTTP/3, TTFB ~0.25 s, small HTML payload, zero raster `<img>` on content pages.
- 🟡 Render-blocking Google Fonts CSS (mitigated by `preconnect`; `display=swap` already set; self-hosting would give full control).
- 🟡 Client-side Mermaid/Chart.js: defer is set, but monitor CLS/INP on diagram-heavy pages.
- ℹ️ No field data (CrUX/GSC) in this run — connect Search Console for the chosen domain to get real LCP/INP/CLS.

## Images

- ✅ No content `<img>` tags → no missing-alt debt, no oversized inline images, no image-driven CLS.
- ✅ 69 OG share images (1200×630 PNG, ~34–50 KB each) generated and referenced via `og:image`/`twitter:image`.
- 🟡 OG images are PNG; JPEG/WebP would cut file size ~50% (minor — already small).
- 🔴 OG image URLs point to `kendom.fi/ilmiöt/og/…` (domain defect — social previews 404 on ilmiöt.fi unless the path also exists there).

## AI Search Readiness

- ✅ AI crawlers explicitly allowed; `llms.txt` present; `DefinedTerm` schema + definitional structure; deep, citable content.
- 🔴 Every AI-facing URL (`llms.txt`, canonical, schema `@id`) points to kendom.fi → citations accrue to the wrong domain.
- 🟠 No author/dateline authority signals for AI to attribute.

---

## Category Scores (local build, ilmiöt.fi target)

| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Technical SEO | 22% | 60 | 13.2 |
| Content Quality | 23% | 78 | 17.9 |
| On-Page SEO | 20% | 65 | 13.0 |
| Schema / Structured Data | 10% | 82 | 8.2 |
| Performance (CWV, lab) | 10% | 80 | 8.0 |
| AI Search Readiness | 10% | 78 | 7.8 |
| Images | 5% | 75 | 3.8 |
| **Total** | **100%** | | **≈ 72 / 100** |

The content and schema are genuinely strong (a 68-article, deeply-written topical corpus is a real asset). The score is held back almost entirely by **infrastructure/config issues that are fast to fix**: the domain canonical defect, the CSP conflict, host canonicalization, and undeployed state. Resolve those four and this is an ~85 site.

---

*See `ACTION-PLAN.md` for the prioritized, step-by-step fix list.*
