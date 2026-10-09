"""Original editorial content for the Stratum concept site.

Every article, company and person here is fictional. Each entry renders to
/<kind dir>/<slug>.html; `sections` is a list of (title, lede, html) blocks.
"""

ARTICLES = [
    # ------------------------------------------------------------------ blog
    {
        "kind": "blog", "slug": "inside-market-dynamics", "date": "2026-10-05", "cover": "img/forest.webp",
        "title": "Inside Market Dynamics: who is buying carbon credits, and where the money is going",
        "desc": "How we built a single view of retirements, issuances and capital flows — and three patterns it has already revealed.",
        "sections": [("", "", """
<p>Buyers, investors and developers all ask us the same question in different words: <strong>what is the rest of the market doing?</strong> Until now, answering it meant stitching together registry exports, press releases and anecdote. Market Dynamics is our attempt to replace that patchwork with one consistent view.</p>
<h2>What the module tracks</h2>
<p>Market Dynamics combines anonymised data from every RFP run on the Stratum platform with public registry records, harmonised into a single dataset. It covers three things:</p>
<ul><li><strong>Demand</strong> — retirements by buyer, sector, project type and vintage, updated quarterly.</li>
<li><strong>Supply</strong> — issuances, available volumes and pipeline by developer and methodology.</li>
<li><strong>Funding</strong> — capital committed to, and deployed into, future supply through forwards and offtakes.</li></ul>
<h2>Three patterns we already see</h2>
<h3>1. Removals are no longer niche</h3>
<p>Removal credits remain a minority of retirements by volume, but their share of spend keeps climbing. Buyers are pairing a core of high-quality avoidance with a growing sleeve of removals, and paying a clear premium for durability.</p>
<h3>2. Forward commitments are concentrating</h3>
<p>A small group of buyers accounts for a large share of forward capital. That gives those buyers real influence over which methodologies scale — and leaves late movers competing for what remains.</p>
<h3>3. Vintage matters more than ever</h3>
<p>Older vintages continue to trade at a steep discount, while recent vintages from well-rated projects hold their value. Price benchmarks that ignore vintage are increasingly misleading.</p>
<blockquote>Market Dynamics is available to all Intelligence subscribers. Book a walkthrough with our team to see it applied to your sector.</blockquote>
""")],
    },
    {
        "kind": "blog", "slug": "insetting-in-2026", "date": "2026-09-28", "cover": "img/grass.webp",
        "title": "Insetting in 2026: what the new standards change",
        "desc": "Value-chain interventions are finally getting clearer accounting rules. Here is what that means for Scope 3 strategies.",
        "sections": [("", "", """
<p>For years, insetting — investing in emissions reductions and removals inside your own value chain — sat in an accounting grey zone. Companies liked the idea; auditors struggled with the claims. That is changing.</p>
<h2>Why insetting is back on the agenda</h2>
<p>Scope 3 is where most corporate emissions live, and land-related emissions dominate for food, beverage and consumer goods companies. Investing in regenerative agriculture or agroforestry with your own suppliers can cut those emissions while strengthening supply resilience.</p>
<h2>What the new guidance clarifies</h2>
<ul><li><strong>Traceability:</strong> clearer rules on how closely an intervention must be linked to your supply chain before you can count it.</li>
<li><strong>Certificates:</strong> a growing role for environmental attribute certificates that can travel separately from physical goods.</li>
<li><strong>Claims:</strong> a firmer line between reductions counted against targets and contributions reported alongside them.</li></ul>
<h2>Three steps for buyers</h2>
<p><strong>Map your sourcing regions.</strong> Insetting only works where you can show a credible link between the intervention and what you buy.</p>
<p><strong>Choose the right instrument.</strong> Certificates, direct supplier programmes and insetting-specific credits each carry different claims and risks.</p>
<p><strong>Plan for verification.</strong> Build measurement and third-party verification into contracts from day one, not as an afterthought.</p>
""")],
    },
    {
        "kind": "blog", "slug": "corsia-guarantees-explained", "date": "2026-09-23", "cover": "img/clouds.webp",
        "title": "CORSIA guarantees explained: who carries the risk?",
        "desc": "Why eligible units need a guarantee, what can go wrong, and how insurance is reshaping airline procurement.",
        "sections": [("", "", """
<p>Airlines buying units for CORSIA compliance are not just buying tonnes. They are buying a promise that those tonnes will not be counted twice — once by the airline and once by the country that hosts the project.</p>
<h2>Why a guarantee is needed</h2>
<p>For a unit to be eligible, the host country must authorise its use and apply a corresponding adjustment to its own emissions accounts. If that authorisation is withdrawn, or the adjustment never happens, the unit's compliance value is at risk.</p>
<h2>Who carries that risk?</h2>
<p>Historically, the answer was often unclear. Contracts now increasingly assign the risk explicitly, with three common models:</p>
<ul><li><strong>Developer replacement:</strong> the seller commits to replace any unit that loses eligibility.</li>
<li><strong>Insurance:</strong> a third-party policy pays out, or funds replacement, if a defined event occurs.</li>
<li><strong>Price adjustment:</strong> the buyer accepts some risk in exchange for a lower price.</li></ul>
<h2>What this means for airlines</h2>
<p>The cheapest unit on paper is rarely the cheapest once delivery and eligibility risk are priced in. We recommend comparing offers on a <em>risk-adjusted</em> basis and agreeing replacement mechanisms before signing, not after a problem emerges.</p>
""")],
    },
    {
        "kind": "blog", "slug": "the-business-case-for-carbon-credits", "date": "2026-08-20", "cover": "img/valley.webp",
        "title": "The business case for carbon credits: what to put in front of finance",
        "desc": "CFOs want evidence, not adjectives. A practical structure for getting a credit budget approved.",
        "sections": [("", "", """
<p>Sustainability teams often lose budget arguments not because the case is weak, but because it is framed in the wrong language. Finance teams think in risk, cost and optionality. Here is how to translate.</p>
<h2>1. Start with exposure</h2>
<p>Quantify what is at stake: regulatory requirements, customer commitments, tender criteria and the cost of missing public targets. A credit strategy is a hedge against those exposures.</p>
<h2>2. Show the price curve</h2>
<p>High-quality supply is tightening. Forward prices for removals sit well above spot prices for older avoidance credits. Locking in part of your need early can be cheaper than buying everything later.</p>
<h2>3. Prove the process</h2>
<p>CFOs approve processes they can defend. A competitive, documented RFP with independent due diligence answers the questions an audit committee will ask.</p>
<h2>4. Offer options, not a single number</h2>
<p>Present two or three portfolio scenarios with clear trade-offs between price, quality and delivery risk. It turns a yes/no decision into a choice.</p>
""")],
    },
    {
        "kind": "blog", "slug": "net-zero-standard-v2-what-changes", "date": "2026-06-16", "cover": "img/lake.webp",
        "title": "Net-zero standard v2: what changes for carbon credit buyers",
        "desc": "The latest revision of corporate net-zero guidance gives credits a clearer — and more demanding — role.",
        "sections": [("", "", """
<p>The newest generation of corporate net-zero guidance does not make carbon credits optional extras any more. It defines where they fit, and it raises the bar for the ones that count.</p>
<h2>The headline changes</h2>
<ul><li><strong>Residual emissions:</strong> clearer expectations for neutralising the emissions that remain at net-zero, with a strong preference for durable removals.</li>
<li><strong>Interim action:</strong> recognition for companies that take responsibility for ongoing emissions before their net-zero date.</li>
<li><strong>Quality:</strong> explicit reference to integrity criteria for the credits used.</li></ul>
<h2>What buyers should do now</h2>
<p><strong>Separate your portfolio by purpose.</strong> Credits that support interim claims and those that neutralise residuals will be judged differently.</p>
<p><strong>Build a removals pathway.</strong> Durable removal supply is scarce; multi-year offtakes are often the only route to secure it at a reasonable price.</p>
<p><strong>Document everything.</strong> Claims will be scrutinised. Keep a clear audit trail of selection criteria, diligence and retirements.</p>
""")],
    },
    {
        "kind": "blog", "slug": "reading-forward-curves", "date": "2026-06-04", "cover": "img/terraces.webp",
        "title": "Why forward curves beat price forecasts",
        "desc": "Forecasts tell you what someone thinks will happen. Forward curves tell you what the market is pricing today.",
        "sections": [("", "", """
<p>Ask ten analysts where carbon prices will be in 2030 and you will get ten answers. Forward curves offer something more useful: a data-based view of what buyers and sellers are actually agreeing to pay for future delivery.</p>
<h2>How our curves are built</h2>
<p>Stratum's vintage forward curves draw on real offers and contracts submitted through our procurement platform, segmented by project type, region and rating. They are recalibrated as new transactions come in.</p>
<h2>How buyers use them</h2>
<ul><li>Benchmarking forward offers against the market before negotiating.</li>
<li>Deciding how much of a future need to lock in now versus later.</li>
<li>Valuing existing offtake contracts for internal reporting.</li></ul>
<h2>Limits to keep in mind</h2>
<p>Forward curves reflect today's expectations, which can shift quickly with policy. They are a tool for decision-making, not a guarantee — which is why we pair them with policy analysis and expert judgement.</p>
""")],
    },
    # ------------------------------------------------------------ case studies
    {
        "kind": "case-study", "slug": "northwind-climate-resilience-portfolio", "date": "2026-03-03", "cover": "img/mountains.webp",
        "title": "Building a climate-resilience carbon portfolio for Northwind Re",
        "desc": "How a global reinsurer combined frontier removals with high-integrity nature-based projects.",
        "facts": [("Client", "Northwind Re"), ("Sector", "Insurance & reinsurance"), ("Engagement", "Strategy, sourcing and due diligence"), ("Solution", "Diversified removal-led portfolio"), ("Outcome", "Five projects across three continents")],
        "stats": [("22%", "Savings vs initial quotes"), ("5", "Projects contracted"), ("3", "Continents"), ("100%", "Projects with site-level diligence")],
        "sections": [
            ("", "", "<p>Northwind Re wanted its carbon programme to reflect how it already thinks about climate: as a long-term risk to be understood and managed. Stratum worked with the sustainability and risk teams to design and deliver a portfolio built around resilience.</p>"),
            ("Challenge", "Northwind needed a portfolio it could defend to clients, regulators and its own risk committee.", "<p>Previous purchases had been made opportunistically through brokers, with little visibility on price or quality. The team wanted a clear rationale for every project, a credible share of durable removals, and a process that could be repeated each year.</p>"),
            ("Solution", "A structured strategy and competitive RFP, with diligence matched to each project's risk.", "<p><strong>Strategy first.</strong> We translated Northwind's climate commitments into procurement criteria, including target shares for removals and nature-based projects.</p><p><strong>Market-wide sourcing.</strong> The RFP reached our full developer network and returned dozens of comparable proposals.</p><p><strong>Tiered diligence.</strong> Automated screening narrowed the field; analyst-led and on-site reviews covered the final shortlist.</p><p><strong>One contract.</strong> Stratum acted as contracting counterparty, giving Northwind a single agreement across all five projects.</p>"),
        ],
    },
    {
        "kind": "case-study", "slug": "meridian-capital-net-zero-fund", "date": "2025-08-21", "cover": "img/elephants.webp",
        "title": "Enabling Meridian Capital to deliver a net-zero fund strategy",
        "desc": "Multi-year offtakes, a custom risk framework and ongoing monitoring for an infrastructure investor.",
        "facts": [("Client", "Meridian Capital"), ("Sector", "Private infrastructure investment"), ("Engagement", "Procurement and due diligence"), ("Solution", "Multi-year forward offtakes"), ("Outcome", "Net-zero commitment met on schedule")],
        "stats": [("30+", "Hours saved per diligence report"), ("4", "Offtake agreements"), ("6", "Years of forward supply"), ("1", "Consolidated contract")],
        "sections": [
            ("", "", "<p>Meridian Capital committed one of its flagship funds to net zero, including responsibility for residual emissions across its portfolio companies. Stratum became an extension of the investment team for procurement and diligence.</p>"),
            ("Challenge", "Securing long-term, high-quality supply without tying up the team for months.", "<p>Forward offtakes carry delivery, policy and counterparty risk over many years. Meridian needed a framework its investment committee would trust — and a partner able to monitor projects long after signing.</p>"),
            ("Solution", "A competitive process for offtakes, backed by a bespoke forward-risk framework.", "<p>We designed a due diligence framework tailored to forward purchases, assessed every proposal against it, and carried out in-person monitoring visits on shortlisted projects. Ongoing portfolio monitoring flags delivery or policy issues as they arise.</p>"),
        ],
    },
    {
        "kind": "case-study", "slug": "velo-carbon-removal-programme", "date": "2025-08-06", "cover": "img/canopy.webp",
        "title": "Helping Velo launch a targeted carbon removal programme",
        "desc": "From ad-hoc purchases to a removal programme a digital marketplace's board could back.",
        "facts": [("Client", "Velo"), ("Sector", "Digital marketplace"), ("Engagement", "Strategy and sourcing"), ("Solution", "Removal-focused portfolio"), ("Outcome", "Board-approved multi-year plan")],
        "stats": [("20%+", "Average cost savings"), ("3", "Removal projects"), ("2", "Weeks to shortlist"), ("1", "Clear board narrative")],
        "sections": [
            ("", "", "<p>Velo had bought credits before, but without a strategy tying them to its net-zero target. Stratum helped the company define what it wanted to support — and why.</p>"),
            ("Challenge", "Turning good intentions into a programme the board would fund.", "<p>The sustainability team needed a clear story: which projects, at what price, and how they connected to Velo's climate vision and targets.</p>"),
            ("Solution", "A focused strategy and a short, competitive sourcing round.", "<p>We ran a strategy workshop, defined criteria centred on durable removals, and sourced options through a targeted RFP. The final portfolio came with a presentation-ready narrative for the board.</p>"),
        ],
    },
    {
        "kind": "case-study", "slug": "verdant-alliance-removals-rfp", "date": "2026-03-31", "cover": "img/mangrove.webp",
        "title": "Powering a coalition's nature-based removals RFP",
        "desc": "A rolling, multi-stage intake model for one of the market's most ambitious advance commitments.",
        "facts": [("Client", "Verdant Alliance"), ("Sector", "Buyers' coalition"), ("Engagement", "End-to-end RFP support"), ("Solution", "Custom multi-stage platform"), ("Outcome", "Rolling intake across cycles")],
        "stats": [("1,300+", "Suppliers reached"), ("3", "Intake stages"), ("100%", "Automated eligibility checks"), ("1", "Shared scorecard")],
        "sections": [
            ("", "", "<p>Verdant Alliance brings together several large buyers committed to purchasing nature-based removals at scale. It selected Stratum to run its procurement cycle.</p>"),
            ("Challenge", "Evaluating a large, diverse pipeline fairly and efficiently.", "<p>A coalition needs a process every member can trust, and developers need a submission process that does not waste months of effort on projects that will never qualify.</p>"),
            ("Solution", "A customised version of the Stratum RFP platform.", "<ul><li>Redesigned multi-stage submission process</li><li>A shared scorecard agreed by all members</li><li>Automated eligibility and geospatial screening</li><li>End-to-end procurement support from our team</li></ul>"),
        ],
    },
    # ------------------------------------------------------------------ reports
    {
        "kind": "report", "slug": "how-to-structure-your-carbon-portfolio-under-new-net-zero-standards", "date": "2026-07-09", "cover": "img/river.webp",
        "title": "How to structure your carbon portfolio under new net-zero standards",
        "desc": "A practical guide to building a portfolio that holds up under the latest corporate climate guidance.",
        "sections": [("", "", """
<p>New net-zero guidance changes what a credible carbon portfolio looks like. This guide sets out a step-by-step approach for sustainability and procurement teams.</p>
<h2>What you will learn</h2>
<ul><li>How to separate credits by purpose: interim responsibility versus residual neutralisation</li>
<li>How to set a removals pathway and phase it over time</li>
<li>How to balance spot purchases, forwards and offtakes</li>
<li>Which quality criteria buyers are using as minimum standards</li>
<li>How to document decisions for audit and disclosure</li></ul>
<h2>Who it is for</h2>
<p>Heads of sustainability, procurement leads and finance partners responsible for carbon budgets and climate claims.</p>
""")],
    },
    {
        "kind": "report", "slug": "resilient-removals-portfolio", "date": "2026-05-14", "cover": "img/tree.webp",
        "title": "How to build a resilient carbon removals portfolio",
        "desc": "Diversification, durability and delivery risk: the three levers of a removals strategy that lasts.",
        "sections": [("", "", """
<p>Removal supply is scarce and expensive, and delivery risk is real. This report shows how leading buyers are building removal portfolios that stay resilient as the market evolves.</p>
<h2>Inside the report</h2>
<ul><li>A framework for comparing nature-based and engineered removals</li>
<li>How to diversify across methodologies, geographies and delivery dates</li>
<li>Contract structures that protect against non-delivery</li>
<li>Price benchmarks by removal type</li></ul>
""")],
    },
    {
        "kind": "report", "slug": "buyers-guide-cookstove-credits", "date": "2025-03-11", "cover": "img/cookstove.webp",
        "title": "Buyer's guide to high-quality cookstove carbon credits",
        "desc": "What separates credible cookstove projects from the rest — and the questions to ask before you buy.",
        "sections": [("", "", """
<p>Clean cookstove projects can deliver large health and climate benefits — but quality varies widely. This guide helps buyers tell the difference.</p>
<h2>What the guide covers</h2>
<ul><li>The main sources of over-crediting risk and how to spot them</li>
<li>Which methodologies and monitoring approaches buyers favour</li>
<li>Co-benefits and how to verify them</li>
<li>A due diligence checklist for cookstove offers</li></ul>
""")],
    },
]
