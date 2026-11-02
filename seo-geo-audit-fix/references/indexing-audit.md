# Indexing audit — condensed (Google · Bing · Naver)

A condensed version of a fuller indexing-audit workflow. For deeper work, use a separate
indexing-audit skill, if you have one (with its own tools, rules, workflows 00–10, templates
and examples). Sitemap and submission mechanics: `sitemaps-and-submission.md`.
**(field experience)** marks the author's own rules from audits.

## Contents
1. When to use which skill
2. Hard rules (override everything)
3. Workflow 00–10 in short
4. Classification categories and typical root causes
5. What "good" looks like (live check table)
6. Dev-AI loop and deploy verification

---

## 1. When to use which skill

| Situation | Use |
|---|---|
| "Why aren't my pages indexed?", "Discovered – currently not indexed" grew, Bing sitemap error, Naver index count flat, re-audit at +14/+28 days | **a separate indexing-audit skill, if you have one** (typical tools: a Search Console harvester, a page checker, a sitemap checker, a classifier, URL-pattern grouping, Bing and GSC API clients, an nginx bot-log summary). Without one: this file + `scripts/sitemap_validate.py` + `scripts/gsc_sitemaps.py`. |
| Rankings, local pack, NAP, Business Profile, AI-answer visibility, content/compliance, network risk | **this skill** (seo-geo-audit-fix), modules A–H |
| Full audit of a site that also has index problems | This skill for modules A–H; switch to the indexing-audit skill (or this file) for module A's index buckets, then bring its findings back into the Step 3 table |
| Quick one-off (one URL, one bucket) | This file is enough |

Typical modes of a full indexing audit: **Full audit** (01→06, then 07) · **Fix wave** (07→08 per item) · **Re-audit** (10) · **Single question** (jump to the matching workflow).

Sources: (field experience)

## 2. Hard rules (override everything)

**Accounts and safety**
- Never type passwords; the user signs in to Search Console / Bing / Naver.
- Consoles are read-only unless the user says yes to: sitemap (re)submit, "Validate fix", "Request indexing".
- Never sign out, change settings, add/remove users or properties. Never solve or bypass CAPTCHAs.
- No production writes (code, nginx, DB) without approval; give commands, the user runs them.
- Secrets (API keys, service-account JSON, cookies) only in env vars, never in the repo or report.

**Search-console actions**
- **Never press "Validate fix" on "Not found (404)" or "Page with redirect".** They shrink on their own; validation only produces "failed" noise. (field experience)
- Validate only buckets you actually fixed (Discovered / Crawled / Duplicate / noindex), and only after the fix is live. An old "Passed" validation may hide the button — fine; sitemap resubmit + internal links do the work.

**Status codes**
- Deleted → **410** (Google treats 404 and 410 the same; 410 is the honest signal). Unknown → **404** (not a redirect to `/`, which is a soft 404). `?page=N` beyond the last page → 404 + `Cache-Control: no-store`.
- Backend/API failure on a list or detail page → **503 + Retry-After + no-store**, never 404, never an empty 200.
- Moved → **301/308 in one hop** to the final URL; internal links point at the final URL.

**Sitemaps**
- `<lastmod>` = real content date. Never `now()`, build time or cache time. No reliable date → omit it.
- View counters must not touch `updatedAt` (e.g. `timestamps: false` on the increment).
- Empty list pages → `noindex,follow` and out of the sitemap until they have items.
- Keep the sitemap URL stable (`/sitemap.xml` becomes the index).
- Never an empty or partial 200; cold cache → 503 + Retry-After.
- Every `<loc>`: 200, indexable, self-canonical (compare decoded + NFC-normalised).

**Rendering**
- Anything to be indexed or followed is in the initial HTML (SSR/ISR) as a real `<a href>`.
- ISR must not cache an error or empty result; runtime regeneration throws so the last good copy stays.

**Process with the dev AI**
- One item per prompt, in English, with acceptance checks. Implement → report → **review** → commit → push → user deploys → **you verify on prod**. Deploy per item.
- Before `git reset --hard` / `git pull` on the server: `git status --short` must be empty; check the env file (e.g. API URL) before and after.

