# Sources — authoritative public references

**Verified live on 2026-11-02** (each URL was fetched on that date with Firecrawl scrape or WebFetch and
returned the page named here). Pages move; if a link breaks, search the publisher's site for the title.
Only URLs that were verified are listed. URLs that failed or redirected elsewhere are listed at the end.

Rules in the other reference files cite these URLs. A rule marked **(field experience)** comes from the
author's own audits and incidents, not from engine documentation. A rule marked **(third-party study)**
comes from an industry study that was not re-verified for this list.

## Contents
1. Google Search Central — crawling, indexing, sitemaps, robots.txt
2. Google Search Central — canonicals, redirects, status codes, international
3. Google Search Central — structured data
4. Google Search Central — quality and spam policies
5. Google Search Console — help pages and APIs
6. Google Business Profile and Maps content policies
7. Core Web Vitals (web.dev)
8. Protocols: sitemaps.org, RFC 9309, schema.org
9. Bing Webmaster Tools and IndexNow
10. Naver Search Advisor
11. Daum Webmaster Tools and Kakao Map
12. AI crawlers and llms.txt
13. Korean attorney-advertising regulation
14. Framework and server documentation (implementation)
15. Off-site entity sources: Wikidata, Wikipedia, Knowledge Graph, review rules
16. Dropped or redirected URLs

---

## 1. Google Search Central — crawling, indexing, sitemaps, robots.txt

| Topic | URL |
|---|---|
| What is a sitemap | https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview |
| Build and submit a sitemap (50 MB uncompressed / 50,000 URLs per file) | https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap |
| Sitemap index files (large sitemaps) | https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps |
| Image sitemaps | https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps |
| Video sitemaps | https://developers.google.com/search/docs/crawling-indexing/sitemaps/video-sitemaps |
| News sitemaps | https://developers.google.com/search/docs/crawling-indexing/sitemaps/news-sitemap |
| "Sitemaps ping endpoint is going away" (2023-06-26: ping deprecated, `lastmod` guidance, `changefreq`/`priority` unused) | https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping |
| robots.txt introduction | https://developers.google.com/search/docs/crawling-indexing/robots/intro |
| How Google interprets robots.txt (only the most specific matching user-agent group applies) | https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt |
| Google's common crawlers (incl. the Google-Extended token) | https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers |
| Block indexing with noindex | https://developers.google.com/search/docs/crawling-indexing/block-indexing |
| Robots meta tag and X-Robots-Tag specification | https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag |
| Crawl budget management (for 1M+ pages, or 10k+ pages changing daily) | https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget |
| Link best practices (crawlable `<a href>`) | https://developers.google.com/search/docs/crawling-indexing/links-crawlable |
| JavaScript SEO basics | https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics |

## 2. Google Search Central — canonicals, redirects, status codes, international

| Topic | URL |
|---|---|
| What is URL canonicalization | https://developers.google.com/search/docs/crawling-indexing/canonicalization |
| How to specify a canonical (rel=canonical, redirects, sitemaps) | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls |
| Redirects and Google Search | https://developers.google.com/search/docs/crawling-indexing/301-redirects |
| How HTTP status codes affect Google's crawlers (404 and 410 are treated the same; soft 404s) | https://developers.google.com/search/docs/crawling-indexing/http-network-errors |
| Localized versions of your pages (hreflang in HTML, headers and sitemaps; x-default) | https://developers.google.com/search/docs/specialty/international/localized-versions |
| Managing multi-regional and multilingual sites | https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites |
| Influencing title links | https://developers.google.com/search/docs/appearance/title-link |

## 3. Google Search Central — structured data

| Topic | URL |
|---|---|
| General structured data guidelines | https://developers.google.com/search/docs/appearance/structured-data/sd-policies |
| LocalBusiness | https://developers.google.com/search/docs/appearance/structured-data/local-business |
| Organization | https://developers.google.com/search/docs/appearance/structured-data/organization |
| Article | https://developers.google.com/search/docs/appearance/structured-data/article |
| ProfilePage | https://developers.google.com/search/docs/appearance/structured-data/profile-page |
| BreadcrumbList | https://developers.google.com/search/docs/appearance/structured-data/breadcrumb |
| Review snippets (self-serving reviews make LocalBusiness/Organization pages ineligible) | https://developers.google.com/search/docs/appearance/structured-data/review-snippet |
| Search documentation updates (FAQ rich result deprecated 2026-05-08, documentation removed 2026-06-15) | https://developers.google.com/search/updates |
| Rich Results Test | https://search.google.com/test/rich-results |
| Schema Markup Validator | https://validator.schema.org/ |

