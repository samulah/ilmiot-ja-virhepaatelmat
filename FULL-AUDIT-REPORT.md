# Full SEO Audit — ilmiöt.fi

**Audited:** 2026-07-25 · **URL:** https://www.ilmiöt.fi/ (`xn--ilmit-mua.fi`)
**Scope:** 111 live URLs crawled (100% of sitemap), all returning 200.
**Previous audit:** 2026-07-05 — 84/100

## SEO Health Score: **80 / 100**

| Category | Weight | Score | Weighted |
|---|---|---|---|
| Technical SEO | 22% | 83 | 18.3 |
| Content Quality | 23% | 76 | 17.5 |
| On-Page SEO | 20% | 78 | 15.6 |
| Schema / Structured Data | 10% | 92 | 9.2 |
| Performance (CWV) | 10% | 74 | 7.4 |
| AI Search Readiness | 10% | 82 | 8.2 |
| Images | 5% | 85 | 4.3 |
| **Total** | | | **80.4** |

> **On the score vs. the prior 84/100:** this is not a regression. The prior run scored Content on raw text extraction; this run measured article *prose* separately from boilerplate, which revealed that median body copy is 269 words rather than the 462 a naive extraction reports. Several real defects were also fixed since then (see Progress). Treat 80 as a re-baselined number, not a drop.

**Business type:** Independent Finnish-language reference/publisher site — a glossary of 109 social, cognitive and organisational phenomena. Non-commercial, no transactions, no local presence. The relevant playbook is publisher/knowledge-base SEO: entity coverage, passage citability, and E-E-A-T — not conversion or local signals.

---

## Executive Summary

This is a well-built, carefully maintained site. There are **no Critical issues** — nothing blocks indexing, nothing risks a penalty, and the whole sitemap resolves cleanly. Security headers, structured data, compression and editorial quality are all above what most independent sites achieve.

The remaining upside is concentrated in two places: **canonical host discipline** (four URL variants currently serve identical 200s) and **passage structure** (97 of 111 pages have no subheadings in the body, which is the main thing standing between this content and featured snippets / AI citations).

### Top 5 issues

1. **Four host/protocol variants all serve 200 with no redirect** — `http://`, `http://www.`, `https://www.` and `https://` apex are all live. Canonical tags mitigate the duplication, but HTTP is served without an HTTPS redirect.
2. **97 of 111 pages have only two headings** (the `h1` and "Liittyvät ilmiöt"). The two most valuable sections — *Ilmiö arjessa* and *Tunnistaminen ja vastakeinot* — are `<strong>` inside a `<div>`, not headings.
3. **`llms.txt` is 3 pages out of date** — it claims 109 phenomena but lists 106, omitting `1-prosentin-saanto`, `aanekas-vahemmisto` and `pareto-periaate`.
4. **`sitemap.xml` freshness signals are inconsistent** — 93 of 111 `<lastmod>` values disagree with the schema `dateModified`, and the most recently edited page (`bikeshedding.html`) is stale in the sitemap.
5. **929 KB of third-party JavaScript** (`mermaid@11`) loads on 87 article pages from `cdn.jsdelivr.net` to render diagrams that never change.

### Top 5 quick wins

1. Add a canonical-host redirect rule (`.htaccess`) — one block, resolves issue 1.
2. Re-run the sitemap + `llms.txt` build and commit — resolves issues 3 and 4.
3. Promote the two box labels to `<h2>` in the article template — resolves issue 2 across ~97 pages in one edit.
4. Add `defer` to `chart.js` on the 3 finance pages — it currently sits in `<head>` un-deferred and blocks render.
5. Fix the live typo "Katkais**tt**u y-akseli" in `tilastoilla-valehtelu.html`.

---

## Progress since the 2026-07-05 audit

