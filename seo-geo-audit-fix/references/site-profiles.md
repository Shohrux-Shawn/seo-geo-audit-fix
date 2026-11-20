# Site profiles — which modules apply, and the checks each type adds

Read in Step 0, right after the fact sheet. A site can have more than one profile (an online store with a
physical shop is *e-commerce* + *local business*; a SaaS with a blog is *SaaS* + *content*). Run every
profile that applies. Rendering checks (`rendering-and-javascript.md`) apply to every profile.

## Contents
1. Choosing the profile
2. Module routing table
3. Local business (one or more physical locations)
4. E-commerce (catalogue, product pages, checkout)
5. SaaS and web apps (marketing site + logged-in app)
6. Content and media (blog, news, magazine, knowledge base)
7. Marketplaces, directories and user-generated content
8. Documentation and developer sites
9. Multi-site networks
10. Scores per profile

---

## 1. Choosing the profile

Ask, or find out from the site itself:
- **Does a customer visit a place, or does the business serve a defined area in person?** → local business.
- **Can a visitor buy a product with a price on the site?** → e-commerce.
- **Is the main product software people sign in to?** → SaaS / web app.
- **Is most indexable traffic from articles, news or guides?** → content / media.
- **Do third parties create most of the pages (listings, profiles, posts, reviews)?** → marketplace / UGC.
- **Is there public product or API documentation?** → docs.
- **More than one domain or subdomain aimed at search?** → multi-site network.

Also record, for every site: rendering mode (static, server-rendered, client-rendered SPA, hybrid), the
framework/CMS/platform, the hosting/CDN, and the markets/languages. These decide which recipes in
`stacks.md` and `rendering-and-javascript.md` you need.

---

## 2. Module routing table

| Module (SKILL.md Step 2) | Local | E-com | SaaS/app | Content | UGC | Docs | Network |
|---|---|---|---|---|---|---|---|
| A Reachability, crawl, sitemaps | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| A2 Rendering and JavaScript | ✔ | ✔ | ✔ (critical) | ✔ | ✔ | ✔ | ✔ |
| B On-page per template | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| C Structured data and entity | LocalBusiness | Product/Offer | SoftwareApplication | Article | per type | TechArticle optional | one `@id` |
| D Performance | ✔ | ✔ (listing + product) | ✔ (marketing pages) | ✔ (ads, embeds) | ✔ | ✔ | ✔ |
| E Content quality, duplicates | ✔ | facets, variants | thin feature pages | scale, freshness | thin/spam pages | versions | doorways |
| F Local profiles (GBP, Naver, Kakao) | ✔ | if a shop | — | — | — | — | per location |
| G NAP consistency | ✔ | if a shop | — | — | — | — | ✔ if local |
| H Rankings and GEO | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| I Off-site entity authority | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| J Profile checks (this file) | §3 | §4 | §5 | §6 | §7 | §8 | §9 |

"—" means skip and say so in the report ("not applicable: no physical location"), so nobody reads a
missing module as a pass.

---

## 3. Local business

Modules F and G in SKILL.md, the browser prompts 02–06, `korea-search.md` for Korea, and the worked
example `case-study-multisite-law-firm.md`. Extra checks:
- One location page per real location (address, hours, map, phone), each with its own `LocalBusiness`
  subtype node and `@id`; the organisation node links them.
- Service-area businesses without a storefront: hide the address on the profile, use `areaServed`, never
  invent addresses or virtual offices.
- Regulated professions (legal, medical, financial): advertising rules from the fact sheet override SEO
  advice; see `content-scale-and-quality.md` §9 for the Korean legal example.

---

## 4. E-commerce

**URLs and duplicates**
- One canonical URL per product. Platforms often expose the same product under several paths (for
  example under every collection); the canonical must point at the plain product URL and internal links
  should use it.
- Variants (size/colour): either one URL with a selector, or one URL per variant when each variant has
  real search demand; never both indexable for the same variant. Variant URLs canonicalise to themselves
  only if they are meant to rank.
