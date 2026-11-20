---
name: "seo-geo-audit-fix"
description: "Audit any website or web app (local business, e-commerce, SaaS/web app, content/media, marketplace/UGC, docs, multi-site network; any framework or CMS, including client-rendered SPAs) for SEO, local SEO where it applies, and GEO (AI-search visibility), prove every finding with live evidence, then plan and apply exact fixes after approval (code, rendering, redirects, structured data, sitemaps and search-console submission, CMS, Google/Naver/Kakao listings) and verify them live. Also covers the off-site entity layer AI engines read (Wikidata, Wikipedia, Namuwiki, knowledge panel, profiles, earned mentions). Use for site audits, rankings, indexing and sitemap problems, JavaScript/SPA rendering and AI-crawler visibility, e-commerce facets and product data, keeping app routes out of the index, NAP or Business Profile checks, AI-answer visibility, 'what does ChatGPT say about our company', Wikidata/Wikipedia/knowledge-panel work, or 'audit this project and tell me what to fix'."
---

# SEO · GEO · Local SEO — audit and fix for any website or web app

This skill turns "audit this project and tell me what to fix" into a repeatable job:
**facts → live evidence → scored findings → exact fixes → applied with approval → verified live.**

It works for any kind of website or web app, one site or a network, on any stack, in any market. Step 0 sets the **site profile** (local business, e-commerce, SaaS/web app, content/media, marketplace/UGC, docs, multi-site network), and the profile decides which modules run: a SaaS dashboard needs no Business Profile check, a local office needs no faceted-navigation audit. Rendering (what crawlers and AI engines receive without JavaScript) is checked on every site. Extra notes for Korea (Naver, Daum, Kakao), where Google-only habits miss half the picture, apply only when Korea is a market.

The value is in two things generic audits skip:
1. **Every claim has evidence** (URL + exact text, or a screenshot description). Anything not checked is marked NOT VERIFIED. A confident wrong finding costs more than a missing one, because people act on it.
2. **Every finding ends in a fix someone can actually apply.** Each fix says the exact change, who does it (website code / CMS / listing owner / content team / another business) and how to verify it. Owner decisions override generic best practice.

Reply in the user's language. Write prompts for coding agents in English unless the user says otherwise.

---

## Step 0 — Site profile and project fact sheet (do this first, every time)

**0a. Site profile.** For every site, record:
- **Profile(s):** local business · e-commerce · SaaS/web app · content/media · marketplace/UGC · docs · multi-site network (a site can have several).
- **Rendering:** static · server-rendered · hybrid · client-rendered SPA.
- **Stack:** framework / CMS / platform, hosting / CDN.
- **Markets and languages.**

Then open `references/site-profiles.md` §2 (module routing table): it says which Step 2 modules run, which profile checks (module J) apply, and which score areas replace "Local" and "Entity/NAP" for non-local sites. Modules that do not apply are reported as "not applicable", never silently skipped.

**0b. Fact sheet.** Look for an existing `seo-geo-facts.md` in the project (repo root, docs/, or your notes folder). Reuse it if it exists; otherwise build it from `templates/seo-geo-facts.md`. Ask the user only for what you cannot find yourself. Fill the core block for every project and only the blocks of the profiles that apply:

