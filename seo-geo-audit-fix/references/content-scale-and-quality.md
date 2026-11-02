# Content scale and quality — volume, scaled-content risk, writing, compliance

Read before planning content volume, before module E, and before writing or approving any
content for a regulated business. Korean wording examples are given in English translation;
apply the rules to the original language. **(field experience)** marks the author's own findings.

## Contents
1. Publishing volume: decision rules
2. Scaled-content-abuse risk
3. Natural (non-AI-sounding) writing
4. Thin and duplicate content
5. Multilingual content, the locale gate, sitemap reliability
6. Q&A-to-article pipelines and their pitfalls
7. Sample-article pattern (foreign-reader articles)
8. Facts, statutes and dates
9. Lawyer-advertising compliance (Korea)

---

## 1. Publishing volume: decision rules

**No search engine publishes a safe daily number.** Google and Naver never stated a per-day limit; claims like "max N/day" or "grow ≤ N%/month" have no primary source. John Mueller (Google): publishing frequency alone does not make something spam (2023-01), and there is no indexing limit per day (2021-06). Safe volume = the volume at which the index rate does not drop.

| Rule | Why |
|---|---|
| Measure first (baseline per site), then a small step, then **wait 2 weeks**, then measure again. Write the rollback trigger **before** raising volume. | Volume decisions without measurement reversed themselves: the first plan wanted to raise the biggest site most; data showed it had the longest queue. (field experience) |
| Rollback trigger: "Discovered – currently not indexed" > **10%** of a site's pages, or Naver's "collection on hold" rising → back to the previous level for that site. | This bucket means "found, not crawled yet" — a direct "slow down" signal. |
| Raise volume **asymmetrically**: healthiest sites first (≥ 90% indexed, tiny queue); freeze sites over the trigger. | In one network: sites at 97.4% / 93.3% / 87.6% indexed got more; sites at 43.6% (514 queued) and 67.1% (31.5% queued) were frozen. (field experience) |
| Fast growth of a *new* domain is not by itself the danger. | A satellite grew 85%/month and was 93.3% indexed — the "growth % limit" was folklore in our own data. (field experience) |
| **Volume is capped by topic supply, not writing capacity.** Before raising, count genuinely new topics; keep ≥ 7 days (≥ 2× the daily rate) in stock, else refill first. | A "280-topic" bank was really 60 new topics (220 duplicates). All three publishing gaps came from an empty queue. (field experience) |
| Drip, never batch: e.g. 1 item per 10 min per network, inside working hours. **No backlog dumps.** A backlog of 300 is spread over 10 days. | 485 pages in 3.5 h (≈ 3/min) is the "100 pages in 10 seconds" class of pattern. Naver sanctions macro/flooding (102/day at 2–3 min). The interval also protects server load (crawl capacity). (field experience) |
| Spreading the same volume over 24 h is harmless; multiplying volume is not. | Time of day isn't a factor. A 20× increase (144/site/day) was rejected: it would blow up an already-tripped queue, exhaust topics and the statute cache in weeks, and drop quality. |
| ~1,000+ new URLs (pages or template cohorts) are never offered in one day; open in cohorts with 2 weeks between. | Same rule applied to sitemaps. |

Example timeline in one 7-site network (yours will differ): 32/day → 40/day asymmetric (next day) → 46/day across 6 sites (3 weeks later) → 10/site/day across 7 sites = 70/day (about 5 weeks after the start). The rollback trigger had already tripped on two sites partway through; check current Search Console data before advising more.

