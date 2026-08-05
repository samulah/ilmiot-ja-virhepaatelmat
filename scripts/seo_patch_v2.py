#!/usr/bin/env python3
"""One-off SEO patch (2026-06-21 audit, items High#1, High#2, #5).

- Mermaid: replace head <script defer …>+inline initialize with an
  IntersectionObserver lazy-loader that loads mermaid only when a diagram
  nears the viewport, and runs init->run in the correct order.
- Schema: Organization.logo, Article.image (ImageObject), author Person
  description + @id link to the canonical #ilmiomies entity.

Idempotent: each transform is skipped if its result marker already exists or
its anchor is missing.
"""
import glob, sys

# ---- Mermaid lazy-loader (55 article pages) -------------------------------
THEME = ("{ startOnLoad: false, theme: 'base', themeVariables: { fontSize: '12px', "
         "fontFamily: \"'DM Sans', system-ui, sans-serif\", primaryColor: '#FBF5E0', "
         "primaryTextColor: '#1A1100', primaryBorderColor: '#C9A84C', lineColor: '#8B6914', "
         "secondaryColor: '#F5F0E5', tertiaryColor: '#FDFAF2', mainBkg: '#FBF5E0', "
         "nodeBorder: '#C9A84C', clusterBkg: '#F5F0E5', titleColor: '#3A2000', "
         "edgeLabelBackground: '#FDFAF2' } }")

MERMAID_OLD = (
    '  <script defer src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>\n'
    "  <script>mermaid.initialize({ startOnLoad: true, theme: 'base', themeVariables: "
    "{ fontSize: '12px', fontFamily: \"'DM Sans', system-ui, sans-serif\", primaryColor: "
    "'#FBF5E0', primaryTextColor: '#1A1100', primaryBorderColor: '#C9A84C', lineColor: "
    "'#8B6914', secondaryColor: '#F5F0E5', tertiaryColor: '#FDFAF2', mainBkg: '#FBF5E0', "
    "nodeBorder: '#C9A84C', clusterBkg: '#F5F0E5', titleColor: '#3A2000', "
    "edgeLabelBackground: '#FDFAF2' } });</script>"
)

MERMAID_NEW = """  <script>
  window.addEventListener('DOMContentLoaded', function () {
    var nodes = document.querySelectorAll('.mermaid');
    if (!nodes.length) return;
    var loaded = false;
    function load() {
      if (loaded) return;
      loaded = true;
      var s = document.createElement('script');
      s.src = 'js/mermaid.min.js';
      s.onload = function () {
        mermaid.initialize(%s);
        mermaid.run();
      };
      document.head.appendChild(s);
    }
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { load(); io.disconnect(); }
        });
      }, { rootMargin: '200px 0px' });
      nodes.forEach(function (n) { io.observe(n); });
    } else {
      load();
    }
  });
  </script>""" % THEME

# ---- Article publisher Organization + logo (68 articles) ------------------
PUB_OLD = """      "publisher": {
        "@type": "Organization",
        "name": "Ilmiöitä",
        "url": "https://www.ilmiöt.fi/",
        "@id": "https://www.ilmiöt.fi/#organization"
      },"""
PUB_NEW = """      "publisher": {
        "@type": "Organization",
        "name": "Ilmiöitä",
        "url": "https://www.ilmiöt.fi/",
        "@id": "https://www.ilmiöt.fi/#organization",
        "logo": {
          "@type": "ImageObject",
          "url": "https://www.ilmiöt.fi/favicon.svg",
          "width": 64,
          "height": 64
        }
      },"""

# ---- Article author Person + @id + description (68 articles) --------------
AUTH_OLD = """      "author": {
        "@type": "Person",
        "name": "Ilmiömies",
        "url": "https://www.ilmiöt.fi/tietoa.html"
      },"""
