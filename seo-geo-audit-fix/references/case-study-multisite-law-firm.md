# Case study: a multi-site law-firm network

A worked, anonymised example of a multi-site professional-services network: a Korean law firm's
branch office running a main site plus 6 practice-area satellites. Use it in Step 0 as a precedent
for what to ask, what to record, and which traps to expect. Names, domains, phone numbers, addresses
and people are replaced with placeholders; numbers are real but anonymised.

Timeline is given as relative months: **month 1** = the CMS migration that started the project,
**month 7** = the latest local/GEO audit.

## Contents
1. Sites and roles
2. Architecture summary
3. Entity and NAP situation
4. Owner decisions (examples of what to record)
5. Publishing rules
6. Deploy rules
7. Measured state (snapshots)
8. What worked, what didn't
9. Open items at the end of the period
10. How to reuse this case

---

## 1. Sites and roles

| Site | Role | Notes |
|---|---|---|
| www.example.com | Main firm site | Migrated from WordPress in month 1. Region hub + region pages + region × practice pages; English pages from month 5; an AI legal-chat page added in month 6. |
| www.example-divorce.com | Divorce / family satellite | First satellite; the original template. |
| www.example-criminal.com | Criminal-defence satellite | Healthiest index rate in months 4–5. |
| www.example-sexcrime.com | Sex-crime defence satellite | Weakest; Bing/Copilot sensitive-topic filter. |
| www.example-estate.com | Real-estate satellite | Live in month 3. |
| www.example-civil.com | Civil / damages satellite | First satellite that needed new backend enum values before launch. |
| www.example-school.com | School-violence / juvenile satellite | Live in month 6. |
| Planned, never built | six more practice domains | Existed only as enum values and old plan tables. **They were listed in an audit prompt in month 6 and produced six false "site down" findings.** Resolve every domain before auditing it. |

Languages: ko (root, unprefixed) + en, ja, zh, ru, vi, uz under `/{lang}/`; two more languages prepared but held back until a native reviewer was available.

Sources: (field experience)

## 2. Architecture summary

- Next.js (Pages Router) frontends: main site in its own repo; satellites in a Turborepo monorepo (`apps/<site>` + shared `packages/ui`, `packages/config`, `packages/graphql`). One NestJS GraphQL backend, MongoDB, Docker Compose behind nginx on one small VPS.
- Content isolation via a `siteOrigin` field on each article and case record; the backend overrides any client-supplied origin with the one in the editor's token. A satellite record opened on the main domain → 301 to the satellite.
- One shared NAP constant for all JSON-LD; a per-site config (practice, slug, colours, verification tokens, nav items to hide).
- Region registry: 251 entries kept byte-identical between repos; 75 gated into sitemaps and `areaServed`. Footer capped at 24 regions + a hub link. Main site: region × practice pages for tier-1 regions only; satellites: none (a satellite already *is* one practice).
- Content types in production: Article (by category: legal info, Q&A, case analysis, insights, press) and Case (anonymised results). Four further content collections were built but never used — build only what the publishing plan needs.
- Publishing pipeline on a desktop PC: platform Q&A exports and topic banks → LLM writing → QC script → queue → two daily release windows → 1 item per 10 min through the CMS GraphQL API; IndexNow ping on create, update and delete.
- Sitemaps: the main `/sitemap.xml` is an index of 18 files (≈3,300 URLs in month 6); it returns 503 when data is unavailable.

Sources: (field experience)

## 3. Entity and NAP situation

- The entity is a branch office of a multi-office firm (an ordinary law-firm corporation, not the limited-liability form). Road address with building name and floor.
- **Building-name conflict:** the site and schema used one building name, Kakao Map showed another for the same address (Kakao uses its own address database). Fix: pick one and use it everywhere.
- Phones: one main number (`1500-0000`) for all offices on the firm's own pages, schema and managed profiles; the branch's direct line (`02-000-0000`) shown in addition. Office-local numbers on Kakao/Naver were not copied to the firm's pages.
- Kakao listed about 10 offices of the firm plus one duplicate; which offices were active and who sat where was still open in month 5.
- The principal lawyer held two registered specialties; only those fields may carry "certified by the Korean Bar Association" wording. Years of experience must be stated identically everywhere (an older, different figure was still on some pages).
- Hours were inconsistent: the site said one schedule (10:00–20:00 daily), the listings another (09:00–18:00); an official value was still undecided in month 5.

