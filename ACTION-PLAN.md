# SEO Action Plan — ilmiöt.fi

Generated **2026-07-25**. Live health score: **80/100** (re-baselined; see the audit report on why this is not a drop from 84).
Priority: Critical > High > Medium > Low.

**No Critical issues.** Nothing blocks indexing, nothing risks a penalty, all 111 sitemap URLs return 200, and live matches `main` byte-for-byte. The previous audit's Critical item — the deploy gap — is closed.

---

## ✅ Done 2026-07-25 (uncommitted, in working tree)

| Item | What was done |
|---|---|
| 3 | **llms.txt: 3 missing entries added** → 109/109. Root cause fixed: `paivita_llms()` now syncs the entry list from index.html hub cards |
| 4 | **sitemap.xml regenerated** → lastmod mismatches **93 → 0**. New `scripts/build_sitemap.py` derives `<loc>` from hub cards, `<lastmod>` from schema `dateModified` |
| 6 | **chart.js deferred** on the 3 finance pages, with the init IIFE wrapped in `DOMContentLoaded` so ordering stays correct |
| 12 | **Typo fixed** — "Katkaisttu" → "Katkaistu" |
| 19 | **`rel="noopener"` added** to the ssrn link (it was in `halo-efekti.html`, not `brandolinin-laki.html` as first reported) |
| 1 | **Root cause found:** the redirect matched `ilmioita.fi`, a domain the site does not use → dead rule. Corrected block supplied; `.htaccess` is `.gitignore`d by choice, so the repo copy is a local reference and the server file is authoritative. **Still needs deploying + verifying** |

Also regenerated: `search-index.js` (picked up the typo fix, 1-byte diff).

**Verification performed:** `node --check` on all three modified chart scripts; both build scripts confirmed idempotent on a second run; sitemap XML well-formedness asserted before write; llms.txt entry count asserted to equal the card count; zero external links left without `rel`.

**Not committed** — the working tree is ready for you to review and commit.

> **`defer` alone would have broken all 12 charts.** The inline `new Chart()` calls ran at parse time with no `DOMContentLoaded` guard, so deferring the library would have left `Chart` undefined — the same ordering bug that hit mermaid previously. Hence the wrapper.

> **llms.txt keeps its hand-tuned wording.** Three entries deliberately differ from the hub cards ("Argumenttitulva (Gish Gallop)", "Simple Sabotage Field Manual", "Lowball-hinnoittelu"), as does the "Tilastoilla valehtelu" category description. The sync deliberately preserves existing text and only reports divergences — it syncs *membership and order*, never overwrites editorial wording.

---

## High (fix within 1 week)

### 1. Enforce one canonical host

All four variants serve 200 with no redirect: `http://` apex, `http://www.`, `https://www.`, `https://` apex. Serving plain HTTP without a redirect is the real problem — HSTS only protects visitors who have already made one HTTPS request.

**Root cause confirmed: the rule targets the wrong domain.** The server's `.htaccess` has a canonical-host block whose comment says "force HTTPS + www on www.ilmiöt.fi", but the rules match and redirect to **`ilmioita.fi`** — a domain this site does not use. Since the site runs on `xn--ilmit-mua.fi`, neither condition ever matches: the rule is dead code, which is precisely why all four variants return 200. It also was not in the repo, so nothing surfaced the mismatch.

**Written 2026-07-25** to a repo-tracked `.htaccess`. Both conditions are combined with `[OR]` so any non-canonical request is fixed in a **single 301 hop** rather than two:

```apache
RewriteEngine On
RewriteCond %{HTTPS} !=on [OR]
RewriteCond %{HTTP_HOST} !^www\. [NC]
RewriteRule ^ https://www.xn--ilmit-mua.fi%{REQUEST_URI} [R=301,L,NE]
```

`%{REQUEST_URI}` preserves the path, the query string survives automatically (no `?` in the substitution), and `NE` prevents double-encoding of already-escaped characters. After the redirect both conditions are false, so there is no loop.

