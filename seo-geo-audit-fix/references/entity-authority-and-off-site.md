# Off-site entity authority — Wikidata, Wikipedia, wikis, profiles and earned mentions

How to make AI answer engines (ChatGPT, Google AI Overviews/AI Mode, Perplexity, Gemini, Copilot,
Claude, Naver AI Briefing) describe a company **quickly and correctly**. They rarely rely on the
company's own site alone: they pull from encyclopedias and wikis, knowledge graphs, profile sites,
reviews, video, forums and press. This file is the marketing side of module C/G/H: audit those
sources, fix what the company controls, and earn the rest honestly.

Rules marked **(third-party study)** come from industry studies that were not re-verified here;
**(field experience)** comes from the author's audits. Policies are quoted from the platform's own
pages (`sources.md` §15, verified 2026-11-07).

## Contents
1. What AI engines actually cite
2. Audit: the AI source map and the entity inventory
3. Priority ladder — what to do first
4. The entity home (own site) and one canonical description
5. Wikidata
6. Wikipedia
7. Korean wikis and portals (Namuwiki, Naver)
8. Google Knowledge Graph and knowledge panel
9. Profiles the company controls
10. Earned mentions: press, video, forums, reviews
11. Hard limits (what never to do)
12. Measuring progress

---

## 1. What AI engines actually cite

| Finding | Use it like this |
|---|---|
| Brand **web mentions** correlate with AI-Overview brand visibility far more than backlinks (0.664 vs 0.218); the top 3 factors were all off-site. The top quartile by mentions got ~10× the AI mentions of the next quartile. (third-party study: Ahrefs, 75k brands) | Count mentions, not links. A brand nobody writes about is invisible to AI. |
| In the follow-up study **YouTube mentions** (title, description, transcript) correlated most (~0.737) across ChatGPT, AI Mode and AI Overviews; branded web mentions 0.66–0.71; link metrics stayed weak. (third-party study: Ahrefs) | Being *talked about* in videos (own channel + other creators) is a top lever. |
| Citation sources are concentrated and per-engine: ChatGPT leaned on Wikipedia and Reddit (Wikipedia ≈ 48% of its top-10 source share in 2024–25); AI Overviews/AI Mode lean on YouTube, Reddit, LinkedIn and Google properties; Perplexity on YouTube and Reddit; Claude mostly on first-party sites in one SaaS sample. (third-party studies: Profound 680M citations; Semrush 230k prompts; Ahrefs Brand Radar 2026; OtterlyAI) | Don't optimise for one platform's habit. Cover the reference layer (wiki/knowledge graph), the conversation layer (video, forums, LinkedIn) and the first-party layer (own site). |
| Shares swing within weeks: ChatGPT's Reddit citations fell from ~60% to ~10% of responses between Aug and Sep 2025. (third-party study: Semrush) | Measure your own query set (§12); never promise a citation share. |
| For a firm's own name, Google's AI Overview cited only an encyclopedia page and the Business Profile, not the firm's websites. (field experience, `multisite-and-technical.md` §8) | Fix the encyclopedia/profile facts first; they are what the AI reads. |

## 2. Audit: the AI source map and the entity inventory

**AI source map.** Logged out, ask each engine 5 questions: "What is <brand>?", "Who founded / runs <brand>?",
"Where is <brand> and how do I contact it?", "Is <brand> good for <service>?", "Best <service> in <city/market>".
Record per answer: mentioned? correct? every cited URL and its domain type (wiki, knowledge panel, directory,
review, video, forum, press, own site). The domains that appear repeatedly are the ones to fix or earn.
Template: `templates/browser-prompts/07-ai-source-map-and-offsite-entity.md`.

**Entity inventory.** One row per source; keep it in the fact sheet's entity table.

| Source | Exists? URL / ID | Facts match the fact sheet? | Who can edit | Linked from site `sameAs`? | Action |
|---|---|---|---|---|---|
| Wikidata item (QID) | | | anyone (COI rules) | | |
| Wikipedia (each language) | | | anyone (COI rules) | | |
| Namuwiki / local wikis | | | anyone | | |
| Google knowledge panel / KG ID | | | owner after claim | n/a | |
| LinkedIn company page | | | owner | | |
| Crunchbase / business databases | | | owner (claim) | | |
| YouTube channel | | | owner | | |
| Map listings (GBP, Naver, Kakao, Bing) | | | owner | | |
| Industry directories / registers | | | owner or register | | |
| Review sites relevant to the industry | | | reviewers | | |
| Press coverage (last 24 months) | | | journalists | n/a | |

Run `scripts/wikidata_entity_check.py` to read the Wikidata item, list missing core statements and
compare its official website with the site's JSON-LD `sameAs`.

## 3. Priority ladder — what to do first

Work top-down. Each level makes the next one easier; skipping levels (a Wikipedia article before any
independent coverage) fails and can damage the brand.