Sources: [HTTP status codes](https://developers.google.com/search/docs/crawling-indexing/http-network-errors) · [Redirects](https://developers.google.com/search/docs/crawling-indexing/301-redirects) · [Sitemaps ping/lastmod post](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping) · [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) · [Link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) · [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) · validation and process rules: (field experience)

## 3. Workflow 00–10 in short

| # | Step | Key points |
|---|---|---|
| 00 | Baseline | Per engine, dated: GSC indexed / not indexed / count per reason + validation status, sitemaps (type, last read, discovered), 28-day clicks/impressions. Bing: sitemap status + error text, indexed by folder, referring domains (how many are your own), IndexNow. Naver (user collects): impressions/clicks, site diagnosis, collection status, content spread, sitemap status. Server: sitemap check summary, bot-log summary. GSC lags by days. |
| 01 | GSC collect | Reason URL lists are **not** in the API. Browser: open Page indexing with `hl=en`, viewport ≥ 1400 px, export each reason (≤ 1,000 rows each — the UI cap). API (`scripts/gsc_sitemaps.py list`, URL Inspection API): sitemaps + ~2,000 inspections/day/property — good for scheduled checks. |
| 02 | Bing collect | Prefer the official API (`BING_WEBMASTER_API_KEY`): feeds, crawl issues, crawl stats, URL info. UI fallback; `site:` searches on bing.com hit CAPTCHAs fast. Look for "Failed to download" with a working file (→ server logs), stale `http://` entries, spam URLs still indexed (→ 410), self-link-dominated backlinks, IndexNow key served. |
| 03 | Naver collect | The owner sends screenshots (see `korea-search.md` §2). Flat index count + growing sitemap → discovery problem: internal links + RSS. Low collection → Yeti 429/444. |
| 04 | Live check | `scripts/sitemap_validate.py` on every sitemap (status, redirect, X-Robots-Tag, meta robots, canonical, hreflang; exits non-zero on errors). A page checker on 2–3 URLs per (reason × pattern) plus probes: `/`, list pages, `?page=2`, `?page=999`, `?page=1`, `/x/undefined`, unknown slug, deleted id, locale variant of a single-language page. |
| 05 | Classify | Group URLs by pattern; per site write rules = (reason prefix, path regex, category, diagnosis, fix); re-run until nothing is unclassified. Confirm each diagnosis with the live check, never from the URL alone. |
| 06 | Report | Every claim has a number and an example URL; each category row: count, diagnosis, fix, acceptance check, priority. Attach the CSV, live-check output, sitemap URL list. State what must **not** be done. End with deploy order and re-audit dates (+14, +28). Body in the reader's language; dev prompts in English. |
| 07 | Dev handoff | See §6 and `implementation-playbook.md`. |
| 08 | Deploy + verify | The user deploys the reviewed commit by id. Re-run the live check and `sitemap_validate.py`, follow every new link once, report check → expected → actual. After the wave: resubmit sitemaps (with a yes), validate only fixed buckets, write a dated summary, schedule the re-audit. |
| 09 | Server logs | Add `host=$host rt=$request_time` to the nginx log format first (several sites on one nginx). Codes: 429 = rate limit hit by a crawler (exempt verified bots); 444 = `default_server` closing an unknown Host (a bug only if it's your domain); 499 = slow response; 5xx = crawlers back off; 301 on a sitemap fetch = an old `http://`/non-www sitemap still registered. Test with the bot UA via curl from the server. |
| 10 | Re-audit (+14/+28 d) | Repeat 00; before/after table per engine and per child sitemap; the sitemap check must show 0 errors; harvest only buckets that didn't shrink. Expected: Discovered ↓, Indexed ↑, 404/redirect slowly ↓, noindex stable. If Discovered didn't move after 28 days → crawl stats, Googlebot volume/errors in logs, content quality/duplication (scaled-content risk). |

Sources: [Page indexing report](https://support.google.com/webmasters/answer/7440203) · [Sitemaps report](https://support.google.com/webmasters/answer/7451001) · [URL Inspection API](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect) · [API usage limits](https://developers.google.com/webmaster-tools/limits) · [Bing Webmaster API access](https://learn.microsoft.com/en-us/bingwebmaster/getting-access) · workflow design: (field experience)

## 4. Classification categories and typical root causes

| Prefix | Meaning |
|---|---|
| `P0-…` | Blocks discovery/indexing of real content: no crawlable path, content not in SSR HTML, sitemap broken |
| `P1-…` | Wrong status or structure: soft 404, template params in links, locale links to missing pages, duplicates, empty shells |
| `P2-…` | Quality, encoding, cosmetic, small counts |
| `OK-…` | Correct as is: deleted (410), legacy redirects, intentional noindex, robots-blocked login |

| Bucket | Usual cause | Fix |
|---|---|---|
| Discovered – not indexed (large) | Button/JS pagination; `?page=N` canonical → page 1; no related links; client-only list blocks; no archive. Also: pages reachable only through `hreflang` but not in the sitemap; templated near-duplicates; formulaic title suffixes. | Crawlable pagination, archive, related links, SSR blocks; align "open" and "offered" lists; rewrite formulaic titles |
| Soft 404 | Catch-all route redirecting unknown paths to `/`; SSR shell with client-loaded text (terms/privacy pages) | 404/410; SSR the text or drop it from the sitemap |
| Not found on `/{lang}/…` | Language switcher, `hreflang` or `next/link` adding the active locale to single-language routes | Pin links to the default locale; 404 honestly for untranslated pages |
| Duplicate, Google chose different canonical | Near-identical posts (forms, Q&A batches), empty detail shells | Merge/differentiate; 404 empty shells |
| Excluded by noindex | Often an old crawl | Verify live; keep in the sitemap if now 200/indexable |
| Links with `undefined`, `[id]`, `__config__` | href built from a missing field | Fix the template |

Measured caveat: "thin" was **not** the cause in one bucket — 84% of thin articles were indexed; age and a templated title suffix were (same-age articles: 50% stuck with the suffix vs 0% without). Measure before choosing a fix. (field experience)

Sources: [Page indexing report](https://support.google.com/webmasters/answer/7440203) · [Canonicalization](https://developers.google.com/search/docs/crawling-indexing/canonicalization) · [Localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions) · categories and causes: (field experience)

## 5. What "good" looks like (live check)

| Page type | Expect |
|---|---|
| Real content | 200, indexable, self-canonical, H1 = headline, a few hundred+ characters of text, related links in SSR |
| List page N>1 | 200, self-canonical `?page=N`, `<a href>` to neighbours |
| `?page=1` | 301/308 to the bare list URL |
| Beyond the last page | 404, `no-store` |
| Deleted record | 410 |
| Unknown path | 404 (not a redirect to `/`) |
| Backend down | 503 + Retry-After + no-store |
| Empty list | `noindex,follow`; not in the sitemap |

Sources: [HTTP status codes](https://developers.google.com/search/docs/crawling-indexing/http-network-errors) · [Block indexing with noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing) · table: (field experience)

## 6. Dev-AI loop and deploy verification

- Prompt (keep a dev-prompt template): what is already done and verified on prod → the decision (approved / not approved / do X instead) → acceptance checks to report (counts, curl results, diffs) → "Report before committing. Do not commit or push until I approve."
- Typical fix order, one commit and deploy each: crawlable pagination + 503 on failure → archive pages → related block → titles/descriptions/H1 → soft-404 fix → SSR for link-carrying blocks → sitemap index with real lastmod → footer archive link → RSS (for Naver).
- Review checklist: the diff touches only needed files (spot-check untouched pages' HTML); acceptance numbers present and plausible (URL totals = previous + added − removed, with reasons); failure paths tested (API down, empty, unknown id); lastmod from real dates; did it push before review?
- If newer unreviewed commits are already on the remote, deploy the reviewed commit **by id** (`git fetch && git reset --hard <id>`), never "whatever is on master".
- Never trust "deployed"; verify on prod yourself (`implementation-playbook.md` §12).

Sources: (field experience)
