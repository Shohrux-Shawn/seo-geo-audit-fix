---
name: "seo-geo-audit-fix"
description: "Audit a website or site network for SEO, local SEO and GEO (AI-search visibility), prove every finding with live evidence, then plan and apply exact fixes after approval (code, redirects, structured data, sitemaps and search-console submission, CMS, Google/Naver/Kakao listings) and verify them live. Use for site audits, rankings, indexing and sitemap problems, NAP or Business Profile checks, AI-answer visibility, or 'audit this project and tell me what to fix'."
---

# SEO · Local SEO · GEO — audit and fix

This skill turns "audit this project and tell me what to fix" into a repeatable job:
**facts → live evidence → scored findings → exact fixes → applied with approval → verified live.**

It works for one site or a network (main site + satellites), in any market. It has extra notes for Korea (Naver, Daum, Kakao), where Google-only habits miss half the picture.

The value is in two things generic audits skip:
1. **Every claim has evidence** (URL + exact text, or a screenshot description). Anything not checked is marked NOT VERIFIED. A confident wrong finding costs more than a missing one, because people act on it.
2. **Every finding ends in a fix someone can actually apply.** Each fix says the exact change, who does it (website code / CMS / listing owner / content team / another business) and how to verify it. Owner decisions override generic best practice.

Reply in the user's language. Write prompts for coding agents in English unless the user says otherwise.

---

## Step 0 — Project fact sheet (do this first, every time)

Look for an existing `seo-geo-facts.md` in the project (repo root, docs/, or your notes folder). Reuse it if it exists; otherwise build it. Ask the user only for what you cannot find yourself.

```
# SEO/GEO facts — <project>
Sites (verified live, canonical host):
- https://www.example.com — role (main / satellite: practice area)
Entity:
- Legal name / office name (exact spacing):
- Parent organization / head office (if a branch):
- Address (road address, building, floor, postcode):
- Geo (lat, lng) from the site's JSON-LD:
- Phones (main / direct) and where each is used:
- Hours (exact, incl. breaks):
- Categories (Google / Kakao / Naver):
- Official profiles (GBP URL, Naver Place ID, Kakao place ID, YouTube, Instagram, directories):
Markets & engines: (e.g. Google KR, Naver, Daum, Bing; AI: Google AIO, Naver AI Briefing, Perplexity, ChatGPT, Gemini, Copilot)
Languages / hreflang set:
Access available: repo path, CMS admin, GSC, Bing WMT, Naver Search Advisor, GBP manager account, browser profile
Owner decisions (do not contradict):
- e.g. keep existing figures/stats on page X; keep repeated region wording; no '24h'/'free' claims; entity = firm, not a person
Regulatory limits (e.g. lawyer/medical advertising rules):
Deploy rules (who approves, time windows, one-site-at-a-time):
```