| # | Prior item | Status |
|---|---|---|
| 1 | **Deploy the backlog** (was Critical) | ✅ **Done** — live matches the repo byte-for-byte on all 111 pages (md5-verified) |
| 5 | Strengthen thin pages | ✅ **Largely done** — pages under 320 total words fell from 23 → 4 |
| 10 | Differentiate `og:title` from `og:site_name`; category breadcrumb node | ✅ **Done** — breadcrumb position 2 now points to `index.html#<category>` |
| 3 | `defer` on `chart.js` | ❌ Not done — still in `<head>`, un-deferred, on 3 pages |
| 2 | Punycode host standardisation | ❌ Not done — see the reassessment below |
| 4 | Per-article OG images | ❌ Not done — all 111 pages share `/og/brand.png`; `/og/<slug>.png` still 404s |
| 6 | `SearchAction` + `?q=` deep linking | ❌ Not done |
| 7 | Trim over-length titles | ❌ Regressed — titles over 65 chars went 21 → 32 |
| 8 | Tighten CSP | ❌ Not done — `fonts.googleapis.com` / `fonts.gstatic.com` still allowed but unused (0 pages reference them) |
| 9 | Branded 404 | ❌ Not done — still the 1,251-byte stock LiteSpeed page (status code is correct) |
| 11 | Per-passage anchors / FAQ blocks | ❌ Not done — 1 `FAQPage` across the site |
| 12 | GSC / Bing verification | ⚠️ Unverified — no API credentials configured locally |

**The deploy gap is closed.** That was the previous audit's Critical item and the long-running failure mode for this project. All 111 live pages are byte-identical to `main`.

### Reassessing the punycode item

The prior audit rated this **High**. I'd downgrade it to **Medium**, and the reasoning matters more than the label:

- Every signal on the site consistently uses the UTF-8 form `https://www.ilmiöt.fi/` — canonicals (111/111), `og:url`, all JSON-LD `@id`/`url`, all 111 sitemap `<loc>` entries, `llms.txt`, and the `robots.txt` `Sitemap:` line. There is no *mixing*, which is the failure mode that actually splits signals.
- Google documents support for IDNs and normalises UTF-8 URLs to punycode on its side.
- So the practical risk is low. What remains is genuine but narrower: the sitemaps.org spec and RFC 3986 both call for ASCII URIs, and third-party tooling (validators, log processors, some crawlers) handles raw non-ASCII inconsistently.

Worth doing as hygiene, and it must be done *all at once* — a half-migration is worse than either end state.

---

## Technical SEO — 83/100

### Working well

- **HTTPS everywhere**, valid cert, HTTP/2 with HTTP/3 advertised via `alt-svc`.
- **A genuinely complete security header set** — HSTS (`max-age=31536000; includeSubDomains`), CSP, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`. This is better than most commercial sites.
- **Brotli** on HTML, CSS and JS.
- **Correct 404s** — unknown paths and wrong-case paths both return a true 404, not a soft 200.
- **Canonical on 111/111 pages**, all self-referential and consistent.
- **Clean crawl**: 111/111 URLs returned 200, zero broken internal links, zero orphan pages.
- **Utility pages correctly excluded** — `random.html` (`noindex, follow`) and `artikkelein_sisaltolustaus_not_article.html` (`noindex,nofollow`) are out of the sitemap and out of the index.

### Issues

**No canonical host enforcement (High).** All four variants return 200 with zero redirects:

```
http://xn--ilmit-mua.fi/        → 200   (no HTTPS redirect)
http://www.xn--ilmit-mua.fi/    → 200
https://www.xn--ilmit-mua.fi/   → 200
https://xn--ilmit-mua.fi/       → 200
```

The canonical tag points to the `www` host, so Google will very likely consolidate correctly — this is why it's High and not Critical. But serving plain HTTP without a redirect is the part that matters: HSTS only protects a visitor who has *already* completed one HTTPS request, so first-time visitors and crawlers can be served over unencrypted HTTP. Verified with `--max-redirs 0`: all four return `200`, no `Location` header, and plain HTTP serves the complete homepage (120 hub cards, correct title).

**Root cause confirmed: the redirect rule targets the wrong domain.** The server's `.htaccess` does contain a canonical-host block, and its comment correctly says "force HTTPS + www on www.ilmiöt.fi" — but the rules underneath match and redirect to **`ilmioita.fi`**, a domain this site does not use:

```apache
RewriteCond %{HTTP_HOST} ^ilmioita\.fi$ [OR]
RewriteCond %{HTTP_HOST} ^www\.ilmioita\.fi$
RewriteRule ^(.*)$ "https\:\/\/www\.ilmioita\.fi\/$1" [R=301,L]
```

The site is served on `xn--ilmit-mua.fi`, so neither condition ever matches and the rule is dead code — which is exactly why all four variants return 200. Had it matched, it would have redirected to the wrong domain entirely. The comment documents the intent; the code does something else. `.htaccess` was also absent from the repo, so this was invisible to review — it should be version-controlled as part of the fix.

**Sitemap freshness is inconsistent (Medium).** 93 of 111 `<lastmod>` values disagree with the page's own schema `dateModified`:

| Page | sitemap `<lastmod>` | schema `dateModified` |
|---|---|---|
| `argumenttitulva.html` | 2026-07-13 | 2026-06-19 |
| `bikeshedding.html` | 2026-07-13 | **2026-07-21** |
| `1-prosentin-saanto.html` | 2026-07-21 | 2026-07-14 |

`bikeshedding.html` is the tell: it was edited on 2026-07-21 (commit `28d5e5a`) but the sitemap still reports 2026-07-13. The sitemap is not being regenerated as part of the content workflow, so it now understates freshness on the newest edit and overstates it on 42 older pages.

**`robots.txt` sitemap URL is non-ASCII (Low).** The directive reads `Sitemap: https://www.ilmiöt.fi/sitemap.xml`. RFC 9309 expects an ASCII URI here; this is the one place where punycode is worth using regardless of what the rest of the site does, because `robots.txt` parsers are the least forgiving consumers.

