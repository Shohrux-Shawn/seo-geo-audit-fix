# Stack recipes — where each SEO control lives, per framework and platform

Read in Step 4 before changing code on a stack other than the one in `implementation-playbook.md`
(which uses Next.js Pages Router and nginx for its examples). The rules are the same everywhere; only
the place differs. Always confirm against the framework's current docs and the project's installed
version: APIs change between major versions.

## Contents
1. What to locate in any stack
2. JavaScript frameworks
3. CMS and hosted platforms
4. Hosting, CDN and server layer
5. Plain single-page apps

---

## 1. What to locate in any stack

For each, find the file or setting before proposing a fix:

| Control | Question to answer |
|---|---|
| Rendering mode | Which routes are static, server-rendered, client-only? |
| Head tags | Where are title, description, canonical, robots, hreflang, `og:` set, per route? |
| JSON-LD | Rendered in server HTML, or injected client-side / by a tag manager? |
| Status codes | How does a missing record return 404/410? How are redirects (301/308) declared? |
| Sitemap | Generated how, from which data, refreshed when? |
| robots.txt / llms.txt | Static file or generated route? Per environment? |
| Headers | Where do `X-Robots-Tag`, cache and security headers come from (app, server, CDN)? |
| Images | Optimiser, sizes, lazy-loading, LCP image priority |
| Environments | How are staging/preview hosts kept out of the index? |

---

## 2. JavaScript frameworks

**Next.js (App Router)**
- Head: `export const metadata` or `generateMetadata()` per route (`alternates.canonical`,
  `alternates.languages`, `robots`, `openGraph`). JSON-LD: a `<script type="application/ld+json">` in
  the server component.
- Sitemap/robots: `app/sitemap.ts` (or `generateSitemaps` for splitting), `app/robots.ts`.
- Status: `notFound()` → 404, `permanentRedirect()` → 308; config redirects in `next.config` `redirects()`.
- Rendering: server components by default; `'use client'` blocks are still server-rendered on first load
  unless they fetch their data in the browser.

**Next.js (Pages Router)**
- Head: `next/head`; give tags a `key` so page-level tags replace defaults instead of duplicating.
- Data: `getStaticProps` (+ `revalidate`) or `getServerSideProps`; `notFound: true` → 404, `redirect`
  → 301/308. Sitemap: a `pages/sitemap.xml.tsx` route writing XML in `getServerSideProps`.
- Recipes in `implementation-playbook.md`.

**Nuxt 3/4**
- Head: `useSeoMeta()` / `useHead()`; site-wide in `app.vue` or `nuxt.config` `app.head`.
- Rendering and redirects per route: `routeRules` (`prerender`, `isr`, `ssr: false`, `redirect`).
- Status: `throw createError({ statusCode: 404 })`. Sitemap/robots: the community `@nuxtjs/sitemap` and
  `@nuxtjs/robots` modules (or a server route).

**SvelteKit**
- Head: `<svelte:head>` in the page/layout. Page options: `export const prerender = true`, `ssr`, `csr`.
- Status: `error(404, ...)` and `redirect(301, ...)` from `@sveltejs/kit` in `load`.
- Sitemap/robots: a `+server.ts` route returning XML/text.

**Astro**
- Static by default; `output: 'server'` or per-page `export const prerender = false` for SSR.
- Head: in the layout component. Sitemap: `@astrojs/sitemap` (needs `site` in the config).
- Redirects: `redirects` in `astro.config`, or the host's redirect file for static output.
- Islands (`client:*`) hydrate only interactive parts; text outside islands is plain HTML.

**Remix / React Router v7 (framework mode)**
- Head: the route `meta` export (and `links` for canonical/hreflang).
- Status: throw a `Response` with 404 from the `loader`; `redirect()` from the loader or action.
- Pre-render static routes with the `prerender` config; sitemap/robots as resource routes.

**Angular**
- SSR/prerender with `@angular/ssr`; head via the `Title` and `Meta` services; canonical via
  `DOCUMENT`/`Renderer2` on the server. Without SSR an Angular app is a client-only SPA (§5).

**Gatsby**
- Static output; head via the Head API; sitemap via `gatsby-plugin-sitemap`; redirects via
  `createRedirect` plus the host's adapter.

