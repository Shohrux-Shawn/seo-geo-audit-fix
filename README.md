# seo-geo-audit-fix

A Claude skill that audits a website — or a whole network of sites — for **SEO, local SEO and GEO** (visibility in AI answers), proves every finding with live evidence, and turns the findings into exact fixes that are applied only after approval and then verified live.

It works in any market, with extra depth for **Korea** (Naver Search Advisor, Naver Smart Place, Naver KnowledgeiN, Daum Webmaster Tools, Kakao Map, Korean attorney-advertising rules), where Google-only habits miss half the picture.

It also covers the **off-site entity layer** that AI engines actually read — Wikidata, Wikipedia, Namuwiki, the Google knowledge panel, company profiles and earned mentions — so that ChatGPT, Perplexity, Google AI Overviews and Naver AI Briefing describe a company quickly and correctly, within the wikis' conflict-of-interest rules.

It also teaches the AI that uses it **how to change code safely** (redirects, canonical/hreflang, JSON-LD, robots.txt, Core Web Vitals, CMS persistence) and **how to build, validate and submit sitemaps** to Google Search Console, Bing, IndexNow, Naver and Daum.

## What it does

The skill runs one repeatable loop:

**audit → evidence → fixes → approval → verification**

1. **Fact sheet first.** Build or reuse a `seo-geo-facts.md` with sites, entity/NAP facts, markets, access and owner decisions. Every listed domain is resolved before it is audited.
2. **Audit modules A–I.** Reachability and crawl, on-page, structured data and entity, performance, content quality and network risk, local profiles (Google Business Profile, Naver Smart Place, Kakao Map), NAP consistency across the web, rankings and AI answers, and off-site entity authority (AI source map, Wikidata/Wikipedia/Namuwiki, knowledge panel, profiles, earned mentions).
3. **Evidence for every claim.** URL + exact text or numbers. Anything not checked is marked NOT VERIFIED.
4. **Scored findings and a fix plan.** Severity, owner, effort and a verification step for each fix; owner decisions override generic advice and are listed under "Skipped by owner decision".
5. **Apply only after approval.** Code, CMS, sitemap-submission and listing changes are staged and approved per group, following a safe change workflow (branch → minimal diff → tests/build → deploy → live curl check).
6. **Verify and re-measure.** Same day, after 1–3 days, and again after 2–4 weeks against the baseline.

## Folder structure

```
seo-geo-audit-fix/
├── SKILL.md                              # the workflow Claude follows
├── references/
│   ├── knowledge-base.md                 # core SEO + GEO rules (crawl, on-page, schema, E-E-A-T, links, GEO, measurement)
│   ├── korea-search.md                   # Naver, Daum/Kakao, Google KR, local strategy, legal directories
│   ├── indexing-audit.md                 # condensed Google/Bing/Naver indexing audit
│   ├── content-scale-and-quality.md      # publishing volume, scaled-content risk, writing, lawyer-ad compliance
│   ├── multisite-and-technical.md        # satellite architecture, doorway risk, setup checklist, migration, deploy
│   ├── lessons-learned.md                # symptom → cause → fix → early detection, from real incidents
│   ├── case-study-multisite-law-firm.md  # anonymised worked example: main site + 6 satellites
│   ├── entity-authority-and-off-site.md  # AI citation sources, Wikidata/Wikipedia/Namuwiki, knowledge panel, profiles, PR, COI rules
│   ├── implementation-playbook.md        # code recipes: redirects, canonical/hreflang, JSON-LD, CWV, CMS, curl checks
│   ├── sitemaps-and-submission.md        # sitemap protocol, generation per stack, GSC/Bing/IndexNow/Naver/Daum steps
│   └── sources.md                        # verified official sources, with the verification date
├── scripts/
│   ├── README.md                         # how to add a script
│   ├── site_check.py                     # redirects, robots/AI bots, llms.txt, sitemap crawl, per-page tags
│   ├── sitemap_validate.py               # sitemap/index validation + sample URL checks + hreflang
│   ├── indexnow_submit.py                # IndexNow key-file check and batch submit (--apply)
│   ├── gsc_sitemaps.py                   # Search Console sitemaps list/submit via service account (--apply)
│   ├── nap_compare.py                    # NAP master table and mismatches
│   ├── geo_grid.py                       # Google Maps geo-grid plan + summary
│   └── wikidata_entity_check.py          # Wikidata item completeness + site sameAs/P856 link check
└── templates/
    ├── seo-geo-facts.md                  # Step 0 fact sheet
    └── browser-prompts/                  # fill-in prompts for a browser agent (Claude in Chrome etc.)
        ├── README.md                     # order of use + shared safety rules
        ├── 01-site-network-audit.md
        ├── 02-entity-nap-and-geo-live-test.md
        ├── 03-gbp-readonly-status-check.md   # strict read-only, run before any profile edit
        ├── 04-maps-location-and-geogrid-test.md
        ├── 05-gbp-update-stage1.md       # category, hours, description, services, replies
        ├── 06-gbp-update-stage2.md       # attributes, retried replies, address change last
        └── 07-ai-source-map-and-offsite-entity.md  # which sources AI cites for the brand + entity inventory
```

## Install

**Claude.ai / Claude desktop app**
- Upload `seo-geo-audit-fix.skill` (or a zip of the `seo-geo-audit-fix/` folder) in Settings → Capabilities → Skills.

**Claude Code**
- Copy the folder into your skills directory:
  ```bash
  cp -r seo-geo-audit-fix ~/.claude/skills/seo-geo-audit-fix
  ```
- Or put it in a project at `.claude/skills/seo-geo-audit-fix/`.