**Still to do:** deploy, then verify all four variants land on one URL in one hop:

```bash
for u in http://xn--ilmit-mua.fi/ http://www.xn--ilmit-mua.fi/ \
         https://xn--ilmit-mua.fi/ https://www.xn--ilmit-mua.fi/; do
  curl -sS -o /dev/null -w "%{http_code} %{num_redirects} -> %{url_effective}\n" -L "$u"
done
```

Expect `200 1 -> https://www.xn--ilmit-mua.fi/` for the first three and `200 0` for the last.

### 2. ✅ DONE — Give articles real heading structure

**Done 2026-07-25** via `scripts/laatikko_otsikot.py` (idempotent — re-run it after adding new pages). 181 boxes across 106 pages converted; pages with only two headings went **97 → 3**.

Original finding: 97 of 111 pages had only two headings (`h1` + "Liittyvät ilmiöt"), because the most citable blocks opened with a `<strong>` label inside a `<div>` instead of a heading.

**These labels are already well-written subheadings** — 181 boxes carrying 139 distinct, article-specific texts ("Tunnistaminen ja vastakeinot:", "Tunnettuja tapauksia:", "Miksi laki toimii:", "Kolme yleistä väärinymmärrystä:"). Nothing needs rewriting; only the markup is wrong.

| | Boxes | Distinct labels | Pages |
|---|---|---|---|
| `.infolaatikko` | 78 | 66 | 72 |
| `.huomiolaatikko` | 103 | 73 | 92 |

Apply as a **structural rule**, not a text replacement — promote the leading `<strong>` of each box:

```html
<!-- now -->
<div class="infolaatikko">
<strong>Tunnettuja tapauksia:</strong>
<ul>…

<!-- proposed -->
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Tunnettuja tapauksia:</h2>
<ul>…
```

98 of the 181 boxes continue into running text rather than a list, so style the heading as a run-in to preserve the current look exactly:

```css
.infolaatikko h2, .huomiolaatikko h2 {
  display: inline; font-size: 1em; font-weight: 700;
  font-family: inherit; margin: 0;
}
```

CSS `display` does not affect heading semantics — crawlers and screen readers get a real outline, readers see no visual change. Note that the box CSS currently lives in each page's inline `<style>`, not in `style.css`, so this rule can be added in the same scripted pass (which avoids a `?v=` cache-bust bump across 110 pages).

This one change fixes the top On-Page issue and the top GEO issue simultaneously, and partly improves the 12 `h1→h4` skips.

### 3. Add the 3 missing entries to `llms.txt`

It claims 109 phenomena but lists 106. Missing: `1-prosentin-saanto.html`, `aanekas-vahemmisto.html`, `pareto-periaate.html` (published in commit `9120be2`). This is the file AI systems read first, so three of the newest articles are invisible to that path.

**Root cause found.** `scripts/paivita_maarat.py` → `paivita_llms()` only rewrites the *count*:

```python
uusi = re.sub(r"selittää \d+ yhteiskunnallista ilmiötä",
              f"selittää {yhteensa} yhteiskunnallista ilmiötä", txt)
```

So the header dutifully updated itself to 109 while the `- [Title](url): description` list stayed at 106. The script silently guarantees the two disagree. Fix the three entries now, then extend `paivita_llms()` to regenerate the entry list from the index.html hub cards — it already has `hub-nimi` and `hub-kuvaus`, which is exactly the `- [name](url): description` shape `llms.txt` needs.

### 4. Regenerate `sitemap.xml` — and script it

93 of 111 `<lastmod>` values disagree with the page's own schema `dateModified`. `bikeshedding.html` was edited 2026-07-21 but the sitemap still says 2026-07-13, while 42 older pages claim a freshness they don't have.

