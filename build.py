"""Static site generator for Stratum — a fictional environmental-markets platform (portfolio concept).

    python build.py          -> renders src/ + data/ into site/
"""
import json
import shutil
from datetime import date, datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "site"
SITE_URL = "https://stratum-markets.vercel.app"

# --------------------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-left": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "arrow-up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
    "arrow-ur": '<path d="M7 17L17 7M8 7h9v9"/>',
    "chevron": '<path d="M6 9l6 6 6-6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
    "rfp": '<rect x="5" y="3.5" width="14" height="17" rx="2.5"/><path d="M9 3.5h6v3H9zM8.5 11h7M8.5 14.5h7M8.5 18h4"/>',
    "compass": '<circle cx="12" cy="12" r="8.5"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "shield": '<path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.3-7.5 9.5-4.3-1.2-7.5-4.9-7.5-9.5V6z"/><path d="M8.8 12.2l2.2 2.2 4.3-4.4"/>',
    "chart": '<path d="M4 20V4M4 20h16"/><path d="M7.5 15l3.5-4 3 2.5 5-6.5"/>',
    "handshake": '<path d="M3 11l4-4 5 2 5-2 4 4"/><path d="M7 7v6l5 5 5-5V7"/><path d="M10 13l2 2"/>',
    "leaf": '<path d="M5 19c0-8 5-14 15-14 0 10-6 15-14 15"/><path d="M5 19c3-4 6-7 10-9"/>',
    "plane": '<path d="M10.5 13.5L4 11l1.5-1.5 7 1 4-4.5c1-1 2.6-1.2 3.2-.6.6.6.4 2.2-.6 3.2l-4.5 4 1 7L14 21l-2.5-6.5L8 18v2.5L6.5 22l-1-3.5L2 17.5 3.5 16H6z"/>',
    "building": '<path d="M4 21V6l8-3v18M12 9h8v12M4 21h17"/><path d="M7.5 9h1M7.5 13h1M7.5 17h1M15.5 13h1M15.5 17h1"/>',
    "trending": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    "sprout": '<path d="M12 21v-9"/><path d="M12 12c0-4-3-7-8-7 0 4 3 7 8 7zM12 10c0-3.5 2.5-6 7-6 0 3.5-2.5 6-7 6z"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.6 3.7 5.4 3.7 8.5s-1.2 5.9-3.7 8.5c-2.5-2.6-3.7-5.4-3.7-8.5S9.5 6.1 12 3.5z"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.3-6 6.5-6s5.9 2.4 6.5 6"/><path d="M16 4.6a3.5 3.5 0 010 6.8M18 14.4c2 .9 3.3 2.9 3.6 5.6"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "file": '<path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "play": '<circle cx="12" cy="12" r="8.5"/><path d="M10 8.8v6.4l5-3.2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/>',
    "pin": '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0113 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
    "scale": '<path d="M12 4v16M7 20h10M5 8h14M5 8l-2.5 6a3.2 3.2 0 005 0zM19 8l-2.5 6a3.2 3.2 0 005 0z"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
    "database": '<ellipse cx="12" cy="6" rx="7.5" ry="3"/><path d="M4.5 6v12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3V6M4.5 12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3"/>',
    "map": '<path d="M9 4L3.5 6v14L9 18l6 2 5.5-2V4L15 6z"/><path d="M9 4v14M15 6v14"/>',
    "award": '<circle cx="12" cy="9" r="5.5"/><path d="M8.5 13.5L7 21l5-2.5 5 2.5-1.5-7.5"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8 10.5V8a4 4 0 018 0v2.5"/>',
    "zap": '<path d="M13 3L5 13.5h6L10 21l8-10.5h-6z"/>',
    "sparkle": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
    "satellite": '<path d="M7 10l3-3 7 7-3 3z"/><path d="M5 8l2-2M12 15l-2 2M17 17l2.5 2.5M4.5 15.5a4 4 0 004 4M3 15a6 6 0 006 6"/>',
    "refresh": '<path d="M20 11a8 8 0 00-14.6-4.5L4 8M4 4v4h4M4 13a8 8 0 0014.6 4.5L20 16M20 20v-4h-4"/>',
    "portfolio": '<rect x="3.5" y="7" width="17" height="13" rx="2.5"/><path d="M9 7V5.5A1.5 1.5 0 0110.5 4h3A1.5 1.5 0 0115 5.5V7M3.5 12.5h17"/>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0013 0M12 17.5V21"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="3.5"/><path d="M8 10.5V16M8 7.5v.1M12 16v-3.2c0-1.4 1-2.3 2.2-2.3s2 .9 2 2.3V16M12 10.5V16"/>',
    "youtube": '<rect x="2.5" y="5.5" width="19" height="13" rx="4"/><path d="M10.5 9.5v5l4.3-2.5z"/>',
    "quote": '<path d="M9 7H5.5v5H9v1.5A2.5 2.5 0 016.5 16M19 7h-3.5v5H19v1.5a2.5 2.5 0 01-2.5 2.5"/>',
    "download": '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>',
    "eye": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "coins": '<ellipse cx="9" cy="7" rx="5.5" ry="2.5"/><path d="M3.5 7v4c0 1.4 2.5 2.5 5.5 2.5s5.5-1.1 5.5-2.5V7M3.5 11v4c0 1.4 2.5 2.5 5.5 2.5 1 0 2-.1 2.8-.4"/><ellipse cx="16" cy="15" rx="4.5" ry="2"/><path d="M11.5 15v3c0 1.1 2 2 4.5 2s4.5-.9 4.5-2v-3"/>',
}


def icon(name, cls=""):
    body = _I.get(name, _I["sparkle"])
    c = f' class="{cls}"' if cls else ""
    return Markup(
        f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{body}</svg>'
    )


LOGO = Markup(
    '<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
    '<rect width="32" height="32" rx="9" fill="#0f3329"/>'
    '<path d="M6 25.5C9.6 16.4 12.6 9.8 16 7c3.4 2.8 6.4 9.4 10 18.5" fill="none" stroke="#d4ea7c" stroke-width="1.9" stroke-linecap="round"/>'
    '<path d="M10.8 25.5c2.1-5.4 3.7-9.1 5.2-10.7 1.5 1.6 3.1 5.3 5.2 10.7" fill="none" stroke="#a7c2a3" stroke-width="1.6" stroke-linecap="round"/>'
    '<circle cx="16" cy="21.3" r="1.9" fill="#eaa43c"/></svg>'
)

# --------------------------------------------------------------------------- navigation
SOLUTIONS = [
    {"title": "By use case", "items": [
        {"href": "/procurement.html", "label": "Run an RFP", "desc": "Undertake structured procurement", "icon": "rfp"},
        {"href": "/advisory.html", "label": "Build your strategy", "desc": "Tap into our expertise", "icon": "compass"},
        {"href": "/due-diligence.html", "label": "Conduct due diligence", "desc": "Understand every risk", "icon": "shield"},
        {"href": "/intelligence.html", "label": "Get market intelligence", "desc": "Keep up to speed", "icon": "chart"},
        {"href": "/access-demand.html", "label": "Access demand", "desc": "Sell environmental assets", "icon": "handshake"},
    ]},
    {"title": "By market", "items": [
        {"href": "/voluntary.html", "label": "Voluntary carbon market", "desc": "Buy high-integrity credits", "icon": "leaf"},
        {"href": "/corsia.html", "label": "CORSIA", "desc": "Navigate aviation compliance", "icon": "plane"},
    ]},
    {"title": "By organisation", "items": [
        {"href": "/buyers.html", "label": "Buyers", "desc": "Procure environmental assets", "icon": "building"},
        {"href": "/investors.html", "label": "Investors", "desc": "Locate opportunities", "icon": "trending"},
        {"href": "/developers.html", "label": "Developers", "desc": "Access guaranteed demand", "icon": "sprout"},
    ]},
]
RESOURCES = [
    {"href": "/reports/", "label": "Reports", "desc": "In-depth analysis", "icon": "file"},
    {"href": "/blog/", "label": "Blog", "desc": "Latest news and updates", "icon": "layers"},
    {"href": "/resources.html#events", "label": "Webinars & events", "desc": "Tune in", "icon": "mic"},
    {"href": "/case-studies/", "label": "Customer stories", "desc": "How we've helped", "icon": "award"},
    {"href": "/resources.html#newsletter", "label": "Newsletter", "desc": "Monthly market briefing", "icon": "mail"},
]