**No `preconnect` to `cdn.jsdelivr.net` (Low)** despite 89 pages loading from it.

---

## Content Quality — 76/100

### Working well

- **Meta descriptions are excellent.** 111/111 present, 111/111 unique, all 120–172 characters, all hand-written with a consistent "what it is → what we explain" structure. Only `index.html` (172) exceeds the ~160-char display budget. This is the single best-executed area of the site.
- **E-E-A-T signals are strong for an independent site:** bylines on 110/111 pages, a real author entity (`Ilmiömies`) with a `Person` node and an about page, visible "Päivitetty" dates matching schema on 110/111 pages, and sourcing on 109/111 pages (102 cite books, 109 link external references).
- **No duplicate content** — zero duplicate titles, descriptions or canonical targets.
- **Genuinely differentiated angle.** Every article ends with *Tunnistaminen ja vastakeinot*. A glossary that tells you what to *do* about the phenomenon is materially more useful than the Wikipedia entry it links to, and that is the site's real competitive moat.

### Issues

**Body copy is thinner than it first appears (Medium).** Raw text extraction reports a median of 462 words, but that includes the sources list, related-phenomena cards, navigation and footer. Measuring article prose only:

| Metric | Article prose |
|---|---|
| Median | **269 words** |
| Minimum | 152 (`astroturf.html`) |
| Maximum | 575 |
| Under 300 words | **63 of 109** |

Thinnest: `astroturf` (152), `scope-creep` (157), `hippo-efekti` (159), `pinta-alaharha` (161), `door-in-the-face` (167), `ponzi-pyramidi` (170), `pump-and-dump` (170), `darvo` (176).

Concision is a legitimate editorial choice for a glossary and I would not turn these into 1,500-word essays — that is how good reference sites get worse. But at 269 median words there is room for one concrete worked example per article, which is also the highest-value addition for AI citation.

**Raw diagram source is indexable text (Low).** The `.mermaid` divs contain flowchart syntax as literal DOM text until JavaScript rewrites them. Any non-rendering crawler reads:

```
flowchart TD V["Vähän osaamista"] --> E["Ei kykyä nähdä\nomia virheitä"] ...
```

That is **6.6% of all extractable text sitewide** (3,440 of 52,248 words), median 8% per diagram page, peaking at 13% on `saantelijan-kaappaus.html`. Mitigated by the `.kaavio-selitys` paragraph that follows each diagram with a plain-language summary — a good pattern already in place.

**One live typo:** "Katkais**tt**u y-akseli" → "Katkaistu" in `tilastoilla-valehtelu.html`.

---

## On-Page SEO — 78/100

### Working well

- Titles: 111/111 present and unique, none under 30 chars.
- Exactly one `h1` on every page — no missing, no duplicates.
- `lang="fi"` on 111/111.
- Open Graph and Twitter Card tags complete on 111/111.
- Internal linking is healthy: 9.2 outbound links per page, **zero orphans**, zero broken targets.

### Issues

**Article bodies have no heading structure (High).** This is the most consequential on-page finding.

