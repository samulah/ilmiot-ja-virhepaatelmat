# SEO Action Plan — ilmiöt.fi (TODO)

Generated: 2026-06-19 · Target: https://www.ilmiöt.fi
Companion to `FULL-AUDIT-REPORT.md`

Each item lists **what** to do and **why it matters** (the concrete payoff).

> ⚠️ A batch of changes (related-links, today's dates, Mermaid CLS fix, self-hosted fonts + tightened CSP, brand OG image) is **done locally but not yet deployed** — push to make them live.

---

## 🟡 MEDIUM

- **Search Console + Bing.**
  **What:** Verify www.ilmiöt.fi, submit `sitemap.xml`, enable URL inspection.
  **Why it matters:** This is the only way to see *real* data instead of guessing — actual queries, impressions, clicks, CTR and position; which URLs are indexed vs excluded and why; crawl errors; and real Core Web Vitals from CrUX (field data) rather than lab estimates. Submitting the sitemap also gets all 70 URLs discovered fast. Bing's index additionally feeds Microsoft Copilot citations.

- **Titles (~27 over 60 chars).**
  **What:** Trim/restructure the over-long titles.
  **Why it matters:** Google truncates titles past ~60 chars with "…", cutting off the distinctive keyword/hook. Tightening them makes the full, click-worthy title visible in results — more clicks at the *same* ranking, no extra content needed.

---

## 🟢 LOW — backlog

- **Harden CSP (nonces instead of `'unsafe-inline'`).** `'unsafe-inline'` currently lets *any* injected inline script run, weakening XSS protection. Nonces or external scripts restore strong XSS defense while keeping Mermaid/Chart working.
- **Per-category hub pages.** Gives each of the 8 themes a dedicated, rankable landing page for broader category-level keywords and concentrates topical authority into a cleaner hub-and-spoke structure.
- **`.ico`/PNG favicon fallback.** Some older/edge browsers ignore SVG favicons; a raster fallback guarantees the flag logo shows in every tab and bookmark (brand consistency).

---

## ⚠️ Repo hygiene

**What:** Commit the repo — the SEO build, `favicon.svg`, `tietoa.html`, `fonts/`, `scripts/`, and `.htaccess` are uncommitted.
**Why it matters:** Untracked files keep getting deleted (`.htaccess` twice this session). A commit makes the whole session's work recoverable via git history and enables rollback — without it, a stray cleanup can silently wipe live-critical config again.