| Level | Work | Typical owner | Time to effect (field experience) |
|---|---|---|---|
| 0 | Entity home on the own site + Organization JSON-LD + one canonical description (§4) | code / content | days after re-crawl |
| 1 | Profiles the company controls, all with identical facts (§9) | marketing | days–weeks |
| 2 | Wikidata item, if the entity meets notability (§5) | marketing (disclosed) | weeks–months to reach knowledge graphs |
| 3 | Earned mentions: press, trade media, podcasts, YouTube creators, genuine forum answers (§10) | PR / experts | months, cumulative |
| 4 | Wikipedia article, only when §6's source test passes; otherwise not at all | volunteers, or disclosed request | slow; review queues |

## 4. The entity home (own site) and one canonical description

- One **About page** that states the facts a wiki would: legal name, brand names and former names,
  founding date, founders/leaders, headquarters and offices, what the company does, registrations
  (business number, licences), and links to every official profile. AI engines quote it verbatim.
- Organization JSON-LD on the home or About page: `name`, `legalName`, `alternateName`, `url`, `logo`,
  `foundingDate`, `founder`, `address`, `sameAs` (every official profile **of exactly this entity**,
  incl. its Wikidata item), and identifiers where they exist (`iso6523Code` with `0199:` LEI or `0060:` DUNS,
  `taxID`, `vatID`). Google uses some of these "behind the scenes to disambiguate your organization".
  Code: `implementation-playbook.md` §5. A branch office follows `multisite-and-technical.md` §8 instead.