Why this matters: in real audits, a wrong domain list (sites that don't exist) produced false "site is down" findings, and a wrong geo in the brief produced a false NAP mismatch. **Resolve every listed domain before auditing it** (DNS + HTTP status). Drop or flag the ones that don't resolve.

---

## Step 1 — Pick tools and operating mode

- **Public pages, search, crawl:** use Firecrawl first if connected (scrape, search, map). Otherwise use WebFetch/WebSearch.
- **Rendered/JS pages, signed-in tools (GBP manager, CMS admin, Search Console UI), map apps:** use the browser (Claude in Chrome / built-in browser).
- **Code:** the repo (local or via device shell). Read the real source before proposing a fix.
- **APIs if credentials exist:** GSC Search Analytics / URL Inspection, Bing Webmaster, PageSpeed Insights. Keep keys in env only, never in output.

If this session cannot do a part (no browser, a site blocked, a login needed), switch to **delegation mode**: write a self-contained prompt for a browser agent or coding agent (see "Prompt templates" at the end). Then review its report with this skill.

Operating rules for live checks:
- Read-only by default. Never log in with typed passwords, solve CAPTCHAs, submit forms, post, review, claim listings or accept terms.
- Space search-engine queries 20–30 s apart. On reCAPTCHA or empty result pages, stop that engine and mark the rest NOT VERIFIED.
- Record the test conditions: date/time, signed-in or not, which location the engine says it is using. A signed-in manager sees different map-pack results than the public.

---

## Step 2 — Audit modules

Run the modules that fit the request. A full audit runs all of them. For each, collect evidence into a findings list (see Step 3).

### A. Reachability and crawl
- Every host variant (http/https × apex/www): first-hop status and the redirect chain. The target is **one 301 hop** to the canonical host.
- robots.txt: syntax and disallows. AI crawlers allowed or blocked: GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Bingbot, Yeti (Naver), Daum.
  - A bot with its own `User-agent` group ignores the `*` group, so it loses the shared disallows.
- Sitemaps: fetch every URL and report status codes, redirects, noindex, canonical mismatches, fake lastmod, and live URLs that are referenced (by hreflang or links) but missing from the sitemap. Run `scripts/sitemap_validate.py`.
- Ownership and submission state per engine (Google Search Console, Bing Webmaster Tools, IndexNow key, Naver Search Advisor, Daum Webmaster Tools). Protocol rules, per-engine steps and a troubleshooting table → `references/sitemaps-and-submission.md`.
- llms.txt: present, accurate, matches the entity facts.
- Soft 404s, redirect chains, mixed content, 5xx.
- Index buckets (Discovered / Crawled / 404 / redirect), Bing and Naver index reports → `references/indexing-audit.md` (for deeper work, a separate indexing-audit skill, if you have one).

### B. On-page (per template, not just the home page)
- title, meta description, H1, canonical, `lang`, hreflang (reciprocal, matches `lang`), OG image size.
- Duplicate titles and descriptions (group them). Titles cut mid-phrase. Home title equal to a location page title.
- Thin hub pages: measure characters inside `<main>`.
- Forbidden or regulated wording from the fact sheet. Search the raw HTML as well as the visible text, because hidden copy is still read by crawlers and AI.
- H1 carries the entity and topic (e.g. "<region> <entity>"), not only a slogan.
- Pixel-based title/meta limits for Korean, title tactics, H1 rules → `references/knowledge-base.md` §3.

### C. Structured data and entity
- One canonical `@id` for the organization across all sites. Satellites describe services or departments with `parentOrganization` → that `@id`. Avoid N copies of the same business.
- name, address, telephone, geo, `openingHoursSpecification`, `hasMap`, and `sameAs` (all official profiles) match the fact sheet exactly.
- A **branch-office** site keeps only its own profiles in `sameAs`; the firm's Wikidata/Wikipedia/head-office identities go on `parentOrganization` (`@id` = Wikidata URL). Each site's `image` is its own og image; add `logo`. Search thumbnails, `max-image-preview` placement and the Wikidata/Wikipedia (COI) workflow → `references/multisite-and-technical.md` §8.
- People: `ProfilePage` + `Person` (`worksFor` → org `@id`), not a LocalBusiness subtype per person.
- Articles: `image`, `publisher.logo`, dates. FAQPage only where the Q&A is visible on the page.
- Validate a sample with validator.schema.org and the Rich Results Test. Report errors and warnings verbatim.
- **Never** add Review/AggregateRating markup for testimonials the business wrote or selected itself.

### D. Performance
- PageSpeed Insights on mobile for each home template: field CWV (LCP, INP, CLS) and lab values.
- If LCP is far later than FCP, suspect a hero that is hidden until an animation runs. If CLS is high, find the shifting element (DevTools → Performance → Layout shifts).

### E. Content quality and network risk
- Templated pages at scale (same title pattern, pasted user questions), exact duplicates, cross-domain duplicate bodies.
- City × service page matrices on several domains (doorway pattern).
- **Cannibalization:** which URL actually ranks or gets clicks for each query cluster. Use GSC Pages × Queries when available.
- Cross-site linking: main ↔ satellites. Count the linking pages, check for UTM on internal links, find orphaned satellites.
- Volume, scaled-content, thin/duplicate and doorway rules → `references/content-scale-and-quality.md` §1–4 and `references/multisite-and-technical.md` §2–3.

### F. Local profile (Google Business Profile; Naver Place / Smart Place; Kakao Map)
- **Order for a business with a profile:** site audit → entity/NAP + GEO live test → strict read-only profile status check → Maps location + geo-grid test → (approval) stage-1 edits → wait 3–5 days → stage-2 edits → re-test after 2–4 weeks. Ready prompts for each step: `templates/browser-prompts/` (start with its README).
- Field by field vs the website:
  - name, primary and additional categories;
  - address and building name, pin distance from the JSON-LD geo (metres);
  - phone(s), website (no UTM), hours;
  - description, services, attributes (flag any that look untrue);
  - photos (count, entrance/sign visible), posts, Q&A;
  - reviews (count, owner replies).
- **Review-policy risk:**
  - reviews written by the owner or staff accounts;
  - bursts (many reviews in a few weeks);
  - one-review accounts;
  - scripted wording with keywords or attorney/staff names;
  - count drops (the platform filtering reviews).
  Report the pattern, not an accusation.
- Other listings on the same pin or Plus Code, and listings with a similar name: same company? sibling office? different business? Do they use our phone or website?
- **Geo-grid (Maps visibility):** `https://www.google.com/maps/search/<QUERY>/@<LAT>,<LNG>,14z` from 6–9 fixed centres (office, nearby districts, court area, transit hub, neighbouring city) × 4–6 core queries. Record our position (count to 20; "20+" if absent) and the top 3 at each point. Expect proximity to dominate; judge mainly the office-area cells.
- **Map pack on Search:** for head queries, is there a 3-pack, and are we in it?
- Compare with the 5 listings that beat us most often: category, hours, description, services, photos, review count/age, replies, posts. Note when competitors break platform rules (keyword-stuffed names, false "24h") — **do not copy that.**
- Naver Smart Place, Kakao Map and GBP specifics, local strategy → `references/korea-search.md` §6–9.

### G. Entity / NAP consistency across the web
Build one master table. Columns: Source | Name | Address/building | Phone | Hours | Website | Category | Description | People named.

Sources:
- every site (JSON-LD, footer, contact, location page, llms.txt);
- GBP; Naver Place; Kakao; Bing Places;
- vertical directories (e.g. legal or medical directories);
- YouTube and Instagram about pages;
- wiki pages;
- sibling or head-office websites;
- business directories.

Then:
- list mismatches by impact;
- propose **one canonical value per field**, with the reason;
- check business registration info where public (e.g. head office vs branch).

Sibling offices that share the brand are not competitors. Missing links between them are an easy win.

### H. Rankings and GEO (AI answers)
- Query set: brand (exact + with location), head terms (city + service), practice terms, 3–5 long-tail.
  - Google: `https://www.google.com/search?q=<Q>&gl=<cc>&hl=<lang>&pws=0`, organic positions to page 3.
  - Local engines (e.g. Naver integrated search): which section shows us (Place, website, blog, Q&A, AI briefing).
- AI engines, logged out: 3 recommendation questions, 1 "is <brand> good?", 1 "address and phone of <brand>". Record:
  - mentioned? cited URL?
  - wrong facts, quoted exactly;
  - sources used instead, and **why** they were chosen (registered credentials, directories, reviews).
- Trace every wrong AI fact back to the page it came from. Fixing that page is usually the fix.
- GEO rules (AI search bots, quotable structure, llms.txt priority, Copilot citations) → `references/knowledge-base.md` §8.

---

## Step 3 — Findings, scores, and the fix plan

Each finding:

```
ID | Severity (Critical/High/Medium/Low) | Problem + evidence (URL, exact text, numbers) | Why it matters | Exact fix | Owner (code / CMS / listing owner / content / other business) | Effort | How to verify
```

Severity guide:
- **Critical:** can demote the whole site or network, or a legal/regulatory breach. Examples: scaled templated content, doorway matrices, false claims.
- **High:** blocks local visibility or entity clarity. Examples: wrong primary category, no hours, NAP drift on the main listings, mobile CWV failure on main templates.
- **Medium:** single-hop redirects, missing sitemap URLs, schema gaps, duplicate titles.
- **Low:** cosmetic consistency.

Scores 1–10, each with a one-line reason: Technical · On-page · Local · Entity/NAP · Brand search · GEO. Score only what was verified.

Apply the **owner-decision filter** before presenting:
- drop or adjust any recommendation that contradicts the fact sheet;
- list what you dropped under "Skipped by owner decision", so nothing is silently lost.

Sort the final list by impact ÷ effort. Separate it into:
1. **Do now (technical, no content change)**
2. **Needs owner decision** (write the question in the owner's language, simple and short)
3. **Plan only / later** (structural or content work, data-dependent)
4. **Not ours** (other offices/businesses: write the message they need)

---

## Step 4 — Apply fixes (only after approval)

Ask for approval per group, unless the user already approved that exact change.

### Website code
1. Read the real source. Write a plan with the files to change.
2. Show the diff. Before committing, check:
   - only the relevant files are staged (not lockfiles or tool folders);
   - line endings are unchanged (a CRLF rewrite makes the whole file look changed and can break shell scripts);
   - no secrets.
3. Respect deploy rules (time window, one site at a time). Verify live after deploy: status, rendered HTML or JSON-LD, PageSpeed if relevant.
4. When handing off to a coding agent, give an English prompt with: the evidence, the exact change, what not to touch, the tests, and the verification. Then review the agent's report against the live site yourself, not just its claims.
5. Code recipes (redirects, canonical/hreflang, titles, JSON-LD, robots.txt, llms.txt, Core Web Vitals, internal links, thin/duplicate handling, CMS persistence) and the safe change workflow with a curl checklist → `references/implementation-playbook.md`.
6. Sitemap generation per stack (Next.js App/Pages Router, WordPress, static generators, Nginx) and submission (Search Console, Bing, IndexNow, Naver, Daum) → `references/sitemaps-and-submission.md`. Submitting or re-submitting is an action: ask first, then use `scripts/gsc_sitemaps.py submit --apply` / `scripts/indexnow_submit.py --apply`.
7. Deploy, CMS-storage and line-ending traps seen in real projects → `references/multisite-and-technical.md` §7 and `references/lessons-learned.md` §4.

### CMS / admin content
- Before trusting "saved", find where the CMS stores the content. Example failure: admin edits were written into git-tracked files and every deploy (`git reset --hard`) wiped them.
  - Snapshot the live content into the repo before the next deploy.
  - Then move the store out of the deploy path (DB, or a git-ignored or volume path), seeded once from the defaults.
- After saving, verify the public URL, not the editor.

### Listings (GBP, Naver Place, Kakao, directories)
- Before any edit, run `templates/browser-prompts/03-gbp-readonly-status-check.md` (access, every field, notices, reviews, insights). Then use `05-gbp-update-stage1.md` and, 3–5 days later, `06-gbp-update-stage2.md`.
- Edit only the owner's own listing, only with explicit OK, signed in as the manager.
- **Stage edits.** First: category, hours, description, services, extra phone, review replies. Wait 3–5 days. Then the address or building name on its own, because address edits can trigger re-verification.
- Screenshot before and after each section. Report Google's exact status messages (under review, published, error).
- Review replies: 1–2 varied sentences, no case or customer details, no keywords, no phone or URL. Skip negative reviews and reviews that describe a specific matter; list them for the owner.
- Never write, delete or buy reviews. Never claim another business's listing. Never stuff keywords into the business name. Never set "open 24 hours" unless true.
- Owner or staff reviews of their own business break platform policy. Tell the owner to delete them from their own account; do not do it for them.

### Content
- In regulated industries (law, medicine, finance), content changes need human approval.
- Batch in small groups. Keep claims verifiable: registered specialties only, no superlatives or unsupported statistics, no fake testimonials.
- Do not mass-publish to sites that a search update has just hit. Fix and consolidate first.

---

## Step 5 — Verify and re-measure

- Same day: re-open each changed page or listing in public view and confirm the change shows.
- 1–3 days: services, posts and review replies often publish late. Re-check.
- 2–4 weeks: re-run the geo-grid and map-pack tests **signed out and signed in**, the core ranking queries, and the AI questions. Compare with the baseline table. Offer to schedule this check.

---

## Bundled scripts and templates

Use these instead of writing ad-hoc code. All of them are read-only or dry-run by default (anything that sends data needs `--apply`); run any one with `--help` for usage. Secrets come from environment variables only.

- **`templates/seo-geo-facts.md`** — Step 0 fact sheet. Copy it into the project and fill it in.
- **`templates/browser-prompts/`** — six fill-in prompts for a browser agent: 01 site/network audit · 02 entity/NAP + rankings + GEO live test · 03 strict read-only Business Profile status check · 04 Maps pin/duplicates/geo-grid/map-pack test · 05 profile update stage 1 · 06 profile update stage 2. Its README gives the order and the shared rules.
- **`scripts/site_check.py <site>... --max-urls N --forbidden "a,b" --out DIR`**
  - Covers modules A/B/E: redirects, robots/AI bots, llms.txt, sitemap crawl, per-page tags, duplicates, thin pages, forbidden wording, UTM links.
  - Run it first on every site. Use `--max-urls 0` for a full crawl.
  - It runs from any machine with internet access. If this session's shell can't reach the sites, run it on the user's machine or give the command to the user.
- **`scripts/sitemap_validate.py <sitemap-or-index-url> --host www.example.com --max 500 --out DIR`**
  - Module A: follows indexes; limits, namespace, duplicates, host mismatch, lastmod format/future/fake; fetches a sample for status, redirects, noindex, canonical ≠ URL; validates hreflang alternates. Exit 1 on errors.
- **`scripts/indexnow_submit.py --host www.example.com --urls-file urls.txt [--key-location URL] [--apply]`**
  - Verifies the key file, batches up to 10,000 URLs; posts to `https://api.indexnow.org/indexnow` only with `--apply`. Key from env `INDEXNOW_KEY`.
- **`scripts/gsc_sitemaps.py list|submit --site sc-domain:example.com --sitemap URL [--apply]`**
  - Search Console sitemaps via a service account (`GOOGLE_APPLICATION_CREDENTIALS`; needs `google-api-python-client` + `google-auth`). Add the service-account e-mail in Search Console (Full/Owner to submit). `submit` requires `--apply`.
- **`scripts/nap_compare.py sources.csv canonical.json`** — module G master table and mismatches. Fill `sources.csv` from the listings you checked; `canonical.json` comes from the fact sheet.
- **`scripts/geo_grid.py plan centres.csv "q1,q2" --out DIR`** then **`summary DIR/results.csv`** — module F. `plan` gives the exact Maps URLs for you or a browser agent; `summary` turns the filled CSV into the grid table.

When you build a new helper, add it under `scripts/` following `scripts/README.md`, and list it here.

---

## Knowledge base (references/)

Distilled from real audits, research notes and incidents. Read only what the current step needs:

- **Step 0, or whenever a concrete precedent helps** → `references/case-study-multisite-law-firm.md` — a worked example of a multi-site professional-services network (architecture, owner decisions, publishing and deploy rules, measured results, what worked and what didn't).
- **Before Step 2 modules A–C and H, or when a rule of thumb is needed** → `references/knowledge-base.md` (quality and crawling, on-page limits, schema/entity, E-E-A-T, internal links, GEO, measurement).
- **Module A index buckets, or any "why isn't it indexed" question** → `references/indexing-audit.md` (condensed indexing audit: hard rules, workflows 00–10, classification, dev loop).
- **Before Step 2 module E, when planning content volume, or before writing/approving content** → `references/content-scale-and-quality.md` (volume rules, scaled-content risk, natural writing, duplicates, multilingual, Q&A pipelines, lawyer-ad compliance).
- **Korean market, modules F–H for Korea, Naver/Kakao/directories** → `references/korea-search.md`.
- **Networks of sites, a new domain, or a CMS migration** → `references/multisite-and-technical.md` (satellite architecture, doorway/cannibalisation, setup checklist, migration, deploy gates).
- **Step 3 (before scoring) and Step 4 (before applying)** → `references/lessons-learned.md` (symptom → cause → fix → early detection).
- **Step 4, any code change** → `references/implementation-playbook.md` (safe change workflow, redirects, canonical/hreflang, titles, JSON-LD, robots.txt, llms.txt, Core Web Vitals, internal links, thin/duplicate content, CMS persistence, curl checklist).
- **Module A sitemaps, Step 4 sitemap fixes, any ownership or submission question** → `references/sitemaps-and-submission.md` (protocol, special sitemaps, splitting, generation per stack, robots.txt, Google/Bing/IndexNow/Naver/Daum steps, monitoring, troubleshooting).
- **Citing a rule, or checking whether it is still current** → `references/sources.md` (verified official URLs, with the verification date; rules not backed by an engine document are marked "field experience").

When a reference and the fact sheet disagree, the fact sheet's owner decisions win; list the conflict under "Skipped by owner decision".

---

## Report template

```
# <Project> — SEO · Local · GEO audit (<date>)
## Summary (5 bullets: biggest risk, fastest win, where we rank, entity/NAP state, AI visibility)
## Test conditions (time, signed-in?, location, limits hit)
## Scores (6 areas, 1–10, one-line reasons)
## Findings by severity (table per Step 3)
## Fix plan: Do now / Needs owner decision / Plan only / Not ours
## Tables: per-site checks · NAP master table + canonical values · rankings · geo-grid · GEO answers
## Skipped by owner decision
## NOT VERIFIED (item + reason)
## Owner summary (6–10 lines, owner's language, plain words, ends with the decisions needed)
```

For a daily or after-work report to a manager, use: **found → done** per item (numbered), then "requests for you", in the manager's language.

---

## Prompt templates for delegation

Use these when another agent must do the live work. Fill them from the fact sheet, and always include the hard rules and the owner decisions. For browser work, prefer the complete templates in `templates/browser-prompts/`; the outlines below are for cases they don't cover.

**Browser audit agent:**
"You are a hands-on SEO/local/GEO tester in my real Chrome. Live checks only, read-only, no guessing." Then:
- the fact sheet;
- the known findings to re-verify;
- the hard rules (no login, no CAPTCHA solving, no edits, 20–30 s spacing, NOT VERIFIED);
- the modules to run, with exact URLs and queries;
- the output sections from the report template, plus an owner summary in their language.

**Browser listing-fix agent:**
- the exact field values to set (category names, hours, description text, services);
- the "do not" list (name, address, other listings, reviews, photos, terms/ads);
- the process: screenshot → edit one section → save → re-open → before/after table with Google's exact messages.

**Coding agent:** evidence → exact change → files → constraints (owner decisions, deploy rules) → tests → verification commands → "show diff, commit only after OK".

---

## Korea notes

- Engines: Google KR, Naver (largest local engine; Smart Place drives the map results), Daum/Kakao.
  - Daum Webmaster verification goes in robots.txt (`#DaumWebMasterTool:<hash>:<suffix>`).
  - Naver's crawler is Yeti.
- Kakao Map shows the building name from Kakao's own address database. Daum search cards copy Kakao's place data.
- Naver pages often block automated browsers. If they do, ask the owner to check the Naver Search Advisor and Smart Place dashboards, and mark it NOT VERIFIED.
- Business registration numbers: the middle code 85 means a corporate branch. Use it to tell a branch from the head office.
- Naver supports IndexNow (verified 2026-11-02); Naver has no public sitemap-submission API (its crawl-request API is partner-only). Naver rejects sitemap files of 10 MB or more. Details → `references/sitemaps-and-submission.md` §6.4.
- Lawyer advertising (Korean Bar Association Regulations on Attorney Advertising, under the Attorney-at-Law Act):
  - certification wording ("certified by the Korean Bar Association as a <field> specialist") only for fields the lawyer has registered; for plain "<field> specialist" wording follow `references/content-scale-and-quality.md` §9 and confirm with the lawyer responsible for advertising;
  - no "best", "No. 1" or "only";
  - no satisfaction or results figures without a documented basis;
  - name the lawyer responsible for advertising.
  Fake or seeded reviews also breach the Act on Fair Labeling and Advertising.
- Nuance on "specialist" wording (since the 2021 revision of the Regulations, plain "<field> specialist" is allowed for fields actually practised; only certification wording is limited to registered fields), and the full compliance table → `references/content-scale-and-quality.md` §9.
