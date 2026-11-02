# 01 — Site / network audit (read-only)

You are an expert in technical SEO, local SEO and GEO (visibility in AI answers: Google AI Overviews, ChatGPT, Perplexity, Gemini, Copilot, and local engines such as Naver AI Briefing). Work in my real browser. Live checks only; do not guess.

## Context
- Business: <business name> (<industry>)
- Main office: <full address> · Phone: <main phone> (direct line <direct phone>, if any) · Geo in JSON-LD: <lat>, <lng>
- Hours: <hours> · Paid/free consultations or quotes: <policy> · Wording the business never uses: <e.g. "free", "24 hours">
- Entity focus: <the firm/brand, not an individual>
- Languages: <default language + alternates/hreflang set>

## Sites (check every one; canonical host = www unless stated)
| # | Site | Role | Target queries (local language) |
|---|---|---|---|
| 1 | https://www.example.com | main | <city> <service>, <district> <service>, <brand> |
| 2 | https://www.example-<topic>.com | satellite: <topic> | <city> <topic> <provider> |

There are no other sites in the network. Do not audit any other domain. If a listed domain does not resolve, report it and continue.

## Hard rules
- Read only. No logins with typed passwords, no forms, no posting.
- Space search-engine queries 20–30 s apart. On a CAPTCHA, stop that engine and mark the rest NOT VERIFIED; do not solve it.
- Report test conditions: time, signed in or not, the location the engine says it uses.
- Evidence for every claim (URL + exact text or numbers). Unchecked = NOT VERIFIED.

## Checks per site
**A. Reachability and indexing**
- HTTPS and redirects (http/https × apex/www); the target is one 301 hop.
- `site:` counts on Google (and the local engine).
- robots.txt (AI crawler access), sitemap validity, llms.txt.

**B. Location signals**
- Target queries on Google (`https://www.google.com/search?q=QUERY&gl=<cc>&hl=<lang>&pws=0`) and on the local engine: our position, competitors above us.
- The same services with other cities.
- JSON-LD: name, address, phone and geo exactly as in Context.
- NAP identical across sites, footer, contact page and map listings.
- Each satellite's own location signals (title, H1, description, JSON-LD).

**C. Page quality**
- Title, description, H1, canonical, OG image, `lang`, hreflang reciprocity.
- Duplicates across sites; topic isolation per satellite; UTM on internal links.
- Rich Results Test / validator.schema.org on a sample of templates.
- Core Web Vitals (PageSpeed Insights, mobile); broken links, soft 404s, redirect chains, mixed content.

**D. GEO**
- 3–5 AI-style questions (recommendation, "is <brand> good?", "address and phone of <brand>"), logged out.
- Is the brand mentioned or cited? Which URL? Any wrong facts (quote them)?
- Is content quotable (FAQ blocks, clear Q&A, author info, dates)?

**E. Off-site**
- Mentions on blogs, Q&A platforms, directories, video and news, and whether they link to the right domain.
- Natural cross-linking between the sites.

## Output
1. Summary table per site: Live? · Indexed (Google / local engine) · Best position · Location logic OK? (✅/⚠️/❌) · Score /10.
2. Per-site details with evidence.
3. Problems by priority (Critical / High / Medium / Low): problem, why it matters, exact fix.
4. Missing things to add.
5. Top 10 actions for the next 2 weeks.
6. NOT VERIFIED list with reasons.

Constraints for recommendations (owner decisions; do not contradict):
- <e.g. keep existing statistics on page X>;
- <e.g. keep region wording>;
- no fake or seeded reviews and no review schema for self-written testimonials;
- no individual's name in titles/H1/meta if the entity is the firm.