Sources: [Page indexing report](https://support.google.com/webmasters/answer/7440203) · [Spam policies (scaled content abuse)](https://developers.google.com/search/docs/essentials/spam-policies) · Mueller statements as attributed · numbers: (field experience)

## 2. Scaled-content-abuse risk

- Google's spam policy (since 2024-03) defines scaled content abuse as many pages generated for the primary purpose of manipulating rankings and not helping users, **no matter how it's created**. AI use is allowed; low-value scale is not. Manual actions were issued for exactly this in 2025.
- The clause that hits **networks**: creating multiple sites with the intent of hiding the scaled nature of the content. Several domains writing on the same legal topics drift toward it.
- Site reputation abuse (third-party pages published on a host site to exploit its ranking signals) is a separate policy; don't host partner content for ranking purposes.
- Risk is in the **average**, not the sum: Google's site-level quality signals and Naver's source-level C-Rank both dilute as weak pages accumulate.
- Heuristics named by practitioners (a 2026-07 prediction, not an announcement): publishing velocity bursts, % page growth, **title patterns**, H1/document-name patterns, internal-link patterns, backlink patterns; strongest defence = a real brand with branded search. (third-party study)
- Highest-risk page types: templated "legal info / Q&A" pages built from statutes; lowest: real case write-ups with real facts. (field experience)
- A "spike then crash" traffic curve = likely penalty; check whether positions also fell.

Mitigations that worked or were adopted (field experience):
1. Kill bulk batches (drip only).
2. Soften title templates (no fixed prefix on every title; varied endings).
3. One topic → one domain across the network (the older rule "a similar title on another site is fine because crawl budget is per domain" was retired on 2026-09-08: the risk is judged at owner/network level).
4. Byline, reviewed-by line, AI-process disclosure, editorial policy page.
5. An original element per article.
6. Don't auto-insert the same CTA/signature/outbound-link block in the same position on every page.

Sources: [Spam policies (scaled content abuse, site reputation abuse)](https://developers.google.com/search/docs/essentials/spam-policies) · [Creating helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) · practitioner heuristics: (third-party study)

## 3. Natural (non-AI-sounding) writing

Detectors and readers notice low **perplexity** (always the most likely word) and low **burstiness** (sentences of equal length). Legal text is falsely flagged as AI even when human-written, so this genre needs *more* effort. Detector scores are information, not the criterion; the criterion is "useful and reads smoothly". Korean examples are translated.

| Level | Rule |
|---|---|
| Sentence | Mix lengths: at least one very short sentence (< 10 characters in Korean, e.g. "The timing is the problem.") per section. |
| Sentence | Vary sentence endings (in Korean: formal, polite, conversational and question endings); never the same ending 3+ times in a row. |
| Sentence | Connector budget: "also / moreover / furthermore / in conclusion" ≤ 2 per article. |
| Sentence | Remove translationese: "is located in" → "is in"; "in the process of doing" → "when doing"; "is in possession of" → "has"; "in spite of the fact that" → "although". |
| Sentence | No ad verbs or puffery: "boasts", "we recommend", "we hope you visit", "a satisfying experience", "groundbreaking", "perfect". |
| Article | Open with the reader's situation, never "X is defined as …". |
| Article | 1–2 practice observations ("this is one of the questions we hear most in consultations"), never invented client stories. |
| Article | At least one concrete number, period or unexpected comparison. |
| Article | H2s as sentences/questions, not labels. Keep statute text out of the body (list the laws at the end). |
| Process | Read-aloud test on the intro and closing. Within a batch, intros and first connectors must not clone each other (n-gram checks miss structural clones). |
| Process | Don't rely on human review alone: people who write with AI find AI errors *less* often (automation complacency). Mechanical checks (QC script, statute cache, n-gram) stay the backbone. |
| Images | Images for articles: no AI-looking text, no visible "AI" label; Naver now inspects image content. Real photos convert best on money pages. |

Sources: [Creating helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) · writing rules: (field experience)

## 4. Thin and duplicate content

- **Measure the cause before "fixing thin".** In one 135-URL bucket, 84% of thin articles were indexed; non-thin ones were 2.2× *more* likely to be stuck. The real variables were age and a templated title suffix (a fixed "… legal solutions" ending): same month, 50% stuck with the suffix vs 0% without. Rewriting 52 titles beat lengthening 173 articles. (field experience)
- Template pages (city pages) must be compared with **names neutralised**; 0.85+ similarity → don't open them at once; add real per-region blocks (local articles, cases, courts) first. Title/description variation alone does not change the body.
- Per-region title/description variation: assign combinations by **ordinal within the province**, not a hash (a hash put a city and one of its own districts on the same combination).
- Similarity metrics are untrusted until they catch known duplicate pairs. Failed in practice: word Jaccard (interrogatives inflate the denominator; a near-duplicate scored 0.29), character 4-grams (0.22 duplicate vs 0.18 unrelated), longest common substring (cross-word fragments). Worked: split into words, strip particles, drop short words and stop-words, flag any shared *rare* topic word (corpus document frequency ≤ 8). Put failed methods in the script docstring. When a format guarantees a shared suffix (all titles are questions), add that suffix to the stoplist.
- Cross-domain duplicates: one topic, one domain. Satellite articles accidentally on the main domain are 301'd to their satellite (de-duplication, not linking).
- Same page on several domains with the same `<title>` (e.g. a firm-wide taxonomy page): one canonical owner; the others `noindex, follow` or a cross-domain canonical.
- Pages whose text loads client-side (terms, privacy, news shells) are empty to crawlers → soft 404. SSR them or drop them from the sitemap.
- Which tool when (301 vs noindex vs canonical vs 410): `implementation-playbook.md` §10.

Sources: [Canonicalization methods](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) · [Block indexing with noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing) · [HTTP status codes / soft 404](https://developers.google.com/search/docs/crawling-indexing/http-network-errors) · [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) · measurements: (field experience)

## 5. Multilingual content, the locale gate, sitemap reliability

- **Two questions drift apart silently:** "is the page open (200)?" and "do we offer it (in the sitemap)?". If they live in different files, they diverge with no error. 1,386 URLs were open but not offered — and the default-language page itself announced them via `hreflang` → all stuck in "Discovered". Fix: **one list, one source**, used by the gate, hreflang cluster, language switcher, sitemap and footer chips; a **build-time assert** (with a negative test) where a copy is unavoidable. Anything outside the list → an honest 404 in that language. (field experience)
- Hiding a page from the menu is a navigation decision; removing it from the sitemap is an indexing decision. Never one config for both. A page leaves the sitemap only when it is `noindex`.
- `next/link` and `router.push` add the active locale: links to single-language routes must pin the default locale. This produced 68 live broken links.
- Translations must be **linked** (a shared translation-group id → hreflang cluster + switcher to the same article). Unlinked, six language versions are six unrelated records; build the link *before* publishing content.
- Translation of a verified source is localisation, which hreflang exists for; the penalised thing is valueless generation. Cross-language duplicates are intended; **within-language** duplicates are a problem — run duplicate checks per language.
- Content for foreigners must pass the test: "would a local (Korean) reader get exactly the same text?" If yes, it doesn't belong in the set. Each article needs at least one foreigner-specific dimension (visa consequence, language barrier, fear about status, different documents/systems, leaving the country).
- Language rollout: open each new language only after native review; staged per language. Two languages waited for a reviewer.
- Sitemap reliability: `catch {}` + `?? []` + a GraphQL client with `errorPolicy: 'all'` = an empty 200 sitemap when the API is down (847 → 328 URLs, no error) — a mass "deleted" signal. Return 503 + Retry-After + `no-store` when any data call fails; `s-maxage` only on success. Test four failure modes (refused, GraphQL error, HTTP 500, hanging) with a real build.
- Don't publish `<lastmod>` you can't trust: omit it until a real content-updated date exists.
- Sitemap mechanics and the validator: `sitemaps-and-submission.md` §3 and `scripts/sitemap_validate.py`.

Sources: [Localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions) · [Managing multilingual sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites) · [Sitemaps ping/lastmod post](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping) · incidents: (field experience)

## 6. Q&A-to-article pipelines and their pitfalls

Flow seen in practice: a manager answers questions on Naver KnowledgeiN or a legal Q&A platform → chat export (JSON) → Q&A split + topic → site routing → LLM rewrite to an article JSON → QC → push via the CMS API → drip publish → log. (field experience)

| Pitfall | Rule |
|---|---|
| Routing by keyword sends a topic to the wrong site; the content's origin field decides its real home (a mismatch triggers a 301 chain). | Validate target site ↔ origin field before publishing; stop on mismatch. |
| Draft scripts writing into an auto-published folder published drafts (happened twice). | Write down which writer may write to each auto-consumed folder; drafts go to a separate folder, not a filename prefix. |
| A format rule ("no FAQ in Q&A articles") remembered in one place regresses. | Enforce it in two places: the generator drops it, the checker blocks it. |
| A correction arriving after publication is quarantined by the duplicate gate and never applied. | Plan an in-place edit path (keeps id → URL and index) alongside the pre-publication path. |
| A scheduled release that refuses on a precondition loses a whole day. | Retry or a manual trigger flag; the manual batch covers the whole day. |
| A hanging step (dead LLM keys) blocks every later line of the batch, incl. the release. | Critical fast steps first, hangable steps last with timeouts. |
| Logs show success while state didn't change (a shell redirect locked the log the script opens). | Judge by state, not by log. |
| Parallel writer agents each report "clean"; together they collide. | One global check after every parallel round, including correction rounds; rules in a repo file, not in messages; derive exclusion lists from files; regenerate snapshots each round. |
| Your own audit script flags 45 false errors (it treated generator markup as author markup). | Validate any audit/QC script on a known-good batch first. |
| Keep the original question visible (Q-block) | It is the article's original element and the long-tail match. |
| Templated title suffix on every Q&A article | Write titles from the question the body actually answers; vary endings. |

Sources: (field experience)

## 7. Sample-article pattern (foreign-reader articles)

Three sample articles for foreign readers (written in the readers' language, marked "not yet reviewed") defined the international format: (field experience)
- Title = the reader's literal question (e.g. "My wages were not paid. What do I do on the first day?").
- First paragraph = the direct answer, including the honest limit (e.g. "In some cases, yes … but this is not an automatic penalty").
- Sections: today's actions → what counts → talking to the employer → filing → fear about status → what to watch out for → next step.
- The local-language term in parentheses at first use (e.g. the Korean words for "petition", "employment contract", "alien registration card") — it is what the reader sees on paper and what they search.
- Tables for conditions/deadlines; short sentences; 1,200–2,000 words; statute numbers only in a closing "rules applied" block, and only when in the local cache.
- An honest "what this does not mean" section (a protection is not legal status).
- Closing CTA: consultation is paid; a staff member calls and states the fee; firm name + main number. Disclaimer: general information, not legal advice.
- A reviewer note explains every deliberate omission (e.g. article number omitted because the regulation isn't in the cache).

Sources: (field experience)

## 8. Facts, statutes and dates

- Every article/case number, date and amount comes from a **local verified copy read at write time**. The model's memory is not a source; a comment in a plan file is not a source.
- Not in the cache → write only the law's name, no article number. Unverified → mark it `[verification needed]` and the article doesn't ship.
- A rule with a **pending amendment** is not cited until its effective date is checked; a date-shifted "the law says X" is worse than silence. Don't present roadmaps (e.g. a 2030 immigration strategy) or announced-but-not-enacted changes as current law.
- Real errors caught this way: repealed or unconstitutional provisions, wrong attempted-offence lists, changed penalty articles.
- Never use crime statistics by nationality (stigma; sources warn against it).
- Length-bounded regexes must be tested against the shortest real value (a pattern for 2–25-character statute names missed the three short names of the Civil, Criminal and Commercial Acts in Korean).

Sources: (field experience)

## 9. Lawyer-advertising compliance (Korea)

Norm stack (check quarterly, it changes): the **Attorney-at-Law Act** (Article 23 governs advertising) → the Korean Bar Association **Rules on Attorney Advertising** (latest amendment seen: 2025-06-30) → the Korean Bar Association **Regulations on Attorney Advertising** (full revision in 2021; amended 2025-02-06, promulgated 2025-02-10; Article 7 governs "specialist"/"dedicated" wording) → the Bar Association's operating guidelines for lawyer-search services (2025-05, for directory platforms). The old "regulation on attorney business advertising" is the repealed predecessor. Breaches lead to a warning, stop or correction order from the local bar → publication → discipline. Fake or seeded reviews also breach the **Act on Fair Labeling and Advertising**. Collecting contact details through forms falls under the **Personal Information Protection Act**; marketing messages and online notices under the **Act on Promotion of Information and Communications Network Utilization and Information Protection (Network Act)**.

| Never | Use instead |
|---|---|
| "Certified by the Korean Bar Association" / "registered specialist in <field>" for a field **not registered** by that lawyer (a false statement under the Attorney-at-Law Act). Certification belongs to the individual lawyer, not the firm. | "<firm>, with a Korean Bar Association–certified criminal-law specialist" — for registered fields only |
| Superlatives and comparisons: No. 1, best, most, overwhelming, only, top-tier, "the best at" | "based in <city>", "many", years of practice |
| Win rates, "we got an acquittal", guaranteed outcomes, "chance of winning" claims | a general explanation of how counsel helps |
| Unsourced statistics or satisfaction figures | only figures with a real, documented basis |
| "Free", "zero retainer", "lowest price", "affordable"; **free consultation, 24 hours, 365 days** where untrue (e.g. consultations are paid and not 24 h) | "When you request a consultation, a staff member will call you and explain the consultation fee." |
| Former-prosecutor/judge influence, connections | — |
| Direct solicitation: "hire us now", "don't hesitate", "before it's too late" | "We recommend a formal consultation." |
| Self-described recommendation ("many people recommend us", "the lawyer we recommend") | "recommended" only as the reader's question (an H2 or FAQ) or quoting the search intent once; "how to choose / what to check" in titles |
| Fake, paid, staff-written or scripted reviews; Review stars for self-selected testimonials | genuine reviews requested open-endedly |
| Advertising AI use ("AI legal diagnosis", "reviewed by AI") | disclose the editorial process neutrally |
| Implying offices that don't exist ("<region> branch / office / network") | "we handle matters from <region>" |
| Real client details | change 5 elements: sex/age/job, region, family, amounts/dates, outcome |

**"Specialist" wording — the corrected rule (as of 2026-09):** plain "<field> specialist lawyer" or "dedicated to <field>" (without certification wording) is allowed for any field the lawyer actually practises, after the 2021 revision of the Regulations (Article 7). Only the *certification* wording is restricted to registered fields. Older view (found in earlier internal prompts and plans): "'specialist' only for registered fields" — that came from the repealed regulation; a same-day cleanup removed the word in 160+ places before the decision was reversed. Confirm against the current text of the Regulations before relying on this. (field experience)

Also name the **lawyer responsible for advertising**, and send borderline wording (centre names like "<field> Specialist Centre", unverified stat tiles) to that lawyer rather than deciding it in a pipeline. Owner decisions (e.g. "keep existing figures and repeated region/'recommended' wording") override generic advice: list them under "Skipped by owner decision" and note the regulatory risk once.

Sources: [Korean Bar Association: Regulations on Attorney Advertising (2025-02-06)](https://www.koreanbar.or.kr/pages/board/law_view.asp?category=3&page=1&searchstr=&searchtype=&seq=14402&teamcode=&types=6) · [Korean Bar Association: Rules on Attorney Advertising (2025-06-30)](https://www.koreanbar.or.kr/pages/board/law_view.asp?teamcode=&page=1&seq=14681&types=6&category=3&searchtype=&searchstr=) · [Review snippets (self-serving reviews)](https://developers.google.com/search/docs/appearance/structured-data/review-snippet) · statute names are official English titles; read the current statute text before citing an article · interpretation history: (field experience)
