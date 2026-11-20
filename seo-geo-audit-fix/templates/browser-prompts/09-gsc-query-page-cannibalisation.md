# 09 — Search Console query → page table for cross-domain cannibalisation (read-only)

Use before any change meant to stop two of your own sites (main site and a topic satellite, or two satellites) competing for the same queries. Ranking samples show one query at a time; this table shows every query each page actually wins, so a canonical, redirect or copy change does not throw away long-tail traffic no one sampled. Needs owner or full-user access to every Search Console property.

```
TASK: Read-only data collection in Google Search Console. Do not change anything.

PROPERTIES (open each one):
- <https://www.example.com>  (main site)
- <https://www.example-topic1.com>
- <https://www.example-topic2.com>
  (list every site of the network; Domain properties are fine)

HEAD TERMS (one filter at a time; use the local language):
- <city> <topic1>
- <city> <topic2>
- <district> <service>
  (one or two words per practice/satellite topic, plus brand + district)

STEPS, for each property:
1. Performance → Search results. Date range: last 3 months. Search type: Web.
2. Add filter Query → "Queries containing" → the first head term.
3. Queries tab: note the top 5 queries by impressions.
4. For each of those queries: click it, open the Pages tab, record every page with impressions: query | page URL | clicks | impressions | CTR | average position. Remove the query filter again.
5. Repeat steps 2–4 for every head term, then for the next property.

RULES
- If a login screen appears, stop and ask me to log in. Never type a password.
- Never click "Request indexing", "Validate fix", "Submit", "Remove", or any setting.
- Do not export to Google Sheets or share anything; copy numbers into your report.
- If a property is missing from the account, write "NO ACCESS: <property>" and continue.
- If a query shows "no data" or anonymised rows only, say so instead of guessing.

OUTPUT
1. One table per property: property | head term | query | page | clicks | impressions | CTR | position.
2. "Overlap" list: every query where two or more of OUR properties both have impressions. For each: the query, each URL with clicks/impressions/position, and which one wins today.
3. "Satellite absent" list: head-term queries where the topic satellite has no row but the main site does.
4. NOT VERIFIED: anything you could not open or read.
```

How to use the result:
- Act only on the overlap clusters, and only after the owner picks one target URL per cluster.
- Prefer, in order: internal links and anchor text pointing to the target, then trimming the competing page's copy so it no longer answers the same intent, and only then a canonical or redirect. A canonical is a hint across domains and moves every query the page wins, not just the head term.
- Re-run this prompt 4–6 weeks after the change and compare clicks per cluster, not only positions.
