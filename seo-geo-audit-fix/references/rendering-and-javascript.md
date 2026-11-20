# Rendering and JavaScript — what crawlers and AI engines actually receive

Read for module A2 on every site, and before any fix on a site built with a JavaScript framework.
The question is always the same: **is the content, the links and the meta in the HTML the server sends,
or only in the page after JavaScript runs?**

## Contents
1. Who renders JavaScript
2. Rendering modes and their SEO cost
3. How to test (no tools beyond curl and a browser)
4. Common failures in client-rendered sites
5. Fixes, in order of preference
6. Verification after a fix

---

## 1. Who renders JavaScript

- **Googlebot** renders JavaScript, but in a second pass that can lag the first crawl; rendering fails
  silently when scripts error, time out, or are blocked by robots.txt.
- **Bing** renders, with more limits; other engines vary. Naver's crawler (Yeti) is best served plain
  HTML.
- **AI crawlers** (GPTBot/ChatGPT, ClaudeBot, PerplexityBot and others) do **not** execute JavaScript
  according to an industry log study (Vercel + MERJ, 2024): they read only the HTML the server sends.
  Content that appears only after JavaScript runs is invisible to them, so it cannot be quoted in AI
  answers. Applebot is an exception (renders like Googlebot).
- Social preview crawlers (link cards in chat apps and social networks) read only server HTML
  `og:`/`twitter:` tags.

Consequence: a site that "looks fine in the browser and in Google" can be empty for AI engines and link
previews.

---

## 2. Rendering modes and their SEO cost

| Mode | What the server sends | SEO / GEO risk |
|---|---|---|
| Static (SSG, pre-rendered) | full HTML at build time | lowest; data can go stale until the next build |
| Server-rendered (SSR) | full HTML per request | low; watch server time (TTFB) and caching |
| Incremental / ISR / cached SSR | full HTML, refreshed periodically | low; check that error pages are never cached |
| Hybrid (SSR shell + client islands) | HTML for most content; some blocks client-side | check which blocks are client-only |
| Client-side SPA (CSR) | an empty `<div id="root">` + scripts | high: content, links and meta depend on JS |
| Dynamic rendering (bots get pre-rendered HTML, users get the SPA) | depends on user agent | Google calls it a workaround, not a recommended solution; drift between versions risks cloaking |

---

## 3. How to test

Run on each page template (home, listing, detail, article), not only the home page.

1. **Raw HTML (what AI crawlers get):**
   ```bash
   curl -sL -A "Mozilla/5.0 (compatible; GPTBot/1.0)" https://example.com/page | sed 's/<[^>]*>/ /g' | tr -s ' \n' | head -c 2000
   curl -sL https://example.com/page | grep -oE '<title>[^<]*|<link rel="canonical"[^>]*|<meta name="(description|robots)"[^>]*|<h1[^>]*>[^<]*'
   curl -sL https://example.com/page | grep -o '<a [^>]*href="/[^"]*"' | wc -l      # internal links in server HTML
   ```
   Is the main text there? Title, description, canonical, robots, H1, JSON-LD? Real `<a href>` links?
2. **Rendered HTML (what Google sees after rendering):** Search Console URL Inspection → "Test live URL"
   → "View tested page" (HTML + screenshot + JavaScript console errors). Rich Results Test shows the same
   rendered HTML without Search Console access.
3. **JavaScript off:** in the browser, disable JavaScript and reload. What remains is roughly what
   non-rendering crawlers see.
4. **Compare:** text length, link count, title/canonical/robots and JSON-LD between raw and rendered.
   Anything present only after rendering is a finding (severity depends on what it is: main content or
   meta = High; a widget = Low).
5. **Status codes:** request a URL that should not exist (`/this-does-not-exist-123`). It must return
   404/410 from the server. A 200 with "page not found" drawn by JavaScript is a soft 404.

---

## 4. Common failures in client-rendered sites

- Title, description, canonical or `noindex` set by JavaScript only (or changed by it). Google may use
  the raw value, the rendered value, or both; AI and social crawlers use only the raw one. A
  `noindex` in raw HTML that JavaScript later removes still blocks indexing.
- Navigation built with `onClick` handlers or `<button>`s instead of `<a href>`; crawlers follow only
  real links.
- Hash routes (`/#/products/1`): the fragment is not sent to the server and is generally not crawled
  as a separate URL.
- Every route returns 200 (soft 404s); redirects done in JavaScript instead of HTTP 301.
- Content loaded on scroll, click or tab change only ("load more", infinite scroll, accordions fetched
  on open); content behind a consent wall or geolocation prompt.
- Data fetched from an API the crawler cannot reach (blocked by robots.txt, needs a cookie, CORS, rate
  limit) → rendered page is empty or shows an error.
- JSON-LD injected by a tag manager: visible to Google only after rendering, invisible to AI crawlers.
- Huge JavaScript bundles: slow rendering, poor INP/LCP, render timeouts.
- `robots.txt` disallowing `/static/`, `/_next/`, `/assets/` or the API: Google cannot render.

---

## 5. Fixes, in order of preference

1. **Static generation or server rendering for every indexable page** using the framework's own
   mechanism (`stacks.md`): Next.js, Nuxt, SvelteKit, Astro, Remix/React Router, Angular SSR, Vike for
   plain Vite apps. Keep client-side code for interactive parts only.
2. **Pre-render at build time** for a plain SPA with a fixed set of public pages (marketing site,
   docs): generate HTML per route in the build, serve it, hydrate on load.
3. **Split the marketing site from the app**: a static site for public pages, the SPA only behind login
   (`site-profiles.md` §5).
4. **Server-side meta at minimum**: if full SSR is not possible now, have the server (or the edge)
   inject the correct title, description, canonical, robots, `og:` tags, JSON-LD and the main text per
   route.
5. **Dynamic rendering** only as a temporary bridge with a dated removal plan; the bot version must
   match the user version.

Always alongside: real `<a href>` links, real HTTP status codes and redirects, history-API URLs instead
of hashes, paginated URLs behind any infinite scroll, scripts and API endpoints needed for rendering not
blocked in robots.txt.

---

## 6. Verification after a fix

- The raw-HTML checks in §3 show the main text, meta, JSON-LD and links for each template.
- URL Inspection live test: no JavaScript console errors that remove content; screenshot complete.
- Unknown URL returns 404; removed pages return 404/410 or a single 301.
- Link preview of one page in a chat app shows the right title and image (some apps cache previews;
  use their debugger to refresh).
- Ask an AI engine with browsing about a fact that appears only on that page; it should now find it.

Sources: [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) · [Fix JavaScript issues in Search](https://developers.google.com/search/docs/crawling-indexing/javascript/fix-search-javascript) · [Dynamic rendering as a workaround](https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering) · [Crawlable links](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) · [The rise of the AI crawler (Vercel + MERJ, 2024, industry study)](https://vercel.com/blog/the-rise-of-the-ai-crawler)
