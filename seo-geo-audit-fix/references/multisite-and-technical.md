# Multi-site architecture and technical SEO — satellites, setup checklist, migration

Read when auditing or building a network (main site + practice/region satellites), when
launching a new domain, or when migrating a CMS. Code recipes: `implementation-playbook.md`.
Sitemaps and console submission: `sitemaps-and-submission.md`. **(field experience)** marks the
author's own findings.

## Contents
1. Satellite / multi-domain architecture
2. Doorway and cannibalisation risk
3. Cross-linking policy
4. New-domain setup checklist
5. Migration lessons (WordPress → Next.js)
6. Copy-paste and multi-tenant traps
7. Deploy and verification rules
8. Search thumbnails and entity linking (branch-office networks)

---

## 1. Satellite / multi-domain architecture

| Rule | Why |
|---|---|
| One backend, one database; every record carries a **site-origin** field that decides which domain owns it. | Content isolation per domain; the field is the record's real address, not a tag. |
| The backend, not the client, sets the origin: override a client-supplied origin with the one in the editor's token; reject cross-origin edits. | A client-trusted origin field is a security and duplication bug (fixed in a real network). |
| A satellite record requested on the main domain → **301 to the satellite URL**; unmapped non-main origins → 404. | Kills cross-domain duplicates. A mismatched origin ↔ target site = a 301 chain. |
| Each satellite is a full standalone site: own about/contact/bios, own articles, own sitemap, own Search Console/Naver/Bing properties. | Mirrored content across domains is the classic penalty. |
| One NAP constant shared by every JSON-LD block; per-site config holds only what genuinely differs (practice label, slug, colours, verification tokens, nav items to hide). | Hand-written NAP drifts; tokens in shared packages verify the wrong site. |
| One organisation `@id`; satellites describe a department/service with `parentOrganization` (or `publisher`) → that `@id`. | Avoid N copies of the same business in the knowledge graph. |
| www-canonical everywhere; apex → www **301 in one hop**; `siteUrl` in config with `www`. | A non-www `siteUrl` makes the sitemap emit URLs that 301. |
| Members are global, sessions per origin: member pages live on each satellite with relative links, `noindex, nofollow`, excluded from the sitemap. | A link to the main site's member page showed another session (an admin profile). |

