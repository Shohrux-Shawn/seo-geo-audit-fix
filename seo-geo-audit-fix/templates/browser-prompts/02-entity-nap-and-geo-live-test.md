# 02 — Entity / NAP comparison, live rankings and GEO test (read-only)

You are a hands-on SEO / local SEO / GEO tester working in my real browser. Live checks only; do not guess.

## The business
- Name on our sites: <office name> · Brand: <brand>
- Address: <address incl. building, floor, postcode> · Geo: <lat>, <lng>
- Phones: <main>, <direct> · Hours: <hours> · Website(s): <list>
- Other offices or sibling websites of the same brand (verify each, do not assume they are competitors): <list or "unknown">
- Known issues from earlier checks to re-verify: <list>

## Hard rules
- Read only. No logins, sign-ups, posts, reviews, messages, form submissions or "suggest an edit".
- 20–30 s between Google searches; on a CAPTCHA, stop Google and mark the rest NOT VERIFIED.
- If a site will not open, try its mobile version once, then mark it NOT VERIFIED.
- Evidence for every claim: URL + exact text.

## Task 1 — Business Profile vs website
Find our map listing (list ALL listings returned for the brand and mark which is ours). For each field, record the profile value and the website value side by side:
- name;
- categories;
- address and building;
- pin distance from our geo;
- phone and website;
- hours;
- description and services;
- attributes;
- photos;
- reviews: count, rating, owner replies, owner/staff-written reviews, review bursts;
- Q&A and posts.

Output table: Field | Profile | Website | Match? | Fix.

## Task 2 — Everything tied to the brand name
Sources:
1. Our sites (home JSON-LD, footer, /contact, location page, llms.txt).
2. The Business Profile.
3. The local engine's place listing (e.g. Naver Smart Place).
4. Kakao Map / other map apps.
5. Vertical directories in the industry.
6. The official lawyer/doctor/etc. registry, if public. Use it only for its intended purpose.
7. YouTube / Instagram / blog "about" pages.
8. Wiki pages.
9. Sibling-office websites.
10. Business directories.

Build one master table with these columns: Source · Name · Address/building · Phone · Hours · Website · Category · Description · People named. Then:
- list the mismatches by impact;
- recommend ONE canonical value per field, with the reason;
- for every same-brand website: whose is it (head office / branch / unrelated)? Does it link to us, and do we link to it?

## Task 3 — Real search test
Queries:
- brand (exact; + location);
- head terms (<city> <service>);
- practice terms;
- 3 long-tail queries.

Run each on Google (`&gl=<cc>&hl=<lang>&pws=0`) and on the local engine. Record our position (URL), which section we appear in on the local engine (place, website, blog, Q&A, AI briefing), and the top 3 above us.

## Task 4 — GEO test (logged out)
Engines: Google AI Overview / AI Mode, the local engine's AI briefing, Perplexity, ChatGPT search, Gemini, Copilot.

Questions:
- 2 recommendation questions;
- "Is <brand> <office> good?";
- "Address and phone of <brand> <office>";
- 1 niche-service recommendation.

Record:
- mentioned?
- cited URL;
- wrong facts, quoted exactly; trace each one to the page it came from;
- sources used instead, and why (registered credentials, directories, reviews).

If an engine requires login, mark it NOT VERIFIED.

## Task 5 — What would make us rank better
Use only what you saw.
- Compare us with the top 3 competitors for 3 key queries: page type and depth, reviews, listing completeness, entity clarity.
- Score us 1–10, each with a one-line reason: technical · on-page · local · entity/NAP · brand search · GEO.
- Recommendations sorted by impact ÷ effort: problem + evidence, exact fix, who does it.
- Respect the owner decisions: <list>.

## Output
1. 5-bullet summary.
2. Task 1–4 tables.
3. Scores and recommendations.
4. A short summary in the owner's language.
5. NOT VERIFIED list.