## 4. Google Search Central — quality and spam policies

| Topic | URL |
|---|---|
| Spam policies (incl. scaled content abuse, site reputation abuse, doorway abuse) | https://developers.google.com/search/docs/essentials/spam-policies |
| Creating helpful, reliable, people-first content | https://developers.google.com/search/docs/fundamentals/creating-helpful-content |
| Core Web Vitals and Google Search results | https://developers.google.com/search/docs/appearance/core-web-vitals |

## 5. Google Search Console — help pages and APIs

| Topic | URL |
|---|---|
| Verify your site ownership (HTML file, HTML tag, Analytics, Tag Manager, Sites/Blogger, domain name provider) | https://support.google.com/webmasters/answer/9008080 |
| Managing owners, users and permissions (Owner and Full user can submit sitemaps) | https://support.google.com/webmasters/answer/7687615 |
| Sitemaps report | https://support.google.com/webmasters/answer/7451001 |
| Page indexing report ("Discovered" and "Crawled – currently not indexed") | https://support.google.com/webmasters/answer/7440203 |
| URL Inspection tool | https://support.google.com/webmasters/answer/9012289 |
| Search Console API: `sitemaps.submit` (PUT, scope `webmasters`) | https://developers.google.com/webmaster-tools/v1/sitemaps/submit |
| Search Console API: URL Inspection `index.inspect` | https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect |
| Search Console API usage limits (URL Inspection: 2,000/day and 600/min per site) | https://developers.google.com/webmaster-tools/limits |
| Indexing API quickstart (only JobPosting and BroadcastEvent-in-VideoObject pages) | https://developers.google.com/search/apis/indexing-api/v3/quickstart |
| OAuth 2.0 for server-to-server apps (service accounts) | https://developers.google.com/identity/protocols/oauth2/service-account |

## 6. Google Business Profile and Maps content policies

| Topic | URL |
|---|---|
| Guidelines for representing your business on Google | https://support.google.com/business/answer/3038177 |
| Maps user-generated content: prohibited and restricted content | https://support.google.com/contributionpolicy/answer/7400114 |
| Maps user-generated content: fake engagement | https://support.google.com/contributionpolicy/answer/11414422 |

## 7. Core Web Vitals (web.dev)

| Topic | URL |
|---|---|
| Web Vitals (good: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1) | https://web.dev/articles/vitals |
| Largest Contentful Paint | https://web.dev/articles/lcp |
| Optimize LCP | https://web.dev/articles/optimize-lcp |
| Cumulative Layout Shift | https://web.dev/articles/cls |
| Optimize CLS | https://web.dev/articles/optimize-cls |
| Interaction to Next Paint | https://web.dev/articles/inp |
| Optimize INP | https://web.dev/articles/optimize-inp |
| Fetch Priority API (`fetchpriority="high"`) | https://web.dev/articles/fetch-priority |
| Best practices for fonts (`font-display`, preload, self-hosting) | https://web.dev/articles/font-best-practices |

## 8. Protocols: sitemaps.org, RFC 9309, schema.org

| Topic | URL |
|---|---|
| Sitemaps XML protocol (50,000 URLs / 50 MB per file; W3C datetime `lastmod`) | https://www.sitemaps.org/protocol.html |
| RFC 9309 — Robots Exclusion Protocol | https://www.rfc-editor.org/rfc/rfc9309.html |
| schema.org LegalService | https://schema.org/LegalService |
| schema.org Attorney (superseded by LegalService) | https://schema.org/Attorney |
| schema.org LocalBusiness | https://schema.org/LocalBusiness |
| schema.org Organization | https://schema.org/Organization |
| schema.org OpeningHoursSpecification | https://schema.org/OpeningHoursSpecification |
| schema.org ProfilePage | https://schema.org/ProfilePage |
| schema.org Person | https://schema.org/Person |
| schema.org Article | https://schema.org/Article |
| schema.org BreadcrumbList | https://schema.org/BreadcrumbList |
| schema.org FAQPage | https://schema.org/FAQPage |

