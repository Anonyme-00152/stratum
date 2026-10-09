# Stratum — environmental markets platform (concept)

**Stratum is a fictional company.** This is a portfolio concept: a complete, production-grade marketing
site for a carbon-credit procurement, intelligence and advisory platform. All companies, people,
testimonials and articles are invented; figures are illustrative.

Design & development: **Ebubekir Arti — EbuStudio**

## Highlights

- 34 pages: home, platform, 5 use-case pages, 2 market pages, 3 audience pages, about, resources hub,
  contact, legal, 404, plus blog posts, case studies and gated reports
- Animated topographic contour background (value noise + marching squares on canvas, cursor-reactive)
- Live RFP mock, interactive price chart, savings calculator, scroll-driven process stepper
- Mega menu, accessible tabs and carousel, filters + search, validated forms, cookie banner
- Responsive to 375 px, keyboard accessible, `prefers-reduced-motion` aware, SEO metadata + sitemap
- No framework, no dependencies at runtime — static HTML, one CSS file, one JS file

## Build

    pip install jinja2 markupsafe
    python build.py                                   # src/ + data/ -> site/
    python -m http.server 3071 --directory site

## Structure

| Path | Purpose |
| --- | --- |
| `build.py` | Generator + site data (brand, navigation, team, testimonials, icons) |
| `data/articles.py` | Blog posts, case studies and reports |
| `data/legal.json` | Privacy policy and terms |
| `src/templates/` | Base layout, macros, article and listing templates |
| `src/pages/` | One template per page |
| `static/` | CSS, JS, favicon, images |
| `site/` | Built output (deployed as-is) |

To rename the brand, change `BRAND` in `build.py` and the literal name in `src/`.

## Notes

- Forms validate and show a success state but do not send anywhere (demo).
- Charts marked "illustrative" use example data.
- Photographs remain the property of their respective owners.
