# Korea search — Naver, Daum/Kakao, Google KR, local, lawyer directories

Korea-specific rules from real audits and research. Generic rules: `knowledge-base.md`. Submission
steps for Naver and Daum: `sitemaps-and-submission.md` §6.4–6.5. Korean search queries are written
here in English with placeholders, e.g. `"<city> divorce lawyer"` (in Korean). Each section ends with
its sources; **(field experience)** marks the author's own audit findings.

## Contents
1. Market and engine behaviour
2. Naver Search Advisor and Yeti (website indexing)
3. Naver content signals (C-Rank, similarity, spam)
4. Naver Blog
5. Naver KnowledgeiN and legal Q&A platforms
6. Naver Smart Place, Kakao Map, Daum
7. Google KR and Google Business Profile
8. Bing / Copilot in Korea
9. Local-search strategy
10. Lawyer directories and citations

---

## 1. Market and engine behaviour (as of 2026-09)

- Share depends on the method: Naver 63–64% / Google 28–30% (Korean-domain log panels) or Google 47% / Naver 42% (StatCounter). Google is 30–47%, strongest on desktop and Android/Chrome. Plan for both engines. (third-party study)
- Naver has moved toward Google-like evaluation since 2025-12: "smart blocks" removed; wiki pages, official channels and influencers on top; keyword repetition no longer works; content substance is checked; ranking now takes ~1 month (was hours); **image content is checked by a vision-language model**. One effort (E-E-A-T, original content, real photos) serves both. (field experience)
- Naver AI surfaces: Cue: and CLOVA X **closed on 2026-04-09**. Current: the **AI Briefing** on integrated search (types: official, multi-source, place, shopping, short-form video) and the **AI tab** (launched 2026-06-26; from 2026-07 the briefing's chat box opens the AI tab). Don't name closed services in content or plans. (field experience)
- The Naver AI Briefing pulls from the Naver ecosystem (Smart Place, Blog, KnowledgeiN, news); C-Rank is the entry ticket; local intent uses the place type. Global AIs read the open web. (field experience)
- Korean queries arrive both with and without spaces (e.g. `"<city> divorce lawyer"` typed as three words or as one run-together word). Use the natural spaced form in titles; mention the unspaced variant once in the body or an H2. (field experience)

Sources: market shares and Naver behaviour: (third-party study) / (field experience) as marked

## 2. Naver Search Advisor and Yeti (website indexing)

| Rule | Why / how |
|---|---|
| Register the **canonical origin** (`https://www.<domain>`), verify by HTML meta tag or HTML file, submit the sitemap. | An unregistered site is collected less reliably. Keep verification robust (meta *and* file is fine). Scheme and `www` variants are separate sites. |
| **Submit RSS** (Request → RSS submission) in addition to the sitemap. | Naver revisits submitted RSS and sitemaps as content feeds; RSS must carry full text. If the index count stays flat while the sitemap grows, RSS + internal links are the fix. Exclude nav-hidden or noindex paths from RSS too. |
| Sitemap files under **10 MB**, URLs only on the verified domain. | Naver's own submission rules. |
| Manual web page collection request: a few key URLs only. | The tool showed about 50 URLs per day in our use; the guide states no number. It does not limit sitemap collection. (field experience) |
| Allow `Yeti` in robots.txt and in any server bot filter; check logs for Yeti 429/444. | A "restricted collection" count near zero means the server is not blocking. |
| `/favicon.ico` must return **200 + an image**: never disallowed, never redirected (use a rewrite). | Naver's favicon crawler fetched only `/favicon.ico` and did not follow redirects; the logo never showed in Naver results while it was 308 + disallowed. (field experience) |
| Server-render everything that matters. | Naver renders JavaScript worse than Google. (field experience) |
| Deleted pages → 404/410, an **IndexNow ping on delete**, and "web page search exclusion" for urgent removals. | 23 deleted URLs sat as "inaccessible" for weeks because IndexNow pinged only on create/update. (field experience) Naver's IndexNow FAQ confirms 404/301/302 changes can be notified. |
| Naver supports **IndexNow** (own endpoint `https://searchadvisor.naver.com/indexnow`; also reached via the shared protocol). | Verified 2026-11-02 on Naver's guide and indexnow.org. The older internal note "Naver does not use IndexNow" (2026-08) is wrong. |
| No public sitemap/RSS submission API; the crawl-request API is partner-only. | Verified 2026-11-02. |
| Search Advisor is usually blocked for agent browsers. Ask the owner for screenshots: content impressions/clicks (30 days, top 30 keywords); site diagnosis (indexed / restricted collection / excluded from index / SEO, with per-type rows); collection status; content spread (top linking domains); sitemap/RSS status; a brand-query results page. | Mark the rest NOT VERIFIED. |
| Brand-query CTR far below ~30% → others outrank you for your own name (clones, directories, sibling offices). | Real case: 2.8% on 706 impressions. (field experience) |
| "Content spread" dominated by your own satellites → possible artificial-link judgement. Report it; don't silently change it. | ~1.53M links from own satellites in one audit. (field experience) |

Sources: [Naver: basic guideline](https://searchadvisor.naver.com/guide/seo-basic-intro) · [Naver: RSS and sitemap submission](https://searchadvisor.naver.com/guide/request-feed) · [Naver: crawl requests and exclusion](https://searchadvisor.naver.com/guide/request-crawl) · [Naver: robots.txt](https://searchadvisor.naver.com/guide/seo-basic-robots) · [Naver: IndexNow requests](https://searchadvisor.naver.com/guide/indexnow-request) · [Naver: IndexNow FAQ](https://searchadvisor.naver.com/guide/indexnow-faq) · [Naver: crawl-request API (partner-only)](https://searchadvisor.naver.com/guide/crawl-request-api) · [IndexNow participants](https://www.indexnow.org/searchengines.json)

## 3. Naver content signals (C-Rank, similarity, spam)

- **C-Rank is a source-level score** (context, content and chain → the source's trust and popularity). No axis counts posts, but volume dilutes the *average* quality of the source.
- Naver's stated position: a good document can rank regardless of how it was generated, but **automatically publishing documents written only by generative AI** is listed as abuse. Defence: quality, real experience signals, limited volume.
- Naver penalises **macro posting and flooding**. Sanctioned cases seen: 102 posts/day at 2–3 minute intervals; 20+/hour; 60+/day. No official daily limit exists. Popular "low-quality thresholds" (1,500 characters, 2 posts/day) have no primary source.
- A documented drop-out case was caused by repeating a "<region> + <business type>" keyword for a long time, not by volume. Template region pages fall into this pattern.
- **The similar-document filter is strict:** copying text from one blog to another and changing a part is enough for the copy to disappear. Synonym swaps and reordering don't help; "similarity-evasion" tools lead to a low-quality judgement. Naver largely ignores `rel=canonical` here.
- Naver favours **first-hand experience** and dwell time; its good-document criteria: reliability, honest experience, originality, depth, readability.
- A question → answer structure ("What happens if …? → answer") is what the AI Briefing analyses first.

Sources: Naver policy statements as summarised from Naver's search blog and guides (field experience; not re-verified for this file) · sanction cases: (field experience)

## 4. Naver Blog

- Naver Blog is a **Naver-only channel**. Desktop blog URLs are `noindex`; some mobile/post-view URLs leaked into Google and get dropped in cleanups. Since 2025 Naver Blog's robots.txt blocks GPTBot, PerplexityBot and Google-Extended, so ChatGPT and Perplexity don't cite it. Old, entity-linked blogs (e.g. a lawyer's 7-year blog linked from the firm site) can still appear in Google and AI Overviews — an exception, not a channel you control.
- For Google and AI visibility you need your own domain (site, Tistory or WordPress).
- When a post is missing from search, check the post's "allow search" setting.
- **Reusing blog posts on the website:** don't copy or spin. Either move the content (delete/redirect the original, losing its traffic) or, better, use the post as a *source* and write a new, differently structured article. A canonical pointing to the blog tells Google to rank the blog — the opposite of the goal.
- Original vs re-worked channels: the website is the canonical original; secondary blogs get a re-worked version (summary, new angle, new example) with a link to the original, published after the original is indexed.

Sources: (field experience) · canonical semantics: [Canonicalization methods](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)

## 5. Naver KnowledgeiN and legal Q&A platforms

- A lawyer's expert answers on Naver KnowledgeiN put the firm entity into Naver's trusted data pool. Answer general rules accurately; no solicitation.
- Platform rules (KnowledgeiN and legal Q&A/directory platforms): no direct phone, e-mail, personal address or concrete fee in the answer; consultation is booked through the platform.
- Example house format for platform answers (one firm's answer prompt, 2026-08): sections only as Roman numerals I.–IV. (conclusion / legal issues / analysis / strategy), a 1–2 sentence direct answer first, 800–900 characters with spaces, **no colons, asterisks or bold** (platform text filters), statute names without article numbers.
- These answers can be turned into site articles by a pipeline — see `content-scale-and-quality.md` §6 for the pitfalls.
- Conflict to flag: a platform-answer prompt may ask for self-descriptive "recommended <region> <field> specialist lawyer" closings, "a sure-win strategy" and "chance of winning" claims up front, while the firm's own website rules ban self-claimed recommendations and win-likelihood claims. Treat such a prompt as an owner-approved platform format and flag those phrases for the lawyer responsible for advertising; never carry them into website content.

Sources: (field experience) · advertising limits: see `content-scale-and-quality.md` §9

## 6. Naver Smart Place, Kakao Map, Daum

- **Naver Smart Place** drives the map results for queries like `"<city> lawyer"` or `"<district> law firm"` (in Korean) and the place-type AI Briefing: exact business name (same spacing on every channel), category (law firm / lawyer), address, phones, hours, website, photos (exterior, interior, sign), a description without "recommended" or "No. 1", directions, booking/inquiry.
- **Kakao Map** shows the building name from Kakao's own address database; Daum search cards copy Kakao place data. One building can appear under two names (the site said one, Kakao another) — pick one and use it everywhere.
- Owners manage a Kakao Map listing through **Kakao Map store management** (Kakao Business Partner Center): location, hours, prices, website, tags, news/coupons and replies to reviews. A place that doesn't exist yet can be requested as a new place; Kakao reviews it before it appears.
- Kakao audit pattern (2026-09, query = the firm's brand name, 11 results): each office pointed to a different website/blog (brand split 6+ ways); three name formats; hours ranged from "daily 00:00–24:00" to "Mon–Fri 09:00–18:00"; seven offices with 0 reviews; one office at 2.0 stars on 551 reviews; one duplicate listing with no phone. Fix: one name template ("<firm> <office name> office"), website → the office's own location page, one hours policy, request a merge of duplicates. (field experience)
- The Daum Webmaster Tools verification line lives in robots.txt as a comment (`#DaumWebMasterTool:<hash>:<suffix>`); login uses the site URL + a PIN.

Sources: [Kakao Map store management](https://kakaobusiness.gitbook.io/main/partner/smb/channel/service_biz/mystore) · [Kakao: registering a place (new-place request, review)](https://kakaobusiness.gitbook.io/main/tool/booking/pc/undefined-1) · [Daum Webmaster Tools](https://webmaster.daum.net/) · [Daum help: PIN](https://cs.daum.net/faq/service/15/category/4118/detail/38321) · Smart Place fields and the Kakao audit pattern: (field experience)

## 7. Google KR and Google Business Profile

- Google Business Profile works in Korea (verification by post/phone/video depending on the case). Google received conditional approval to export map data on 2026-02-27, so local-pack competition will grow. (field experience)
- Local-pack weights in one industry survey: GBP 27%, reviews 22%, behaviour 18%, citations 11% (third-party study: Whitespark 2026). Top local organic factor: a **dedicated page per service** with the geo keyword in the title.
- **The primary category decides relevance.** A profile in a generic "corporate office" category with no hours was the main local gap while competitors used law categories (2026-11). Use "law firm" / "lawyer" + practice-related secondary categories. (field experience)
- One profile per *real* office. Serve other areas through "service areas", never extra listings (Google's guidelines don't allow listings for locations without a real staffed presence).
- Fill every field: services at practice level, 10+ photos, weekly posts, hours, Q&A. Website = that office's location page, no UTM.
- Reviews: steady velocity (8–12/month beats 100 at once); a last review older than 90 days is a problem; reply within 48 h; ask open-endedly; never script, seed, pay for or write reviews; owner/staff reviews of their own business violate the fake-engagement policy. A keyword-laden burst plus staff reviews got 2 of 8 reviews filtered (2026-11). (field experience for the numbers)
- Never set "open 24 hours" unless true; never stuff keywords into the business name, even if competitors do.

Sources: [Guidelines for representing your business](https://support.google.com/business/answer/3038177) · [Maps content: prohibited and restricted](https://support.google.com/contributionpolicy/answer/7400114) · [Maps content: fake engagement](https://support.google.com/contributionpolicy/answer/11414422) · weights: (third-party study) · cases: (field experience)

## 8. Bing / Copilot in Korea

- Bing sitemap "Error / 0 URLs" while Search Console reads the same file fine: confirm the file is a clean `urlset` on the canonical host, then resubmit and wait days. Bing's "Success" right after resubmit is optimistic; recheck the next day. (field experience)
- Remove stale `http://` or non-www sitemap entries (their 301s show in server logs).
- Bing relies on `<lastmod>` heavily; a false lastmod breaks its recrawl schedule.
- Bing/Copilot filters sensitive topics: a sex-crime defence site had 3 impressions in 30 days with a healthy sitemap. Use Google and Naver as the main channels for such topics. (field experience)
- Bing can import sites (and their sitemaps) from Search Console; then only a rescan is needed.

Sources: [Bing: importance of lastmod](https://blogs.bing.com/webmaster/february-2023/The-Importance-of-Setting-the-lastmod-Tag-in-Your-Sitemap) · [Bing: add and verify site / import](https://www.bing.com/webmasters/help/add-and-verify-site-12184f8b) · other rows: (field experience)

## 9. Local-search strategy

- `"<city> lawyer"` is answered by a **dedicated landing page + a local profile**, not a blog post. Long-tail articles reach page 1 on low-competition questions; commercial city queries sat at positions 40–78 with zero clicks. (field experience)
- **Build location pages for real office cities first**: real NAP, office photos, that city's court, the lawyers who work there, local procedure. Office-less regions → merge into the nearest real-office page or `noindex`; describe them as "we handle matters from <region>", never as "<region> office/branch".
- Where competition is low, satellites already reached page 1 (e.g. `"<smaller city> real-estate lawyer"` at average positions 7.4 and 7.9 in two such cities) — pick these first. (field experience)
- Multi-office phone policy (an owner decision in one multi-office firm): our pages, schema and managed profiles show the main number for every office; if office listings keep local numbers, label the main number as the main line (`contactType: customer service`) to limit NAP noise.
- The 12-combination keyword matrix (`<region>` × {lawyer, law firm} × {—, + field, + "specialist" + field} × {—, + "recommended"}) is a **coverage checklist**, not a page list. One good article covers many cells; creating a page per cell is a doorway pattern.
- Rotate "lawyer" and "law firm" as head terms; the full entity name ("<firm> <attorney name>, attorney") covers both.
- Map-pack visibility tests: fixed geo-grid centres × core queries, signed out and signed in; proximity dominates, so judge mainly the office-area cells.
- Never use words implying a bigger organisation than exists ("network", "nationwide", "branch", "branch network", "partner firms", "affiliated lawyer group" — a typical banned-token list).
- Map the whole brand entity: sibling offices of the same firm outranked the main office for the brand query and nobody cross-linked them (2026-11). Siblings are not competitors.

Sources: [Spam policies (doorway abuse)](https://developers.google.com/search/docs/essentials/spam-policies) · [Guidelines for representing your business](https://support.google.com/business/answer/3038177) · strategy rows: (field experience)

## 10. Lawyer directories and citations

- Honest citation sources: the Korean Bar Association's public lawyer directory (must match registered specialties), legal Q&A/directory platforms, the major legal newspaper's directory of legal professionals, local bar associations, regional news. Link them to the relevant location/practice page and add each to the entity table and `sameAs` the same day.
- Lawyer-search platforms are also covered by the Korean Bar Association's operating guidelines for lawyer-search services (2025-05), in addition to the advertising rules. (field experience; check the current version on the Bar Association's site)
- No "recommended / No. 1 / best" in any directory profile; NAP identical to the site.
- Showing platform stats on your own site: profile counters often come from inline scripts or undocumented JSON endpoints (answer counts, review counts, published posts); such endpoints change without notice. Cache server-side (e.g. 6 h), fall back to the last known value, and show an honest baseline with "+" where no endpoint exists. (field experience, as of 2026-07)
- Most top Korean firms had no LegalService schema in one third-party scan — having it is an advantage. (third-party study)

Sources: [Korean Bar Association: Regulations on Attorney Advertising](https://www.koreanbar.or.kr/pages/board/law_view.asp?category=3&page=1&searchstr=&searchtype=&seq=14402&teamcode=&types=6) · [schema.org LegalService](https://schema.org/LegalService) · other rows as marked