Lesson: write the fact sheet *before* the audit and mark every unresolved field as an open owner decision.

Sources: [Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization) · [Guidelines for representing your business](https://support.google.com/business/answer/3038177) · situation: (field experience)

## 4. Owner decisions (examples of what to record)

These are the kinds of decisions that override generic best practice. Record each with its date and, where relevant, its regulatory risk.

| When | Decision (generic form) |
|---|---|
| Month 4 | Volume raised only by measurement; written rollback trigger: "Discovered – not indexed" > 10%. |
| Month 5 | Consultations are **paid**, never free, not 24 h: no "free" / "24 hours" / "365 days" in titles, meta, schema or GBP. CTA: "When you request a consultation, a staff member will call you and explain the consultation fee." |
| Month 5 | Phone policy: one main number for every office; the branch also shows its direct line. |
| Month 5 | Plain "<field> specialist lawyer" allowed in all practised fields; "certified by the Korean Bar Association" only for the registered fields. Existing "<field> Specialist Centre" names kept (the lawyer's call). |
| Month 5 | No lawyer-name prefix or brand in article titles; titles ≤ 25 Korean characters; meta ≤ 80; ` - <brand>` suffix only where a brand is used. |
| Month 5 | Foreign-reader content: one topic published in all site languages at once, source written in English, legal review memo in Korean; no Korean version for that set. |
| Month 6 | Don't repeat the principal lawyer's name heavily across sites; put the firm name forward. |
| Month 6 | For SEO/GEO work: fix code bugs and SEO/GEO problems only; **existing site content stays**, including existing stat tiles (case counts, satisfaction %) on strength pages and repeated region / "lawyer" / "law firm" / "recommended" wording. Record such decisions and their regulatory risk once, and list anything they block under "Skipped by owner decision". |

Sources: [Korean Bar Association: Regulations on Attorney Advertising](https://www.koreanbar.or.kr/pages/board/law_view.asp?category=3&page=1&searchstr=&searchtype=&seq=14402&teamcode=&types=6) · decisions: (field experience)

## 5. Publishing rules

- Drip only, inside working hours (two release windows, 1 item per 10 min); no backlog dumps.
- Volume history: 32/day → 40/day (asymmetric: healthiest sites got more, weak ones were frozen) → 46/day across 6 sites → 10 per site per day across 7 sites = 70/day, with the queue kept 7 days ahead (months 4–6).
- One topic, one domain; duplicate check across the network; per-language duplicate check for international content.
- Statute numbers only from a local statute cache; pending amendments not cited; a `[verification needed]` marker blocks publishing.
- No invented success stories or testimonials — only real anonymised judgments supplied by lawyers.
- Byline "Written and reviewed by <attorney name>, <date>" and an AI-process disclosure in the signature; certification wording only under the registered lawyer's byline.
- Q&A (KnowledgeiN-style) articles keep the original-question block and have no FAQ section (the generator drops it, QC blocks it).
- Answers on legal Q&A/directory platforms and Naver KnowledgeiN follow a separate platform-answer prompt, not the site-article rules.

Sources: [Spam policies (scaled content abuse)](https://developers.google.com/search/docs/essentials/spam-policies) · rules: (field experience)

## 6. Deploy rules

- Satellites deploy **one at a time** with a per-service deploy script (fetch, check out master, `reset --hard origin/master`, rebuild that service only; ~110 s in-container build; a few minutes of 502 are normal). Never rebuild all services at once (OOM on a small VPS). Backend first when frontends depend on it.
- Branch flow: develop → master; the server only ever pulls master.
- Before reset/pull on the server: `git status --short` empty; env file (API URL) checked before and after — a deploy once overwrote production env values with localhost.
- Deploy reviewed commits by id when newer unreviewed commits exist.
- **Runtime content must not live in git-tracked paths** (admin edits stored in `data/*.json` were wiped by `reset --hard` in month 6).
- Review agent diffs with `--ignore-space-at-eol` and reject CRLF rewrites.

Sources: (field experience) · recipes: `implementation-playbook.md` §1 and §11

## 7. Measured state (snapshots)

| When | Measure | Values |
|---|---|---|
| Month 4 | GSC index % / Discovered | main 43.6% / 514 · criminal 97.4% / 3 · divorce 87.6% / 33 · estate 93.3% / 4 · sex-crime 67.1% / 133 |
| Month 4 | Bing 30 d clicks / impressions / Copilot citations | network total 52 / 818 / 493 (main site 407 citations); sex-crime site 3 impressions |
| Month 5 (3-month window) | GSC avg position / CTR | main 12.1 / 2.7% · criminal 16.4 / 4.8% · estate 19.1 / 1.4% · divorce 27.6 / 1.2% · sex-crime 40.6 / 3.5% |
| Month 5 | Query split | long-tail questions at 3–6 with clicks; "<city> + practice + lawyer" at 40–78 with 0 clicks; low-competition cities for real estate at 7–8 |
| Month 5 | English pages | 5–6 consultation leads from Google organic within a week of launch |
| Month 6 | GSC buckets (main) | Indexed 2,460; Discovered 819; 404 864; redirect 748; noindex 136; duplicate 46 |
| Month 6 | Naver (main) | clicks 4.6K/30 d (+31.6%), impressions 350K, indexed 2.3K flat for weeks, brand-query CTR 2.8%, no RSS submitted |
| Month 7 | Local | GBP in a generic category without hours; reviews filtered 8 → 6; satellites cannibalised by the main site's `/location` pages; sibling offices outranked the branch for the brand |

Sources: (field experience) — measured in Search Console, Bing Webmaster Tools and Naver Search Advisor

## 8. What worked, what didn't

**Worked**
- Long-tail Q&A content: page 1 on low-competition questions on Google and #1 on long conversational queries on Bing/Copilot (month 4).
- Measurement-first volume decisions with a pre-written rollback trigger (month 4).
- 410 for deleted records, one-hop 308s for migration URLs.
- Rewriting 52 templated titles instead of lengthening 173 articles (month 5).
- Single-source locale list + build assert; 503 sitemaps on data failure; a runtime link gate (6 sites to 0 broken links, month 5).
- A crawl-path fix wave (pagination, archive, related links, SSR blocks, sitemap index) for the 819-URL Discovered bucket (month 6).
- English core pages producing leads within a week (month 5).

**Didn't work / caused damage**
- Bulk batches (485 pages in 3.5 h, month 4).
- A fixed title prefix on every article; a templated Q&A title suffix.
- Two separate lists for "open" and "in sitemap" (1,386 URLs stuck).
- A view counter moving lastmod; an empty-200 sitemap on API failure.
- One NAP for a 10-office firm; offices pointing to different websites.
- False claims (free / 24 h) in site templates, outside the content QC's reach.
- A footer listing every region on every page (replaced by a 24-region cap + hub, month 3).
- An admin CMS writing into git-tracked files; an imported legal page still carrying a competitor firm's name.

Sources: (field experience)

## 9. Open items at the end of the period

- Satellite merge decision (fold the weakest satellites into the main site) — a quarterly business decision.
- Location strategy: pages for the ~10 real office cities with real NAP and courts; office-less regions → merge or noindex; court table awaiting lawyer verification.
- GBP / Smart Place / Kakao alignment for every real office; one name template; one hours policy; duplicate listing merge.
- RSS for every site + Naver submission; a weekly GSC API report.
- `translationGroup` linking for multilingual articles before scaling them.
- Thumbnail rule (text-free vs text-on-image) never decided.
- Stat tiles kept by owner decision; flag their regulatory basis once to the lawyer responsible for advertising.
- IndexNow consumers: verified on 2026-11-02 that Naver participates (alongside Bing, Yandex, Seznam, Yep and others); Google does not.

Sources: [IndexNow participants (checked 2026-11-02)](https://www.indexnow.org/searchengines.json) · other items: (field experience)

## 10. How to reuse this case

- Copy the **shape** of sections 1–6 into your own `seo-geo-facts.md`: sites with roles and launch dates, architecture, entity conflicts, owner decisions with dates, publishing and deploy rules.
- Use section 7 as a baseline template: same measures, same engines, dated, so the next audit can compare.
- Use section 8 as a pre-mortem checklist when a client wants to scale content or add satellites.
- Never copy this case's numbers into another client's report; they are illustrations, not benchmarks.

Sources: (field experience)
