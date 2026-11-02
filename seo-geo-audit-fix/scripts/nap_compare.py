#!/usr/bin/env python3
"""
nap_compare.py — build the NAP/entity master table and list mismatches against canonical values.

Input 1: a CSV of what each source shows (one row per source; quote any value that contains a comma). Columns (any subset):
  source,name,address,building,phone,hours,website,category,description
Input 2: a JSON file with the canonical value per field, e.g.
  {"name": "<Firm> <Office>", "building": "<Building>",
   "phone": ["1500-0000", "02-000-0000"], "hours": "Mon-Fri 09:00-18:00",
   "website": "https://www.example.com/"}
  A list means "any of these values is acceptable".

Normalisation before comparing (so cosmetic differences don't count as mismatches):
  - name/building/address/category: spaces and middle dots removed, case-folded
  - phone: digits only
  - website: scheme, "www." and trailing slash removed
  - hours: spaces removed, "~" and "–" treated as "-"
Empty cells are reported as "missing", not as mismatches.

Usage:
  python3 nap_compare.py sources.csv canonical.json > nap_report.md
"""
import csv
import json
import re
import sys

FIELDS = ["name", "address", "building", "phone", "hours", "website", "category", "description"]


def norm(field, value):
    v = (value or "").strip()
    if not v:
        return ""
    if field == "phone":
        return re.sub(r"\D", "", v)
    if field == "website":
        v = re.sub(r"^https?://", "", v.lower())
        v = re.sub(r"^www\.", "", v)
        return v.rstrip("/")
    if field == "hours":
        v = v.replace("~", "-").replace("–", "-").replace("—", "-")
        return re.sub(r"\s+", "", v)
    return re.sub(r"[\s\u00b7\u30fb]", "", v).casefold()


def matches(field, value, canonical):
    if canonical is None:
        return None
    options = canonical if isinstance(canonical, list) else [canonical]
    nv = norm(field, value)
    if field in ("address", "description"):
        # contains-check: the canonical fragment must appear in the source value
        return any(norm(field, o) in nv for o in options)
    if field == "phone":
        # a source may show several numbers separated by / or ,
        found = [norm("phone", p) for p in re.split(r"[/,]", value or "") if p.strip()]
        allowed = {norm("phone", o) for o in options}
        return all(f in allowed for f in found)
    return nv in {norm(field, o) for o in options}


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    with open(sys.argv[2], encoding="utf-8") as f:
        canon = json.load(f)

    cols = [c for c in FIELDS if any(c in r for r in rows)]
    out = ["# NAP / entity comparison", "", "## Master table", ""]
    out.append("| Source | " + " | ".join(cols) + " |")
    out.append("|---" * (len(cols) + 1) + "|")
    mismatches, missing = [], []
    for r in rows:
        cells = []
        for c in cols:
            val = (r.get(c) or "").strip()
            ok = matches(c, val, canon.get(c)) if val else None
            mark = "" if canon.get(c) is None else ("" if not val else (" ✅" if ok else " ❌"))
            cells.append((val.replace("|", "\\|") or "—") + mark)
            if canon.get(c) is not None:
                if not val:
                    missing.append((r.get("source", "?"), c))
                elif not ok:
                    mismatches.append((c, r.get("source", "?"), val, canon[c]))
        out.append(f"| {r.get('source', '?')} | " + " | ".join(cells) + " |")

    out += ["", "## Mismatches (grouped by field)", ""]
    if not mismatches:
        out.append("None.")
    for c in cols:
        group = [m for m in mismatches if m[0] == c]
        if not group:
            continue
        canon_v = canon[c] if not isinstance(canon[c], list) else " / ".join(canon[c])
        out.append(f"### {c} — canonical: {canon_v}")
        for _, src, val, _ in group:
            out.append(f"- {src}: {val}")
        out.append("")
    out += ["## Missing values", ""]
    out += [f"- {src}: {c}" for src, c in missing] or ["None."]
    print("\n".join(out))


if __name__ == "__main__":
    main()