AUTH_NEW = """      "author": {
        "@type": "Person",
        "@id": "https://www.ilmiöt.fi/#ilmiomies",
        "name": "Ilmiömies",
        "url": "https://www.ilmiöt.fi/tietoa.html",
        "description": "Kirjoittajanimi, jonka takana on kiinnostus valtaan, vaikuttamiseen ja ihmisen päättelyn vinoumiin. Sisältö perustuu julkisiin lähteisiin ja vakiintuneeseen käsitteistöön."
      },"""

# ---- Article image (68 articles): insert after Article @type -------------
IMG_OLD = '      "@type": "Article",\n'
IMG_NEW = ('      "@type": "Article",\n'
           '      "image": {\n'
           '        "@type": "ImageObject",\n'
           '        "url": "https://www.ilmiöt.fi/og/brand.png",\n'
           '        "width": 1200,\n'
           '        "height": 630\n'
           '      },\n')
IMG_GUARD = '"@type": "ImageObject"'  # don't double-insert near Article

# ---- Homepage Organization logo (index.html) -----------------------------
HOME_ORG_OLD = """      "@type": "Organization",
      "@id": "https://www.ilmiöt.fi/#organization",
      "name": "Ilmiöitä",
      "url": "https://www.ilmiöt.fi/"
    },"""
HOME_ORG_NEW = """      "@type": "Organization",
      "@id": "https://www.ilmiöt.fi/#organization",
      "name": "Ilmiöitä",
      "url": "https://www.ilmiöt.fi/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://www.ilmiöt.fi/favicon.svg",
        "width": 64,
        "height": 64
      }
    },"""

# ---- tietoa.html Organization logo (last graph item, no trailing comma) ---
TIETOA_ORG_OLD = """      "@type": "Organization",
      "@id": "https://www.ilmiöt.fi/#organization",
      "name": "Ilmiöitä",
      "url": "https://www.ilmiöt.fi/"
    }"""
TIETOA_ORG_NEW = """      "@type": "Organization",
      "@id": "https://www.ilmiöt.fi/#organization",
      "name": "Ilmiöitä",
      "url": "https://www.ilmiöt.fi/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://www.ilmiöt.fi/favicon.svg",
        "width": 64,
        "height": 64
      }
    }"""

counts = {"mermaid": 0, "publisher_logo": 0, "author": 0, "article_image": 0,
          "home_org_logo": 0, "tietoa_org_logo": 0}

def sub_once(txt, old, new, guard=None):
    """Replace first occurrence if anchor present and (guard not already there)."""
    if old not in txt:
        return txt, False
    if guard is not None and guard in txt:
        return txt, False
    return txt.replace(old, new, 1), True

for fn in sorted(glob.glob("*.html")):
    txt = open(fn, encoding="utf-8").read()
    orig = txt

    # mermaid (skip if already lazy-loaded)
    if "IntersectionObserver" not in txt:
        txt, ok = sub_once(txt, MERMAID_OLD, MERMAID_NEW)
        if ok:
            counts["mermaid"] += 1

    # article publisher logo
    txt, ok = sub_once(txt, PUB_OLD, PUB_NEW)
    if ok:
        counts["publisher_logo"] += 1

    # article author
    txt, ok = sub_once(txt, AUTH_OLD, AUTH_NEW)
    if ok:
        counts["author"] += 1

    # article image (guard against double-insert)
    if IMG_OLD in txt and IMG_GUARD not in txt.split(IMG_OLD, 1)[1][:300]:
        txt = txt.replace(IMG_OLD, IMG_NEW, 1)
        counts["article_image"] += 1

    # homepage org logo
    if fn == "index.html":
        txt, ok = sub_once(txt, HOME_ORG_OLD, HOME_ORG_NEW)
        if ok:
            counts["home_org_logo"] += 1

    # tietoa org logo
    if fn == "tietoa.html":
        txt, ok = sub_once(txt, TIETOA_ORG_OLD, TIETOA_ORG_NEW)
        if ok:
            counts["tietoa_org_logo"] += 1

    if txt != orig:
        open(fn, "w", encoding="utf-8").write(txt)

for k, v in counts.items():
    print(f"  {k}: {v}")