BRAND = "Stratum"
LEGAL_NAME = "Stratum Markets Ltd"
CONTACT_EMAIL = "hello@stratum.example"

CLIENTS = [
    ("Northwind Re", ""), ("Velo", "wm-light"), ("Meridian Capital", "wm-serif"), ("Lumen Events", "dot"),
    ("Halcyon", "wm-mono"), ("Arcturus Air", ""), ("Solenne", "wm-serif"), ("Kestrel Telecom", ""),
    ("Fernhill", "wm-light"), ("Verdant Alliance", "sq"), ("Canopia", "wm-serif"), ("Greenfield", ""),
]

TESTIMONIALS = {
    "northwind": {"co": "Northwind Re", "name": "Clara Weston", "role": "Head of Sustainability, Northwind Re", "img": "mountains", "case": "/case-studies/northwind-climate-resilience-portfolio.html",
                  "q": "We wanted carbon procurement that reflected how we think about climate risk, not just a line in a report. Stratum helped us design a diversified portfolio that delivers credible impact today and supports the solutions we'll need tomorrow."},
    "halcyon": {"co": "Halcyon Investment Group", "name": "Daniel Osei", "role": "Principal, Halcyon Investment Group", "img": "coast",
                "q": "Stratum has become our reference point for the carbon market — for investment decisions and for understanding how the market really works. The team consistently goes the extra mile on research."},
    "canopia": {"co": "Canopia Restoration", "name": "Amara Ndlovu", "role": "CEO & Co-Founder, Canopia Restoration", "img": "seedling",
                "q": "Through Stratum we reached buyers we could never have found alone. That demand let us scale our restoration work and bring more smallholder families into the carbon market."},
    "meridian": {"co": "Meridian Capital", "name": "Lucas Brandt", "role": "Director of Investments, Meridian Capital", "img": "elephants", "case": "/case-studies/meridian-capital-net-zero-fund.html",
                 "q": "Stratum ran a transparent, competitive process for our multi-year offtakes and gave our investment committee the evidence it needed. It made one of the first net-zero fund strategies in our sector possible."},
    "velo": {"co": "Velo", "name": "Priya Raman", "role": "Chief People & Impact Officer, Velo", "img": "canopy", "case": "/case-studies/velo-carbon-removal-programme.html",
             "q": "Stratum's strategy work and sourcing helped us move from ad-hoc purchases to a removal programme our board understands and supports. Their candour was as valuable as their data."},
    "lumen": {"co": "Lumen Events", "name": "Sofia Marquez", "role": "Director of Environmental Impact, Lumen Events", "img": "terraces",
              "q": "Stratum gave us confidence that our climate contribution matched our ambitions. Their market access and rigour turned a complicated decision into a clear one."},
    "greenfield": {"co": "Greenfield Carbon", "name": "Tom Reilly", "role": "Head of Supply, Greenfield Carbon", "img": "leaf",
                   "q": "The platform makes complex, fast-moving carbon policy across multiple countries genuinely understandable."},
    "bloom": {"co": "Bloom Agroforestry", "name": "Hana Sato", "role": "Founder, Bloom Agroforestry", "img": "farmer",
              "q": "Knowledgeable, professional and warm. In a market that changes every quarter, Stratum is the partner we can rely on."},
}

