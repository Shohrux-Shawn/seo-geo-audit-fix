# Implementation playbook — code recipes for applying fixes

Concrete, minimal recipes the AI can apply **after approval** (Step 4 of SKILL.md). Each recipe is a
starting point: read the project's real code first, match its conventions, and change as little as
possible. Placeholders: `www.example.com`, `<firm>`, `<city>`. URLs are in `sources.md`.

## Contents
1. Safe change workflow (always)
2. Redirects: one hop to the canonical host; 410 for removed content
3. Canonical, meta robots, hreflang + x-default
4. Titles and H1 templates
5. JSON-LD: entity graph, people, articles, breadcrumbs
6. robots.txt generation
7. llms.txt
8. Core Web Vitals fixes
9. Internal linking
10. Thin and duplicate content: which tool when
11. CMS content persistence
12. Live verification: curl checklist

---

## 1. Safe change workflow (always)

1. **Branch:** `git switch -c seo/<short-topic>` from the branch the project deploys from. Never work on the deploy branch directly.
2. **Read before editing:** find where the value is produced (template, config constant, CMS field, middleware). Fix it at the source, once.
3. **Minimal diff:** one concern per commit (e.g. "redirect apex to www", not "SEO fixes").
4. **Keep line endings and encoding:** check with `git diff --stat` vs `git diff --ignore-space-at-eol --stat`. If the numbers differ, an editor rewrote line endings — restore them before committing. Don't reformat files you didn't need to touch.
5. **Stage only relevant files:** `git add -p <files>`; never `git add -A`. No lockfiles, build output, tool folders or `.env`.
6. **No secrets** in code, commits, logs or reports. Tokens for verification can be public (meta tags); API keys cannot.
7. **Test and build:** run the project's tests, type-check and production build. For SEO changes also render the page and inspect the HTML (`curl`), because many SEO bugs only show at runtime.
8. **Show the diff and wait for approval** before committing/pushing if the user asked for review.
9. **Deploy per the project's rules** (who deploys, time window, one site at a time, backend before frontends).
10. **Verify live** with the curl checklist (section 12). A change is done only when the public URL shows it.

Sources: (field experience) — derived from incidents in `lessons-learned.md` §4 and §7.

## 2. Redirects: one hop to the canonical host; 410 for removed content

Goal: every variant (`http://example.com`, `http://www.`, `https://example.com`) reaches
`https://www.example.com/<same path>` in **one 301/308 hop**; moved pages go to their **matching** new
URL; removed pages return **410** (or 404), never a redirect to the home page.

**Nginx**
```nginx
server {                       # port 80, both hosts -> https www in one hop
  listen 80; server_name example.com www.example.com;
  return 301 https://www.example.com$request_uri;
}
server {                       # https apex -> https www
  listen 443 ssl; server_name example.com;
  ssl_certificate /etc/ssl/example.pem; ssl_certificate_key /etc/ssl/example.key;
  return 301 https://www.example.com$request_uri;
}
server {
  listen 443 ssl; server_name www.example.com;
  # removed content
  location = /old-campaign { return 410; }
  location ^~ /legacy-board/ { return 410; }
  # moved content (exact map is better than regex chains)
  location = /practice/divorce-old { return 301 /practice/divorce; }
  # ... proxy_pass / root ...
}
```
Test with `nginx -t` before reload.

**Apache (.htaccess or vhost)**
```apache
RewriteEngine On
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} !^www\.example\.com$ [NC]
RewriteRule ^ https://www.example.com%{REQUEST_URI} [R=301,L]
RewriteRule ^old-campaign$ - [G,L]          # 410 Gone
Redirect 301 /practice/divorce-old /practice/divorce
```
Behind a proxy or load balancer, `%{HTTPS}` may always be off: test `X-Forwarded-Proto` instead, or you get a loop.

**Next.js `next.config.js`**
```js
module.exports = {
  async redirects() {
    return [
      { source: '/:path*', has: [{ type: 'host', value: 'example.com' }],
        destination: 'https://www.example.com/:path*', permanent: true },   // 308
      { source: '/practice/divorce-old', destination: '/practice/divorce', permanent: true },
    ]
  },
}
```
`permanent: true` sends **308** (search engines treat 308 like 301). Host redirects are better done at
the proxy/CDN so `http://` is also covered in the same hop. For 410 in the App Router, return a
response with `status: 410` from a route handler or middleware for the removed paths.