| Headings per page | Pages |
|---|---|
| 2 (`h1` + "Liittyvät ilmiöt") | **97** |
| 4–6 | 13 |
| 19 (`index.html`) | 1 |

A typical article renders like this:

```
h1  Dunning–Kruger-ilmiö — itsevarmuus ilman taitoa
    <p> definition
    <p> mechanism
    <div class="mermaid">        diagram
    <div class="infolaatikko">   <strong>Ilmiö arjessa:</strong>
    <div class="huomiolaatikko"> <strong>Tunnistaminen ja vastakeinot:</strong>
    <div class="lue-lisaa">      sources
h2  Liittyvät ilmiöt
```

The `.infolaatikko` and `.huomiolaatikko` blocks are the most citable material on every page — concrete examples and actionable advice — and every one of them opens with a `<strong>` label inside a `<div>` rather than a heading. Google's featured-snippet and passage-ranking systems, and every AI retrieval pipeline, use heading boundaries to segment a document. Right now each article presents as one undifferentiated block.

**The labels are already good heading text.** They are not two boilerplate strings — across the site there are **181 boxes carrying 139 distinct labels** (66 in `.infolaatikko`, 73 in `.huomiolaatikko`), written per article: "Tunnistaminen ja vastakeinot:", "Tunnettuja tapauksia:", "Miksi laki toimii:", "Luku ei valehtele — mutta harhauttaa:", "Kolme yleistä väärinymmärrystä:". Specific, descriptive, query-shaped — exactly what you would write if you were writing subheadings deliberately. They are simply marked up as bold text.

| | Boxes | Distinct labels | Pages |
|---|---|---|---|
| `.infolaatikko` | 78 | 66 | 72 |
| `.huomiolaatikko` | 103 | 73 | 92 |

So the fix is a structural rule — *promote the leading `<strong>` of each box to `<h2>`* — not a find-and-replace of known strings. Because 98 of the 181 boxes continue into running text rather than a list, the `<h2>` should be styled `display: inline` so it renders exactly as the current bold run-in label. Heading semantics are unaffected by CSS display, so this changes the document outline for crawlers and screen readers while changing nothing visually.

**32 titles exceed 65 characters (Medium)** — up from 21 at the last audit; 12 exceed 70, longest is 85. The `— Ilmiöitä` suffix costs 11 characters, so the distinctive part is what gets truncated:

| Chars | Page |
|---|---|
| 85 | `badger-game.html` — Badger game — houkuttele kiusalliseen tilanteeseen, kiristä vaikenemisesta — Ilmiöitä |
| 81 | `rautainen-laki.html` |
| 76 | `jarjestelman-puolustelu.html` |
| 75 | `door-in-the-face.html` |
| 75 | `painostusclose.html` |

**12 pages skip heading levels (Low)** — `h1 → h4`, because `h4` is used to label the two halves of comparison graphics ("Harhaanjohtava (valittu ikkuna)" / "Rehellinen"). Affects `bikeshedding`, `bkt-harha`, `cherry-picking-aikavali`, `halo-efekti`, `kaksois-y-akseli`, `keskiarvo-vs-mediaani`, `p-hakkerointi`, `pinta-alaharha`, `selviytymisharha`, `simpsonin-paradoksi`, `suhteellinen-riski`, `tilastoilla-valehtelu`. Largely resolves itself once real `h2`s exist.

**Uneven internal link distribution (Low).** `index.html` and `tietoa.html` receive 110 inbound links each; the best-connected article is `bait-and-switch.html` at 15. But 12 pages sit at just 3 inbound links — the site-wide nav plus prev/next — including `shrinkflaatio`, `rug-pull`, `qr-koodihuijaus`, `haamutyopaikat`, `tekoalypesu`, `hiljainen-irtisanominen`, `hiljainen-irtisanoutuminen`, `hyvesignalointi`, `tilausansa`, `suunniteltu-vanheneminen`, `toimitusjohtajahuijaus`, `aanekas-vahemmisto`. These are mostly recent additions that older articles never linked back to.

---

## Schema & Structured Data — 92/100

**The strongest area of the site.** 111/111 pages carry JSON-LD, **zero parse errors**, all using a proper `@graph`.

