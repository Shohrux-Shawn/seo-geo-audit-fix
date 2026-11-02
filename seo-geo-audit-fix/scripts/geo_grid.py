#!/usr/bin/env python3
"""
geo_grid.py — plan and summarise a Google Maps geo-grid test (no browsing, no scraping).

Step 1 — plan: generate the exact Maps URLs to open (one per centre x query) and an
empty results CSV to fill in while checking (by you or a browser agent).

  python3 geo_grid.py plan centres.csv "lawyer,law firm,divorce lawyer" --zoom 14 --out grid
  (write the queries in the language people actually search in, e.g. Korean for Korea)
  centres.csv columns: code,area,lat,lng     (e.g.  A,office,37.5665,126.9780)

  Writes grid/urls.md (ordered checklist) and grid/results.csv
  (columns: code,area,query,url,our_position,top1,top2,top3,notes).
  our_position: a number, "20+" if not in the top 20, or "NV" if not verified.

Step 2 — summarise the filled-in CSV into a grid table + top-competitor counts:

  python3 geo_grid.py summary grid/results.csv > grid/summary.md
"""
import argparse
import csv
import os
import sys
import urllib.parse
from collections import Counter, OrderedDict


def plan(args):
    with open(args.centres, encoding="utf-8-sig") as f:
        centres = list(csv.DictReader(f))
    queries = [q.strip() for q in args.queries.split(",") if q.strip()]
    os.makedirs(args.out, exist_ok=True)
    rows, lines = [], ["# Geo-grid checklist", "",
                       "Open each URL as-is (do not drag the map). Count organic results only (skip sponsored/ad results).",
                       "Record our position up to 20 and the top 3 names. Wait 20–30 s between searches.", ""]
    n = 0
    for q in queries:
        for c in centres:
            n += 1
            url = (f"https://www.google.com/maps/search/{urllib.parse.quote(q)}/"
                   f"@{float(c['lat']):.4f},{float(c['lng']):.4f},{args.zoom}z")
            rows.append({"code": c["code"], "area": c["area"], "query": q, "url": url,
                         "our_position": "", "top1": "", "top2": "", "top3": "", "notes": ""})
            lines.append(f"{n}. [{c['code']} {c['area']} · {q}]({url})")
    with open(os.path.join(args.out, "results.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(args.out, "urls.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{n} searches planned → {args.out}/urls.md and {args.out}/results.csv")


def summary(args):
    with open(args.results, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    codes = list(OrderedDict.fromkeys((r["code"], r["area"]) for r in rows))
    queries = list(OrderedDict.fromkeys(r["query"] for r in rows))
    cell = {(r["query"], r["code"]): (r["our_position"] or "NV") for r in rows}
    out = ["# Geo-grid summary", "", "Our position (organic, ads excluded; 20+ = not in top 20; NV = not verified)", ""]
    out.append("| Query | " + " | ".join(f"{c} {a}" for c, a in codes) + " |")
    out.append("|---" * (len(codes) + 1) + "|")
    for q in queries:
        out.append(f"| {q} | " + " | ".join(cell.get((q, c), "NV") for c, _ in codes) + " |")
    def is_rank(v):
        return v.isdigit()
    ranked = [v for v in cell.values() if is_rank(v)]
    out += ["", f"Cells in top 20: {len(ranked)} of {len(cell)}; "
                f"top 3: {sum(1 for v in ranked if int(v) <= 3)}; "
                f"not verified: {sum(1 for v in cell.values() if v == 'NV')}", ""]
    top = Counter()
    for r in rows:
        for k in ("top1", "top2", "top3"):
            if r.get(k):
                top[r[k].strip()] += 1
    out += ["## Listings most often in the top 3", "", "| Listing | Top-3 appearances |", "|---|---|"]
    out += [f"| {name} | {n} |" for name, n in top.most_common(10)]
    print("\n".join(out))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan", help="Write urls.md and an empty results.csv")
    p.add_argument("centres", help="CSV with columns code,area,lat,lng")
    p.add_argument("queries", help="Comma-separated queries")
    p.add_argument("--zoom", type=int, default=14)
    p.add_argument("--out", default="geo-grid")
    s = sub.add_parser("summary", help="Summarise a filled results.csv")
    s.add_argument("results", help="Filled results.csv from the plan step")
    args = ap.parse_args()
    plan(args) if args.cmd == "plan" else summary(args)


if __name__ == "__main__":
    main()