**Vue/React/Svelte with plain Vite** → §5 (client-only unless SSR/prerender is added, e.g. with Vike).

---

## 3. CMS and hosted platforms

**WordPress**
- Titles, descriptions, canonical, robots, sitemaps and most schema usually come from one SEO plugin
  (e.g. Yoast SEO, Rank Math). Use exactly one; two plugins duplicate tags.
- Thin archives (tag, author, date, attachment pages) are the classic index bloat; `noindex` them in the
  plugin unless they are real hubs.
- Redirects: a redirect plugin or the server; avoid redirect chains after permalink changes.
- Headless WordPress: the front end (often Next.js/Nuxt/Astro) owns the head tags and sitemap; make sure
  the plugin's SEO fields are actually read by the front end.

**Shopify**
- Sitemaps and canonical tags are generated; robots.txt is editable through the `robots.txt.liquid`
  theme template.
- Products are reachable under collection paths; the theme should link to the plain `/products/<handle>`
  URL (the canonical points there).
- Head tags and JSON-LD live in the theme (`theme.liquid`, product/collection templates); check apps
  that inject duplicate schema.
- Redirects: Online Store → Navigation → URL redirects (also used after handle changes).

**Webflow, Wix, Squarespace and similar builders**
- Per-page title/description/canonical/noindex in the page settings; sitemap generated; custom code
  areas for JSON-LD. Limits: some do not allow full control of robots.txt, headers or status codes —
  record those as "platform limit" findings with the workaround, not as code fixes.

**Headless CMS (Contentful, Sanity, Strapi, etc.)**
- The CMS only stores fields; the front-end framework (§2) renders them. Add SEO fields (title,
  description, canonical override, noindex, og image) to the content model, and regenerate or revalidate
  pages when content changes (webhook → rebuild/revalidate).

---

## 4. Hosting, CDN and server layer

- **nginx / Apache:** host redirects (apex/www, http→https), `X-Robots-Tag` headers, compression,
  HTTP/2 (`multisite-and-technical.md` §9). nginx recipes: `implementation-playbook.md` §2.
- **Vercel:** `vercel.json` `redirects`/`headers`, or the framework's own config; preview deployments
  are on separate hosts — keep them out of the index (Vercel adds `X-Robots-Tag: noindex` to preview
  URLs by default; verify on the project).
- **Netlify:** `_redirects` / `netlify.toml` redirects and `_headers`; deploy previews on separate hosts.
- **Cloudflare (Pages, Workers, proxy):** `_redirects` and `_headers` for Pages; Bulk/Single Redirects
  and Transform Rules on the zone; check that bot protection does not challenge Googlebot, Bingbot or
  AI crawlers you want (and does block the ones you do not).
- Any CDN: the canonical host redirect should happen at the edge in one hop; error pages must never be
  cached as 200.

---

## 5. Plain single-page apps

A Vite/CRA-style React, Vue, Svelte or Angular app without SSR sends an empty HTML shell for every
route. Options, from best to minimum (details in `rendering-and-javascript.md` §5):
1. Move public pages to an SSR/SSG framework of the same UI library (Next.js/Remix for React,
   Nuxt for Vue, SvelteKit for Svelte, Angular SSR, or Vike on top of Vite).
2. Pre-render the public routes at build time and serve the generated HTML per route.
3. Separate static marketing site; the SPA stays behind login.
4. Minimum: server or edge injection of per-route head tags, JSON-LD and main text; a server rule that
   returns 404 for unknown routes instead of `index.html` with 200.

Sources: [Next.js generateMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) · [Nuxt SEO and meta](https://nuxt.com/docs/getting-started/seo-meta) · [SvelteKit page options](https://svelte.dev/docs/kit/page-options) · [Astro sitemap integration](https://docs.astro.build/en/guides/integrations-guide/sitemap/) · [React Router pre-rendering](https://reactrouter.com/how-to/pre-rendering) · [Angular SSR](https://angular.dev/guide/ssr) · [Vike](https://vike.dev/) · [Shopify robots.txt.liquid](https://shopify.dev/docs/storefronts/themes/seo/robots-txt) · [Netlify redirects](https://docs.netlify.com/routing/redirects/) · [Cloudflare Pages redirects](https://developers.cloudflare.com/pages/configuration/redirects/) · [Vercel project configuration](https://vercel.com/docs/project-configuration)