**Root cause: `sitemap.xml` is the one artefact still maintained by hand** (`paivita_maarat.py` covers index/tietoa/llms counts, `build_search_index.py` the search index, `build_liittyvat.py` the related-cards — nothing covers the sitemap). Adding a `scripts/build_sitemap.py` that derives `<loc>` from the index.html hub cards and `<lastmod>` from each page's schema `dateModified` removes the whole class of drift.

---

## Medium (fix within 1 month)

### 5. Pre-render mermaid diagrams to static SVG

`mermaid@11` is **929 KB Brotli** from `cdn.jsdelivr.net` on 87 pages — ~60× the weight of the 15 KB article it decorates. The `IntersectionObserver` lazy-load is well implemented, but the diagram sits right after the opening paragraphs, so it is inside the 200 px `rootMargin` on load and fires immediately anyway.

These diagrams never change. Render them at build time with `@mermaid-js/mermaid-cli`, following the existing `scripts/build_search_index.py` pattern. One change buys:

- 929 KB of third-party JS eliminated, plus its main-thread parse cost
- diagrams paint with the HTML instead of after a CDN round-trip
- the CDN dependency and privacy surface removed
- the 6.6% raw-syntax text pollution (item 12) fixed for free
- `<title>`/`<desc>` available inside the SVG for accessibility and indexing

Highest-value performance change available. Keep `.kaavio-selitys` either way.

### 6. Add `defer` to `chart.js` on 3 pages

`korkoa-korolle.html`, `korkokierre.html`, `negatiivinen-korkoa.html` — a 72 KB script sits in `<head>` un-deferred and blocks render. Carried over from the last audit; it is a one-attribute fix.

### 7. Trim over-length titles

32 titles exceed 65 chars (was 21 — this regressed), 12 exceed 70, longest is 85. The `— Ilmiöitä` suffix costs 11 chars, so the distinctive part is what truncates. Start with `badger-game` (85), `rautainen-laki` (81), `jarjestelman-puolustelu` (76), `door-in-the-face` (75), `painostusclose` (75). Target ≤60 including the suffix.

### 8. Standardise the host to punycode — all at once

Replace `https://www.ilmiöt.fi/` → `https://www.xn--ilmit-mua.fi/` in canonicals (111), `og:url`/`twitter` URLs, all JSON-LD `url`/`@id`, `sitemap.xml` (111 `<loc>`), the `robots.txt` `Sitemap:` line, and `llms.txt`.

**Downgraded from High.** Everything currently uses the UTF-8 form *consistently*, and Google normalises IDNs on its side, so the practical risk is low. The real argument is spec compliance (sitemaps.org, RFC 3986) and third-party tooling that handles raw non-ASCII unpredictably. Do it in one pass — a half-migration is worse than either end state. If you only do one piece, do the `robots.txt` line, since `robots.txt` parsers are the least forgiving.

### 9. Per-article OG images

All 111 pages share `/og/brand.png`; `/og/<slug>.png` returns 404. Every link shared from the site looks identical in social and chat previews. `scripts/generate_og_images.py` reportedly already exists — generate 1200×630 per slug and set per-page `og:image` + `og:image:alt`.

### 10. Add one worked example to the thinnest articles

Median article prose is **269 words** (the 462 figure a naive count gives includes sources, related cards, nav and footer). 63 of 109 are under 300 prose words.

Do **not** inflate these into essays — concision is right for a glossary. Add one concrete example each, which is also the most citable thing you can give an AI system. Start with: `astroturf` (152), `scope-creep` (157), `hippo-efekti` (159), `pinta-alaharha` (161), `door-in-the-face` (167), `ponzi-pyramidi` (170), `pump-and-dump` (170), `darvo` (176).

---

## Low (backlog)