- Faceted navigation (filters, sort, price ranges) explodes into near-infinite URLs. Pick the few facet
  combinations with search demand and give them clean, linked, indexable URLs; keep the rest out of the
  crawl (robots.txt disallow on the parameters, or filters in the URL fragment, which Google does not
  crawl). `noindex` alone still lets them eat crawl budget. Sort and session parameters never index.
- Pagination: every page of a category is a real URL with a self-canonical (not canonical to page 1) and
  real `<a href>` links; "load more" and infinite scroll must also be reachable through paginated URLs.
- Internal search result pages: `noindex` and kept out of the sitemap.

**Product page content and data**
- `Product` with `offers` (`price`, `priceCurrency`, `availability`), `image`, `sku`/`gtin`/`brand` where
  real, and merchant fields (shipping, returns) when the store wants merchant listings. Price and
  availability in the markup must match the visible page and the feed exactly.
- `aggregateRating`/`review` only from genuine customer reviews collected on the site or a review
  platform, never hand-picked testimonials.
- Unique descriptions for the top sellers; manufacturer copy duplicated across hundreds of stores adds
  nothing. Thin variant pages are a common "Crawled – not indexed" cause.
- Category pages are usually the strongest landing pages for head terms: a short, useful intro, the
  product grid in server HTML, and links to sub-categories.

**Stock and lifecycle**
- Temporarily out of stock: keep the page 200, mark `availability` as `OutOfStock`, show alternatives.
- Permanently discontinued: 301 to the closest replacement or the category if one really exists;
  otherwise 404/410. Never mass-redirect everything to the home page (treated as soft 404).
- Seasonal pages (sale, holiday): keep one evergreen URL and update it each year instead of a new URL
  per year.

**Feeds and engines**
- Google Merchant Center (and the local equivalents, e.g. Naver Shopping in Korea) is a separate surface
  from organic search. Feed and on-page data must agree, or listings get disapproved.
- Large catalogues: split sitemaps by type (products, categories, content), keep `lastmod` true to the
  product data change, and monitor indexed products vs submitted per sitemap.

**Performance**
- Measure a category page and a product page, not just the home page. Common causes: large uncompressed
  product images, third-party scripts (reviews, chat, tracking), client-rendered price/stock.

---

## 5. SaaS and web apps

**Split the surfaces**
- Public, indexable: home, product/feature pages, pricing, use-case and industry pages, integrations,
  comparison pages, docs, blog, changelog, legal pages.
- Private, never indexed: the app itself (dashboards, settings, editors), sign-in and sign-up flows,
  password reset, invite links, user workspaces, preview/staging hosts.
- Put the app on its own subdomain or path and protect it with authentication. `robots.txt` is not
  access control; use `noindex` (meta or `X-Robots-Tag`) on any app route that can be reached without a
  login, and keep app URLs out of the sitemap. Staging and preview hosts: password or `noindex` header,
  never only robots.txt (blocked pages can still be indexed from links).
- Shared or public user content (public boards, profile pages, shared documents) is a deliberate
  product decision: index it only with quality controls (§7), otherwise `noindex`.

**Rendering**
- Marketing pages are often built inside the same client-rendered app. AI crawlers do not run
  JavaScript and Google renders later; serve the marketing pages as static or server HTML
  (`rendering-and-javascript.md`).
- Client-side routes that do not exist must return a real 404 status from the server, not a 200 shell
  with "not found" text (soft 404).

**Pages that win searches for software**
- One page per real feature or use case with concrete content (screens, workflow, limits), not a
  template with the keyword swapped.
- Pricing page in plain HTML text (plan names, prices, what is included); AI answers quote it.
- Comparison and alternatives pages: factual, dated, fair about the competitor; no invented numbers.
- Integration pages: one per integration with real setup steps, linked from the integration directory.
- Changelog and docs give freshness and long-tail coverage.

**Structured data**
- `Organization` on the home page; `SoftwareApplication` (or `WebApplication`/`MobileApplication`) with
  `offers` and `operatingSystem`/`applicationCategory` on the product page; `aggregateRating` only from a
  real review source. `FAQPage` only for visible Q&A.

**GEO for software**
- AI engines answer "best <category> tool" from comparison articles, review platforms (e.g. G2,
  Capterra), community threads and docs. Module I's source map shows which ones; a correct, current
  profile there matters more than any on-site change.
