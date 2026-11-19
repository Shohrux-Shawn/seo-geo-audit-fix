# 08 — Post-fix re-measure: technical, rankings, local engine, AI answers (read-only, one session)

Use after a round of fixes (or monthly) to measure the whole network in one pass: structured data and speed per template, positions for the head terms, the local engine's sections, and what AI engines say. Shorter than 01 + 02 together; run 01/02 for a first audit.

```
TASK: Read-only SEO and GEO (AI search) re-measure of our websites from a real browser. Measure and report only. Do not change anything, do not submit forms, do not request indexing, do not edit any account setting.

THE SITES
- Main: <https://www.example.com>
- <topic>: <https://www.example-topic.com>
  (list every site of the network)
Business facts that must match everywhere: <legal name> · <full address incl. building name and floor> · <one main phone>.

RULES
- If a login screen appears (Search Console, local webmaster tools, Bing, an AI engine), stop and ask me to log in. Never type a password. Never solve a CAPTCHA.
- Never click "Request indexing", "Validate fix", "Submit", or anything that changes data.
- Note whether you were logged in to each engine; prefer a logged-out view where possible.
- Quote numbers and wrong facts exactly; give the URL for every finding.
- If the browser cannot open a site (some local engines block extensions), say so and use another read-only fetch with a local location; label those results as fetched, not seen.

PART 1 — Technical spot checks (each site: home + one record page such as a case result + one article)
1. Rich Results Test: home and one record page per site. Record detected items, errors, warnings, and open every "non-critical issue".
2. validator.schema.org: main home, one Q&A article, one practice/hub page. Record types and errors/warnings. (FAQPage is not shown by the Rich Results Test for non-government/health sites; validate it here.)
3. PageSpeed Insights, mobile: main home and the heaviest satellite home. Record Performance, LCP, CLS, INP, total page weight, and the top 3 opportunities. Name the single largest file.
4. Open /llms.txt and two of its Markdown copies (e.g. /index.md, /about.md). Confirm 200 and that the text matches the visible page; list blocks that are missing (client-rendered widgets often are).
5. On 3 record pages: document images load (no broken image); no identifying reference numbers in visible text.

PART 2 — Google rankings (google.com, gl=<cc>, hl=<lang>, pws=0; pages 1–3)
Queries: <city> <service> and <district> <service> for every practice/satellite topic, the brand + district, and 3 long-tail queries that earlier showed positions 4–10.
For each: our best URL and position (or "not in top 30"), which of our sites ranks, top 3 competitors, map-pack position, AI Overview present? cites us?

PART 3 — Local engine (e.g. Naver)
Same queries. Record the section that shows us (place, web documents, blog, Q&A, video, AI briefing) and the position inside it; which place listing appears (if there are several for the business); which domain the AI briefing cites.

PART 4 — AI answer engines (ChatGPT with search, Perplexity, Gemini, Copilot, the local engine's AI)
Ask in the local language:
1. "<district> <service> lawyer recommendation"
2. "a firm good at <service> in <city>"
3. "<brand> address and phone number"
4. "what kind of firm is <brand>? is it trustworthy?"
5. one informational question our article answers
For each: mentioned? cited URL? wrong or unverifiable facts (quote exactly — phone, building name, founding year, people's titles)? which sources were used instead?

PART 5 — One competitor per head term
For the top competitor page: page type, length, section structure, structured data — one line each. Do not copy their content.

REPORT (one message)
1. Summary: biggest risk, fastest win, where we rank, fact (NAP) accuracy, AI visibility — 5 bullets.
2. Tables for Parts 1–4; notes for Part 5.
3. NOT VERIFIED: what could not be checked and why.
Include date/time, location setting, logged-in state per engine.
```

## What this run typically finds (field experience, 2026-11)
- AI engines quote a **second phone number** if the structured data publishes one (`contactPoint`), and a **building name** from the map profile if it differs from the website.
- Several local-engine place listings for one office, each with its own number, split the brand and confuse AI answers.
- Autoplay background videos with `preload="auto"` (16–33 MB) make page weight 24–69 MB and lab LCP over a minute.
- Satellites can be absent for their own head term while the main site's location/practice pages rank — a cannibalisation signal.
- AI engines state unverifiable biography facts (founding year, former offices, credentials); list them for the owner to confirm, never "fix" them from the AI text.
