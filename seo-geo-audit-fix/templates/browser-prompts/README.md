# Browser-agent prompt templates

These are ready-to-fill prompts for a browser agent, such as Claude in Chrome. Use them when the live work must run in a real, signed-in browser: Google Maps, the Business Profile manager, AI answer engines, or local search engines that block automated fetchers.

Each prompt can be pasted on its own. Fill every `<placeholder>` from the project's `seo-geo-facts.md` before sending.

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