11. **Add `mainEntityOfPage`** to the 109 `Article` nodes — the only missing recommended property in otherwise excellent schema.
12. **Fix the typo** "Katkais**tt**u y-akseli" → "Katkaistu" in `tilastoilla-valehtelu.html`.
13. **Boost internal links to the 12 least-linked pages** (3 inbound each — nav plus prev/next only): `shrinkflaatio`, `rug-pull`, `qr-koodihuijaus`, `haamutyopaikat`, `tekoalypesu`, `hiljainen-irtisanominen`, `hiljainen-irtisanoutuminen`, `hyvesignalointi`, `tilausansa`, `suunniteltu-vanheneminen`, `toimitusjohtajahuijaus`, `aanekas-vahemmisto`. Add them to the "Liittyvät ilmiöt" blocks of relevant older articles.
14. **Tighten CSP** — remove the unused `fonts.googleapis.com` / `fonts.gstatic.com` origins (0 pages reference them; fonts are self-hosted).
15. **Branded 404** — still the 1,251-byte stock LiteSpeed page. Status code is already correct; add a small branded page linking home + the 12 categories.
16. **Lazy-load `search-index.js`** on first focus of the search box — 107 KB Brotli currently fetched on every homepage visit for a feature most visitors never use.
17. **Deep-linkable search + `SearchAction`** — have the box read/write `?q=`, then add `WebSite.potentialAction` targeting `/?q={search_term_string}`.
18. **`preconnect` to `cdn.jsdelivr.net`** — only worth it if item 5 is declined; item 5 removes the need entirely.
19. **Add `rel="noopener"`** to the one external link missing it: the `papers.ssrn.com` link in `brandolinin-laki.html` (131 of 132 external links already have it).
20. **Consider excluding `artikkelein_sisaltolustaus_not_article.html` from deploy** — a 76 KB internal audit working file publicly reachable. Correctly `noindex,nofollow` so there is no SEO harm; this is tidiness, not risk.
21. **Verify in Google Search Console + Bing Webmaster Tools** using the **punycode** property (`xn--ilmit-mua.fi`) and submit the sitemap. This unlocks real indexation status, query data and CWV field data — the single biggest blind spot in this audit, and free.

---

## Process note — the recurring failure mode

Two of this audit's four High items (`llms.txt` 3 entries stale, `sitemap.xml` 93 mismatched dates) were the same class of bug: **generated files drifting from content.** The build chain was good but had exactly two holes, and both showed up. **Both are now closed (2026-07-25):**

| Artefact | Script | State |
|---|---|---|
| index/tietoa counts, `llms.txt` **count** | `paivita_maarat.py` | ✅ automated |
| `search-index.js` | `build_search_index.py` | ✅ automated |
| "Liittyvät ilmiöt" cards | `build_liittyvat.py` | ✅ automated |
| `llms.txt` **entry list** | `paivita_maarat.py` | ✅ **fixed 2026-07-25** (was manual → 3 missing) |
| `sitemap.xml` | `build_sitemap.py` | ✅ **fixed 2026-07-25** (was manual → 93 stale dates) |

The `llms.txt` hole was the more insidious of the two: `paivita_maarat.py` updated the count *without* the entries, so the file actively asserted a number its own contents contradicted. The full chain to run after any content change is now:

```bash
python scripts/paivita_maarat.py        # counts + llms.txt entry sync
python scripts/build_sitemap.py         # loc from cards, lastmod from schema
python scripts/build_search_index.py
python scripts/build_liittyvat.py       # note: hardcoded assert len(ilmiot) == 109
```

A pre-commit hook that runs these and fails on an uncommitted diff would make this structural rather than remembered.

Related: the article count is asserted in the title, meta description, `WebSite.description`, `ItemList.numberOfItems`, the `llms.txt` header, and a hardcoded `assert` in `build_liittyvat.py`. `paivita_maarat.py` already derives it from the hub cards — extend that single source to cover the remaining hand-edited spots.

---

*Supersedes the 2026-07-05 plan. No CWV field or lab data in this run (no CrUX/PSI credentials; Chromium cannot launch locally — missing `libnss3`/`libnspr4`/`libnssutil3`/`libasound2`, install requires root). Performance assessed from delivery architecture and live response behaviour: Brotli, HTTP/2+3, 0.09–0.12 s TTFB verified.*