```
# SEO/GEO facts — <project>
Sites (verified live, canonical host) — role · profile(s) · rendering · stack:
- https://www.example.com — main · e-commerce · SSR · <framework/CMS>, <host/CDN>
Entity (all profiles):
- Legal name / brand name (exact spacing); parent organization if any:
- Official profiles (social, app stores, review platforms, directories):
- Entity IDs (Wikidata QID, Wikipedia pages per language, Knowledge Graph ID, LinkedIn, Crunchbase):
- Canonical description (1–2 neutral sentences reused on every profile):
Local business only:
- Address (road address, building, floor, postcode), geo (lat, lng) from JSON-LD:
- Phones (main / direct) and where each is used; hours (exact, incl. breaks):
- Categories (Google / Kakao / Naver) and local profile IDs (GBP, Naver Place, Kakao place):
E-commerce only: catalogue size, platform, feed (Merchant Center etc.), facet/parameter list, out-of-stock policy
SaaS / web app only: public vs private hosts/paths, sign-in URL, preview/staging hosts, review platforms
Content / UGC / docs only: authors, publishing volume, versioning, moderation rules
Markets & engines: (e.g. Google <cc>, Bing, Naver, Daum; AI: Google AIO, ChatGPT, Perplexity, Gemini, Copilot, Naver AI Briefing)
Languages / hreflang set:
Access available: repo path, CMS admin, GSC, Bing WMT, local webmaster tools, profile manager accounts, browser profile
Owner decisions (do not contradict):
- e.g. keep existing figures/stats on page X; no '24h'/'free' claims; entity = company, not a person
Regulatory limits (e.g. legal/medical/financial advertising rules):
Deploy rules (who approves, time windows, one-site-at-a-time):
```