| Type | Count |
|---|---|
| `Article` | 109 |
| `BreadcrumbList` | 109 |
| `Organization` | 2 |
| `Person` | 2 |
| `WebSite` | 1 |
| `CollectionPage` | 1 |
| `FAQPage` | 1 |
| `AboutPage` | 1 |

`Article` nodes are complete: `headline`, `description`, `datePublished`, `dateModified`, `author` (`@id`-referenced), `publisher` with `logo`, `image`, `inLanguage`, `articleSection`, `isPartOf`, and an `about` → `DefinedTerm` → `DefinedTermSet` chain. That last part is unusually good practice — it models each phenomenon as a defined term in a named glossary, which is exactly the shape entity-extraction systems want. `BreadcrumbList` is 3-level and valid on all 109, with zero malformed `itemListElement` entries.

### Gaps

- **`mainEntityOfPage` missing on all 109 `Article` nodes** — a recommended Article property; trivial to add in the template.
- **Only one `FAQPage`** despite content that is natively Q&A-shaped ("miten tunnistat…", "miten toimit…"). Note that Google restricted FAQ rich results to authoritative government and health sites in 2023, so the SERP payoff is now near zero — the remaining value is as an AI-extraction hint, which makes this Low priority rather than Medium.
- **No `SearchAction`** on the `WebSite` node (carried over from the prior audit) — the site has full-text search, so the sitelinks search box is available if `?q=` deep-linking is added first.

---

## Performance — 74/100

**No field data available.** No CrUX/PageSpeed API key is configured, and Playwright's Chromium cannot launch on this machine — `libnss3`, `libnspr4`, `libnssutil3` and `libasound2` are missing and installing them needs root, which I did not do unprompted. **LCP, INP and CLS are therefore unmeasured.** What follows is network and architecture analysis, which is solid on delivery and weaker on interaction.

### Measured

| Metric | Value |
|---|---|
| TTFB (homepage) | **0.12 s** |
| TTFB (article) | **0.09 s** |
| TCP connect / TLS | 0.031 s / 0.058 s |
| Homepage | 101 KB → **20 KB** (Brotli) |
| Article | 58.6 KB → **15 KB** (Brotli) |
| Subresource requests/article | **4** |
| Static asset cache | `public, max-age=604800` (7 days) |

Delivery is genuinely fast — sub-100 ms TTFB, four requests per article, self-hosted WOFF2 fonts with `font-display: swap`, no external font or analytics calls, HTTP/2 with HTTP/3 available.

### Issues

**`mermaid@11` is 929 KB compressed (High for CWV).** It loads from `cdn.jsdelivr.net` on 87 pages — roughly **60× the weight of the article it decorates**.

The implementation is thoughtful: `IntersectionObserver` with a 200 px `rootMargin`, `startOnLoad: false`, explicit `mermaid.run()`. But the diagram sits directly after the opening two paragraphs, so on virtually every article view it is within the 200 px margin at load and the fetch fires immediately. The lazy-loading is real but rarely gets to help.

The deeper point: these diagrams are **static**. Nothing about them requires a runtime renderer. Pre-rendering to inline SVG at build time (via `@mermaid-js/mermaid-cli`, matching the existing `scripts/build_search_index.py` pattern) would eliminate 929 KB of third-party JavaScript and a large main-thread parse/execute cost, remove the CDN as a dependency and privacy surface, make diagrams paint with the HTML, and simultaneously fix the 6.6% raw-syntax pollution noted above. This is the highest-value performance change available.

**`chart.js` is render-blocking on 3 pages (Medium).** On `korkoa-korolle.html`, `korkokierre.html` and `negatiivinen-korkoa.html`, a 72 KB script sits in `<head>` with no `defer`. This was item 3 in the previous action plan and is a one-attribute fix.

**`search-index.js` is 293 KB → 107 KB Brotli** on the homepage. It is correctly placed at the end of `<body>` (96% through the document) so it does not block render, but it is still ~107 KB fetched on every homepage visit for a feature most visitors never use. Lazy-loading it on first focus of the search box would be a clean improvement.

---

## AI Search Readiness (GEO) — 82/100

### Working well

