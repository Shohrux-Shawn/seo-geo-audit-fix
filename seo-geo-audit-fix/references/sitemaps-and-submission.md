# Sitemaps and submission — build, publish, submit, monitor

Practical, step-by-step guidance for sitemaps, robots.txt and submission to Google, Bing (IndexNow),
Naver, Daum and (optionally) Yandex. Engine facts were checked on **2026-11-02**; URLs are in
`sources.md`. Use `scripts/sitemap_validate.py`, `scripts/indexnow_submit.py` and
`scripts/gsc_sitemaps.py` instead of ad-hoc code. Anything that submits data runs only after approval.

## Contents
1. Sitemap protocol: the rules
2. Special sitemaps: image, video, news, hreflang
3. Splitting strategy and the one-list rule
4. Generating sitemaps in common stacks
5. robots.txt for sitemaps and bots
6. Ownership and submission per engine
7. Monitoring and re-submission
8. Troubleshooting table

---

## 1. Sitemap protocol: the rules

| Rule | Detail |
|---|---|
| Size per file | Max **50,000 URLs** and **50 MB uncompressed** per sitemap file (and per sitemap index file). **Naver rejects a sitemap of 10 MB or more**, so keep files under 10 MB if Naver matters (e.g. 10,000–20,000 URLs per file). |
| Index | Over the limit → a sitemap index (`<sitemapindex>`) listing child sitemaps. Submit the index once; keep its URL stable (`/sitemap.xml` can *be* the index). |
| Namespace | `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">` (the `http://` namespace is correct). UTF-8, entity-escaped (`&amp;`). |
| `<loc>` | Absolute, fully qualified, on the **canonical host and scheme** (e.g. `https://www.example.com/...`). No relative paths, no session or UTM parameters. |
| What goes in | Only URLs that return **200**, are **indexable** (no `noindex` in meta or `X-Robots-Tag`), are **self-canonical**, and are not blocked by robots.txt. No redirects, no 404/410, no paginated duplicates of the same content. |
| `<lastmod>` | W3C datetime (`2026-11-02` or `2026-11-02T09:30:00+09:00`). Set it only when the **main content, structured data or links really changed**. Omit it when you don't know. Never the build time, request time or a view-counter update. |
| `changefreq`, `priority` | Ignored by Google. Harmless; don't spend effort on them. |
| Compression | `sitemap.xml.gz` is allowed; the 50 MB limit applies to the uncompressed file. Serve `.gz` with a correct `Content-Type` (`application/gzip` or `application/x-gzip`), or gzip at the HTTP layer instead (`Content-Encoding: gzip`) — not both. |
| Location and scope | A sitemap at `https://www.example.com/sitemap.xml` can list any URL on that host. Cross-host sitemaps work only when both hosts are verified in the same Search Console account or the sitemap is referenced from the target host's robots.txt. Simplest: one sitemap set per host. |
| Status of the sitemap itself | 200 with `Content-Type: application/xml` (or `text/xml`). Never an empty 200 when the data source fails: return **503 + `Retry-After` + `Cache-Control: no-store`** so engines retry instead of reading "all URLs removed". (field experience) |