## 9. Bing Webmaster Tools and IndexNow

| Topic | URL |
|---|---|
| Bing Webmaster Guidelines | https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a |
| Bing URL submission (IndexNow, URL/Content Submission APIs, manual submission) | https://www.bing.com/webmasters/help/url-submission-62f2860b |
| Add and verify a site (import from Google Search Console, XML file, meta tag, CNAME, Domain Connect) | https://www.bing.com/webmasters/help/add-and-verify-site-12184f8b |
| Why IndexNow (Bing) | https://www.bing.com/indexnow |
| Getting access to the Bing Webmaster Tools API (API key) | https://learn.microsoft.com/en-us/bingwebmaster/getting-access |
| `SubmitUrlBatch` method (max 500 URLs per batch, subject to quota) | https://learn.microsoft.com/en-us/dotnet/api/microsoft.bing.webmaster.api.interfaces.iwebmasterapi.submiturlbatch?view=bing-webmaster-dotnet |
| Bing blog: calling the Webmaster API with cURL (SubmitUrl, SubmitUrlBatch, GetUrlSubmissionQuota) | https://blogs.bing.com/webmaster/2019/11/Accessing-Bing-webmaster-tools-api-using-cURL/ |
| Bing blog: the importance of setting `lastmod` | https://blogs.bing.com/webmaster/february-2023/The-Importance-of-Setting-the-lastmod-Tag-in-Your-Sitemap |
| IndexNow home (supporting engines named on the page) | https://www.indexnow.org/ |
| IndexNow documentation (key file, `keyLocation`, up to 10,000 URLs per POST, response codes) | https://www.indexnow.org/documentation |
| IndexNow FAQ (submissions are shared with all participating engines) | https://www.indexnow.org/faq |
| IndexNow participating engines (machine-readable list) | https://www.indexnow.org/searchengines.json |
| Yandex Webmaster: sitemap files (optional market) | https://yandex.com/support/webmaster/en/indexing-options/sitemap |

On 2026-11-02, `searchengines.json` listed: Bing, Yandex, Seznam, **Naver**, Yep, Internet Archive and
Amazonbot. Google is not a participant.

## 10. Naver Search Advisor

All pages are in Korean; titles are given in English translation.

| Topic | URL |
|---|---|
| "Purpose of search engine optimization" — basic guideline (ownership by meta tag or HTML file, allow Yeti, submit sitemap and RSS) | https://searchadvisor.naver.com/guide/seo-basic-intro |
| "Site registration and ownership verification" FAQ | https://searchadvisor.naver.com/guide/faq-start-register |
| "Setting up robots.txt" (crawler name Yeti; robots check in Webmaster Tools) | https://searchadvisor.naver.com/guide/seo-basic-robots |
| "RSS and sitemap submission" (same domain as the verified site; a sitemap file must be under 10 MB and at most 50,000 URLs; RSS must carry full text) | https://searchadvisor.naver.com/guide/request-feed |
| "Crawl requests and search exclusion" (manual web page collection request; removal steps) | https://searchadvisor.naver.com/guide/request-crawl |
| "Crawl-request API specification" (partner-only API; requires a partnership application) | https://searchadvisor.naver.com/guide/crawl-request-api |
| IndexNow: "Requesting page updates" (endpoint `https://searchadvisor.naver.com/indexnow`, up to 10,000 URLs per POST) | https://searchadvisor.naver.com/guide/indexnow-request |
| IndexNow: "Creating an API key" | https://searchadvisor.naver.com/guide/indexnow-api-key |
| IndexNow FAQ (does not replace sitemap/RSS/collection requests; bursts are throttled) | https://searchadvisor.naver.com/guide/indexnow-faq |

## 11. Daum Webmaster Tools and Kakao Map

