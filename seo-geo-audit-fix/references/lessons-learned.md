# Lessons learned — mistakes and their fixes

Each entry: **Symptom → Cause → Fix → How to detect early.** Grouped by area; newest first
inside each group. All incidents come from real projects and are anonymised; dates are year-month.
Everything in this file is **(field experience)**; where an engine document backs the fix, it is
listed under the section's Sources.

## Contents
1. Audit scoping and evidence
2. Local profiles and reviews
3. Network, entity and cannibalisation
4. CMS, deploy and code hygiene
5. Indexing, sitemaps and i18n
6. Content pipeline and volume
7. Working with AI agents and checkers

---

## 1. Audit scoping and evidence

**Non-existent domains in the audit brief (2026-10)**
- Symptom: "site down" findings for 6 domains.
- Cause: the prompt listed planned satellite domains that were never registered.
- Fix: drop or flag them; audit only domains that resolve.
- Detect early: resolve DNS and HTTP status for every listed domain in Step 0.

**AI answer repeats a false claim from our own page (2026-11)**
- Symptom: an AI engine said the office is "near the court" (it isn't).
- Cause: the business's own page said so; AI engines quote pages verbatim.
- Fix: correct the source page, then re-test the AI question weeks later.
- Detect early: for every wrong AI fact, search the site's raw HTML for the phrase.

**Wrong redirect code diagnosed through a proxy (2026-08)**
- Symptom: "302 is the main problem" finding.
- Cause: the fetch tool's proxy reported 302; the server actually sent 308/301.
- Fix: retracted after a live curl check.
- Detect early: confirm status codes with curl from a clean shell before reporting.

**Wrong "thin content" hypothesis (2026-09)**
- Symptom: plan to lengthen 173 articles to fix a "Discovered" bucket.
- Cause: assumed thinness; measurement showed 84% of thin pages indexed. Age and a templated title suffix were the real variables.
- Fix: rewrote 52 titles instead.
- Detect early: cross the bucket export with candidate causes, controlling for age, before choosing a fix.

Sources: [URL Inspection / verifying live state](https://support.google.com/webmasters/answer/9012289) · [HTTP status codes](https://developers.google.com/search/docs/crawling-indexing/http-network-errors)

## 2. Local profiles and reviews

**Wrong GBP category, no hours (2026-11)**
- Symptom: almost no map-pack presence for "<city> lawyer".
- Cause: primary category "corporate office" and no opening hours; competitors use law categories.
- Fix: law-office/lawyer primary category, practice secondary categories, real hours.
- Detect early: compare category and hours with the top 5 local competitors first in module F.

**Reviews filtered 8 → 6 (2026-11)**
- Symptom: review count dropped.
- Cause: a burst of keyword-laden reviews plus owner/staff reviews.
- Fix: never script, seed or ask staff for reviews; owner deletes own-account reviews; steady, open-ended asks only.
- Detect early: watch velocity, one-review accounts, repeated keywords or staff names, count drops.

**NAP split across Kakao listings (2026-09)**
- Symptom: 10 offices, each pointing to a different site/blog; two building names for one address; three name formats; one duplicate listing.
- Cause: listings created independently over years.
- Fix: one NAP canon table; one name template; website → own location page; merge duplicates.
- Detect early: search the brand on every map app and fill the NAP master table.

Sources: [Guidelines for representing your business](https://support.google.com/business/answer/3038177) · [Maps content: fake engagement](https://support.google.com/contributionpolicy/answer/11414422) · [Kakao Map store management](https://kakaobusiness.gitbook.io/main/partner/smb/channel/service_biz/mystore)

## 3. Network, entity and cannibalisation

**Satellites invisible, main `/location` pages ranking instead (2026-11)**
- Symptom: practice satellites ranked almost nowhere for their own queries.
- Cause: the main site's region pages targeted the same "<city> + practice" queries — cannibalisation across domains.
- Fix: one owner URL per query cluster; link the other to it or trim it.
- Detect early: GSC Pages × Queries per property; list which URL wins each cluster.

**Sibling offices outrank us for the brand (2026-11)**
- Symptom: other offices of the same firm appeared above the main office for the brand query.
- Cause: the brand entity was never mapped; no cross-links.
- Fix: map every office/listing of the brand; link siblings; treat them as part of the entity.
- Detect early: brand query on Google, Naver, Kakao in Step 0.

**Every site showed only one office (2026-09)**
- Symptom: 10 real offices, all sites/schema list one.
- Cause: single NAP constant modelled one office.
- Fix: a location page + LegalService per real office.
- Detect early: compare the map-app listing count with schema `address` count.

**Template region pages near-identical (2026-09)**
- Symptom: raw similarity 0.39 looked "different".
- Cause: city names inflate raw difference; with names neutralised 0.89.
- Fix: per-host switch; cohort opening; real per-region blocks.
- Detect early: neutralise names before measuring similarity.

Sources: [Spam policies (doorway abuse)](https://developers.google.com/search/docs/essentials/spam-policies) · [LocalBusiness structured data](https://developers.google.com/search/docs/appearance/structured-data/local-business)

## 4. CMS, deploy and code hygiene

**Admin edits wiped on every deploy (2026-10)**
- Symptom: legal-page edits saved in the admin disappeared after deploys.
- Cause: the CMS wrote to git-tracked `data/*.json`; deploy runs `git reset --hard`.
- Fix: snapshot live content into the repo once; move runtime content to the DB or a git-ignored volume.
- Detect early: before trusting "saved", find where the CMS writes and whether deploy touches that path.

**CRLF rewrite made full-file diffs (2026-10; also 2026-09)**
- Symptom: every line changed in the diff; batch scripts broke.
- Cause: a coding agent / text-mode edit changed line endings.
- Fix: restore original endings; edit binary-sensitive files in binary mode.
- Detect early: `git diff --stat` vs `git diff --ignore-space-at-eol --stat` before commit.

**Imported legal page still carried another business's name (flagged 2026-09, still present 2026-10)**
- Symptom: an imported terms-of-service page still contained another firm's name.
- Cause: copied text never reviewed.
- Fix: replace with the firm's own terms.
- Detect early: grep all legal pages and templates for other brand names.

**False claims in site templates (2026-09)**
- Symptom: "consultations 24 hours, 365 days" in templates and schema `priceRange: "free consultation"`, while consultations are paid.
- Cause: template strings outside the content QC's reach.
- Fix: grep the sites for the local-language words for "free", "24 hours" and "365 days" and replace them with an honest CTA.
- Detect early: run the forbidden-wording scan on raw HTML of every template.

**Verification missing on the main site (2026-08 → resolved 2026-09)**
- Symptom: no Google/Naver verification meta on the main site in production.
- Cause: env variables not set; satellites hard-coded tokens in config.
- Fix: HTML-file verification was already in place; meta added as fallback.
- Detect early: check both meta and file methods.

**Tenant lists out of sync**
- Symptom: editor 403s on a new satellite; IndexNow silently skipped.
- Cause: domain missing from the origin resolver / IndexNow map.
- Fix: one checklist line per tenant list.
- Detect early: create one test record from the new domain and check logs.

Sources: [Verify site ownership](https://support.google.com/webmasters/answer/9008080) · [General structured data guidelines (markup must match accurate, visible content)](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) · fixes: `implementation-playbook.md` §1 and §11

## 5. Indexing, sitemaps and i18n

**Open but not offered: 1,386 URLs stuck (2026-09)**
- Symptom: huge "Discovered – not indexed" on locale pages.
- Cause: the locale gate and the sitemap used different lists; Korean pages announced the extra pages via hreflang.
- Fix: one list for gate, hreflang, switcher, sitemap, footer; build-time assert.
- Detect early: diff "URLs returning 200" against "URLs in sitemap".

**Empty 200 sitemap when the API was down (2026-09)**
- Symptom: 847 → 328 URLs, articles 0, no error.
- Cause: `catch {}` + `?? []` + `errorPolicy: 'all'`.
- Fix: 503 + Retry-After + no-store on any data failure.
- Detect early: build against a dead/erroring/hanging stub API.

**lastmod = last read date (2026-09)**
- Symptom: 1,221 of 1,231 articles "changed", 494 in one day.
- Cause: view counter `$inc` moved `updatedAt`.
- Fix: `timestamps: false` on counters; omit lastmod until a real content date exists.
- Detect early: compare `updatedAt` vs `createdAt` on unedited records.

**Locale added to single-language links (2026-09)**
- Symptom: 68 live broken links (3 even in the default language).
- Cause: `next/link`/`router.push` add the active locale; copied literals pointed to another site's route.
- Fix: pin default locale; read site values from config.
- Detect early: runtime link gate on the running build.

**Nav-hidden page dropped from the sitemap (2026-09)**
- Symptom: 200, indexable page never offered.
- Cause: one config controlled both menu and sitemap.
- Fix: separate decisions; leave the sitemap only via noindex.
- Detect early: the 200-vs-sitemap diff above.

**Naver logo never shown (2026-07)**
- Symptom: no favicon in Naver results.
- Cause: `/favicon.ico` disallowed in robots.txt and 308-redirected.
- Fix: rewrite to an image with 200; un-block.
- Detect early: `curl -I /favicon.ico`.

**Deleted pages lingering in Naver (2026-09)**
- Symptom: 23 URLs shown as "inaccessible" in Naver for weeks.
- Cause: IndexNow pinged on create/update only.
- Fix: ping on delete too.
- Detect early: list webhook/ping events per CRUD action.

Sources: [Localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions) · [Sitemaps ping/lastmod post](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping) · [IndexNow documentation](https://www.indexnow.org/documentation) · [Naver: IndexNow FAQ](https://searchadvisor.naver.com/guide/indexnow-faq) · mechanics: `sitemaps-and-submission.md`

## 6. Content pipeline and volume

**Bulk publishing bursts (2026-08)**
- Symptom: 485 pages in 3.5 h (≈3/min).
- Cause: backlog pushed at once.
- Fix: drip only; spread backlogs over days.
- Detect early: per-hour counts from the upload log.

**Formulaic titles everywhere (2026-08/09)**
- Symptom: fixed `<name> [keyword]` prefix on every title; a templated suffix on Q&A titles.
- Cause: a style guide forcing one pattern.
- Fix: titles from the question the body answers; prefix removed 2026-09.
- Detect early: count the most common title prefix/suffix share per site.

**Topic bank looked full but wasn't (2026-09)**
- Symptom: three publishing gaps; 280 "unused" topics.
- Cause: 220 were duplicates; the similarity metric was too weak.
- Fix: rare-topic-word duplicate check validated on known pairs.
- Detect early: test the duplicate checker on known duplicate pairs.

**Drafts auto-published (2026-08, again 2026-09)**
- Symptom: unfinished drafts went live.
- Cause: a draft script wrote into the auto-published folder.
- Fix: written writer-list per auto-consumed folder; separate draft folder.
- Detect early: list every process that writes into a watched folder.

**Late correction never applied (2026-09)**
- Symptom: FAQ tails stayed on 3 live articles.
- Cause: the duplicate gate (correctly) blocked re-publishing.
- Fix: in-place edit keeping the id.
- Detect early: have the post-publication edit path ready before publishing.

Sources: [Spam policies (scaled content abuse)](https://developers.google.com/search/docs/essentials/spam-policies) · [Influencing title links](https://developers.google.com/search/docs/appearance/title-link)

## 7. Working with AI agents and checkers

**Parallel agents all "clean", 6 collisions together (2026-09)**
- Cause: each agent sees only its own slice; corrections collided again.
- Fix: one global check after every parallel round, incl. correction rounds.
- Detect early: never accept per-agent PASS as the batch result.

**Agent rewrote with unverified facts**
- Cause: agents restate rules and numbers confidently.
- Fix: every figure, rule, date in an agent report is unverified until checked at the source.
- Detect early: spot-check 3 claims per report.

**Own audit script: 45 false errors (2026-09)**
- Cause: it treated generator markup as author markup.
- Fix: validate the checker on a known-good batch.
- Detect early: compare tag profiles of new vs approved batches.

**Timeout that never fired (2026-09)**
- Cause: `init?.signal ?? mine` never used `mine` because the client always sets a signal.
- Fix: `AbortSignal.any`; per-request signal; short-circuit after first failure.
- Detect early: test against a stub that never answers.

Sources: (field experience) — no engine documentation covers agent and checker workflows.