The skill works best with a web-fetch or crawling tool (e.g. Firecrawl) and a browser tool for rendered pages and signed-in dashboards. Without them it switches to "delegation mode" and writes prompts for another agent.

## Quick start prompts

- "Audit https://www.example.com and its satellites for SEO/GEO and give me a fix plan."
- "Check our Google Business Profile, Naver Place and Kakao listings against the website and build a NAP master table."
- "Why are 800 URLs stuck in 'Discovered – currently not indexed' on https://www.example.com?"
- "Run a geo-grid test for '<city> lawyer' around our office and summarise where we rank."
- "Do ChatGPT, Perplexity and Google AI Overviews mention us? Trace every wrong fact back to its source page."
- "We want to raise publishing to 50 articles a day across 5 sites. Is that safe?"
- "What do ChatGPT and Perplexity say about our company, where do they get it, and should we be on Wikidata or Wikipedia?"
- "Our sitemap shows 3,000 URLs but only 1,200 are indexed. Validate it, fix the generator in our Next.js app and submit it again."

## Scripts

All scripts are read-only or dry-run by default; anything that sends data needs `--apply`. They use the Python standard library, except `gsc_sitemaps.py` (`pip install --upgrade google-api-python-client google-auth`). Secrets come from environment variables only. Run any of them with `--help`.

```bash
# Modules A/B/E: redirects, robots.txt, llms.txt, sitemap crawl, tags, duplicates, forbidden wording
python3 scripts/site_check.py https://www.example.com https://www.example-divorce.com \
    --max-urls 200 --forbidden "free consultation,24 hours" --out ./audit-out   # use the site's own language

# Module G: NAP master table against canonical values
python3 scripts/nap_compare.py sources.csv canonical.json > nap_report.md

# Module F: plan a geo-grid, fill in results.csv, then summarise
python3 scripts/geo_grid.py plan centres.csv "lawyer,law firm,divorce lawyer" --out grid
python3 scripts/geo_grid.py summary grid/results.csv > grid/summary.md

# Module A: validate a sitemap index (sample of 500 URLs)
python3 scripts/sitemap_validate.py https://www.example.com/sitemap.xml --host www.example.com --max 500 --out ./sitemap-out

# Module I: find the company's Wikidata item, then check it against the site's JSON-LD
python3 scripts/wikidata_entity_check.py --search "Example Law Firm" --lang ko
python3 scripts/wikidata_entity_check.py --qid Q12345 --site https://www.example.com --langs en,ko --out ./entity-out

# After approval: IndexNow for changed URLs (dry run first; key in INDEXNOW_KEY)
python3 scripts/indexnow_submit.py --host www.example.com --urls-file changed.txt          # dry run
python3 scripts/indexnow_submit.py --host www.example.com --urls-file changed.txt --apply

# Search Console sitemaps via a service account (GOOGLE_APPLICATION_CREDENTIALS)
python3 scripts/gsc_sitemaps.py list --site sc-domain:example.com
python3 scripts/gsc_sitemaps.py submit --site sc-domain:example.com --sitemap https://www.example.com/sitemap.xml --apply
```

`centres.csv` columns: `code,area,lat,lng` (e.g. `A,office,37.5665,126.9780`).
`canonical.json` example: `{"name": "<Firm> <Office>", "building": "<Building>", "phone": ["1500-0000", "02-000-0000"], "website": "https://www.example.com/"}`.

## Safety principles

- **Read-only by default.** Live checks never log in with typed passwords, submit forms, post, review, claim listings or accept terms.
- **Approval before changes.** Code, CMS content and listing edits are applied only after the owner approves that exact change, then verified on the public URL.
- **No fake reviews.** The skill never writes, buys, seeds or deletes reviews, and never adds Review/AggregateRating markup for self-selected testimonials.
- **No CAPTCHA solving.** On a CAPTCHA or empty result page it stops that engine and marks the rest NOT VERIFIED. Search queries are spaced 20–30 s apart.
- **No secrets in output.** API keys, IndexNow keys and service-account files stay in environment variables and are never printed in full.
- **Dry run by default.** Scripts that submit to search engines do nothing until `--apply` is given, and the skill asks before using it.
- **Regulated industries.** Content changes for law, medicine and finance need human approval; claims must be verifiable.
- **Wikis by the rules.** Wikidata, Wikipedia and Namuwiki work is done by a named person with disclosed conflict of interest, through talk-page requests where required; no paid wiki or "knowledge panel" services, no sock puppets, no removing criticism.

## Contributing

Add new helpers under `scripts/` following [`scripts/README.md`](seo-geo-audit-fix/scripts/README.md): one job per script, standard library preferred, read-only unless an explicit `--apply` flag is given, secrets only from environment variables. Then add a row to the scripts table and one line in `SKILL.md` → "Bundled scripts and templates".

Corrections to the reference rules are welcome; please cite a primary source (official documentation or a statement by the search engine) for any rule you change, add it to `references/sources.md` with the date you verified it, and label rules that come from your own experience as "(field experience)".

## Sources

The official documentation behind the rules (Google Search Central, Search Console, Business Profile, web.dev, sitemaps.org, RFC 9309, schema.org, Bing/IndexNow, Naver Search Advisor, Daum, Kakao, AI-crawler docs, llms.txt, Wikidata/Wikipedia policies, the Knowledge Graph API, the FTC review rule, the Korean Bar Association's advertising regulation) is listed in [`references/sources.md`](seo-geo-audit-fix/references/sources.md), with the date each URL was last verified.

## Author

Shohrux Muhiddiyn — Senior Software Developer

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 Shohrux Muhiddiyn.