- **`llms.txt` is genuinely well-executed** and rare in Finnish. Correct format: `# H1`, `>` blockquote summary, `## Kategoriat`, `###` sections, and `- [Title](url): description` entries — each with a real one-sentence explanation rather than a bare link. It names the author and states the content is freely citable.
- **AI crawlers are explicitly welcomed** in `robots.txt` (`GPTBot`, `OAI-SearchBot`, `ClaudeBot`, `PerplexityBot`), and all four — plus `Google-Extended` — were verified to receive 200s.
- **Strong entity grounding.** The `DefinedTerm` / `DefinedTermSet` modelling, plus `Organization`, `Person` and `articleSection`, gives retrieval systems unusually clean structure.
- **Definition-first writing.** Every article opens with a direct one-sentence definition — the ideal shape for extraction.
- **Low-competition niche.** Finnish-language explanations of these concepts are scarce, and citation-worthy sourcing (books + Wikipedia + primary sources) is present on 109/111 pages.

### Issues

**`llms.txt` is out of date (High).** It states 109 phenomena but lists **106**. Missing:

- `/1-prosentin-saanto.html`
- `/aanekas-vahemmisto.html`
- `/pareto-periaate.html`

These are exactly the three pages published in commit `9120be2`. Because `llms.txt` is the file AI systems read *first* to understand the site, three of the newest articles are invisible to that path.

**Passage structure limits citability (High).** Same root cause as the on-page heading finding. AI retrieval chunks documents on heading boundaries; 97 pages present as a single unsegmented block, so the *Tunnistaminen ja vastakeinot* content — the most citation-worthy material on the site — has no addressable boundary. This is the single highest-leverage GEO fix, and it is the same one-template edit as the on-page fix.

**No per-passage anchors.** Adding `id` attributes to the new `h2`s would make sections directly linkable, which helps both AI citation and the deep links Google generates to page fragments.

---

## Images — 85/100

There is effectively **one image asset on the entire site**: `favicon.svg`, referenced 437 times. All diagrams are mermaid-rendered SVG and all charts are canvas.

| Check | Result |
|---|---|
| `<img>` missing `alt` attribute | **0** |
| Decorative `alt=""` | 327 — **correct usage** (`.random-siirtyma-logo` transition overlay) |
| Meaningful images with descriptive `alt` | Yes — e.g. `alt="Ilmiöitä-logo: punainen varoituslippu"` with `width`/`height` |
| `og:image` | `/og/brand.png`, 200, 29 KB, correct 1200×630, with `og:image:alt` |

Alt-text handling is correct — decorative images take empty alt, meaningful ones are described. That is the right pattern and I want to be clear it is **not** a defect, despite what a naive "327 images missing alt text" scan would report.

Two genuine gaps:

- **All 111 pages share one OG image.** Every link shared from this site looks identical on social and in chat previews. `/og/<slug>.png` returns 404, and the prior audit notes `scripts/generate_og_images.py` already exists.
- **436 of 437 `<img>` lack `width`/`height`.** CLS impact is minimal — these are the fixed-position transition overlay logos, not layout-participating content — so this is Low, not the Medium a generic checklist would assign.

---

## Methodology & limitations

**Method:** all 111 sitemap URLs fetched live over HTTPS (5 concurrent) and parsed for on-page signals; live output diffed against the working tree by md5; `robots.txt`, `sitemap.xml` and `llms.txt` validated; host/protocol variants, 404 behaviour, compression and cache headers probed directly; internal link graph reconstructed from all 111 pages; JSON-LD parsed and validated on every page.

**Limitations to be explicit about:**

- **No Core Web Vitals data — neither field nor lab.** No CrUX/PSI credentials, and Chromium cannot launch locally (missing `libnss3`, `libnspr4`, `libnssutil3`, `libasound2`; installation requires root). LCP, INP and CLS are unmeasured. The Performance score reflects delivery architecture only and carries the widest error bar of any category here.
- **No indexation or traffic data.** No Search Console or GA4 credentials, so actual indexed-page count, impressions, clicks and query data are unknown. Everything above is what a crawler sees, not what Google has done with it.
- **No backlink data.** Moz and Bing Webmaster keys are absent; only the Common Crawl tier was available.
- **No rank or SERP data.** No DataForSEO access, so competitive positioning is not assessed.

Verifying the site in **Google Search Console and Bing Webmaster Tools** (using the punycode property, `xn--ilmit-mua.fi`) would close the largest of these gaps and costs nothing.

---

*Audit performed with the `seo-audit` skill, run inline. Findings verified against the live site on 2026-07-25.*