Sources: [sitemaps.org protocol](https://www.sitemaps.org/protocol.html) · [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) · [Sitemap index files](https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps) · [Sitemaps ping endpoint is going away (lastmod, changefreq, priority)](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping) · [Naver: RSS and sitemap submission (10 MB)](https://searchadvisor.naver.com/guide/request-feed) · [Bing: the importance of lastmod](https://blogs.bing.com/webmaster/february-2023/The-Importance-of-Setting-the-lastmod-Tag-in-Your-Sitemap)

## 2. Special sitemaps: image, video, news, hreflang

**Image** (extra namespace; up to 1,000 images per `<url>`):
```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://www.example.com/team/jane-doe</loc>
    <image:image><image:loc>https://www.example.com/img/jane-doe.jpg</image:loc></image:image>
  </url>
</urlset>
```

**Video:** `xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"` with at least
`video:thumbnail_loc`, `video:title`, `video:description` and `video:content_loc` or `video:player_loc`.

**News** (only for sites in Google News; articles from the last 2 days; up to 1,000 URLs per file):
`xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"` with `news:publication` (name, language),
`news:publication_date`, `news:title`.

**hreflang in the sitemap** (an alternative to `<link rel="alternate">` in HTML; use one method, not
a different set in each):
```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://www.example.com/en/fees</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.example.com/en/fees"/>
    <xhtml:link rel="alternate" hreflang="ko" href="https://www.example.com/fees"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://www.example.com/fees"/>
  </url>
  <url>
    <loc>https://www.example.com/fees</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.example.com/en/fees"/>
    <xhtml:link rel="alternate" hreflang="ko" href="https://www.example.com/fees"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://www.example.com/fees"/>
  </url>
</urlset>
```
Rules: every language version gets its own `<url>` entry; each lists **all** versions **including
itself**; links are reciprocal; codes are ISO 639-1 language (+ optional ISO 3166-1 region), or
`x-default`; every `href` is a 200, indexable, self-canonical URL that is also in the sitemap.
`sitemap_validate.py` checks self-reference, reciprocity, code format and alternates missing from the sitemap.

Sources: [Image sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps) · [Video sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/video-sitemaps) · [News sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/news-sitemap) · [Localized versions (hreflang, x-default)](https://developers.google.com/search/docs/specialty/international/localized-versions)

## 3. Splitting strategy and the one-list rule

Split by **content type**, then by **locale**, then by size:
```
/sitemap.xml                 (index)
  /sitemaps/pages.xml        static pages, hubs, location pages
  /sitemaps/articles-1.xml   articles 1–10,000 (by id or date)
  /sitemaps/articles-2.xml
  /sitemaps/people.xml       profile pages
  /sitemaps/en/articles.xml  per-locale files when locales differ in size
```
Why: Search Console's Sitemaps and Page indexing reports can be filtered per child sitemap, so a
split by type tells you *which template* is not getting indexed.

**One list, one source.** The question "is this URL open (200)?" and the question "do we offer it (in
the sitemap, hreflang, language switcher, footer)?" must be answered by the **same shared list or
function**. If the locale/visibility gate and the sitemap use different lists, they drift silently:
pages announced by `hreflang` but missing from the sitemap pile up in "Discovered – currently not
indexed". Where a copy is unavoidable, add a build-time assert (with a negative test) that both lists
are equal. Hiding a page from the menu is a navigation decision; removing it from the sitemap is an
indexing decision — never one config for both. (field experience)

```ts
// lib/indexable.ts — the single source used by the route gate, sitemap, hreflang and switcher
export async function indexableUrls(locale: string): Promise<{ url: string; updatedAt?: Date }[]> {
  const rows = await db.article.findMany({
    where: { locale, status: 'published', noindex: false },
    select: { slug: true, contentUpdatedAt: true }, // a real content date, not updatedAt
  })
  return rows.map(r => ({ url: `${SITE_URL}/${locale}/articles/${r.slug}`, updatedAt: r.contentUpdatedAt ?? undefined }))
}
```

Sources: [Sitemap index files](https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps) · [Sitemaps report](https://support.google.com/webmasters/answer/7451001) · [Page indexing report](https://support.google.com/webmasters/answer/7440203) · one-list rule: (field experience)

## 4. Generating sitemaps in common stacks

### Next.js App Router — `app/sitemap.ts` (+ `generateSitemaps` for large sets)
```ts
// app/sitemap.ts — small site
import type { MetadataRoute } from 'next'
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const pages = await indexableUrls('en')
  return pages.map(p => ({
    url: p.url,
    ...(p.updatedAt ? { lastModified: p.updatedAt } : {}),   // omit when unknown
    alternates: { languages: await languagesFor(p.url) },     // optional hreflang
  }))
}
```
```ts
// app/articles/sitemap.ts — large set: child files at /articles/sitemap/0.xml, /1.xml ...
import type { MetadataRoute } from 'next'
const PER_FILE = 10000
export async function generateSitemaps() {
  const total = await countIndexableArticles()
  return Array.from({ length: Math.ceil(total / PER_FILE) }, (_, id) => ({ id }))
}
export default async function sitemap(props: { id: Promise<string> }): Promise<MetadataRoute.Sitemap> {
  const id = Number(await props.id)              // a Promise since Next.js 16; a number before
  const rows = await listIndexableArticles({ offset: id * PER_FILE, limit: PER_FILE })
  return rows.map(r => ({ url: r.url, lastModified: r.contentUpdatedAt }))
}
```
Notes: check whether your Next.js version emits a sitemap index for `generateSitemaps` children; if it
does not, publish your own index (a route handler that lists the child URLs) or list each child file
in robots.txt and in the consoles.
`sitemap.ts` is cached by default; if data changes after deploy, use revalidation (e.g.
`export const revalidate = 3600`) and make the handler **throw** on data failure so the last good copy
or an error is served — never an empty list.

### Next.js Pages Router — `pages/sitemap.xml.ts` or next-sitemap
```ts
// pages/sitemap.xml.ts
import type { GetServerSideProps } from 'next'
const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;')
export const getServerSideProps: GetServerSideProps = async ({ res }) => {
  let rows
  try { rows = await indexableUrls('ko') } catch {
    res.statusCode = 503; res.setHeader('Retry-After', '600'); res.setHeader('Cache-Control', 'no-store')
    res.end(); return { props: {} }
  }
  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${rows.map(r => `  <url><loc>${esc(r.url)}</loc>${r.updatedAt ? `<lastmod>${r.updatedAt.toISOString()}</lastmod>` : ''}</url>`).join('\n')}
</urlset>`
  res.setHeader('Content-Type', 'application/xml; charset=utf-8')
  res.setHeader('Cache-Control', 'public, s-maxage=3600, stale-while-revalidate=600')
  res.end(body)
  return { props: {} }
}
export default function Sitemap() { return null }
```
For static exports, `next-sitemap` generates `sitemap.xml`, child files and `robots.txt` at build time
(`postbuild: next-sitemap`); set `siteUrl` to the **www/https canonical** origin and use `exclude` for
private and noindex paths.

### WordPress
- Core (5.5+): `/wp-sitemap.xml` (index). Disable with `add_filter('wp_sitemaps_enabled', '__return_false');` when an SEO plugin provides its own.
- Yoast SEO: `/sitemap_index.xml`; Rank Math: `/sitemap_index.xml`. Use **one** generator; two generators means two competing indexes.
- Exclude noindex post types/taxonomies in the plugin settings; check that attachment pages and tag archives are not offered.
- After a plugin switch, update robots.txt `Sitemap:` lines and re-submit the new index in each console.

### Static-site generators (Hugo, Jekyll, Eleventy, Astro)
- Use the generator's sitemap feature or plugin (e.g. Hugo has a built-in `sitemap.xml`; Astro `@astrojs/sitemap`; Jekyll `jekyll-sitemap`).
- Set the production base URL (`baseURL`, `url`, `site`) to the canonical origin; a missing base URL produces relative or `localhost` `<loc>`s.
- Take `lastmod` from front matter (`lastmod:` / `updated:`) or git commit dates of the content file, not the build time.

### Nginx serving static sitemap files
```nginx
location = /sitemap.xml { default_type application/xml; add_header Cache-Control "public, max-age=3600"; try_files $uri =404; }
location ^~ /sitemaps/   { default_type application/xml; gzip on; gzip_types application/xml text/xml; try_files $uri =404; }
location = /robots.txt  { default_type text/plain; try_files $uri =404; }
```
Regenerate the files as part of the deploy (not by hand) and purge CDN caches for `/sitemap*` and
`/robots.txt` after each deploy.

Sources: [Next.js sitemap](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap) · [Next.js generateSitemaps](https://nextjs.org/docs/app/api-reference/functions/generate-sitemaps) · [next-sitemap](https://www.npmjs.com/package/next-sitemap) · [WordPress 5.5 core sitemaps](https://make.wordpress.org/core/2020/07/22/new-xml-sitemaps-functionality-in-wordpress-5-5/) · [nginx rewrite/return module](https://nginx.org/en/docs/http/ngx_http_rewrite_module.html) · 503-on-failure and cache purge: (field experience)

## 5. robots.txt for sitemaps and bots

```
User-agent: *
Disallow: /admin/
Disallow: /api/
Disallow: /mypage/

User-agent: GPTBot          # training crawler: an owner decision
Disallow: /admin/
Disallow: /api/
Disallow: /mypage/

Sitemap: https://www.example.com/sitemap.xml
#DaumWebMasterTool:<hash>:<suffix>
```
- `Sitemap:` lines take **absolute** URLs, can appear anywhere, and are not tied to a group. List the index (or each child) for every host.
- **A bot with its own `User-agent` group ignores the `*` group** (only the most specific matching group applies). Repeat the shared disallows inside every named group, or don't create a named group.
- Never disallow `/sitemap.xml`, `/robots.txt`, `/favicon.ico`, CSS/JS needed for rendering, or the IndexNow key file.
- robots.txt blocks crawling, not indexing. To remove a page use `noindex` or 404/410 (and keep it crawlable so the engine can see that).
- AI crawlers (tokens as documented by each vendor on 2026-11-02):
  - search/user agents — `OAI-SearchBot`, `ChatGPT-User`, `Claude-SearchBot`, `Claude-User`, `PerplexityBot`, `Perplexity-User`: allow them if you want to be cited in AI answers;
  - training — `GPTBot`, `ClaudeBot`, and the `Google-Extended` token (Gemini training/grounding; does not affect Google Search): an owner decision.
- Naver's crawler is `Yeti`; Daum's is `Daum`. Check server/WAF bot filters too: a 403/429 at the WAF overrides a friendly robots.txt.
- RFC 9309 requires crawlers to parse at least 500 KiB; keep robots.txt small.

Sources: [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html) · [How Google interprets robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt) · [robots.txt intro](https://developers.google.com/search/docs/crawling-indexing/robots/intro) · [Google common crawlers / Google-Extended](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers) · [OpenAI crawlers](https://developers.openai.com/api/docs/bots) · [Anthropic crawlers](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler) · [Perplexity crawlers](https://docs.perplexity.ai/guides/bots) · [Naver: robots.txt](https://searchadvisor.naver.com/guide/seo-basic-robots)

## 6. Ownership and submission per engine

General order for a new site: canonical host decided → sitemap and robots.txt live and validated
(`sitemap_validate.py`) → verify ownership in each console → submit → check the next day.
Ownership verification and sitemap submission in a console are done by the **owner, signed in**;
an agent prepares the files and values and reads the result.

### 6.1 Google Search Console
1. **Property type.** *Domain property* (`sc-domain:example.com`; covers all hosts and schemes; DNS TXT verification only) or *URL-prefix property* (`https://www.example.com/`; HTML file, HTML tag, Google Analytics, Google Tag Manager, Google Sites/Blogger, or domain name provider). Use a Domain property when DNS access exists; otherwise a URL-prefix property that matches the **canonical** host exactly.
2. **Verify.** Deploy the file or meta tag first, then press Verify. Keep the token in place permanently (removing it un-verifies the property). Keep both HTML file and meta tag if the CMS might drop one.
3. **Submit.** Indexing → Sitemaps → enter `sitemap.xml` (or the index URL) → Submit. Submit the index, not every child.
4. **API submit (optional, automation).** Search Console API `sitemaps.submit`: `PUT https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}` with OAuth scope `https://www.googleapis.com/auth/webmasters`. With a **service account**: create it in Google Cloud, enable the Search Console API, download its JSON key, then **add the service-account e-mail as a user in Search Console → Settings → Users and permissions** — **Owner or Full user** to submit sitemaps (Restricted can only read). Use `scripts/gsc_sitemaps.py list|submit` (`submit` needs `--apply`).
5. **URL Inspection API** (`POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect`): read-only status of one URL. Quota **2,000 per day and 600 per minute per property**. It cannot request indexing; "Request indexing" exists only in the UI (manual, small numbers).
6. **Indexing API** is officially **only for pages with `JobPosting` or `BroadcastEvent` (in a `VideoObject`)**. Do not use it for articles, products or location pages.
7. **No ping.** Google's sitemap ping endpoint was deprecated on 2023-06-26 and stopped working six months later (requests return 404). Submit via Search Console or a `Sitemap:` line in robots.txt.

Sources: [Verify site ownership](https://support.google.com/webmasters/answer/9008080) · [Users and permissions](https://support.google.com/webmasters/answer/7687615) · [Sitemaps report](https://support.google.com/webmasters/answer/7451001) · [sitemaps.submit API](https://developers.google.com/webmaster-tools/v1/sitemaps/submit) · [URL Inspection API](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect) · [API usage limits](https://developers.google.com/webmaster-tools/limits) · [Indexing API quickstart](https://developers.google.com/search/apis/indexing-api/v3/quickstart) · [Service accounts](https://developers.google.com/identity/protocols/oauth2/service-account) · [Ping deprecation](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping)

### 6.2 Bing Webmaster Tools
1. **Add the site.** Fastest: *Import from Google Search Console* (imports verified sites and their sitemaps; up to 100 sites at a time). Otherwise verify with an XML file, a meta tag, a CNAME record or Domain Connect.
2. **Sitemaps.** Sitemaps → Submit sitemap (the index URL). Status "Success" right after submit can be optimistic; re-check the next day for "Processed" and the URL count. (field experience)
3. **IndexNow** (recommended by Bing for automatic change notification) — see 6.3.
4. **URL Submission API** (Bing only): `POST https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlBatch?apikey=<key>` with `{"siteUrl": "...", "urlList": [...]}`; at most 500 URLs per batch, within the daily quota (`GetUrlSubmissionQuota`). The API key comes from Bing Webmaster Tools → Settings → API access; keep it in an env var.
5. Bing documents `lastmod` as an important recrawl signal: a fake `lastmod` hurts more here.

Sources: [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a) · [Add and verify site](https://www.bing.com/webmasters/help/add-and-verify-site-12184f8b) · [URL submission](https://www.bing.com/webmasters/help/url-submission-62f2860b) · [API access](https://learn.microsoft.com/en-us/bingwebmaster/getting-access) · [SubmitUrlBatch](https://learn.microsoft.com/en-us/dotnet/api/microsoft.bing.webmaster.api.interfaces.iwebmasterapi.submiturlbatch?view=bing-webmaster-dotnet) · [Bing API with cURL](https://blogs.bing.com/webmaster/2019/11/Accessing-Bing-webmaster-tools-api-using-cURL/) · [Bing lastmod](https://blogs.bing.com/webmaster/february-2023/The-Importance-of-Setting-the-lastmod-Tag-in-Your-Sitemap)

### 6.3 IndexNow protocol
1. **Key.** 8–128 characters from `a-z A-Z 0-9 -`. Generate once (e.g. `python3 -c "import uuid;print(uuid.uuid4().hex)"`), store it in an env var (`INDEXNOW_KEY`), never in the repo.
2. **Key file.** Host a UTF-8 text file at `https://www.example.com/<key>.txt` whose content is the key. Or host it elsewhere on the same host and send `keyLocation`; then only URLs under that file's directory are accepted. It must return 200 without redirects or auth, and must not be disallowed in robots.txt.
3. **Submit.** One URL: `GET https://api.indexnow.org/indexnow?url=<url>&key=<key>`. A batch: `POST https://api.indexnow.org/indexnow` with `Content-Type: application/json; charset=utf-8` and `{"host":"www.example.com","key":"...","keyLocation":"...","urlList":[...]}` — **up to 10,000 URLs per POST**, all on that host.
4. **Responses.** 200 OK · 202 accepted, key validation pending · 400 bad request · 403 key not valid · 422 URLs don't belong to the host or key doesn't match · 429 too many requests. 200 means "received", not "indexed".
5. **Participants.** A submission to any participating endpoint is shared with all of them. On **2026-11-02**, indexnow.org's `searchengines.json` listed **Bing, Yandex, Seznam, Naver, Yep, Internet Archive and Amazonbot**, and Naver documents its own endpoint (`https://searchadvisor.naver.com/indexnow`). **Google is not a participant.**
6. **When to ping.** On create, update **and delete** (a URL that now returns 404/410 or a redirect), from the CMS or publish pipeline, not from a cron that re-sends everything. Send only URLs changed since you started using IndexNow; don't re-send unchanged URLs.
7. Use `scripts/indexnow_submit.py` — it checks the key file first and posts only with `--apply`.

Sources: [IndexNow documentation](https://www.indexnow.org/documentation) · [IndexNow FAQ](https://www.indexnow.org/faq) · [IndexNow participants](https://www.indexnow.org/searchengines.json) · [IndexNow home](https://www.indexnow.org/) · [Naver: IndexNow requests](https://searchadvisor.naver.com/guide/indexnow-request) · [Naver: IndexNow FAQ](https://searchadvisor.naver.com/guide/indexnow-faq) · [Why IndexNow (Bing)](https://www.bing.com/indexnow) · ping-on-delete: (field experience)

### 6.4 Naver Search Advisor
1. **Register the site** in Naver Search Advisor → Webmaster Tools with the exact canonical origin (`https://www.example.com`). Scheme, `www` and port variants are separate sites.
2. **Verify ownership** with the HTML file upload or the HTML meta tag. The home page must answer without a JavaScript or meta-refresh redirect (use an HTTP redirect), and the tag must not sit inside a frame. Make sure the firewall does not block Naver's crawler.
3. **Submit the sitemap:** Request → Sitemap submission. Every URL must be on the verified domain; the file must be **under 10 MB** and at most 50,000 URLs; a slow response can block submission.
4. **Submit RSS:** Request → RSS submission. Naver treats submitted RSS and sitemaps as "content feeds" it revisits; new content is often found faster via RSS. The feed needs at least one item and **full article text** (not excerpts), under 10 MB, on the verified domain. Exclude noindex and hidden paths.
5. **Web page collection request:** Request → Web page collection, for a few important URLs. Don't re-request the same URL daily; a request is a hint, not a guarantee. (Field experience: the tool showed a limit of about 50 URLs per day; the guide page does not state a number.)
6. **robots.txt check:** Verification → robots.txt (re-collect and validate) shows how Yeti reads your file.
7. **Removing a page:** delete it so it returns 404, confirm with the page-optimization check, then Request → Web page search exclusion.
8. **APIs.** As of 2026-11-02 there is **no public API for sitemap or RSS submission**. Naver's crawl-request API (`https://apis.naver.com/searchadvisor/crawl-request/submit.json`) exists but is **partner-only** (apply through a NAVER partnership proposal; bearer token; up to 1,000 URLs per call). The public programmatic route is **IndexNow**, which Naver supports.
9. Naver Search Advisor often blocks automated browsers. Ask the owner for screenshots of the reports instead and mark the rest NOT VERIFIED.

Sources: [Naver: basic guideline](https://searchadvisor.naver.com/guide/seo-basic-intro) · [Naver: registration and ownership](https://searchadvisor.naver.com/guide/faq-start-register) · [Naver: RSS and sitemap submission](https://searchadvisor.naver.com/guide/request-feed) · [Naver: crawl requests and exclusion](https://searchadvisor.naver.com/guide/request-crawl) · [Naver: robots.txt](https://searchadvisor.naver.com/guide/seo-basic-robots) · [Naver: crawl-request API (partner-only)](https://searchadvisor.naver.com/guide/crawl-request-api) · [Naver: IndexNow](https://searchadvisor.naver.com/guide/indexnow-request)

### 6.5 Daum Webmaster Tools
1. Open Daum Webmaster Tools and choose "Issue a PIN code": enter the site URL and an 8–12 character PIN of your choice, accept the terms. The PIN acts as the login for that site; consent resets after 24 months, so re-issue then.
2. The tool gives a verification line to put in robots.txt as a comment, in the form `#DaumWebMasterTool:<hash>:<suffix>`. Add it (top of the file is fine), deploy, then log in with site URL + PIN to complete verification. (field experience: format as shown by the tool)
3. Submit the sitemap and use the collection request in the tool's menus. Daum's crawler is `Daum`; allow it in robots.txt and the WAF. (field experience)
4. Kakao place data is separate from Daum web search: listings are managed in Kakao Map store management (see `korea-search.md`).

Sources: [Daum Webmaster Tools](https://webmaster.daum.net/) · [Daum help: PIN issuance](https://cs.daum.net/faq/service/15/category/4118/detail/38321) · robots.txt line, sitemap and collection steps: (field experience)

### 6.6 Yandex (optional)
Only for sites targeting markets where Yandex matters: verify in Yandex Webmaster, add the sitemap there,
and note that IndexNow submissions already reach Yandex.

Sources: [Yandex: sitemap files](https://yandex.com/support/webmaster/en/indexing-options/sitemap) · [IndexNow participants](https://www.indexnow.org/searchengines.json)

## 7. Monitoring and re-submission

| What | Where | What to do |
|---|---|---|
| Submitted vs indexed per child sitemap | GSC → Sitemaps (status, discovered URLs) and Page indexing filtered by sitemap | A child sitemap with a low indexed share points to a template problem. Compare per type. |
| "Discovered – currently not indexed" | GSC → Page indexing | Google found the URL but has not crawled it yet. Fix crawl paths (real `<a href>` links in HTML), internal links, duplication and quality. Not fixed by re-submitting. |
| "Crawled – currently not indexed" | GSC → Page indexing | Crawled, not indexed (yet). Improve or merge the content; Google says resubmitting is not needed. |
| Sitemap errors ("Couldn't fetch", "Sitemap is HTML", invalid date, URL not allowed) | GSC → Sitemaps → open the sitemap | Fix the file (status, content type, domain, date format), then re-submit once. |
| Bing sitemap status and URL count | Bing WMT → Sitemaps | "Error / 0 URLs" while GSC reads the same file: check it is a clean `urlset` on the canonical host; re-submit; check the next day. (field experience) |
| Naver collection and indexing | Naver Search Advisor reports (owner screenshots) | Flat index count while the sitemap grows → discovery problem: RSS + internal links. Low collection → server blocking Yeti (429/444). (field experience) |
| Server view | Access logs with host + bot UA | 301 on sitemap fetches = an old `http://` or non-www sitemap still registered somewhere. |

Re-submission rules:
- Re-submit only after a **real change** (new child sitemap, large URL addition, fixed errors). Re-submitting an unchanged sitemap does nothing.
- Never call deprecated ping endpoints (Google's ping returns 404; Bing removed anonymous sitemap submission in 2022, per Google's announcement). Use the consoles, robots.txt `Sitemap:` lines and IndexNow.
- Re-check counts at +1 day (fetch status), +14 and +28 days (indexing). Search Console data lags by days.

Sources: [Sitemaps report](https://support.google.com/webmasters/answer/7451001) · [Page indexing report](https://support.google.com/webmasters/answer/7440203) · [Ping deprecation](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping) · [Link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)

## 8. Troubleshooting table

| Symptom | Likely cause | Fix |
|---|---|---|
| `<loc>` URLs on the wrong host (`http://`, apex instead of `www`, a staging or `localhost` host, `www.example.comhttps://...`) | `siteUrl`/base URL misconfigured; absolute and relative paths mixed in one loop | Build URLs from one canonical `SITE_URL` constant; validate with `sitemap_validate.py --host www.example.com`; re-submit. |
| Many sitemap URLs redirect (301/308) or are non-canonical | Old URLs, trailing-slash mismatch, uppercase/encoded variants, canonical pointing elsewhere | Emit only final, self-canonical URLs; normalise trailing slashes; fix canonical tags or remove the URL. |
| `lastmod` identical on every URL, or always "now" | Generated from build/request time or a cache timestamp; a view counter updating `updatedAt` | Use a real content-change date; omit `lastmod` when unknown; exclude counters from `updatedAt` (e.g. `timestamps: false` on the increment). |
| Sitemap "blocked by robots.txt" | `Disallow: /sitemap` or a broad rule; WAF blocks bots | Allow the sitemap path; test the bot UA with curl through the CDN. |
| URLs in the sitemap reported as soft 404 | Empty list pages, client-rendered text, "not found" pages returning 200, unknown paths redirected to `/` | Return real 404/410; server-render the text; drop empty lists from the sitemap (`noindex, follow` until they have items). |
| Sitemap not refreshed after deploy | Static file generated once; Next.js `sitemap.ts` cached at build with no revalidation; generator not in the deploy script | Generate in the build/deploy step or revalidate; check the URL count right after deploy. |
| CDN serves a stale sitemap (old count, old URLs) | Long `max-age`/`s-maxage`; cache key ignores the deploy | Shorter cache for `/sitemap*` and `/robots.txt`; purge them on deploy; verify with `curl -sI` (`Age`, `cf-cache-status`, `x-cache`). |
| Sitemap suddenly has far fewer URLs (empty 200) | Data API failed and the code fell back to `[]` | Return 503 + `Retry-After` + `no-store` on any data failure; alert on a large URL-count drop. (field experience) |
| Naver rejects the sitemap | File ≥ 10 MB, URL domain differs from the verified site, slow response | Split into smaller files; keep every URL on the verified origin; serve statically or cached. |
| Bing shows "Error" or 0 URLs while Google is fine | Stale registration of an old sitemap URL; transient fetch failure | Remove stale entries, re-submit the canonical index, re-check next day. (field experience) |
| Sitemap index lists child files that 404 | Child file names changed (e.g. Next.js `/sitemap/[id].xml` vs `/sitemap.xml/[id]` in older versions) | List the exact child URLs the framework serves; validate the index with `sitemap_validate.py`. |
| hreflang alternates missing from the sitemap | Locale gate and sitemap use different lists | One shared list (section 3); `sitemap_validate.py` reports alternates not offered. |

Sources: [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) · [HTTP status codes and soft 404s](https://developers.google.com/search/docs/crawling-indexing/http-network-errors) · [Redirects](https://developers.google.com/search/docs/crawling-indexing/301-redirects) · [Canonicalization](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) · [Naver: sitemap rules](https://searchadvisor.naver.com/guide/request-feed) · [Next.js generateSitemaps](https://nextjs.org/docs/app/api-reference/functions/generate-sitemaps) · rows marked (field experience) come from audits