PEOPLE = {
    "elena": ("Elena Varga", "CEO and Co-founder", "A decade building data products at consumer and fintech scale-ups before founding Stratum to bring the same rigour to climate markets."),
    "marcus": ("Marcus Lindqvist", "Co-founder", "Former investment banker advising corporates on nature-based and impact portfolios; helped launch a nine-figure nature fund."),
    "ines": ("Inès Moreau", "Chief Operating Officer", "Runs operations and delivery across offices; previously chief of staff at a high-growth agri-tech company and a qualified lawyer."),
    "rafael": ("Rafael Ortega", "Director of Policy", "Fifteen years in international climate negotiations, specialising in Article 6 and aviation compliance frameworks."),
    "noah": ("Noah Bennett", "Global Commercial Director", "Has built climate programmes with hundreds of companies; leads Stratum's relationships with buyers worldwide."),
    "yara": ("Yara Haddad", "Director of Product", "Twenty years shipping financial and data platforms, now leading the Stratum platform roadmap."),
    "chloe": ("Chloé Dubois", "Director of Go-To-Market", "Scaled B2B climate and SaaS products from first customer to enterprise; leads marketing and partnerships."),
    "kenji": ("Kenji Watanabe", "Director of People", "Builds people-first, high-performing teams; previously scaled people functions at two venture-backed start-ups."),
    "aisha": ("Dr. Aisha Bello", "Head of Science", "Leads technical due diligence and methodology review. PhD in Earth Science; independent reviewer for carbon standards."),
    "liam": ("Liam O'Connor", "Climate Strategy Manager", "Helps companies integrate credits, insetting and removals into credible net-zero pathways."),
    "mateo": ("Mateo Silva", "Knowledge & Data Manager", "Builds Stratum's pricing models and CORSIA supply and demand forecasts. MSc in Carbon Finance."),
    "zofia": ("Zofia Kowal", "Policy Manager", "Tracks national regulation, Article 6 engagement and compliance mechanisms across 40+ countries."),
    "lucia": ("Lucía Herrera", "Policy Associate", "Covers Latin America and the Caribbean; leads on Free, Prior and Informed Consent and co-benefits assessment."),
    "anika": ("Dr. Anika Shah", "Head of Origination", "Fifteen years scaling nature-based solutions; leads sourcing and contract structuring with developers."),
    "olu": ("Olu Adeyemi", "Origination Manager", "Sources CORSIA-eligible supply and manages long-term relationships with Stratum's developer network."),
}

EVENTS = [
    ("2026-09-17", "Webinar", "Guarantees and insurance for CORSIA units, explained", "clouds"),
    ("2026-06-22", "Event", "Stratum at Climate Action Week 2026", "valley"),
    ("2026-03-18", "Webinar", "Carbon markets in 2026: where voluntary meets compliance", "river"),
    ("2025-05-06", "Webinar", "High stakes, higher integrity: a new era of market maturity", "mountains"),
    ("2024-10-31", "Webinar", "Investing in carbon projects: managing policy risk", "forest"),
    ("2024-10-02", "Webinar", "Article 6 in practice: what to watch, and why it matters", "lake"),
]

KIND = {
    "blog": {"label": "Blog", "dir": "blog", "plural": "Blog"},
    "case-study": {"label": "Case study", "dir": "case-studies", "plural": "Customer stories"},
    "report": {"label": "Report", "dir": "reports", "plural": "Reports"},
}