Why this matters: in real audits, a wrong domain list (sites that don't exist) produced false "site is down" findings, and a wrong geo in the brief produced a false NAP mismatch; a wrong profile (auditing an app as a local business) fills a report with irrelevant findings. **Resolve every listed domain before auditing it** (DNS + HTTP status). Drop or flag the ones that don't resolve.

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

Run the modules that fit the request and the site profile (`references/site-profiles.md` §2). A full audit runs every module that applies to the profile; mark the others "not applicable" with the reason. For each, collect evidence into a findings list (see Step 3).

### A. Reachability and crawl
- Every host variant (http/https × apex/www): first-hop status and the redirect chain. The target is **one 301 hop** to the canonical host.
- robots.txt: syntax and disallows. AI crawlers allowed or blocked: GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Bingbot, Yeti (Naver), Daum.
  - A bot with its own `User-agent` group ignores the `*` group, so it loses the shared disallows.
- Sitemaps: fetch every URL and report status codes, redirects, noindex, canonical mismatches, fake lastmod, and live URLs that are referenced (by hreflang or links) but missing from the sitemap. Run `scripts/sitemap_validate.py`.
- Ownership and submission state per engine (Google Search Console, Bing Webmaster Tools, IndexNow key, Naver Search Advisor, Daum Webmaster Tools). Protocol rules, per-engine steps and a troubleshooting table → `references/sitemaps-and-submission.md`.
- llms.txt: present, accurate, matches the entity facts.
- Soft 404s, redirect chains, mixed content, 5xx.
- Index buckets (Discovered / Crawled / 404 / redirect), Bing and Naver index reports → `references/indexing-audit.md` (for deeper work, a separate indexing-audit skill, if you have one).

### A2. Rendering and JavaScript (every site)
- For each template (home, listing, detail, article): compare the **raw server HTML** (what AI crawlers and link previews get; they do not run JavaScript) with the **rendered HTML** (URL Inspection live test or Rich Results Test). Main text, title, description, canonical, robots, hreflang, JSON-LD and `<a href>` links must be in the raw HTML.
- Unknown URLs return a real 404 from the server (not a 200 shell); redirects are HTTP 301/308, not JavaScript.
- Navigation uses real links, not click handlers; no hash routes for content; infinite scroll and "load more" have paginated URLs.
- Scripts, styles and API endpoints needed for rendering are not blocked in robots.txt; JSON-LD is not injected only by a tag manager.
- Test commands, failure list and fixes by preference (SSR/SSG → pre-render → split marketing site → server-side meta → dynamic rendering as a dated bridge) → `references/rendering-and-javascript.md`; where each control lives per framework/CMS/host → `references/stacks.md`.

### B. On-page (per template, not just the home page)
- title, meta description, H1, canonical, `lang`, hreflang (reciprocal, matches `lang`), OG image size.
- Duplicate titles and descriptions (group them). Titles cut mid-phrase. Home title equal to a location page title.
- Thin hub pages: measure characters inside `<main>`.
- Forbidden or regulated wording from the fact sheet. Search the raw HTML as well as the visible text, because hidden copy is still read by crawlers and AI.
- H1 carries the entity and topic (e.g. "<region> <entity>"), not only a slogan.
- Pixel-based title/meta limits for Korean, title tactics, H1 rules → `references/knowledge-base.md` §3.

### C. Structured data and entity
- Types follow the profile: `Organization` (every site) plus a `LocalBusiness` subtype (local), `Product`/`Offer` (e-commerce), `SoftwareApplication` (SaaS), `Article` with a real author (content), `QAPage`/`DiscussionForumPosting` (UGC) → `references/site-profiles.md` §3–8. Markup must match the visible page (prices, availability, ratings).
- One canonical `@id` for the organization across all sites. Satellites describe services or departments with `parentOrganization` → that `@id`. Avoid N copies of the same business.
- name, `logo` and `sameAs` (all official profiles) match the fact sheet exactly; for local businesses also address, telephone, geo, `openingHoursSpecification` and `hasMap`.
- A **branch-office** site keeps only its own profiles in `sameAs`; the firm's Wikidata/Wikipedia/head-office identities go on `parentOrganization` (`@id` = Wikidata URL). Each site's `image` is its own og image; add `logo`. Search thumbnails, `max-image-preview` placement and the Wikidata/Wikipedia (COI) workflow → `references/multisite-and-technical.md` §8.
- People: `ProfilePage` + `Person` (`worksFor` → org `@id`), not a LocalBusiness subtype per person.
- Articles: `image`, `publisher.logo`, dates. FAQPage only where the Q&A is visible on the page.
- Home: `WebSite` + `SearchAction` (real site-search URL). Every template carries at least `WebPage` + `BreadcrumbList` (hub pages are the usual gap). Record pages that show a document image put it in `image`.
- Generic `<meta name="robots">` with `max-snippet:-1, max-image-preview:large` as well as `googlebot`/`bingbot` (Naver/Daum read only `robots`); key it so page-level `noindex` tags survive → `references/multisite-and-technical.md` §8.
- Validate a sample with validator.schema.org and the Rich Results Test. Report errors and warnings verbatim.
- The Rich Results Test does not list FAQPage for non-gov/health sites (since 2023-08); validate FAQPage with validator.schema.org instead.
- **Never** add Review/AggregateRating markup for testimonials the business wrote or selected itself.

### D. Performance
- Protocol and compression: HTTP/2 via ALPN for every host (`openssl s_client -alpn h2`), br/gzip. nginx `http2` must be on every `listen 443` incl. `default_server` → `references/multisite-and-technical.md` §9.
- PageSpeed Insights on mobile for each main template (home plus the profile's money pages: category and product, pricing and feature pages, article): field CWV (LCP, INP, CLS) and lab values.
- If LCP is far later than FCP, suspect a hero that is hidden until an animation runs. If CLS is high, find the shifting element (DevTools → Performance → Layout shifts).

### E. Content quality and network risk
- Templated pages at scale (same title pattern, pasted user questions), exact duplicates, cross-domain duplicate bodies.
- City × service page matrices on several domains (doorway pattern).
- **Cannibalization:** which URL actually ranks or gets clicks for each query cluster. Use GSC Pages × Queries when available.
- Cross-site linking: main ↔ satellites. Count the linking pages, check for UTM on internal links, find orphaned satellites.
- Volume, scaled-content, thin/duplicate and doorway rules → `references/content-scale-and-quality.md` §1–4 and `references/multisite-and-technical.md` §2–3.

### F. Local profile (Google Business Profile; Naver Place / Smart Place; Kakao Map) — local businesses only
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

### G. Entity / NAP consistency across the web — local businesses only (others: check name, description and profile links in module I)
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
- Query set: brand (exact, and with location for local businesses), head terms (category, or city + service), product/feature terms, comparison terms ("<brand> vs", "best <category>") for e-commerce and SaaS, 3–5 long-tail.
  - Google: `https://www.google.com/search?q=<Q>&gl=<cc>&hl=<lang>&pws=0`, organic positions to page 3.
  - Local engines (e.g. Naver integrated search): which section shows us (Place, website, blog, Q&A, AI briefing).
- AI engines, logged out: 3 recommendation questions, 1 "is <brand> good?", 1 "address and phone of <brand>". Record:
  - mentioned? cited URL?
  - wrong facts, quoted exactly;
  - sources used instead, and **why** they were chosen (registered credentials, directories, reviews).
- Trace every wrong AI fact back to the page it came from. Fixing that page is usually the fix.
- GEO rules (AI search bots, quotable structure, llms.txt priority, Copilot citations) → `references/knowledge-base.md` §8.
- Markdown copies of key pages (`/<path>.md`, allowlisted, noindex + canonical Link, cached) listed in llms.txt → `references/multisite-and-technical.md` §10. A full technical comparison against a competitor → §9. Free tool pages on public data (calculators, lookups) as citable, linkable pages → §11.

### I. Off-site entity authority (wikis, knowledge graph, profiles, earned mentions)
AI engines describe a company mostly from third-party sources: in industry studies brand *mentions* (web and YouTube) correlate with AI visibility far more than backlinks, and ChatGPT, AI Overviews and Perplexity each lean on different sources (Wikipedia, Reddit, YouTube, LinkedIn, press).
- **AI source map:** for 5 fixed brand questions per engine, record every cited URL and its domain type. The domains that recur are what to fix or earn. Prompt: `templates/browser-prompts/07-ai-source-map-and-offsite-entity.md`.
- **Entity inventory:** Wikidata (QID), Wikipedia per language, Namuwiki, knowledge panel / Knowledge Graph ID, LinkedIn, Crunchbase, YouTube, directories/registers, review sites, independent press. Facts match the fact sheet? Linked from the site's `sameAs`? Run `scripts/wikidata_entity_check.py`.
- **Work the priority ladder:** entity home (About page + Organization JSON-LD + one canonical description) → own profiles → Wikidata if notable → earned coverage → Wikipedia only when its notability test passes.
- **Wikis are COI territory:** disclose paid/COI editing (Wikimedia Terms of Use), propose changes on talk pages, never buy wiki or "knowledge panel" services, never use sock puppets, never delete criticism.
- Full playbook, Wikidata property list, Wikipedia source test, Korean wikis, measurement → `references/entity-authority-and-off-site.md`.

### J. Profile checks
Run the section of `references/site-profiles.md` for each profile that applies:
- **E-commerce (§4):** one canonical per product, variants, faceted navigation kept out of the crawl except demand-backed facets, paginated categories, internal search `noindex`, `Product`/`Offer` matching page and feed, genuine reviews only, out-of-stock and discontinued handling, sitemaps split by type.
- **SaaS / web app (§5):** public vs private surfaces, app routes and staging/preview hosts kept out of the index (auth + `noindex`, not robots.txt alone), marketing pages server-rendered, real 404s, feature/use-case/pricing/comparison/integration pages, review-platform presence for GEO.
- **Content / media (§6):** article schema with real authors and honest `dateModified`, author pages, consolidation of overlapping articles, thin tag/date archives, paywall markup, ad-slot CLS.
- **Marketplace / UGC (§7):** index-quality threshold for user pages, spam and link controls, expired listings, location × category pages only with real listings.
- **Docs (§8):** versions and canonicals, code as text, `llms.txt` and `.md` copies for coding assistants.
- **Multi-site network (§9):** `references/multisite-and-technical.md` and browser prompt 09 before any consolidation.

---

## Step 3 — Findings, scores, and the fix plan

Each finding:

```
ID | Severity (Critical/High/Medium/Low) | Problem + evidence (URL, exact text, numbers) | Why it matters | Exact fix | Owner (code / CMS / listing owner / content / other business) | Effort | How to verify
```

Severity guide:
- **Critical:** can demote the whole site or network, or a legal/regulatory breach. Examples: scaled templated content, doorway matrices, false claims.
- **High:** blocks indexing, visibility or entity clarity for a main template. Examples: main content only after JavaScript, app or staging pages indexed, facet URLs flooding the crawl, wrong primary category or NAP drift (local), mobile CWV failure on main templates.
- **Medium:** single-hop redirects, missing sitemap URLs, schema gaps, duplicate titles.
- **Low:** cosmetic consistency.

Scores 1–10, each with a one-line reason: Technical (incl. rendering) · On-page · Local · Entity/NAP · Brand search · GEO · Off-site authority. For non-local sites replace Local and Entity/NAP with the profile's area (`references/site-profiles.md` §10). Score only what was verified; write "n/a" for areas that do not apply.

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
5. Code recipes (redirects, canonical/hreflang, titles, JSON-LD, robots.txt, llms.txt, Core Web Vitals, internal links, thin/duplicate handling, CMS persistence) and the safe change workflow with a curl checklist → `references/implementation-playbook.md`. Its examples use Next.js Pages Router and nginx; for any other framework, CMS or host, find where each control lives in `references/stacks.md`, and for rendering fixes use `references/rendering-and-javascript.md` §5.
6. Sitemap generation per stack (Next.js App/Pages Router, WordPress, static generators, Nginx) and submission (Search Console, Bing, IndexNow, Naver, Daum) → `references/sitemaps-and-submission.md`. Submitting or re-submitting is an action: ask first, then use `scripts/gsc_sitemaps.py submit --apply` / `scripts/indexnow_submit.py --apply`.
7. Deploy, CMS-storage and line-ending traps seen in real projects → `references/multisite-and-technical.md` §7 and `references/lessons-learned.md` §4.

### CMS / admin content
- Before trusting "saved", find where the CMS stores the content. Example failure: admin edits were written into git-tracked files and every deploy (`git reset --hard`) wiped them.
  - Snapshot the live content into the repo before the next deploy.
  - Then move the store out of the deploy path (DB, or a git-ignored or volume path), seeded once from the defaults.
- After saving, verify the public URL, not the editor.

### Listings (GBP, Naver Place, Kakao, directories) — local businesses
- Before any edit, run `templates/browser-prompts/03-gbp-readonly-status-check.md` (access, every field, notices, reviews, insights). Then use `05-gbp-update-stage1.md` and, 3–5 days later, `06-gbp-update-stage2.md`.
- Edit only the owner's own listing, only with explicit OK, signed in as the manager.
- **Stage edits.** First: category, hours, description, services, extra phone, review replies. Wait 3–5 days. Then the address or building name on its own, because address edits can trigger re-verification.
- Screenshot before and after each section. Report Google's exact status messages (under review, published, error).
- Review replies: 1–2 varied sentences, no case or customer details, no keywords, no phone or URL. Skip negative reviews and reviews that describe a specific matter; list them for the owner.
- Never write, delete or buy reviews. Never claim another business's listing. Never stuff keywords into the business name. Never set "open 24 hours" unless true.
- Owner or staff reviews of their own business break platform policy. Tell the owner to delete them from their own account; do not do it for them.

### Off-site entity (Wikidata, wikis, profiles)
- Profiles the company owns: fill them with the fact sheet's canonical facts and description, then add each to `sameAs` and to the fact sheet the same day.
- Wikidata / Wikipedia / Namuwiki edits are made by a named person with a disclosed COI, never by an agent on a shared account. Prepare the exact statements with their references (Wikidata) or a talk-page edit request (Wikipedia) and hand them to that person. Re-run `scripts/wikidata_entity_check.py` afterwards.
- Knowledge panel claims and suggested changes are done by the owner through Google's own verification flow.

### Content
- In regulated industries (law, medicine, finance), content changes need human approval.
- Batch in small groups. Keep claims verifiable: registered specialties only, no superlatives or unsupported statistics, no fake testimonials.
- Do not mass-publish to sites that a search update has just hit. Fix and consolidate first.

---

## Step 5 — Verify and re-measure

- Same day: re-open each changed page or listing in public view and confirm the change shows.
- 1–3 days: services, posts and review replies often publish late. Re-check.
- 2–4 weeks: re-run the core ranking queries and the AI questions, the raw-HTML rendering checks for changed templates, and for local businesses the geo-grid and map-pack tests **signed out and signed in**. Compare with the baseline table. Offer to schedule this check.
- Monthly for off-site work: AI mention rate and accuracy, cited sources, Knowledge Graph match, Wikidata completeness, new independent mentions (`references/entity-authority-and-off-site.md` §12). Off-site changes take weeks to months to show in AI answers.

---

## Bundled scripts and templates

Use these instead of writing ad-hoc code. All of them are read-only or dry-run by default (anything that sends data needs `--apply`); run any one with `--help` for usage. Secrets come from environment variables only.

- **`templates/seo-geo-facts.md`** — Step 0 fact sheet: a core block for every project plus blocks per site profile. Copy it into the project and fill in the blocks that apply.
- **`templates/browser-prompts/`** — nine fill-in prompts for a browser agent: 01 site/network audit · 02 entity/NAP + rankings + GEO live test · 03 strict read-only Business Profile status check · 04 Maps pin/duplicates/geo-grid/map-pack test · 05 profile update stage 1 · 06 profile update stage 2 · 07 AI source map + off-site entity inventory · 08 post-fix re-measure (technical + rankings + local engine + AI answers, one session) · 09 Search Console query → page table for cross-domain cannibalisation (read-only). Its README gives the order, which prompts apply to which site profile (03–06 are for local businesses only) and the shared rules.
- **`scripts/wikidata_entity_check.py --search "<name>" --lang ko`** then **`--qid Q… --site https://www.example.com --langs en,ko --out DIR`** — module I: labels/descriptions per language, missing core statements, unreferenced core statements, profile identifiers, Wikipedia sitelinks, and whether the site's Organization JSON-LD links the item and matches P856. Read-only (public Wikidata API + one page GET).
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

- **Step 0, always** → `references/site-profiles.md` (profile choice, module routing table, per-profile checks for local, e-commerce, SaaS/web app, content, UGC, docs and networks, and the score areas that replace Local/NAP).
- **Module A2, and any site built with a JavaScript framework** → `references/rendering-and-javascript.md` (who renders JavaScript, rendering modes, raw vs rendered tests, SPA failures, fixes in order of preference).
- **Step 4 on a stack other than Next.js Pages Router + nginx** → `references/stacks.md` (where head tags, status codes, redirects, sitemaps and headers live in Next.js App/Pages, Nuxt, SvelteKit, Astro, Remix/React Router, Angular, Gatsby, plain Vite SPAs, WordPress, Shopify, site builders, headless CMS, Vercel/Netlify/Cloudflare/nginx).
- **Step 0, or whenever a concrete precedent helps (local, multi-site, regulated industries)** → `references/case-study-multisite-law-firm.md` — a worked example of a multi-site professional-services network (architecture, owner decisions, publishing and deploy rules, measured results, what worked and what didn't).
- **Before Step 2 modules A–C and H, or when a rule of thumb is needed** → `references/knowledge-base.md` (quality and crawling, on-page limits, schema/entity, E-E-A-T, internal links, GEO, measurement).
- **Module A index buckets, or any "why isn't it indexed" question** → `references/indexing-audit.md` (condensed indexing audit: hard rules, workflows 00–10, classification, dev loop).
- **Before Step 2 module E, when planning content volume, or before writing/approving content** → `references/content-scale-and-quality.md` (volume rules, scaled-content risk, natural writing, duplicates, multilingual, Q&A pipelines, lawyer-ad compliance).
- **Korean market, modules F–H for Korea, Naver/Kakao/directories** → `references/korea-search.md`.
- **Networks of sites, a new domain, or a CMS migration** → `references/multisite-and-technical.md` (satellite architecture, doorway/cannibalisation, setup checklist, migration, deploy gates).
- **Step 3 (before scoring) and Step 4 (before applying)** → `references/lessons-learned.md` (symptom → cause → fix → early detection).
- **Step 4, any code change** → `references/implementation-playbook.md` (safe change workflow, redirects, canonical/hreflang, titles, JSON-LD, robots.txt, llms.txt, Core Web Vitals, internal links, thin/duplicate content, CMS persistence, curl checklist).
- **Module A sitemaps, Step 4 sitemap fixes, any ownership or submission question** → `references/sitemaps-and-submission.md` (protocol, special sitemaps, splitting, generation per stack, robots.txt, Google/Bing/IndexNow/Naver/Daum steps, monitoring, troubleshooting).
- **Module I, "what does AI say about our company", Wikidata/Wikipedia/Namuwiki/knowledge-panel work, PR or brand-mention planning** → `references/entity-authority-and-off-site.md` (citation studies, AI source map, priority ladder, entity home, Wikidata notability + property list, Wikipedia source test + COI rules, Korean wikis, knowledge graph, profiles, earned mentions, hard limits, measurement).
- **Citing a rule, or checking whether it is still current** → `references/sources.md` (verified official URLs, with the verification date; rules not backed by an engine document are marked "field experience").

When a reference and the fact sheet disagree, the fact sheet's owner decisions win; list the conflict under "Skipped by owner decision".

---

## Report template

```
# <Project> — SEO · Local · GEO audit (<date>)
## Summary (5 bullets: biggest risk, fastest win, where we rank, entity state (NAP for local), AI visibility)
## Site profile(s), rendering and stack per site; modules not applicable and why
## Test conditions (time, signed-in?, location, limits hit)
## Scores (7 areas per profile, 1–10 or n/a, one-line reasons)
## Findings by severity (table per Step 3)
## Fix plan: Do now / Needs owner decision / Plan only / Not ours
## Tables: per-site checks · raw vs rendered per template · rankings · GEO answers · AI source map + entity inventory · (local) NAP master table + geo-grid · (profile) facet/variant, private-route or author tables
## Skipped by owner decision
## NOT VERIFIED (item + reason)
## Owner summary (6–10 lines, owner's language, plain words, ends with the decisions needed)
```

For a daily or after-work report to a manager, use: **found → done** per item (numbered), then "requests for you", in the manager's language.

---

## Prompt templates for delegation

Use these when another agent must do the live work. Fill them from the fact sheet, and always include the hard rules and the owner decisions. For browser work, prefer the complete templates in `templates/browser-prompts/`; the outlines below are for cases they don't cover.

**Browser audit agent:**
"You are a hands-on SEO/GEO tester (plus local SEO if the site is a local business) in my real Chrome. Live checks only, read-only, no guessing." Then:
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

## Korea notes (only when Korea is a market)

- Engines: Google KR, Naver (largest local engine; Smart Place drives the map results), Daum/Kakao.
  - Daum Webmaster verification goes in robots.txt (`#DaumWebMasterTool:<hash>:<suffix>`).
  - Naver's crawler is Yeti.
- Kakao Map shows the building name from Kakao's own address database. Daum search cards copy Kakao's place data.
- Naver pages often block automated browsers. If they do, ask the owner to check the Naver Search Advisor and Smart Place dashboards, and mark it NOT VERIFIED.
- Business registration numbers: the middle code 85 means a corporate branch. Use it to tell a branch from the head office.
- Naver supports IndexNow (verified 2026-11-02); Naver has no public sitemap-submission API (its crawl-request API is partner-only). Naver rejects sitemap files of 10 MB or more. Details → `references/sitemaps-and-submission.md` §6.4.
- Lawyer advertising, for legal clients only (Korean Bar Association Regulations on Attorney Advertising, under the Attorney-at-Law Act):
  - certification wording ("certified by the Korean Bar Association as a <field> specialist") only for fields the lawyer has registered; for plain "<field> specialist" wording follow `references/content-scale-and-quality.md` §9 and confirm with the lawyer responsible for advertising;
  - no "best", "No. 1" or "only";
  - no satisfaction or results figures without a documented basis;
  - name the lawyer responsible for advertising.
  Fake or seeded reviews also breach the Act on Fair Labeling and Advertising.
- Nuance on "specialist" wording (since the 2021 revision of the Regulations, plain "<field> specialist" is allowed for fields actually practised; only certification wording is limited to registered fields), and the full compliance table → `references/content-scale-and-quality.md` §9.
