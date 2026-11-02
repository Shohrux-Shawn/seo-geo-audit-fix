# Knowledge base — core SEO + GEO rules

Distilled from research notes, real audits and measured incidents (2026-08 … 2026-10).
Generalised so they apply to any site; Korean-market specifics are in `korea-search.md`.
Each section ends with its sources (`sources.md`). Rules marked **(field experience)** come from the
author's audits; **(third-party study)** marks industry studies that were not re-verified here;
statements by Google staff in podcasts or forums are attributed by name.

## Contents
1. Quality drives crawling and indexing
2. Crawl and index mechanics
3. On-page: titles, descriptions, headings, URLs
4. Structured data and entity
5. E-E-A-T for YMYL (legal, medical, finance)
6. Internal linking and crawl paths
7. Links and citations
8. GEO: being quoted by AI answers
9. Measurement and decision rules

---

## 1. Quality drives crawling and indexing

| Rule | Why |
|---|---|
| Treat quality as the main lever for crawl *and* index decisions, not volume or ping tricks. | Gary Illyes (Google, *Search Off the Record* podcast): quality is "the biggest driver for most of the indexing and crawling decisions". |
| The crawl of a *new* page depends on the quality of the site's *previous* pages. | Google's scheduler predicts new-page quality from the site's history (same podcast). |
| Google learns quality per URL pattern (`/articles/*`, `/location/*`). A weak pattern gets crawled less. | Removing or moving low-quality sections raised the crawl of the rest. (field experience) |
| Low-quality pages hurt the whole site, not only themselves. | John Mueller (Google), on law-firm sites: quality algorithms may "assume the whole site is like that". The helpful-content guidance evaluates content site-wide. |
| "Sandbox" / "honeymoon" is not an algorithm. Ignore early position swings on a new site. | Mueller: with few signals Google guesses, then corrects when real signals arrive. |

Sources: [Creating helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) · [Crawl budget management](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget) · podcast and forum statements as attributed above

## 2. Crawl and index mechanics

- **Crawl budget is not your problem below ~1M URLs.** Google's crawl-budget guide targets sites with 1M+ pages changing about weekly, or 10k+ pages changing daily. For small and medium sites the bottleneck is *index demand* (quality, relevance). If new pages are crawled the day they are published, stop worrying about budget.
- **"Discovered – currently not indexed"** = Google found the URL but has not crawled it yet. Fix with crawl paths, internal links, external interest and quality — not more pages.
- **"Crawled – currently not indexed"** = fetched, not indexed (yet). Usually thin, duplicate or low-value. Different fix from "Discovered"; resubmitting is not needed.
- Google treats **404 and 410 the same**; both are fine for removed content. **Soft 404s** (an error or empty page returning 200, or a redirect of unknown paths to `/`) waste crawling. Deleted → 410; unknown → 404; never redirect everything to `/`.
- Server speed and 5xx/429 lower crawl *capacity*; crawlers back off after repeated 5xx.
- Publishing time of day is not a ranking or indexing factor. (field experience)
- There is no general "submit URL" API for Google: the Indexing API is only for `JobPosting` and `BroadcastEvent` pages. Levers are sitemap freshness (real `lastmod`), internal links and site health. IndexNow reaches Bing, Naver, Yandex and other participants, not Google (see `sitemaps-and-submission.md` §6.3).
- `robots.txt` blocking ≠ `noindex`. A blocked URL can stay indexed without content. Use `noindex` (or 404/410) to remove, and keep the URL crawlable so the engine sees it.

