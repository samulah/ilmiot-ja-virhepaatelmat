# SEO Full Audit Report — ilmiöt.fi

**Audit target:** https://ilmiöt.fi → 301 → https://www.ilmiöt.fi (`www.xn--ilmit-mua.fi`)
**Audit date:** 2026-06-19 (session 3 — post-deploy)
**Auditor:** Claude Code SEO Audit
**Branch:** seo
**History:** 2026-06-16 live 28/100 · session 2 local build ~83 · **now DEPLOYED**

---

## Executive Summary

### SEO Health Score

| State | Score |
|-------|-------|
| Session 1 (live, pre-SEO) | 28 / 100 |
| **Live now (deployed)** | **≈ 85 / 100** |

🎉 **The full SEO build is live in production.** Live verification (`last-modified` today 04:26 GMT):
- `ilmiöt.fi` **301 → www.ilmiöt.fi** (host canonicalization works)
- Security headers + CSP (`script-src … 'unsafe-inline'`) live — inline Mermaid/Chart/random scripts run
- Canonical, meta descriptions, favicon, header/breadcrumb logo, author=Ilmiömies schema all live
- `tietoa.html` (About) → 200 · old `og/*.png` → 404 (removed) · `favicon.svg` → 200
- robots.txt, sitemap.xml (70 URLs), llms.txt all on `www.ilmiöt.fi`, zero "Kendom"
- **TTFB 0.10 s**, HTTP/2+3, 46 KB homepage

### Business Type
Finnish educational reference site — 68 in-depth articles on power/manipulation/bias phenomena across 8 categories. Non-commercial, informational, YMYL-adjacent. Server: LiteSpeed.

### Top issues remaining (none critical)
1. **🟠 Sparse internal linking** — 2–5 links/page, no "related phenomena" blocks across 68 related articles. Biggest remaining lever.
2. **🟡 No social-share image** — OG images were removed by request; shares (Slack/WhatsApp/LinkedIn/X) now show no preview thumbnail. Consider one brand OG card built from the flag logo.
3. **🟡 27 titles > 60 chars** — minor SERP-truncation risk.
4. **🟡 `datePublished`/`dateModified` are placeholders** (2026-06-16 / 2026-06-19) — set real dates if known.
5. **🟡 Not yet in Search Console / Bing** — no field data (CrUX/GSC) or indexation monitoring.

### Quick wins
1. Add automated "Liittyvät ilmiöt" (3–6 links) to each article.
2. Generate one brand OG image (flag logo + site name) and reference it site-wide.
3. Submit `sitemap.xml` to Google Search Console + Bing Webmaster.
4. Trim the ~27 over-long titles.
5. Commit the repo — untracked files (notably `.htaccess`) keep getting deleted locally.

---

## Technical SEO  — ~90/100

- ✅ **Indexability:** canonical = `https://www.ilmiöt.fi/<page>` on every page (69 pages + About). `random.html` = `noindex, follow` + self-canonical.
- ✅ **Host canonicalization:** non-www + http → `https://www.ilmiöt.fi` (301, live).
- ✅ **Security (live):** HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy, and a working CSP. Inline scripts function because `script-src` includes `'unsafe-inline'`.
- ✅ **Crawl:** robots.txt allows all + explicit GPTBot/OAI-SearchBot/ClaudeBot/PerplexityBot; sitemap.xml (70 URLs) on correct host.
- ✅ HTTP/2 + HTTP/3, TTFB ~0.10 s.
- 🟡 Long-term: replace CSP `'unsafe-inline'` with nonces/external scripts (hardening, not urgent).

## Content Quality — ~88/100

- ✅ Deep, original Finnish content (3,200–4,400 words/article); 1 H1/page; unique per phenomenon.
- ✅ **E-E-A-T:** author **Ilmiömies** (Person schema + visible byline + date), publisher Organization "Ilmiöitä", dedicated **About page** (`tietoa.html`) linked sitewide.
- ✅ Clean, full-sentence meta descriptions (rewritten from the prior truncated ones).
- 🟡 Dates are placeholders; consider per-article real dates.

## On-Page SEO — ~78/100

- ✅ Titles, descriptions, OG/Twitter, single H1, logo in header + breadcrumb.
- 🟠 **Internal linking still sparse** — no related-content sections (top opportunity).
- 🟡 27 titles > 60 chars.

## Schema & Structured Data — ~90/100

- ✅ Article + DefinedTerm + DefinedTermSet + BreadcrumbList per phenomenon; WebSite + Organization + CollectionPage + ItemList on the hub; AboutPage + Person on About.
- ✅ `author`, `datePublished`, `dateModified`, publisher now present; all `@id`/url on ilmiöt.fi; no Kendom.

## Performance — ~82/100 (lab)

- ✅ TTFB ~0.10 s, 46 KB homepage, no raster images, deferred Mermaid/Chart.
- 🟡 Client-side Mermaid/Chart can cause CLS/INP on diagram-heavy pages — reserve container height.
- ℹ️ No field data yet (connect CrUX/GSC).

## Images — ~72/100

- ✅ No content `<img>` → no alt/oversize/CLS debt. Favicon (SVG flag logo) on all pages.
- 🟡 **OG/social images removed** (by request): no share-preview thumbnail anywhere. A single reusable brand OG image would restore social CTR without re-introducing per-page images.

## AI Search Readiness — ~88/100

- ✅ AI crawlers allowed, llms.txt (ilmiöt.fi, names author), DefinedTerm + definitional structure, deep citable content, About page for authority.
- 🟡 Add author/date prominence continues to help attribution.

---

## Category Scores

| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Technical SEO | 22% | 90 | 19.8 |
| Content Quality | 23% | 88 | 20.2 |
| On-Page SEO | 20% | 78 | 15.6 |
| Schema | 10% | 90 | 9.0 |
| Performance | 10% | 82 | 8.2 |
| AI Readiness | 10% | 88 | 8.8 |
| Images | 5% | 72 | 3.6 |
| **Total** | **100%** | | **≈ 85 / 100** |

From **28 → 85** in one session, now live. The single biggest remaining lever is internal "related phenomena" linking; everything else is polish. See `ACTION-PLAN.md`.
