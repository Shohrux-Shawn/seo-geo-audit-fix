# SEO/GEO facts — <project>

Last checked: <YYYY-MM-DD>

Fill the core blocks for every project. Fill a profile block only if that profile applies
(`references/site-profiles.md`); delete the others.

## Sites (verified live; canonical host)
| Site | Role | Profile(s) | Rendering | Stack (framework/CMS · host/CDN) |
|---|---|---|---|---|
| https://www.example.com | main | e.g. SaaS + content | e.g. SSR / SPA / static | e.g. Next.js · Vercel |

## Entity (all profiles)
- Legal name / brand name (exact spacing):
- Parent organization (if a branch, subsidiary or product of another company):
- Official profiles (social, app stores, review platforms, directories):
- Entity IDs: Wikidata QID · Wikipedia pages (per language) · Knowledge Graph ID · LinkedIn · Crunchbase:
- Founded / founders / leaders (as stated on independent sources):
- Canonical description (1–2 neutral sentences, reused on every profile):

## Markets and engines
- Search: Google <cc>, Bing (+ Naver, Daum for Korea; Yandex, Baidu, Seznam etc. where relevant)
- AI: Google AI Overviews / AI Mode, ChatGPT, Perplexity, Gemini, Copilot (+ local AI answers, e.g. Naver AI Briefing)
- Languages / hreflang set:

## Access
- Repo path(s):
- CMS / platform admin:
- Search consoles (GSC, Bing WMT, local webmaster tools):
- Profile manager accounts / browser profile:

## Owner decisions (do not contradict)
-

## Regulatory limits
-

## Deploy rules
- Who approves:
- Time window:
- Order (one site at a time?):

---

## Profile: local business
- Address (road address, building, floor, postcode):
- Geo (lat, lng) in the site's JSON-LD:
- Phones (main / direct) and where each is used:
- Hours (exact, incl. breaks):
- Service area (if no storefront):
- Categories: Google / Kakao / Naver:
- Local profiles: GBP URL (cid) · Naver Place ID · Kakao place ID · Bing Places:

Canonical NAP values (for nap_compare.py → canonical.json):
```json
{"name": "", "building": "", "phone": [""], "hours": "", "website": ""}
```

## Profile: e-commerce
- Platform / catalogue size (products, categories):
- Product feed(s): Merchant Center / local shopping engines:
- Facets and URL parameters (which ones have search demand and must be indexable):
- Variant handling (one URL vs URL per variant):
- Out-of-stock and discontinued policy:

## Profile: SaaS / web app
- Public hosts/paths (marketing, docs, blog):
- Private hosts/paths (app, sign-in, settings, shared links):
- Preview / staging hosts and how they are kept out of the index:
- Review platforms and comparison sites that matter:

## Profile: content / media
- Authors (names, author pages):
- Publishing volume and cadence:
- Paywall / membership:

## Profile: marketplace / UGC
- Page types created by users:
- Minimum quality rule for indexing:
- Moderation and link policy:

## Profile: docs
- Docs host, generator, versions:
- Which versions stay indexable:
