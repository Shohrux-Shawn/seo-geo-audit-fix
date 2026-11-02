# scripts/

Helpers the skill calls instead of re-writing the same code on every audit. Every script runs with
`--help`. They are read-only or dry-run by default: they send GET requests or work on local files,
never log in, and anything that sends data to an engine needs an explicit `--apply`. Secrets come
from environment variables only and are never printed in full.

| Script | Module | What it does | Sends data? |
|---|---|---|---|
| `site_check.py` | A, B, C (partial), E | Redirect chains for http/https × apex/www, robots.txt (AI-bot groups, Daum line), llms.txt, sitemap crawl, per-page title/description/H1/canonical/lang/hreflang/JSON-LD types/phones/forbidden words/`<main>` length/UTM links, and duplicate titles and descriptions. Writes JSON + Markdown. Stdlib only. | No |
| `sitemap_validate.py` | A | Follows sitemap indexes; checks the 50,000-URL / 50 MB limits (and Naver's 10 MB), namespace, duplicates, host/scheme mismatch, `lastmod` format, future dates and fake (identical/"today") lastmod; fetches a sample or all URLs for status, redirects, `X-Robots-Tag`/meta noindex, canonical ≠ URL and soft-404 hints; validates `xhtml:link` hreflang (codes, self-reference, reciprocity, alternates missing from the sitemap). Writes JSON + Markdown; exit 1 on errors. Stdlib only. | No |
| `indexnow_submit.py` | A (fix) | Verifies the IndexNow key file (`https://<host>/<key>.txt` or `--key-location`), filters URLs to the host (and key scope), batches up to 10,000, prints the payload summary. POSTs to `https://api.indexnow.org/indexnow` only with `--apply`. Key from `INDEXNOW_KEY` (or `--key-env`). Stdlib only. | Only with `--apply` |
| `gsc_sitemaps.py` | A (fix) | `list` (read-only) or `submit` (needs `--apply`) sitemaps in Google Search Console through a service account (`GOOGLE_APPLICATION_CREDENTIALS`). Needs `pip install --upgrade google-api-python-client google-auth`; prints that command if missing. The service-account e-mail must be added in Search Console → Settings → Users and permissions (Full or Owner to submit). | Only `submit --apply` |
| `nap_compare.py` | G | Master NAP table from a sources CSV against canonical values (JSON), with normalisation so spacing and URL-scheme differences don't count as mismatches. | No |
| `geo_grid.py` | F | `plan`: exact Google Maps URLs per centre × query plus an empty results CSV. `summary`: grid table and the listings most often in the top 3. | No |

Typical order for a sitemap fix: `sitemap_validate.py` (baseline) → code fix
(`../references/implementation-playbook.md`) → deploy → `sitemap_validate.py` again (0 errors) →
owner approves → `gsc_sitemaps.py submit --apply` and `indexnow_submit.py --apply` for changed URLs.

## Adding a script

1. One job per script, runnable as `python3 scripts/<name>.py --help`.
2. Prefer the standard library. If you need a package, say so in the docstring and fail with a clear message (including the exact `pip install` command) when it is missing.
3. Inputs are arguments or files; outputs are JSON (data) + Markdown (summary) in an `--out` folder.
4. Read-only by default. A script that changes anything (code, CMS, listings, console settings) or sends data to an engine must need an explicit `--apply` flag and print a dry-run summary without it.
5. Secrets (API keys, tokens, service-account files) come from environment variables only. Never print them and never write them to output.
6. Add a row to the table above, and one line in SKILL.md → "Bundled scripts and templates", so the skill knows when to call it.

Ideas not built yet:
- `gsc_pages_queries.py`: Search Console Search Analytics export (Pages × Queries) for the cannibalisation map.
- `psi_batch.py`: PageSpeed Insights API for each home template.
- `schema_check.py`: deeper JSON-LD checks (one `@id`, `sameAs`, address match).
- `bing_wmt.py`: Bing Webmaster stats and `SubmitUrlBatch` (with `--apply`).