**Cloudflare Single Redirects** (Rules → Redirect Rules): when `http.host eq "example.com"` → dynamic
target `concat("https://www.example.com", http.request.uri.path)`, status **301**, *preserve query
string* on. Make sure "Always Use HTTPS" and the origin's own redirects don't add a second hop.

Check every variant: `for u in http://example.com/ http://www.example.com/ https://example.com/; do curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" "$u"; done` — each line must be `301` (or 308) straight to `https://www.example.com/`.

Note: Google treats 404 and 410 the same way; 410 is still the honest signal for deliberately removed
content and some engines drop it sooner. (field experience for the "sooner" part)

Sources: [Redirects and Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects) · [HTTP status codes](https://developers.google.com/search/docs/crawling-indexing/http-network-errors) · [nginx rewrite module](https://nginx.org/en/docs/http/ngx_http_rewrite_module.html) · [Apache mod_rewrite remapping](https://httpd.apache.org/docs/2.4/rewrite/remapping.html) · [Next.js redirects](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects) · [Cloudflare Single Redirects](https://developers.cloudflare.com/rules/url-forwarding/single-redirects/) · [Bing guidelines (301/302, 404 for deleted)](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a)

## 3. Canonical, meta robots, hreflang + x-default

Rules: one absolute, self-referencing canonical per indexable page (on the canonical host); `noindex`
pages don't need a canonical to another URL; hreflang sets are complete, reciprocal, include the page
itself and `x-default`; every alternate is a 200, indexable, self-canonical URL.

**Next.js App Router**
```ts
// app/layout.tsx
export const metadata = { metadataBase: new URL('https://www.example.com') }

// app/[locale]/fees/page.tsx
import type { Metadata } from 'next'
export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params
  const path = '/fees'
  const languages = await availableLocales(path)          // from the ONE shared list
  return {
    title: 'Consultation fees and process',
    alternates: {
      canonical: locale === 'ko' ? path : `/${locale}${path}`,
      languages: {
        ...Object.fromEntries(languages.map(l => [l, l === 'ko' ? path : `/${l}${path}`])),
        'x-default': path,
      },
    },
    robots: { index: true, follow: true },   // { index: false, follow: true } for thin/utility pages
  }
}
```

**Next.js Pages Router (`next/head`)**
```tsx
import Head from 'next/head'
<Head>
  <link rel="canonical" href={`https://www.example.com${pathWithoutQuery}`} />
  {alternates.map(a => <link key={a.lang} rel="alternate" hrefLang={a.lang} href={a.href} />)}
  <link rel="alternate" hrefLang="x-default" href={`https://www.example.com${defaultPath}`} />
  {noindex && <meta name="robots" content="noindex, follow" />}
</Head>
```
Watch out: `next/link` and `router.push` add the active locale to links; pin `locale={false}` or the
default locale for single-language routes, or hreflang/links will point to 404s.

**WordPress**
```php
// functions.php (child theme) — Yoast
add_filter('wpseo_canonical', function ($url) {
  return is_paged() ? $url : strtok($url, '?');            // drop tracking params from canonicals
});
add_filter('wpseo_robots', function ($robots) {
  return is_tag() ? 'noindex, follow' : $robots;           // thin tag archives
});
// Rank Math equivalents: 'rank_math/frontend/canonical' and 'rank_math/frontend/robots' (array)
// Without an SEO plugin: print tags in wp_head
add_action('wp_head', function () {
  if (is_singular()) echo '<link rel="canonical" href="' . esc_url(get_permalink()) . '" />' . "\n";
});
```
For hreflang on WordPress use one multilingual plugin's built-in output (WPML/Polylang); don't add a
second set by hand.

Also send `X-Robots-Tag: noindex` from the server for non-HTML files (PDF drafts, feeds you don't want indexed).

Sources: [Specify a canonical](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) · [Robots meta tag / X-Robots-Tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag) · [Localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions) · [Next.js generateMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) · [Yoast canonical API](https://developer.yoast.com/features/seo-tags/canonical-urls/api/) · [Rank Math filters](https://rankmath.com/kb/filters-hooks-api-developer/) · locale-link trap: (field experience)

## 4. Titles and H1 templates

Pattern: `<query phrase first> <qualifier>` + optional ` - <Brand>` suffix only on home, location and
service pages. Article titles carry no brand and no fixed prefix. The H1 states the entity and topic
(e.g. "<city> divorce lawyer at <firm>"), not a slogan; it can be longer than the title.

```ts
// lib/seo-title.ts
const BRAND = '<firm>'
export function seoTitle(main: string, opts: { brand?: boolean; max?: number } = {}) {
  const max = opts.max ?? 60                      // Latin chars; for CJK use ~25 characters
  const suffix = opts.brand ? ` - ${BRAND}` : ''
  const room = max - suffix.length
  let t = main.trim().replace(/\s+/g, ' ')
  if (t.length > room) {
    const cut = t.slice(0, room + 1)
    const lastSpace = cut.lastIndexOf(' ')
    t = (lastSpace > room * 0.6 ? cut.slice(0, lastSpace) : t.slice(0, room)).replace(/[\s,.:;-]+$/, '')
  }
  return t + suffix                                // no ellipsis; never cut mid-word when avoidable
}
```
Rules: use ` - ` as separator; no trailing year unless the content is about that year; numbers or
brackets only when the content really has them; templates must vary by more than one swapped city name
(Google calls one-item-varying titles "boilerplate"). For Next.js, avoid a global
`title.template: '%s | Brand'` on article routes — use `title.absolute` there.

Sources: [Influencing title links](https://developers.google.com/search/docs/appearance/title-link) · [Next.js title template/absolute](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) · length and brand-suffix numbers: (third-party study) and (field experience), see `knowledge-base.md` §3

## 5. JSON-LD: entity graph, people, articles, breadcrumbs

**Principles**
- One organisation node with a **stable `@id`** (e.g. `https://www.example.com/#org`) defined once in a shared config and **reused** on every site of the network. Satellites point to it with `parentOrganization`; they do not redefine the business.
- NAP values come from **one constant**; never hand-type them per template.
- Only mark up what is visible and true. No `Review`/`AggregateRating` for testimonials the business selected. `FAQPage` only where the Q&A is visible on the page (Google no longer shows FAQ rich results since 2026-05-07, but the type is still valid schema.org).
- `LegalService` (not the superseded `Attorney`) for law offices; another `LocalBusiness` subtype for other industries.

**Organization / LegalService node**
```json
{
  "@context": "https://schema.org",
  "@type": "LegalService",
  "@id": "https://www.example.com/#org",
  "name": "<firm>",
  "url": "https://www.example.com/",
  "logo": "https://www.example.com/logo-512.png",
  "image": "https://www.example.com/office-entrance.jpg",
  "telephone": "+82-0-0000-0000",
  "address": { "@type": "PostalAddress", "streetAddress": "<street> <building>, <floor>",
               "addressLocality": "<city>", "postalCode": "00000", "addressCountry": "KR" },
  "geo": { "@type": "GeoCoordinates", "latitude": 0.0, "longitude": 0.0 },
  "hasMap": "<Google Maps URL of the verified listing>",
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "09:00", "closes": "18:00" }
  ],
  "sameAs": ["https://www.youtube.com/@<channel>", "https://www.instagram.com/<handle>/",
             "<official directory profile URL>"],
  "parentOrganization": { "@id": "https://www.head-office.example/#org" }
}
```
(`parentOrganization` only when this entity is a branch of a head office.)

**Satellite site describing a department**
```json
{ "@context": "https://schema.org", "@type": "WebSite", "@id": "https://www.example-divorce.com/#website",
  "url": "https://www.example-divorce.com/", "name": "<firm> Divorce Practice",
  "publisher": { "@id": "https://www.example.com/#org" } }
```

**ProfilePage + Person** (one per real professional; not a LocalBusiness per person)
```json
{ "@context": "https://schema.org", "@type": "ProfilePage",
  "mainEntity": { "@type": "Person", "@id": "https://www.example.com/people/jane-doe#person",
    "name": "Jane Doe", "jobTitle": "Attorney", "worksFor": { "@id": "https://www.example.com/#org" },
    "image": "https://www.example.com/img/jane-doe.jpg",
    "sameAs": ["<bar association directory profile URL>"] } }
```

**Article**
```json
{ "@context": "https://schema.org", "@type": "Article",
  "headline": "What happens at the first divorce mediation session",
  "image": ["https://www.example.com/img/article-1200x675.jpg"],
  "datePublished": "2026-10-01T09:00:00+09:00", "dateModified": "2026-10-20T09:00:00+09:00",
  "author": { "@id": "https://www.example.com/people/jane-doe#person" },
  "publisher": { "@id": "https://www.example.com/#org", "@type": "Organization", "name": "<firm>",
                 "logo": { "@type": "ImageObject", "url": "https://www.example.com/logo-512.png" } } }
```

**BreadcrumbList**
```json
{ "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
  { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.example.com/" },
  { "@type": "ListItem", "position": 2, "name": "Articles", "item": "https://www.example.com/articles" },
  { "@type": "ListItem", "position": 3, "name": "First mediation session" } ] }
```

**FAQPage** — only for Q&A rendered visibly on the same page; one emitter per page.

**Safe injection in Next.js** (escape `<` so content can't close the script tag):
```tsx
export function JsonLd({ data }: { data: object }) {
  return <script type="application/ld+json"
    dangerouslySetInnerHTML={{ __html: JSON.stringify(data).replace(/</g, '\\u003c') }} />
}
```
Render it in a Server Component (`layout.tsx`/`page.tsx`) so it is in the initial HTML; don't use `next/script` for JSON-LD.

**WordPress**
```php
// Extend Yoast's graph instead of printing a second, conflicting Organization
add_filter('wpseo_schema_graph', function ($graph) {
  foreach ($graph as &$node) {
    if (($node['@type'] ?? '') === 'Organization') {
      $node['@type'] = ['Organization', 'LegalService'];
      $node['sameAs'] = array_values(array_unique(array_merge($node['sameAs'] ?? [], SITE_SAME_AS)));
    }
  }
  return $graph;
});
// Without a plugin: wp_head + wp_json_encode (escapes slashes; add JSON_HEX_TAG to escape < and >)
add_action('wp_head', function () {
  echo '<script type="application/ld+json">' . wp_json_encode(SITE_ORG_NODE, JSON_HEX_TAG | JSON_UNESCAPED_UNICODE) . '</script>';
});
```
Validate a sample with the Rich Results Test and the Schema Markup Validator; report errors verbatim.

Sources: [General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) · [LocalBusiness](https://developers.google.com/search/docs/appearance/structured-data/local-business) · [Organization](https://developers.google.com/search/docs/appearance/structured-data/organization) · [ProfilePage](https://developers.google.com/search/docs/appearance/structured-data/profile-page) · [Article](https://developers.google.com/search/docs/appearance/structured-data/article) · [BreadcrumbList](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb) · [Review snippets (self-serving)](https://developers.google.com/search/docs/appearance/structured-data/review-snippet) · [FAQ rich result deprecation](https://developers.google.com/search/updates) · [schema.org LegalService](https://schema.org/LegalService) · [schema.org Attorney (superseded)](https://schema.org/Attorney) · [Next.js JSON-LD](https://nextjs.org/docs/app/guides/json-ld) · [Yoast schema API](https://developer.yoast.com/features/schema/api/) · [Rich Results Test](https://search.google.com/test/rich-results) · [Schema Markup Validator](https://validator.schema.org/) · single `@id` across a network: (field experience)

## 6. robots.txt generation

**Next.js `app/robots.ts`**
```ts
import type { MetadataRoute } from 'next'
const PRIVATE = ['/admin/', '/api/', '/mypage/']
export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: '*', allow: '/', disallow: PRIVATE },
      // A named group does NOT inherit '*' rules: repeat PRIVATE in every named group
      { userAgent: ['OAI-SearchBot', 'ChatGPT-User', 'Claude-SearchBot', 'Claude-User', 'PerplexityBot', 'Perplexity-User'],
        allow: '/', disallow: PRIVATE },
    ],
    sitemap: 'https://www.example.com/sitemap.xml',
  }
}
```
A Daum verification comment cannot be emitted by the `robots.ts` object; if you need it, serve a
static `app/robots.txt` (or a route handler returning `text/plain`) instead.

**Static file** (`public/robots.txt`, `static/robots.txt`, or the web root) — same content as
`sitemaps-and-submission.md` §5. Generate per host in multi-site setups; a shared file must not point
one site's `Sitemap:` line at another host.

Sources: [Next.js robots](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots) · [How Google interprets robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt) · [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html) · AI-bot tokens: see `sources.md` §12

## 7. llms.txt

Optional and low priority (no major AI vendor documents reading it as of 2026-11); keep it accurate if present.
```markdown
# <firm>

> <firm> is a law office in <city> handling family, criminal and real-estate matters. Consultations are paid and by appointment.

Key facts: address <street>, <city>; phone +82-0-0000-0000; hours Mon–Fri 09:00–18:00.

## Main pages
- [Fees and process](https://www.example.com/fees): how consultations are booked and charged
- [Attorneys](https://www.example.com/people): profiles and registered specialties
- [Location](https://www.example.com/location): directions and parking

## Optional
- [Articles](https://www.example.com/articles): explanations of common legal questions
```
Facts in llms.txt must match the fact sheet; it is one more place that can drift.

Sources: [llms.txt proposal](https://llmstxt.org/) · priority judgement: (field experience)

## 8. Core Web Vitals fixes

Targets (75th percentile, field data): **LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1**.

**CLS — reserve space**
```css
.hero-media { aspect-ratio: 16 / 9; width: 100%; }
.ad-slot, .consult-banner { min-height: 120px; }       /* late-loading blocks */
.nav-dropdown[aria-expanded="false"] { max-height: 0; overflow: hidden; }
```
```tsx
import Image from 'next/image'
<Image src="/office.jpg" alt="Office entrance" width={1200} height={675} sizes="100vw" />
```
Fonts: self-host (e.g. `next/font`), `font-display: swap` or `optional`, preload only the one or two
critical files, and use a fallback with matched metrics (`size-adjust`) so swapping doesn't shift text.

**LCP — make the hero visible at first paint**
```tsx
<Image src="/hero.jpg" alt="..." width={1600} height={900} priority fetchPriority="high" />
```
```html
<img src="/hero.jpg" width="1600" height="900" fetchpriority="high" alt="..."> <!-- not loading="lazy" -->
```
- No entrance animation that starts the hero at `opacity: 0` or off-screen; animate only secondary elements, or start from a visible state.
- LCP much later than FCP → the hero is hidden, lazy-loaded, or waits for JS/a client fetch: render it in the server HTML.
- Preconnect to the image CDN; serve AVIF/WebP at the displayed size.

**INP basics**
- Break up long tasks (> 50 ms): defer non-critical JS, split bundles, `await` a yield (`scheduler.yield()` where available, else `setTimeout(0)`) inside heavy handlers.
- Load chat widgets, analytics and maps on interaction or after load, not in the critical path.
- Keep DOM size reasonable; avoid layout thrashing in input handlers.

Measure before and after with PageSpeed Insights (field + lab) on the main templates, mobile first.

Sources: [Web Vitals](https://web.dev/articles/vitals) · [Optimize LCP](https://web.dev/articles/optimize-lcp) · [Optimize CLS](https://web.dev/articles/optimize-cls) · [Optimize INP](https://web.dev/articles/optimize-inp) · [Fetch Priority](https://web.dev/articles/fetch-priority) · [Font best practices](https://web.dev/articles/font-best-practices) · [Core Web Vitals in Search](https://developers.google.com/search/docs/appearance/core-web-vitals) · opacity-0 hero finding: (field experience)

## 9. Internal linking

- Every link that must be followed is a real `<a href="/path">` in the server HTML (not a button, not JS-only pagination).
- **Related block** on every detail page: ~6–8 links to the same topic, chosen by shared tags/category, rendered server-side.
```tsx
const related = await db.article.findMany({ where: { topic: a.topic, id: { not: a.id }, status: 'published' },
  orderBy: { publishedAt: 'desc' }, take: 8, select: { slug: true, title: true } })
<nav aria-label="Related"><ul>{related.map(r => <li key={r.slug}><a href={`/articles/${r.slug}`}>{r.title}</a></li>)}</ul></nav>
```
- Pagination: `<a href="?page=2">`, each page self-canonical; `?page=1` redirects to the bare URL; pages beyond the last return 404.
- Link to the **final** URL (no redirects), without UTM or tracking parameters — also between your own sites. Cross-site links use brand anchors in a "family sites" block, not keyword anchors on every page.
- Hubs link down to every item; archives (section × month) keep everything ≤ 3 clicks from home.

Sources: [Link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) · [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) · link-count targets: (third-party study), see `knowledge-base.md` §6

## 10. Thin and duplicate content: which tool when

| Situation | Use | Why |
|---|---|---|
| Two pages answer the same intent; one is stronger | **301** the weaker to the stronger, merge useful content first | Users and signals move to one URL. |
| Page must stay for users but shouldn't rank (thin tag archive, internal search, empty list) | **`noindex, follow`**, keep links | Keeps crawl paths; drops the page. Remove it from the sitemap. |
| Same content must exist on two of your domains (syndicated, a shared policy page) | **Cross-domain `rel=canonical`** to the original | Consolidates to the original; both pages stay reachable. Works for Google; Naver largely ignores canonical for its similar-document filter. |
| Content removed for good, no equivalent | **410** (or 404) | Honest; don't redirect to home (soft 404). |
| Near-duplicate templates (city pages that differ only by name) | Add genuinely local content first, or merge into fewer pages; open in cohorts | Doorway and scaled-content risk. |
Measure before choosing: check indexing and clicks of the pages involved (GSC Pages × Queries) so you
don't delete or merge pages that still earn traffic.

Sources: [Canonicalization methods](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) · [Block indexing with noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing) · [Redirects](https://developers.google.com/search/docs/crawling-indexing/301-redirects) · [Spam policies (doorways, scaled content)](https://developers.google.com/search/docs/essentials/spam-policies) · Naver canonical behaviour: (field experience)

## 11. CMS content persistence

- Find **where runtime content is stored** before trusting "saved": database, object storage, a volume, or files in the repo.
- If an admin panel writes to **git-tracked files** (e.g. `data/*.json`) and the deploy runs `git reset --hard` / `git pull` / a fresh checkout, every deploy silently wipes the edits.
- Fix order: (1) snapshot the live content into the repo **before the next deploy**; (2) move the store out of the deploy path — database, a git-ignored directory on a persistent volume, or object storage — seeded once from the repo defaults; (3) add the store path to `.gitignore` and the deploy script's "do not touch" list; (4) verify by editing in the admin, deploying, and re-checking the public URL.
```yaml
# docker-compose: persist runtime content outside the image and the git checkout
services:
  web:
    volumes:
      - cms-data:/app/runtime-data      # app reads/writes here; seed from /app/defaults on first run
volumes:
  cms-data:
```
- Same for uploads and generated sitemaps cached on disk.

Sources: (field experience) — see `lessons-learned.md` §4

## 12. Live verification: curl checklist

```bash
U=https://www.example.com/some/page
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" "$U"                     # status, redirect target
curl -sI "$U" | grep -iE '^(HTTP|location|x-robots-tag|cache-control|content-type|age|cf-cache-status|x-cache)'
curl -s "$U" | grep -oiE '<link[^>]+rel="?canonical"?[^>]*>'                      # canonical
curl -s "$U" | grep -oiE '<meta[^>]+name="?robots"?[^>]*>'                        # meta robots
curl -s "$U" | grep -oiE '<link[^>]+hreflang[^>]*>' | head                        # hreflang
curl -s "$U" | grep -c 'application/ld+json'                                      # JSON-LD blocks present
curl -s "$U" | python3 -c "import sys,re,json;[print(json.loads(b).get('@type')) for b in re.findall(r'<script[^>]*ld\+json[^>]*>(.*?)</script>',sys.stdin.read(),re.S)]"
curl -s -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" -o /dev/null -w "%{http_code}\n" "$U"   # bot UA not blocked
for v in http://example.com/ http://www.example.com/ https://example.com/; do curl -s -o /dev/null -w "$v %{http_code} -> %{redirect_url}\n" "$v"; done
curl -s https://www.example.com/robots.txt; curl -sI https://www.example.com/sitemap.xml | head -5
```
Run curl from a clean shell, not through a fetch tool's proxy (proxies have reported 302 where the
server sent 308). Then run `scripts/site_check.py` and `scripts/sitemap_validate.py` for the whole site.

Sources: [URL Inspection tool](https://support.google.com/webmasters/answer/9012289) · [Rich Results Test](https://search.google.com/test/rich-results) · proxy caveat: (field experience)