- Write **one canonical description**: 1–2 neutral sentences ("<Name> is a <type> founded in <year> in
  <city> that provides <services>."), plus a 50-word and a 150-word version. Use the same facts on every
  profile, directory, press kit and wiki talk-page request. No superlatives — wikis delete them and AI
  engines skip ad tone.
- Keep the facts in sync: when a fact changes (address, CEO, name), update the site, Wikidata, every
  profile and the fact sheet on the same day. Stale third-party facts are the most common source of wrong AI answers.

## 5. Wikidata

Wikidata is the open knowledge graph that search engines, AI systems and Wikipedia infoboxes reuse.
It has a lower bar than Wikipedia, but it is not a directory.

**Notability (policy, quoted).** An item is acceptable if it meets at least one of:
1. it has at least one valid sitelink to a Wikimedia page (e.g. a Wikipedia article);
2. it refers to "a clearly identifiable conceptual or material entity that can be described using
   serious and publicly available references";
3. it fulfils a structural need (other items need it).

For a company without a Wikipedia article, criterion 2 decides: independent public references
(press, government or court registers, industry registers, books). The company's own site may support
individual facts but does not establish notability. Unsure? Ask at *Wikidata:Requests for new items*.

**Conflict of interest.**
- Paid editors must disclose every organisation or person that pays them for contributing
  (*Wikidata:Disclosure of paid editing*; also the Wikimedia Terms of Use). Disclose on the user page.
- Community guidance (RfC on COI): be careful creating an item when you have a COI; don't edit-war;
  keep labels and descriptions neutral — "the task of labels and descriptions are identification, not advertisement".
- One account per person; never shared or company accounts.

**Core statements for a company** (every statement with a reference; property IDs verified via the Wikidata API 2026-11-07):

| Property | ID | Notes |
|---|---|---|
| instance of | P31 | most specific class (e.g. law firm, software company), not just "business" |
| official name | P1448 | with language |
| country | P17 | |
| headquarters location | P159 | the head office only, never a branch |
| inception | P571 | only with a source |
| founder | P112 | |
| industry | P452 | |
| legal form | P1454 | |
| official website | P856 | head-office site preferred rank; branch/satellite sites normal rank (`multisite-and-technical.md` §8) |
| parent / child organization | P749 / P355 | groups, branches, subsidiaries |
| Legal Entity Identifier | P1278 | if the company has an LEI |
| LinkedIn company ID | P4264 | |
| Crunchbase organization ID | P2088 | |
| YouTube channel ID | P2397 | |
| Instagram username / X username | P2003 / P2002 | |
| Namuwiki ID | P8885 | Korean companies with a Namuwiki article |

- Labels, descriptions and aliases in **every market language** (e.g. ko + en): the local name, the
  romanised/English name and common abbreviations as aliases. A missing English label is a common reason
  English-language AI answers miss a Korean company.
- Link both ways: the site's Organization `sameAs` contains `https://www.wikidata.org/wiki/Q…`,
  and the item's P856 points to the site. Use the Wikidata URL as the organisation `@id` target for
  `parentOrganization` on branch sites.
- Never create items for every office, product or person to "build a graph". Thin items get deleted,
  and a deletion discussion is visible history.

## 6. Wikipedia

Wikipedia remains a top citation and training source, but it is the **last** step, not the first.

**Readiness test (Wikipedia's notability guideline for organizations, quoted).** A company is presumed notable
if it "has been the subject of significant coverage in multiple reliable secondary sources that are independent
of the subject". Each source must be significant (in-depth, about the company), completely independent,
reliable and secondary; "a single significant independent source is almost never sufficient", and the sources
must be unrelated to each other.

Does **not** count: press releases and press kits; routine coverage (funding, acquisitions, hires,
product launches, branch openings, financial results); passing mentions and quotes from staff; directory
listings; paid or sponsored articles; self-published material.

→ Before anyone drafts an article, list at least 3 sources that pass every test. If you can't, the work is
§10 (earn coverage), not a draft. A rejected or deleted article stays visible in the logs.

**COI and paid editing.**
- Paid editors must disclose employer, client and affiliation — on the user page, the talk page, or the edit
  summary (required by the Wikimedia Terms of Use).
- People with a COI are "strongly discouraged" from editing affected articles directly. They post proposals on
  the article's **talk page** (an edit request) and put new articles through **Articles for Creation**.
- Allowed and useful with disclosure: fixing clear factual errors with a source, updating the official website
  URL, suggesting a neutral, sourced sentence for an outdated fact. Never re-add text an editor removed.
- Each language edition has its own community and rules (e.g. Korean Wikipedia's COI guideline,
  `multisite-and-technical.md` §8). A Korean article does not imply an English one, and vice versa.
- Never buy "Wikipedia page creation" services. Undisclosed paid editing breaks the Terms of Use, and
  articles built by sock-puppet networks get deleted along with every edit linked to them.

## 7. Korean wikis and portals (Namuwiki, Naver)

(field experience; Namuwiki's policy pages could not be quoted reliably for this file — read the current
*나무위키:편집지침* before acting.)

- **Namuwiki** is the most-read Korean wiki and often appears for Korean company-name queries and in
  Korean-language AI answers. Anyone can edit; promotional (홍보성) writing is removed, and negative
  content cannot be removed just because the company dislikes it.
  - Correct factual errors with a public source in the edit summary; for disputed content use the
    article's discussion (토론) rather than repeated reverts. Never delete criticism wholesale.
  - Use the platform's own legal routes (e.g. a takedown request for defamation or privacy) only for real
    legal problems, through the owner or counsel — not as a marketing tool.
  - If the article exists, add its ID to Wikidata (P8885) so the identities link up.
- **Naver**: Naver's own knowledge features (encyclopedia entries, people search, Smart Place, KnowledgeiN) feed
  Naver's results and AI Briefing. Keep the company's Smart Place and any people-search profiles of its
  representatives factually identical to the site (`korea-search.md` §5–8). Naver Blog does not reach
  external AI engines (`korea-search.md` §4).

## 8. Google Knowledge Graph and knowledge panel

- **Check presence**: the Knowledge Graph Search API
  (`https://kgsearch.googleapis.com/v1/entities:search?query=<brand>&key=<API_KEY>&limit=5`) returns
  matching entities with their ID, type and description. No match ≠ no panel, but a match with the wrong type or
  description tells you what Google believes. Record the entity ID in the fact sheet.
- **Claim the panel** when one shows: "Claim this knowledge panel" at the bottom of the panel → *Get verified on
  Google* (verification through an official profile the entity controls). After verification the owner can
  suggest changes; changes are reviewed, not instant.
- Panels draw on the same sources as above (Wikidata, Wikipedia, the site's Organization markup, Business
  Profile). Fix those; do not buy "knowledge panel" services.
- Adding a `google.com/search?kgmid=` URL to `sameAs` is a practitioner habit with no documented effect —
  optional, low priority. (field experience)

## 9. Profiles the company controls

Create or claim, then fill **every** profile with the canonical facts and description (§4), the same logo,
and a link to the entity home. Add each to `sameAs` and to Wikidata identifiers the same day.

- **LinkedIn company page** (frequently cited by AI Mode and Perplexity; also staff profiles listing the
  company with the correct page link).
- **Crunchbase** or the business database that matters in the market; registers and LEI where applicable.
- **YouTube channel** with an About section using the canonical description; video titles and descriptions
  that name the company and its services naturally (YouTube mentions correlate strongly with AI visibility, §1).
- **Map listings**: Google Business Profile, Bing Places, Naver Smart Place, Kakao Map (module F).
- **Industry directories and registers**: bar/medical association directories, chambers of commerce,
  official licence registers, trade associations. These double as independent references for Wikidata.
- **Review platforms** relevant to the industry (e.g. G2/Capterra for software, Trustpilot/Yelp/TripAdvisor
  for consumer services): claim and keep facts right; ask real customers for reviews without incentives that
  break the platform's rules.

## 10. Earned mentions: press, video, forums, reviews

Earned, independent mentions are what turn "a company with a website" into "an entity AI engines know".

- **Original data and expertise**: publish a small, citable study, index or guide with a clear methodology;
  offer experts for comment to journalists and trade media. In-depth independent articles also become Wikipedia
  and Wikidata references later.
- **Press releases**: fine for distribution and as a factual record (wire services are often cited by ChatGPT,
  third-party study), but they never count as independent coverage, and links with optimised anchor text in
  distributed releases are link spam under Google's policies — keep links plain or `nofollow`/`sponsored`.
- **Podcasts and YouTube creators**: appearances where the brand is named in title, description or transcript.
- **Reddit, Quora and community forums**: answer real questions as a named, disclosed staff member or expert;
  follow each community's self-promotion rules; never use sock puppets or vote manipulation. AI engines cite
  specific discussion threads, so one genuinely useful answer outlasts a campaign.
- **Reviews**: ask real customers; respond; never write, buy, gate or seed reviews (§11).
- Track every new mention in the entity inventory; add the in-depth ones as references to Wikidata statements.

## 11. Hard limits (what never to do)

- Undisclosed paid or COI editing on Wikipedia, Wikidata, Namuwiki or any wiki; shared or sock-puppet accounts.
- Creating wiki articles or items for a non-notable entity, or bending notability with self-published sources.
- Fake, bought, incentivised-without-disclosure or insider reviews. In the US the FTC's Rule on the Use of
  Consumer Reviews and Testimonials (in force 2024-10-21) bans fake reviews (§465.2) and requires clear
  disclosure for reviews by company insiders (§465.5); in Korea the Act on Fair Labeling and Advertising applies.
- Paid articles presented as independent journalism; link-carrying advertorials without `sponsored`/`nofollow`.
- "Knowledge panel", "Wikipedia page" or "AI ranking" packages that promise placement.
- Regulated industries: off-site content (wiki talk requests, forum answers, press quotes) follows the same
  advertising rules as the website (e.g. Korean attorney-advertising rules, `content-scale-and-quality.md` §9).
- Removing criticism instead of answering it. Correct facts with sources; leave opinions alone.

## 12. Measuring progress

Baseline before any work, then monthly, same conditions (logged out, same prompts, date and engine recorded):

| Metric | How |
|---|---|
| AI mention rate | share of the fixed prompt set (§2) where the brand is named, per engine |
| AI accuracy | wrong facts per answer, quoted; trace each to its source |
| Cited sources | domains cited for brand prompts; which are ours, which we influence, which are independent |
| Copilot citations | Bing Webmaster Tools AI performance per page (`knowledge-base.md` §8) |
| Knowledge graph | KG Search API match (ID, type, description); knowledge panel shown / claimed |
| Wikidata completeness | `scripts/wikidata_entity_check.py` missing-statement count; labels per market language |
| Independent mentions | new in-depth articles, videos, podcasts and forum threads naming the brand |
| Branded search | branded impressions in Search Console / Naver Search Advisor |

Expect weeks to months between a fixed source and a changed AI answer; engines re-crawl and re-train on
their own schedules, and repeated runs of the same prompt vary. Report trends over several runs, not one answer.

Sources: [Wikidata:Notability](https://www.wikidata.org/wiki/Wikidata:Notability) · [Wikidata:Disclosure of paid editing](https://www.wikidata.org/wiki/Wikidata:Disclosure_of_paid_editing) · [Wikidata RfC: Conflict of Interest](https://www.wikidata.org/wiki/Wikidata:Requests_for_comment/Conflict_of_Interest) · [Wikipedia:Notability (organizations and companies)](https://en.wikipedia.org/wiki/Wikipedia:Notability_(organizations_and_companies)) · [Wikipedia:Paid-contribution disclosure](https://en.wikipedia.org/wiki/Wikipedia:Paid-contribution_disclosure) · [Wikipedia:Conflict of interest](https://en.wikipedia.org/wiki/Wikipedia:Conflict_of_interest) · [Knowledge Graph Search API](https://developers.google.com/knowledge-graph) · [Get verified on Google (knowledge panel)](https://support.google.com/knowledgepanel/answer/7534902) · [Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization) · [Spam policies (link spam)](https://developers.google.com/search/docs/essentials/spam-policies) · [FTC Consumer Reviews and Testimonials Rule Q&A](https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers) · studies: [Ahrefs AI Overview brand correlation](https://ahrefs.com/blog/ai-overview-brand-correlation/), [Ahrefs AI brand visibility correlations](https://ahrefs.com/blog/ai-brand-visibility-correlations/), [Profound AI platform citation patterns](https://www.tryprofound.com/blog/ai-platform-citation-patterns), [Semrush most-cited domains in AI](https://www.semrush.com/blog/most-cited-domains-ai/) (third-party study)