- `llms.txt` pointing at docs, pricing and the product overview; `.md` copies of docs pages are cheap
  wins (`multisite-and-technical.md` §10).

---

## 6. Content and media

- `Article`/`NewsArticle`/`BlogPosting` with `headline`, `image`, `datePublished`, `dateModified` (only
  when the content really changed), `author` as a `Person` with a real author page, `publisher` →
  organisation `@id`.
- Author pages with real credentials and links to the person's other profiles; no invented bylines.
- Freshness: update and re-date evergreen pieces instead of publishing near-duplicates; merge and 301
  overlapping articles (cannibalisation inside one site).
- Scaled or AI-assisted publishing: `content-scale-and-quality.md` §1–4. Quality per page decides
  site-wide demotions.
- Archives, tag and date pages: index only the ones that are real hubs; thin tag pages `noindex`.
- Paywalls: mark paywalled sections (`isAccessibleForFree` + `hasPart`) so the gating is not read as
  cloaking.
- News publishers: news sitemap, fast server-rendered article HTML, stable URLs.
- Video: `VideoObject` with thumbnail and upload date on the page where the video is the main content.
- Ads and embeds are the usual CLS/INP cause; reserve space for ad slots.

---

## 7. Marketplaces, directories and user-generated content

- Most pages are created by others, so most quality risk is too. Index only pages that pass a minimum
  (enough text, at least one real item/review, not a duplicate); everything else `noindex` until it
  qualifies. Empty listing and profile pages are the main "thin content" source.
- Spam control: link `rel="ugc"`/`nofollow` on user links, moderation, rate limits, no indexing of
  freshly created accounts.
- Location × category pages (e.g. "plumbers in <city>"): only where real listings exist; otherwise they
  are doorway pages.
- Expired listings: keep briefly with "no longer available" + related items, then 404/410 or 301 to the
  category; never a site-wide redirect to home.
- Reviews markup only for genuine reviews of a third-party item, never the site reviewing itself.
- Forums and Q&A: `DiscussionForumPosting` / `QAPage` where the format really fits.

---

## 8. Documentation and developer sites

- Static or server-rendered docs (most docs generators are); search inside docs is client-side, which is
  fine as long as the pages themselves are HTML.
- Versions: one canonical "latest" URL per page; old versions either `noindex` or canonical to latest,
  except versions people still search for explicitly.
- Code samples in text (not images); headings that match the task ("How to authenticate").
- `llms.txt` and `.md` copies of docs pages are what coding assistants read; keep them complete.
- Reference pages generated from an API spec are often thin; add examples and explanations to the top
  ones.

---

## 9. Multi-site networks

`multisite-and-technical.md` (architecture, doorway and cannibalisation risk, cross-linking, new-domain
checklist, deploy rules) and the browser prompt 09 for query → page data before any consolidation.

---

## 10. Scores per profile

Score only the areas that apply (SKILL.md Step 3). Replace "Local" and "Entity/NAP" with the
profile's own area where they do not apply:

| Profile | Area to score instead |
|---|---|
| E-commerce | Catalogue (facets, variants, product data, stock handling) |
| SaaS / web app | App/marketing split (indexing of private routes, rendering of public pages) |
| Content / media | Content quality and freshness (authors, dates, duplicates) |
| UGC / marketplace | Index quality control (thin/spam page ratio) |
| Docs | Docs coverage (versions, completeness for AI assistants) |

Sources: [E-commerce in Google Search](https://developers.google.com/search/docs/specialty/ecommerce) · [Faceted navigation](https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation) · [Pagination and incremental loading](https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading) · [Product structured data](https://developers.google.com/search/docs/appearance/structured-data/product) · [Merchant listing structured data](https://developers.google.com/search/docs/appearance/structured-data/merchant-listing) · [Software app structured data](https://developers.google.com/search/docs/appearance/structured-data/software-app) · [Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article) · [Paywalled content](https://developers.google.com/search/docs/appearance/structured-data/paywalled-content) · [Discussion forum structured data](https://developers.google.com/search/docs/appearance/structured-data/discussion-forum) · [Block indexing with noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing) · [Crawl budget for large sites](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget)
