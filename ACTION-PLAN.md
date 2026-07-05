# SEO Action Plan — ilmiöt.fi

Generated 2026-07-05 (re-audit). Live health score: **84/100** — unchanged since 2026-06-21 because the prior fixes were never deployed. Priority: Critical > High > Medium > Low.

## Critical (blocks value right now)
1. **DEPLOY.** ~2 weeks of committed + staged SEO work is not on the server (live = 19 Jun build). Deploying is the highest-leverage action and needs no new code.
   - Committed to `main`, undeployed: `Organization.logo` + `Article.image`, author `@id`→`#ilmiomies`, mermaid lazy-load + init-ordering fix.
   - Working tree, uncommitted + undeployed: full-text search (`index.html`, `search-index.js`, `scripts/build_search_index.py`) → **commit these first**, then deploy.
   - After deploy: scroll an article to a diagram (confirm gold/cream mermaid render + clean console), run the search box, and confirm `/og/brand.png` still resolves.

## High (fix within 1 week)
2. **Standardise the host to punycode.** Replace `https://www.ilmiöt.fi/` → `https://www.xn--ilmit-mua.fi/` in: every page's `<link rel="canonical">` + `og:url`/twitter URLs (0/71 done), all JSON-LD `url`/`@id`, `sitemap.xml` (70 `<loc>`), the `robots.txt` `Sitemap:` line, and `llms.txt` (69 URLs). Non-ASCII in sitemap `<loc>` is spec-non-compliant. Purely mechanical find-replace; re-run the sitemap/search-index build after.
3. **Add `defer` to `chart.js`** on the 3 finance pages (`korkoa-korolle.html`, `korkokierre.html`, `negatiivinen-korkoa.html`) — currently render-blocking.

## Medium (fix within 1 month)
4. **Per-article OG images.** Generate unique 1200×630 images (`scripts/generate_og_images.py` exists) and set per-page `og:image` + descriptive `og:image:alt` instead of the shared `/og/brand.png` (`/og/<slug>.png` currently 404s).
5. **Strengthen thin / borderline-YMYL pages.** Expand the 23 sub-320-word articles — start with `paskuuttaminen` (241w), `conways-laki`, `hofstadterin-laki`, `brooksin-laki`, `yhdeksanyhdeksan`, `starve-the-beast` — with a concrete example + a short "miten tunnistat" list. For scam/finance topics (`pig-butchering`, `ponzi-pyramidi`, `ennakkomaksuhuijaus`, `korkoa-korolle`, `negatiivinen-korkoa`, `korkokierre`) add explicit citations/sources to lift trust. Re-run `build_search_index.py` after.
6. **Make search deep-linkable, then add `SearchAction`.** Have the search box read/write `?q=` (pre-fill + auto-run on load), then add a `WebSite.potentialAction` `SearchAction` targeting `/?q={search_term_string}` → enables the Google sitelinks search box. Also `defer` the `search-index.js` tag (or lazy-load on first focus).

## Low (backlog)
7. **Trim over-length titles.** ~21 `<title>` tags exceed 65 chars (max 85) and truncate in SERPs; shorten the longest so the meaningful phrase precedes the `— Ilmiöitä` suffix.
8. **Tighten CSP.** Remove the unused `fonts.googleapis.com` / `fonts.gstatic.com` origins (fonts are self-hosted).
9. **Branded 404 page.** Replace the stock LiteSpeed 404 with a small branded page linking home + the 8 categories (status already correct at 404).
10. Differentiate homepage `og:title` from `og:site_name`; point breadcrumb category node (position 2) to `index.html#<category>`.
11. Add per-passage anchors / short FAQ blocks to top phenomena for direct AI citation.
12. Verify the site in Google Search Console + Bing Webmaster Tools using the **punycode** property and submit the sitemap → unlocks real indexation + CWV field data.

## Process note
- **`search-index.js` must be regenerated on every content change** (`python scripts/build_search_index.py`) and committed, or search results drift from the pages. Consider adding it to the deploy/build step so it can't be forgotten.

---
*Re-audit supersedes the 2026-06-21 output. No Playwright/CrUX field data in this run; Performance assessed from architecture + live response behaviour (Brotli, HTTP/2+3, ~0.10 s TTFB verified).*