def load_articles():
    import re
    import sys
    sys.path.insert(0, str(ROOT / "data"))
    from articles import ARTICLES
    items = []
    for src in ARTICLES:
        it = dict(src)
        k = KIND[it["kind"]]
        it["url"] = f"/{k['dir']}/{it['slug']}.html"
        it["label"] = k["label"]
        it["sections"] = [{"title": t, "lede": l, "html": Markup(h.strip())} for t, l, h in it["sections"]]
        it["facts"] = [{"label": l, "value": v} for l, v in it.get("facts", [])]
        it["stats"] = it.get("stats", [])
        words = len(re.sub(r"<[^>]+>", " ", " ".join(x["html"] for x in it["sections"])).split())
        it["read"] = max(2, round(words / 200))
        it["topic"] = topic_of(it)
        items.append(it)
    items.sort(key=lambda x: x["date"], reverse=True)
    return items


def topic_of(it):
    t = (it["title"] + " " + it["desc"]).lower()
    if "corsia" in t or "aviation" in t or "icao" in t:
        return "corsia"
    if any(w in t for w in ("sbti", "net-zero", "net zero", "claim", "directive", "scope 3", "insetting", "ets", "policy", "article 6")):
        return "policy"
    if any(w in t for w in ("price", "pricing", "curve", "market dynamics", "data", "value")):
        return "pricing"
    return "strategy"


def fmt_date(iso, style="long"):
    if not iso:
        return ""
    d = date.fromisoformat(iso)
    return d.strftime("%d %b %Y").lstrip("0") if style == "long" else d.strftime("%b %Y")


def initials(name):
    parts = [p for p in name.replace(".", " ").split() if p[0].isupper()]
    return (parts[0][0] + parts[-1][0]) if len(parts) > 1 else name[:2].upper()


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "static", OUT)

    env = Environment(loader=FileSystemLoader(str(SRC)), autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)
    articles = load_articles()
    legal = {k: {"title": v["title"], "html": Markup(v["html"])} for k, v in json.loads((ROOT / "data" / "legal.json").read_text(encoding="utf-8")).items()}
    by_kind = {k: [a for a in articles if a["kind"] == k] for k in KIND}
    by_slug = {a["slug"]: a for a in articles}
    env.globals.update(
        icon=icon, LOGO=LOGO, SOLUTIONS=SOLUTIONS, RESOURCES=RESOURCES, CLIENTS=CLIENTS, T=TESTIMONIALS, PEOPLE=PEOPLE,
        EVENTS=EVENTS, LEGAL=legal, BRAND=BRAND, LEGAL_NAME=LEGAL_NAME, CONTACT_EMAIL=CONTACT_EMAIL, KIND=KIND, articles=articles, by_kind=by_kind, by_slug=by_slug, SITE_URL=SITE_URL,
        initials=initials, today=date.today().isoformat(), BUILD_YEAR=datetime.now().year,
    )
    env.filters["date"] = fmt_date
    env.filters["zip"] = lambda a, b: list(zip(a, b))

    pages = []
    for tpl in sorted((SRC / "pages").glob("*.html")):
        name = tpl.name
        html = env.get_template(f"pages/{name}").render(page=name.replace(".html", ""))
        (OUT / name).write_text(html, encoding="utf-8")
        pages.append("/" + ("" if name == "index.html" else name))

    for k, meta in KIND.items():
        d = OUT / meta["dir"]
        d.mkdir(exist_ok=True)
        lst = by_kind[k]
        (d / "index.html").write_text(env.get_template("templates/listing.html").render(kind=k, meta=meta, items=lst, page=meta["dir"]), encoding="utf-8")
        pages.append(f"/{meta['dir']}/")
        for i, a in enumerate(lst):
            same = [x for x in lst if x is not a]
            related = sorted(same, key=lambda x: (x["topic"] != a["topic"], -(int((x["date"] or "0000").replace("-", "")))))[:3]
            html = env.get_template("templates/article.html").render(a=a, related=related, page=meta["dir"])
            (d / f"{a['slug']}.html").write_text(html, encoding="utf-8")
            pages.append(a["url"])

    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{SITE_URL}{p}</loc></url>" for p in pages if p != "/404.html"]
    sm.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    print(f"built {len(pages)} pages -> {OUT}")


if __name__ == "__main__":
    build()
