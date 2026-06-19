# SEO Action Plan — kendom.fi/ilmiöt/

Generated: 2026-06-16 | Post-implementation priorities

---

## ✅ DONE (this session)

- [x] robots.txt — created with AI crawler permissions
- [x] sitemap.xml — 69 URLs with lastmod dates
- [x] llms.txt — 68 ilmiöt categorized for AI indexers
- [x] .htaccess — HSTS, CSP, X-Content-Type-Options, X-Frame-Options, charset
- [x] Meta descriptions — 69/69 pages, 100-160 chars
- [x] Canonical tags — 69/69 pages, absolute URLs
- [x] OG + Twitter card tags — 69/69 pages
- [x] JSON-LD schema — Article + BreadcrumbList + DefinedTerm on all ilmiö pages
- [x] CollectionPage + ItemList + WebSite schema on hub
- [x] H2 → H1 promotion — 68/68 ilmiö pages
- [x] Hub categories `<p>` → `<h2>` — 8 categories
- [x] Mermaid.js `defer` — 55/55 CDN-loaded pages
- [x] Google Fonts gstatic preconnect

---

## 🔴 CRITICAL — Before next deployment

### Deploy the changes
All fixes are local only. Push the `seo` branch and deploy.

```bash
git add -A
git commit -m "SEO: meta tags, schema, H1, robots.txt, sitemap, security headers"
git push
```

---

## 🟠 HIGH — Within 1 week

### 1. Add author attribution to all pages
Every ilmiö page needs a visible author. Even "Kendom-toimitus" is better than nothing.

Add to each page's breadcrumb area or below H1:
```html
<p class="ilmio-meta">Kirjoittanut <strong>Kendom</strong></p>
```

Also add to Article schema: `"author": {"@type": "Organization", "name": "Kendom"}`

**Impact:** Biggest remaining E-E-A-T gap. Required for Google AI Overview eligibility.

### 2. Add publication dates to all pages
Add visible date + `datePublished` to schema.

```html
<time datetime="2025-01-01" class="ilmio-pvm">Tammikuu 2025</time>
```

Add to Article schema: `"datePublished": "2025-01-01", "dateModified": "2026-06-16"`

**Impact:** Freshness signal for AI systems. Credibility for YMYL-adjacent content.

### 3. Create /ilmiöt/tietoa.html (About page)
One page explaining: who created this, what it covers, editorial approach, contact.

Current about page returns 404 — this is a disqualifying E-E-A-T signal for QRG raters.

**Impact:** Authoritativeness signal. Required for rater trust on sensitive topics (manipulation, fraud).

### 4. Submit sitemap to Google Search Console
After deployment: Google Search Console → Sitemaps → `https://kendom.fi/ilmiöt/sitemap.xml`

**Impact:** Guarantees all 68 pages are discovered quickly regardless of crawl budget.

---

## 🟡 MEDIUM — Within 1 month

### 5. Expand thin-content pages
Priority pages under 300 words:
- `ponzi-pyramidi.html` (~44 words) — expand to 600+ words with Finnish examples
- `paskuuttaminen.html` (~196 words) — add recognition checklist, Finnish case
- `simple-sabotage.html` (~267 words) — add modern organizational examples

**Impact:** Competitive ranking. Finnish educational queries need 600+ words to beat Wikipedia.

### 6. Add FAQ sections to psychology/manipulation pages
Target: gaslighting, DARVO, backfire-effect, halo-efekti, blame-game

Add 2-3 Finnish Q&A pairs per page → `FAQPage` schema → People Also Ask capture.

Example:
```html
<details class="faq-item">
  <summary>Mitä tarkoittaa gaslighting suomeksi?</summary>
  <p>Gaslighting on psykologinen manipulaatiostrategia, jossa...</p>
</details>
```

**Impact:** Featured snippet + PAA capture for "mitä tarkoittaa X" queries.

### 7. Add `<figcaption>` to Mermaid diagrams
Each diagram gets a Finnish text description below it explaining the flow logic.

Example:
```html
<div class="mermaid">flowchart TD ...</div>
<p class="kaavio-selitys">Kaavio: paskuuttamisen prosessi — budjettileikkaukset johtavat laadun heikkenemiseen, turhautumiseen ja lopulta yksityistämisvaatimukseen.</p>
```

**Impact:** Diagram content becomes crawlable. AI citation readiness improves significantly.

### 8. Fix 11 long title tags
Pages where title > 70 chars get truncated in SERPs. Shorten by removing subtitle after "—":

Pattern: `Rautainen laki oligarkiasta — organisaatioiden väistämätön mätäneminen — Ilmiöitä`
→ `Rautainen laki oligarkiasta — Ilmiöitä`

Pages affected: check with `grep -l ".\{71,\}" *.html` on title tags.

**Impact:** Full title visible in SERPs, better click-through rate.

---

## 🔵 LOW — Backlog

### 9. Self-host Google Fonts
Download DM Sans + Spectral + Source Sans 3, serve from same domain with `font-display: swap`.

**Impact:** Eliminates cross-origin DNS lookup, ~100-300ms LCP improvement on first visit.

### 10. Add contextual cross-links within body text
Each ilmiö page currently only links prev/next. Add 2-4 in-body links to related phenomena.

Example in gaslighting.html: "Gaslighting liittyy läheisesti [DARVO-tekniikkaan](darvo.html)..."

**Impact:** Internal PageRank distribution, topical cluster signals.

### 11. OG image
Create a default 1200×630 px branded image (dark background + ilmiö name in Spectral serif).
Use one image per category or a generic fallback.

**Impact:** Social shares show rich preview instead of blank card.

### 12. Create /ilmiöt/myyntikikat/ sub-hub
Standalone landing page for the sales manipulation cluster (ilmiöt 57-68).
Target query: "myynnin psykologiset tekniikat suomeksi" — currently no strong Finnish competitor.

**Impact:** Category-level ranking opportunity in an uncontested niche.

### 13. IndexNow
LiteSpeed supports IndexNow natively. Register key at indexnow.org, add key file to webroot.

**Impact:** Instant Bing (and via Bing → Copilot) indexing on page updates.

---

## Score Trajectory

| Milestone | Estimated Score |
|-----------|----------------|
| Before this session | 28/100 |
| After deployment (current changes) | 74/100 |
| After author + dates + about page | 82/100 |
| After FAQ + thin content expansion | 87/100 |
| After fonts + images + sub-hubs | 90/100 |
