# Browser-agent prompt templates

These are ready-to-fill prompts for a browser agent, such as Claude in Chrome. Use them when the live work must run in a real, signed-in browser: Google Maps, the Business Profile manager, AI answer engines, or local search engines that block automated fetchers.

Each prompt can be pasted on its own. Fill every `<placeholder>` from the project's `seo-geo-facts.md` before sending.

Which prompts apply depends on the site profile (`references/site-profiles.md`):
- **Every site:** 01 (site audit), 02 (entity, rankings and AI answers), 07 (AI source map and off-site entity), 08 (re-measure), 09 (Search Console query → page data, for networks or any cannibalisation question).
- **Local businesses only:** 03–06 (Business Profile checks and edits) and the local parts of 01, 02 and 08 (address, hours, map pack, geo-grid, local engines).
- **No physical location** (online store, SaaS, media, marketplace, docs): delete the NAP, hours, map and local-engine lines from 01/02/08 before sending, and replace the city + service queries with category, product/feature and comparison queries ("best <category>", "<brand> vs <competitor>", "<brand> pricing"). Add to 01 a raw-HTML vs rendered check per template (`references/rendering-and-javascript.md` §3).

## Order of use for a business with a local profile

| Step | Template | Mode | When |
|---|---|---|---|
| 1 | `01-site-network-audit.md` | read-only | Start of a project: all sites, technical + on-page + local + GEO |
| 2 | `02-entity-nap-and-geo-live-test.md` | read-only | Compare every source that mentions the brand; real rankings; AI answers |
| 3 | `03-gbp-readonly-status-check.md` | read-only | Before ANY profile edit: account access, every field, notices, reviews, insights |
| 4 | `04-maps-location-and-geogrid-test.md` | read-only | Pin, address, duplicates on the same pin, geo-grid ranking, map pack, competitors |
| 5 | `05-gbp-update-stage1.md` | **edits** (after approval) | Category, hours, description, services, review replies |
| — | wait 3–5 days | — | Let stage 1 settle; re-run step 3 to confirm it is live |
| 6 | `06-gbp-update-stage2.md` | **edits** (after approval) | Attributes, retried replies, then the address change alone, last |
| 7 | `04-maps-location-and-geogrid-test.md` again | read-only | 2–4 weeks later, signed out AND signed in, compared with the baseline |

After a round of fixes (or monthly), run `08-post-fix-remeasure.md` (read-only, one session): structured data and speed per template, head-term positions, the local engine's sections, and AI answers.

Before changing anything about two of your own sites competing for the same queries (cross-domain cannibalisation), run `09-gsc-query-page-cannibalisation.md` (read-only): a Search Console query → page table per property and the list of queries where two of your hosts both get impressions.

For any company (with or without a local profile), also run `07-ai-source-map-and-offsite-entity.md` (read-only): which third-party sources AI engines cite for the brand, and the state of Wikidata, Wikipedia, Namuwiki, the knowledge panel and profiles. Repeat it monthly while off-site work is running.

Why this order:
- **Read-only checks come first.** The real state of the profile is often different from what the owner remembers: wrong category, missing hours, an owner-written review, duplicate listings on the same pin.
- **Edits are split into two stages.** Address changes can trigger re-verification, and bundling them with other edits makes it impossible to tell which change caused a problem.

## Rules shared by all templates
- The browser agent never types passwords, solves CAPTCHAs, claims listings, accepts terms or paid offers, writes or deletes reviews, or touches another business's listing.
- Read-only templates may open edit dialogs only to read values, then close them with Cancel.
- Edit templates change only the fields they list, save one section at a time, screenshot before and after, and quote the platform's messages exactly.
- If the platform asks for re-verification or any confirmation the template does not cover, the agent stops and asks.
- Every claim needs evidence. Anything not checked is "NOT VERIFIED".
- Interface labels depend on the account language. Templates use English labels; the agent should match them by meaning, e.g. "Edit profile", "Business Profile settings", "People and access", "Read reviews".