| Topic | URL |
|---|---|
| Daum Webmaster Tools (login with site URL + PIN) | https://webmaster.daum.net/ |
| Daum help: issuing a Webmaster Tools PIN (8–12 characters; resets 24 months after consent) | https://cs.daum.net/faq/service/15/category/4118/detail/38321 |
| Kakao Business guide: Kakao Map store management (owners register and manage their place: hours, website, news, replies to reviews) | https://kakaobusiness.gitbook.io/main/partner/smb/channel/service_biz/mystore |
| Kakao Business guide: registering a place for KakaoTalk booking (incl. requesting a new place on Kakao Map; reviewed in about 3–5 days) | https://kakaobusiness.gitbook.io/main/tool/booking/pc/undefined-1 |

## 12. AI crawlers and llms.txt

| Topic | URL |
|---|---|
| OpenAI crawlers (OAI-SearchBot, GPTBot, ChatGPT-User) — `platform.openai.com/docs/bots` redirects here | https://developers.openai.com/api/docs/bots |
| Anthropic crawlers (ClaudeBot, Claude-User, Claude-SearchBot) and how to block them | https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler |
| Perplexity crawlers (PerplexityBot, Perplexity-User) | https://docs.perplexity.ai/guides/bots |
| Google-Extended (Gemini training/grounding token; no effect on Search) | https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers |
| The llms.txt proposal | https://llmstxt.org/ |

## 13. Korean attorney-advertising regulation

The Korean Bar Association publishes its rules only in Korean, as PDF attachments on its regulation pages.

| Topic | URL |
|---|---|
| Korean Bar Association Regulations on Attorney Advertising (amended 2025-02-06, promulgated 2025-02-10; PDF attached) | https://www.koreanbar.or.kr/pages/board/law_view.asp?category=3&page=1&searchstr=&searchtype=&seq=14402&teamcode=&types=6 |
| Korean Bar Association Rules on Attorney Advertising (the companion rules, amended 2025-06-30) | https://www.koreanbar.or.kr/pages/board/law_view.asp?teamcode=&page=1&seq=14681&types=6&category=3&searchtype=&searchstr= |

The Attorney-at-Law Act, the Act on Fair Labeling and Advertising, the Network Act and the Personal
Information Protection Act are statutes; read the current text on the official national law
information portal before citing an article number. No statute URL is listed here because none was
verified for this file.

## 14. Framework and server documentation (implementation)

| Topic | URL |
|---|---|
| Next.js `sitemap.(xml|js|ts)` (localized and image/video sitemaps) | https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap |
| Next.js `generateSitemaps` (child sitemaps at `/.../sitemap/[id].xml`; `id` is a Promise since v16) | https://nextjs.org/docs/app/api-reference/functions/generate-sitemaps |
| Next.js `robots.(txt|js|ts)` | https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots |
| Next.js `metadata` / `generateMetadata` (`alternates.canonical`, `alternates.languages`, `robots`) | https://nextjs.org/docs/app/api-reference/functions/generate-metadata |
| Next.js `redirects` (`permanent: true` = 308; `has: [{type: 'host'}]`) | https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects |
| Next.js JSON-LD guide (escape `<` as `<`) | https://nextjs.org/docs/app/guides/json-ld |
| next-sitemap package (Pages Router or any Next.js app) | https://www.npmjs.com/package/next-sitemap |
| WordPress 5.5 core sitemaps (`/wp-sitemap.xml`, `wp_sitemaps_enabled` filter) | https://make.wordpress.org/core/2020/07/22/new-xml-sitemaps-functionality-in-wordpress-5-5/ |
| Yoast SEO schema API (`wpseo_schema_graph`) | https://developer.yoast.com/features/schema/api/ |
| Yoast SEO canonical API (`wpseo_canonical`) | https://developer.yoast.com/features/seo-tags/canonical-urls/api/ |
| Rank Math filters and hooks (`rank_math/frontend/canonical`, `rank_math/frontend/robots`) | https://rankmath.com/kb/filters-hooks-api-developer/ |
| Cloudflare Single Redirects | https://developers.cloudflare.com/rules/url-forwarding/single-redirects/ |
| nginx `ngx_http_rewrite_module` (`return 301`) | https://nginx.org/en/docs/http/ngx_http_rewrite_module.html |
| Apache: redirecting and remapping with mod_rewrite | https://httpd.apache.org/docs/2.4/rewrite/remapping.html |

## 15. Off-site entity sources: Wikidata, Wikipedia, Knowledge Graph, review rules

Verified live on **2026-11-07** (used by `entity-authority-and-off-site.md`). Wikidata property IDs in that
file were checked the same day through the public Wikidata API (`wbgetentities`).

| Topic | URL |
|---|---|
| Wikidata notability policy (three criteria: sitelink / "serious and publicly available references" / structural need) | https://www.wikidata.org/wiki/Wikidata:Notability |
| Wikidata disclosure of paid editing (name every organisation or person that pays you) | https://www.wikidata.org/wiki/Wikidata:Disclosure_of_paid_editing |
| Wikidata request for comment on conflict of interest (neutral labels/descriptions, no edit-warring; community guidance, not policy) | https://www.wikidata.org/wiki/Wikidata:Requests_for_comment/Conflict_of_Interest |
| Wikidata property: official website (P856) | https://www.wikidata.org/wiki/Property:P856 |
| Wikipedia notability guideline for organizations and companies (significant, independent, reliable, secondary; multiple sources; press releases and routine coverage excluded) | https://en.wikipedia.org/wiki/Wikipedia:Notability_(organizations_and_companies) |
| Wikipedia paid-contribution disclosure (required by the Wikimedia Terms of Use; COI editors use talk-page proposals and Articles for Creation) | https://en.wikipedia.org/wiki/Wikipedia:Paid-contribution_disclosure |
| Wikipedia conflict-of-interest guideline | https://en.wikipedia.org/wiki/Wikipedia:Conflict_of_interest |
| Google Knowledge Graph Search API (`kgsearch.googleapis.com/v1/entities:search`) | https://developers.google.com/knowledge-graph |
| Google: Get verified on Google (claim a knowledge panel) | https://support.google.com/knowledgepanel/answer/7534902 |
| Google: About knowledge panels | https://support.google.com/knowledgepanel/answer/9163198 |
| Google Organization structured data (`sameAs`, `iso6523Code`, `legalName`, `foundingDate`, `taxID`, `vatID`; used to disambiguate the organisation) | https://developers.google.com/search/docs/appearance/structured-data/organization |
| Google spam policies — link spam includes "links with optimized anchor text in articles, guest posts, or press releases distributed on other sites" | https://developers.google.com/search/docs/essentials/spam-policies |
| FTC Consumer Reviews and Testimonials Rule Q&A (in force 2024-10-21; §465.2 fake reviews, §465.5 insider reviews need clear disclosure) | https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers |

Industry studies cited as **(third-party study)**, not re-verified: [Ahrefs, AI Overview brand correlation](https://ahrefs.com/blog/ai-overview-brand-correlation/) ·
[Ahrefs, AI brand visibility correlations](https://ahrefs.com/blog/ai-brand-visibility-correlations/) ·
[Profound, AI platform citation patterns](https://www.tryprofound.com/blog/ai-platform-citation-patterns) ·
[Semrush, most-cited domains in AI](https://www.semrush.com/blog/most-cited-domains-ai/).

Namuwiki's editing-policy pages (`나무위키:편집지침`) returned no readable policy text to the scraper on
2026-11-07; the Namuwiki notes are therefore marked (field experience).

## 16. Dropped or redirected URLs

- `https://developers.google.com/search/docs/appearance/structured-data/faqpage` — now redirects to the
  Search documentation updates page; Google removed the FAQ rich result documentation on 2026-06-15.
  Use the updates page (section 3) instead.
- `https://platform.openai.com/docs/bots` — redirects (302) to `https://developers.openai.com/api/docs/bots`,
  which is listed instead.
- `https://www.bing.com/webmasters/help/...` pages render with JavaScript; a plain fetch returns only the
  shell. They were verified with a rendering scraper.
- The Naver Search Advisor guide index (`https://searchadvisor.naver.com/guide`) loads its menu with
  JavaScript; the individual guide pages above were verified one by one.
- No official help page was found that documents Daum Webmaster Tools' sitemap and collection-request
  features in detail; those steps in `sitemaps-and-submission.md` are marked (field experience).