Sources: [Crawl budget management](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget) · [Page indexing report](https://support.google.com/webmasters/answer/7440203) · [HTTP status codes and soft 404s](https://developers.google.com/search/docs/crawling-indexing/http-network-errors) · [Indexing API quickstart](https://developers.google.com/search/apis/indexing-api/v3/quickstart) · [Block indexing with noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing) · [IndexNow participants](https://www.indexnow.org/searchengines.json)

## 3. On-page: titles, descriptions, headings, URLs

**Title (as of 2026-09; measured on English sites, converted by pixel width for Korean)**

| Rule | Why |
|---|---|
| Desktop ~600 px ≈ **20–25 Korean (Hangul) characters** (mobile ~20); Latin 40–60 characters. | A Hangul character is ~22–24 px, a Latin character ~7–8 px. Titles of 30+ Hangul characters were almost always rewritten. (third-party study: Zyppy, 80,959 titles) |
| Put the query phrase in the **first 15–18 characters**. | Truncation hides the end. |
| No brand in article titles; brand only on home/location pages, after ` - `. | A 423-title A/B test (2026): the brand lowered CTR on non-brand queries. (field experience) |
| Use ` - `, not ` \| `. | Google replaced `\|` far more often than `-` (41% vs 20%). (third-party study) |
| No trailing year; numerals or brackets only when the content really has them (e.g. "4 steps", "[2026 amendment]"). | Year hurt CTR; numerals helped only when true. (field experience) |
| No boilerplate prefix on every title (e.g. `<Name> [keyword] …`). | Google's title-link guidance warns against boilerplate titles that vary by one item; formulaic titles were the top risk factor in a 220-site study. (third-party study: Lily Ray) |
| Cut at a word boundary, never mid-word, no "…". | Mid-word cuts look broken and get rewritten. |
| Keep a separate SEO title (≤ 25 Hangul characters) from the on-page H1 (can be longer, two-part "main title - subtitle"). Drop any site-wide suffix on article pages, or a 25-character title renders as ~38. | The H1 and the result title have different jobs. |

Older view (an earlier internal guideline, before 2026-09): titles 50–60 characters, meta 120–160. Superseded for Korean.

**Meta description:** ≤ 80 Hangul characters (~920 px ≈ 75–85 Hangul), query + benefit in the first sentence. The old 140–160 rule was the English rule applied to Korean. (field experience)

**Headings:** one H1 = the real headline or "<region> <entity> <topic>". Not an English slogan, not a section label like "Success stories". H2s as questions or sentences, each with at least one concrete value (deadline, amount, statute, step).

**URLs:** keyword slugs only for *new* pages (the correlation is small but the change is cheap). Never change published URLs retroactively (index and link loss). Korean-language slugs are fine and help Naver.

**Templates at scale:** measure similarity *with names neutralised* (replace the city/region with `<R>`) before opening many template pages. Raw Jaccard 0.39 became 0.89 once names were neutralised. (field experience)

Sources: [Influencing title links](https://developers.google.com/search/docs/appearance/title-link) · implementation: `implementation-playbook.md` §4 · length and CTR figures: (third-party study) / (field experience) as marked

## 4. Structured data and entity

- **`LegalService`** for law offices (schema.org `Attorney` is superseded by `LegalService`). One LegalService per real office page, identical NAP.
- One canonical organisation `@id`; other sites and pages reference it (`parentOrganization`, `worksFor`, `author` → `Person`).
- **NAP from one source of truth** (a shared config constant used by every JSON-LD block). Never hand-write NAP per app: a copied, hand-written schema drifted (no hours, and a false "free consultation" price range). (field experience)
- **No Review/AggregateRating stars for self-controlled reviews.** Google: if the entity controls the reviews about itself, its pages using LocalBusiness or Organization markup are ineligible for review snippets; misleading markup also risks a manual action.
- **FAQ rich results are gone:** restricted since 2023, deprecated on 2026-05-08 (no longer shown since 2026-05-07), documentation removed 2026-06-15. Keep a *visible* FAQ block where it helps readers (it answers long-tail queries and AI systems extract it); keep at most one FAQPage emitter; don't spend effort on it.
- `areaServed` only for regions you actually serve and publish pages for.
- Breadcrumbs: still shown, cheap — keep.
- Article + `author` Person has no direct CTR effect but supports the E-E-A-T picture.
- Entity graph: keep a table of every official profile (place listings, directories, video, social, sibling sites) with sameAs ✓, NAP match ✓, last update. Update the table and `sameAs` the same day a new channel opens.
- Do not buy "knowledge panel" services or push wiki entries for a non-notable entity; both backfire. (field experience)
- Code: `implementation-playbook.md` §5.

Sources: [General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) · [LocalBusiness](https://developers.google.com/search/docs/appearance/structured-data/local-business) · [Organization](https://developers.google.com/search/docs/appearance/structured-data/organization) · [Review snippets](https://developers.google.com/search/docs/appearance/structured-data/review-snippet) · [Search documentation updates (FAQ)](https://developers.google.com/search/updates) · [BreadcrumbList](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb) · [schema.org Attorney](https://schema.org/Attorney) · [schema.org LegalService](https://schema.org/LegalService)

## 5. E-E-A-T for YMYL (legal, medical, finance)

| Signal | How |
|---|---|
| Named byline | A real professional per article, linked to a bio page (registration number, bar association, office, `sameAs` directory profiles). One name on 14,600 articles is itself a signal; rotate real authors where true. |
| Reviewed-by + date | "Written and reviewed by <attorney name>, <date>" and a last-reviewed date. Recency is a trust signal. |
| Disclosed process | Google's helpful-content guidance asks whether the use of automation is disclosed. Disclose the *process* on an editorial-policy page. Do **not** advertise AI use as a selling point (Korean attorney-advertising rules restrict that — see `content-scale-and-quality.md` §9). |
| First-hand practice observation | One or two "what we often see in practice" observations per article. Never invent client stories or case results. |
| Primary sources | Statutes and case numbers checked against a local verified copy at write time. Unverified number → write only the law's name. |
| Original element | Each article carries one thing a generic AI answer lacks: anonymised case detail, a fee/timeline table, local court or procedure. |
| "Fluent nothing" filter | Delete paragraphs that only say "it depends / consult an expert"; replace them with values, steps, timing. |

Sources: [Creating helpful content (who, how, why; disclosing automation)](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) · byline and review practices: (field experience)

## 6. Internal linking and crawl paths

- **Everything that must be indexed or followed is in the initial HTML as a real `<a href>`.** Client-only blocks and button/JS pagination are invisible (to Naver even more than to Google). The biggest "Discovered" bucket in a real audit (819 URLs) was a crawl-path problem, not a content problem. (field experience)
- Pagination: `<a href="?page=N">`, self-canonical per page, `?page=1` → 301/308 to the bare URL, beyond the last page → 404 with `no-store`.
- Archive pages (section × month) so every item is ≤ 3 clicks from home; footer link to the archive.
- Related block on every detail page (~8 same-topic links); hub → item links on thin hubs.
- **Internal links target the final URL.** A link that redirects counts as a defect in a link gate.
- Link counts: URLs with 40–44 internal links got ~4× the clicks of those with 0–4; ≥ 1 exact-match anchor → ≥ 5×; plateau above 45–50 (third-party study: Zyppy, 23M links). Target **20–45 inbound internal links per money page**, fed by daily articles: 1 exact-match + 1–2 variant anchors per article.
- Hub-and-spoke: a few deep hub pages (region × practice where you can win), many spokes linking up; ~20 supporting pages under a hard keyword.
- Don't repeat every region in a site-wide footer: it reads as keyword stuffing and splits link equity. Cap it (e.g. 24 regions + a "see all" link to the hub). (field experience)
- No UTM parameters on internal or own-network links (they create redirect/alternate buckets).
- Code: `implementation-playbook.md` §9.

Sources: [Link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) · [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) · counts: (third-party study) / (field experience) as marked

## 7. Links and citations

- Earn links only: bar-association and local-bar member pages, press comments and columns, seminars, real directories, local institutions. Local organic weights in one industry survey: links 28%, on-page 25%, reviews 18%, GBP 15%, citations 8% (third-party study: Whitespark 2026).
- Hyper-local relevance beats raw authority (a low-authority local link can beat an irrelevant high-authority one). (field experience)
- Never buy links, exchange links, use PBNs, paid "sponsored articles" or bulk directory submission. These are link spam under Google's policies, and for lawyers also an advertising-rule risk.
- If ~99% of referring domains are your own sites, flag it as a link-scheme risk. Changing network linking is a business decision.

Sources: [Spam policies (link spam)](https://developers.google.com/search/docs/essentials/spam-policies) · [Bing Webmaster Guidelines (artificial promotion)](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a) · weights: (third-party study)

## 8. GEO: being quoted by AI answers

| Rule | Why |
|---|---|
| **AI engines quote your own pages verbatim.** Trace every wrong AI fact to its source page and fix that page first. | A false "near the court" claim in an AI answer came from the firm's own page (2026-11). (field experience) |
| Be one consistent, verifiable entity across many sources; don't write "recommended / No. 1" about yourself. | Engines select from trusted sources; ad tone, superlatives, win rates and unsourced statistics get excluded. Bing's guidelines ask for clear entity definitions and independently verifiable content. |
| Allow AI **search/user** bots in robots.txt and in the WAF/CDN: OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User, Bingbot. Training bots (GPTBot, ClaudeBot, the Google-Extended token) are an owner choice. | Blocking the search bot removes you from citations. A bot with its own `User-agent` group ignores the `*` group. |
| Quotable structure: a 1–2 sentence direct answer at the very top; a definition box; comparison tables; numbered steps with deadlines; question-form H2 followed immediately by a concrete answer; "as of" / "last reviewed" dates. | Engines lift these blocks whole. Invest in structure, not in one engine's product name (Naver's Cue: and CLOVA X closed on 2026-04-09). (field experience) |
| A summary must not replace the body. General rules get a full answer; case-specific judgement is honestly left to consultation. | Thin "answer-only" pages lose E-E-A-T and conversions. |
| `llms.txt`: optional, low priority. As of 2026 no major AI vendor documents reading it; measured correlation ~0. Keep it accurate if present. | Cheap, but don't spend effort there. (field experience) |
| Near-me queries triggered Google AI Overviews only ~8% of the time (general legal ~78%) in one 2026 sample. For local intent the map pack is still primary. | Prioritise listings for "<city> lawyer"; content for informational queries. (third-party study) |
| Bing Webmaster Tools shows **Copilot citation counts** per site and page — a directly measurable GEO metric. Long conversational queries ranked #1 there. | One main site: 407 AI citations in 30 days (2026-08). (field experience) |
| Naver Blog blocks AI crawlers; external AIs read the open web, not Naver Blog. | Global-AI work and Naver work need separate tracks. (field experience) |
| Run AI checks logged out; record date, engine, query; expect source variance between runs. | Signed-in and repeated runs differ. |

Sources: [OpenAI crawlers](https://developers.openai.com/api/docs/bots) · [Anthropic crawlers](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler) · [Perplexity crawlers](https://docs.perplexity.ai/guides/bots) · [Google-Extended](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers) · [How Google interprets robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt) · [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a) · [llms.txt](https://llmstxt.org/) · other rows as marked

## 9. Measurement and decision rules

- **Split the problem in two.** CTR problem: long-tail queries at positions 3–10 (fix titles/snippets, 1–4 weeks). Ranking problem: "<city> + practice + lawyer" at positions 40–78 (fix landing pages, internal links, local profile, local links, 2–4 months). The second carries the money. (field experience)
- Benchmarks (English studies): position 1 ≈ 28–40% CTR, position 3 ≈ 10%, position 10 ≈ 2–3%; +1 position ≈ +32% relative; sitelinks lift position 1 from 34% to 47%; a **local pack drops position-1 organic CTR from ~40% to ~24%**. Title work is justified for pages at positions 3–6 with CTR < 4%. (third-party study)
- **KPI = leads (consultation requests), commercial-query positions, inbound internal links to money pages.** Not raw traffic.
- Title tests: 20 test pages vs 20 controls, 28 days, one variable.
- Traffic down but position flat → an AI Overview or SERP feature took clicks, not a penalty. Both down → a real problem.
- **Index-rate rollback trigger, written before any volume increase:** "Discovered – currently not indexed" share > 10% of a site's (indexed + not indexed) → stop or reduce that site. (field experience)
- Search Console data lags by days and UI snapshots can be weeks old. Check what the server returns *today* before diagnosing.
- The Search Console property must match the canonical host (www vs non-www); a mismatched URL-prefix property shows almost nothing. A verification meta tag on the site means a URL-prefix property (Domain properties use DNS TXT).
- Verify every "fixed / deployed" claim live. Agent and dashboard reports are claims.

Sources: [Verify site ownership (property types)](https://support.google.com/webmasters/answer/9008080) · [Page indexing report](https://support.google.com/webmasters/answer/7440203) · CTR benchmarks: (third-party study) · decision rules: (field experience)