Sources: [Canonicalization](https://developers.google.com/search/docs/crawling-indexing/canonicalization) · [Redirects](https://developers.google.com/search/docs/crawling-indexing/301-redirects) · [Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization) · architecture rules: (field experience)

## 2. Doorway and cannibalisation risk

- Google's doorway definition includes **multiple domains targeted at specific regions or cities that funnel users to one page**. Practice-area microsites are not doorways per se; the risks are (a) the same templates/articles on several domains, (b) satellites funnelling to the main site's form with thin content, (c) keyword-anchor cross-links.
- City × service matrices on several domains: 6 sites × 25 footer regions = 150 structurally similar pages. Satellites must **not** get a region × practice matrix — a satellite already *is* one practice. Main-site region × practice pages only for regions you can actually win (office proximity). (field experience)
- Before opening template pages, measure similarity with names neutralised (88–91% identical on four sites → kept behind a per-host switch, opened in cohorts: most-different sites first, 2 weeks, then the rest). (field experience)
- **Cross-domain cannibalisation:** check which URL actually ranks/gets clicks per query cluster (Search Console Pages × Queries per property). Seen 2026-11: satellites ranked almost nowhere while the main site's `/location` pages took their queries. Decide one owner per cluster: either the satellite page becomes the target (the main page links to it / is trimmed), or the satellite stops competing.
- Weak satellites (average position 27–41 in 2026-09) are candidates for folding into the main site as sections (link equity pools). Reviewed quarterly; a business decision. Freeze new satellites until that decision. (In one network a seventh satellite still launched a month later — owner decision.)
- Older view (2026-07 plan): expand to ten satellites. Superseded by the 2026-09-08 doorway analysis.

Sources: [Spam policies (doorway abuse, scaled content abuse)](https://developers.google.com/search/docs/essentials/spam-policies) · measurements: (field experience)

## 3. Cross-linking policy

- Network links in a "family sites" footer with **brand anchors**, not keyword anchors.
- A satellite's consultation form stays on the satellite domain; avoid UTM-tagged satellite → main funnels (doorway pattern, and UTM creates redirect/alternate buckets).
- Map and link the whole brand entity, including sibling offices of the same firm (seen 2026-11: siblings outranked the main office for the brand query; nobody linked them).
- Near-100% self-links in Bing/Naver backlink reports are a flag to report, not to "fix" silently.
- Every registration point for a new satellite must be updated together (main-site redirect maps, promo blocks, practice index). A missing entry left one satellite unlinked from the main practice index.

Sources: [Link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) · [Spam policies (link spam)](https://developers.google.com/search/docs/essentials/spam-policies) · policy choices: (field experience)

## 4. New-domain setup checklist

Before anything: **resolve every listed domain** (DNS + HTTP status). Planned domains that were never registered must not enter audit prompts.

1. **Code ready:** app copied from the most recent satellite (not the oldest template); per-site config filled; backend domain → origin mapping added; backend enums exist (new practice areas may need new enum values *before* the frontend ships, or writes are rejected); container on a unique port; DNS for apex and www.
2. **SSL** covering apex + www.
3. **Web server:** the www block proxies; apex 443 → 301 www; port 80 → 301 https www; `nginx -t` then reload; `curl -I` both hosts (`implementation-playbook.md` §2).
4. **Config:** `siteUrl` and `mainSiteUrl` with www; verification tokens per site (never shared).
5. **Sitemap:** opens, all `<loc>` on the www host, no doubled domain (`www.x.comhttps://…` came from mixing absolute and relative paths in one loop), only this site's records, hub pages included. Run `scripts/sitemap_validate.py --host www.<domain>`.
6. **robots.txt:** no legacy CMS rules, disallow only login/API/private paths, `Sitemap:` with www, `/favicon.ico` not disallowed; AI search bots allowed.
7. **`/favicon.ico` → 200 image** (rewrite, not redirect).
8. **IndexNow:** key file at root returns 200; backend origin → base-URL map updated (unmapped origins are skipped *silently*); ping on create, update **and delete** (`scripts/indexnow_submit.py` for manual batches).
9. **Search Console:** a Domain property, or a URL-prefix property on `https://www.<domain>`; meta tag or file deployed *before* pressing Verify; submit the sitemap; resubmit after any large URL addition; spot-check with URL Inspection. Never "Validate fix" on legacy redirects.
10. **Naver Search Advisor:** same, plus RSS.
11. **Bing:** import from Search Console or add; check sitemap status the next day.
12. **Member/private pages** `noindex, nofollow`; the duplicate-signup error shown correctly.
13. **Main-site registration points** updated; content backfilled with the right origin.
14. **Final:** apex 301 → www 200; sitemap/robots/favicon/IndexNow key OK; both verification methods present; run the link gate (§7).

Sources: [Verify site ownership](https://support.google.com/webmasters/answer/9008080) · [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) · [IndexNow documentation](https://www.indexnow.org/documentation) · [Naver: RSS and sitemap submission](https://searchadvisor.naver.com/guide/request-feed) · [Bing: add and verify site](https://www.bing.com/webmasters/help/add-and-verify-site-12184f8b) · checklist order: (field experience)

## 5. Migration lessons (WordPress → Next.js)

| Lesson | Detail |
|---|---|
| Legacy URLs: one-hop 301/308 to the **matching** new URL; deleted → 410; never mass-redirect to `/`. | Redirect-to-home is treated as a soft 404. An older practice (2026-05) 301'd legacy board URLs to `/` and robots-blocked them; superseded by the hard rules. |
| "Page with redirect" growing in Search Console after migration is expected; don't validate it. | It drains on its own; the 404 bucket falls as 410s are processed. (field experience) |
| Diagnose redirect codes with curl from a clean shell. | A fetch proxy reported 302 where the server sent 308/301 — a wrong diagnosis nearly triggered needless code work. (field experience) |
| Non-ASCII (e.g. Korean) URLs arrive both decoded and percent-encoded. | Redirect maps hold both, or normalise (decode + NFC) before comparing. |
| The sitemap domain must match the canonical host; Naver flagged a sitemap URL domain mismatch. | www vs non-www mismatches split properties and data. |
| The Search Console property variant must match the canonical; keep an old wrong-variant property for a few weeks before deleting it. | Google learns the redirect. |
| Soft 404s from client-rendered legal pages (terms, privacy, disclaimer). | SSR them or drop them from the sitemap. |
| Clean legacy URL debt (hundreds of 404s/redirects) before adding new content. | Low-quality patterns waste crawling; cleaning can raise the crawl of good sections. |
| State before a cleanup how many URLs go 200 → 404 and check their clicks/impressions first. | Avoid deleting pages that still earn traffic. |
| Old WordPress `robots.txt` rules must not be carried into the new site. | — |

Sources: [Redirects and site moves](https://developers.google.com/search/docs/crawling-indexing/301-redirects) · [HTTP status codes / soft 404](https://developers.google.com/search/docs/crawling-indexing/http-network-errors) · [Naver: sitemap rules (same domain)](https://searchadvisor.naver.com/guide/request-feed) · other rows: (field experience)

## 6. Copy-paste and multi-tenant traps

- A copied file inherits hard-coded site literals (a satellite linked to another satellite's practice page, 404 since launch). Site-specific values come from config, never literals.
- The tenant list lives in several places (domain → origin resolver, CORS pattern, IndexNow map, redirect maps); one forgotten entry → editor 403s or silent skips. Keep a mandatory checklist line for each.
- Dependency drift in a copied app (type packages) breaks builds: align devDependencies with a known-good app before debugging.
- Shared nav component changes (e.g. a closed dropdown needs `max-h-0 overflow-hidden`) must be verified in every app.
- GraphQL clients with `errorPolicy: 'all'` don't throw: check `errors?.length` explicitly (signup showed "No token" for "email already in use").
- API transport errors must return 5xx, never 404, or a backend blip de-indexes real pages.
- Timeouts: merge with the client's own abort signal (`AbortSignal.any`), create per request, short-circuit after the first failure (N sequential calls × timeout = minutes).
- View counters must not move `updatedAt` (`timestamps: false`), or lastmod lies (1,221 of 1,231 articles "changed").

Sources: (field experience)

## 7. Deploy and verification rules

- **Two gates:** static (build: registry/list equality asserts) and runtime (release: crawl the running build without JS, open every `<a href>`; 404 **and** redirect are failures; links to `noindex` pages are fine). Static checks never see runtime 404s — none of six real defects was found by reading code.
- Prove live pages didn't change: write the *allowed-difference classes* first (hreflang tags, switcher, build ids), then byte-diff before/after builds.
- One site at a time on a small VPS; never rebuild all services at once (OOM). Backend first when frontends depend on its data (e.g. lastmod), then satellites one by one, then the main site.
- Deploy only reviewed commits by id. A container restart that rebuilds in place shows a few minutes of 502 — normal.
- Runtime content must not live in the deploy path: if the CMS writes into git-tracked files and deploy does `git reset --hard`, every deploy wipes edits. Snapshot live content first, then move the store (DB or a git-ignored volume) — `implementation-playbook.md` §11.
- Check line endings before committing; a CRLF rewrite makes a full-file diff (use `git diff --ignore-space-at-eol` to review, fix before commit). Edit Windows batch files in binary mode.
- Grep legal pages for other brands' names before publishing (an imported terms-of-service page copied from another business still carried its name).
- A deploy without a live health check is unfinished. Verify the public URL, not the editor (`implementation-playbook.md` §12).

Sources: (field experience)

---

## 8. Search thumbnails and entity linking (branch-office networks)

**(field experience, 2026-11)** Owner's complaint: "our representative thumbnail does not show in Google/Naver; Google's AI calls us a small local firm". Root causes and the fix set:

**Thumbnails**

| Check | Rule |
|---|---|
| og:image | One per site, **1200x630**, JPG, under 300 KB (1.5 MB files were found; some previewers drop them). Same visual system on every site of the network (emblem + firm name + "<practice> specialist" line; main site without the line). |
| File name | A **new file name** whenever the artwork changes: KakaoTalk (and other previewers) cache by image URL. Then clear the preview cache **per page URL** (the Kakao debugger "캐시 초기화" clears only the URL you enter; other pages refresh when their cache expires). |
| Size tags | Declare `og:image:width/height` only when the size is known (site default image); record images keep no size tags. Add `og:image:alt`. |
| Large preview | Allow `max-image-preview:large` in **separate `googlebot` and `bingbot` meta tags**, not in `robots`: frameworks de-duplicate `<meta name="robots">` (Next.js `next/head` keeps one), so a default robots tag can silently override a page's own `noindex`. Engines combine directives; the most restrictive still applies. |
| Schema image | Each site's LocalBusiness/Organization `image` = **its own** og image (all satellites pointed to the main site's logo card). Add `logo` (at least 112 px on both sides, crawlable). |
| On-page image | Mobile Google picks thumbnails from in-page images: a 270x64 logo as the first `<img>`, or a client-rendered body (57 visible characters in the server HTML), gives it nothing to pick. |
| Reality check | Google **desktop** showed no organic thumbnails for anyone on local "<city> lawyer" queries; judge thumbnails on mobile Google and Naver. Changes appear days (Google) to weeks (Naver) after re-crawl; request it (GSC URL inspection, Bing Submit URLs, Naver 웹 페이지 수집). |

**Entity: branch office vs. the firm**
- First establish **what the site is**. Here the website was one **branch office** (own business number, own advertising-responsible lawyer), while the firm entity (Wikidata item, Wikipedia article, national hub site) is the head office led by another partner. The AI answer "local firm" was accurate for what our data described.
- Branch site schema: the office keeps its own `sameAs` (its map listings, its channels). Firm-level identities (Wikidata, Wikipedia, encyclopedia pages, head-office site) go on a **`parentOrganization`** node whose `@id` is the Wikidata URL. Putting them in the office's own `sameAs` asserts "this office IS the firm" — wrong.
- Wikidata: add the branch site to P856 with rank **normal** (the head-office site stays preferred), referenced to the firm's own hub page; add English label, description and alias; inception only with a source. Never set a branch as headquarters.
- Wikipedia: conflict-of-interest rules apply. Disclose on the user page, on the article talk page and in every edit summary; keep edits factual (https/URL fixes, links in the article's existing style); never re-add links an editor removed. One account = one person (no shared accounts).
- Building names: one address can carry two building names in different map services (Google vs Kakao). Confirm with the business before "fixing" NAP.
- Check what the AI cites: for "<firm name>" the AI Overview cited only an encyclopedia page and the Business Profile, not the firm's websites — fix those sources first.

Sources: [Robots meta tag (max-image-preview)](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag) · [Logo structured data](https://developers.google.com/search/docs/appearance/structured-data/logo) · [Wikipedia COI guideline (ko)](https://ko.wikipedia.org/wiki/위키백과:이해충돌) · (field experience)
