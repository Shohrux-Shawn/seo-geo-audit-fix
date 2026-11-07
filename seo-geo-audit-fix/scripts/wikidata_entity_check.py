#!/usr/bin/env python3
"""
wikidata_entity_check.py — read a company's Wikidata item and compare it with the website's JSON-LD.

Read-only: it only sends GET requests to the public Wikidata API and to the site you name.
Stdlib only. See ../references/entity-authority-and-off-site.md §5.

What it reports:
  - labels / descriptions / aliases present per language (--langs, default "en,ko")
  - core company statements present or missing (P31, P17, P159, P571, P112, P452, P1454, P856, P1448 ...)
  - statements that have no reference (Wikidata reviewers delete or challenge these)
  - profile identifiers present (LinkedIn, Crunchbase, YouTube, Instagram, X, LEI, Namuwiki)
  - Wikipedia / Namuwiki sitelinks
  - with --site: the Organization-type JSON-LD nodes on that page, whether their sameAs contains
    the Wikidata URL, and whether the item's official website (P856) matches the site's host

Usage:
  python3 wikidata_entity_check.py --search "Example Law Firm" --lang ko        # list candidate QIDs
  python3 wikidata_entity_check.py --qid Q12345 --site https://www.example.com --langs en,ko --out ./entity-out
  python3 wikidata_entity_check.py --qid Q12345 > entity.md                      # Markdown to stdout

Exit code: 0 always for --search; for --qid, 1 if core statements are missing or the site does not
link the item, else 0.
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser

API = "https://www.wikidata.org/w/api.php"
UA = "seo-geo-audit-fix/1.0 (+https://github.com/Shohrux-Shawn/seo-geo-audit-fix) wikidata_entity_check"

CORE = [
    ("P31", "instance of"),
    ("P1448", "official name"),
    ("P17", "country"),
    ("P159", "headquarters location"),
    ("P571", "inception"),
    ("P112", "founder"),
    ("P452", "industry"),
    ("P1454", "legal form"),
    ("P856", "official website"),
]
IDENTIFIERS = [
    ("P4264", "LinkedIn company ID", "https://www.linkedin.com/company/{}"),
    ("P2088", "Crunchbase organization ID", "https://www.crunchbase.com/organization/{}"),
    ("P2397", "YouTube channel ID", "https://www.youtube.com/channel/{}"),
    ("P2003", "Instagram username", "https://www.instagram.com/{}/"),
    ("P2002", "X username", "https://x.com/{}"),
    ("P1278", "Legal Entity Identifier", "https://search.gleif.org/#/record/{}"),
    ("P8885", "Namuwiki ID", "https://namu.wiki/w/{}"),
]
MAX_VALUES = 8  # values shown per property in the Markdown report (JSON keeps all)
STRUCTURE = [("P749", "parent organization"), ("P355", "child organization")]
ORG_TYPES = {"organization", "corporation", "localbusiness", "legalservice", "professionalservice",
             "ngo", "educationalorganization", "medicalorganization", "store", "onlinebusiness"}


def get_json(url, params=None, timeout=30):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def get_text(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        charset = r.headers.get_content_charset() or "utf-8"
        return r.geturl(), r.read().decode(charset, errors="replace")


def search(name, lang, limit=10):
    data = get_json(API, {"action": "wbsearchentities", "search": name, "language": lang,
                          "uselang": lang, "type": "item", "limit": limit, "format": "json"})
    return [(x["id"], x.get("label", ""), x.get("description", "")) for x in data.get("search", [])]


def fetch_item(qid):
    data = get_json(API, {"action": "wbgetentities", "ids": qid, "format": "json",
                          "props": "labels|descriptions|aliases|claims|sitelinks"})
    ent = data.get("entities", {}).get(qid)
    if not ent or "missing" in ent:
        sys.exit(f"Item {qid} not found on Wikidata.")
    if ent.get("redirects"):
        print(f"Note: {qid} redirects to {ent['redirects']['to']}", file=sys.stderr)
    return ent


def labels_for(ids, lang="en"):
    ids = [i for i in ids if re.fullmatch(r"[QP]\d+", i)]
    out = {}
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        data = get_json(API, {"action": "wbgetentities", "ids": "|".join(chunk), "props": "labels",
                              "languages": f"{lang}|en", "format": "json"})
        for k, v in data.get("entities", {}).items():
            lab = v.get("labels", {})
            out[k] = (lab.get(lang) or lab.get("en") or {}).get("value", k)
    return out


def claim_values(claims, pid):
    vals = []
    for c in claims.get(pid, []):
        snak = c.get("mainsnak", {})
        dv = snak.get("datavalue", {}).get("value")
        if isinstance(dv, dict) and "id" in dv:
            v = dv["id"]
        elif isinstance(dv, dict) and "time" in dv:
            v = dv["time"].lstrip("+")[:10]
        elif isinstance(dv, dict) and "text" in dv:
            v = f'{dv["text"]} ({dv.get("language", "?")})'
        elif dv is None:
            v = snak.get("snaktype", "novalue")
        else:
            v = str(dv)
        vals.append({"value": v, "rank": c.get("rank"), "refs": len(c.get("references", []))})
    return vals


class JsonLdParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks, self._in = [], False

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("type", "").lower() == "application/ld+json":
            self._in, self._buf = True, []

    def handle_endtag(self, tag):
        if tag == "script" and self._in:
            self._in = False
            self.blocks.append("".join(self._buf))

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)


def walk_nodes(obj):
    if isinstance(obj, list):
        for x in obj:
            yield from walk_nodes(x)
    elif isinstance(obj, dict):
        yield obj
        for v in obj.values():
            if isinstance(v, (dict, list)):
                yield from walk_nodes(v)


def site_org_nodes(url):
    final_url, html = get_text(url)
    p = JsonLdParser()
    p.feed(html)
    nodes, errors = [], 0
    for b in p.blocks:
        try:
            data = json.loads(b)
        except ValueError:
            errors += 1
            continue
        for n in walk_nodes(data):
            types = n.get("@type", [])
            types = [types] if isinstance(types, str) else types
            if any(str(t).lower() in ORG_TYPES for t in types):
                same = n.get("sameAs", [])
                same = [same] if isinstance(same, str) else same
                nodes.append({"type": types, "id": n.get("@id"), "name": n.get("name"),
                              "sameAs": same, "parentOrganization": n.get("parentOrganization")})
    return final_url, nodes, errors


def host(u):
    h = urllib.parse.urlparse(u if "://" in u else "https://" + u).hostname or ""
    return h.lower().removeprefix("www.")


def main():
    for stream in (sys.stdout, sys.stderr):  # Korean/Windows consoles default to cp949 etc.
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--qid", help="Wikidata item ID, e.g. Q12345")
    g.add_argument("--search", help="company name to look up (lists candidates only)")
    ap.add_argument("--lang", default="en", help="language for --search and value labels (default en)")
    ap.add_argument("--langs", default="en,ko", help="languages that must have label+description (default en,ko)")
    ap.add_argument("--site", help="website URL whose JSON-LD should link the item")
    ap.add_argument("--out", help="folder for entity_check.json + entity_check.md (default: Markdown to stdout)")
    a = ap.parse_args()

    if a.search:
        rows = search(a.search, a.lang)
        print(f"# Wikidata candidates for “{a.search}” ({a.lang})\n")
        if not rows:
            print("No items found. If the company meets Wikidata:Notability, it may need a new item (see §5).")
        for qid, lab, desc in rows:
            print(f"- {qid} — {lab} — {desc or '(no description)'} — https://www.wikidata.org/wiki/{qid}")
        print("\nOpen each candidate and confirm it is the same entity before using its QID.")
        return 0

    qid = a.qid.strip().upper()
    ent = fetch_item(qid)
    claims = ent.get("claims", {})
    langs = [x.strip() for x in a.langs.split(",") if x.strip()]
    item_url = f"https://www.wikidata.org/wiki/{qid}"

    report = {"qid": qid, "url": item_url, "terms": {}, "core": {}, "unreferenced": [], "identifiers": {},
              "structure": {}, "sitelinks": {}, "site": None, "problems": []}

    for L in langs:
        report["terms"][L] = {
            "label": ent.get("labels", {}).get(L, {}).get("value"),
            "description": ent.get("descriptions", {}).get(L, {}).get("value"),
            "aliases": [x["value"] for x in ent.get("aliases", {}).get(L, [])],
        }
        if not report["terms"][L]["label"]:
            report["problems"].append(f"no {L} label")
        if not report["terms"][L]["description"]:
            report["problems"].append(f"no {L} description")

    item_ids = set()
    for pid, name in CORE + STRUCTURE:
        vals = claim_values(claims, pid)
        report["core" if (pid, name) in CORE else "structure"][pid] = {"name": name, "values": vals}
        item_ids.update(v["value"] for v in vals if re.fullmatch(r"Q\d+", str(v["value"])))
        if (pid, name) in CORE and not vals:
            report["problems"].append(f"missing {pid} {name}")
    for pid, name, fmt in IDENTIFIERS:
        vals = claim_values(claims, pid)
        report["identifiers"][pid] = {"name": name, "values": [dict(v, url=fmt.format(v["value"])) for v in vals]}

    # Only the statements a reviewer judges the company by; identifiers and P856 are self-evidencing.
    for pid, _ in CORE + STRUCTURE:
        if pid == "P856":
            continue
        if any(not c.get("references") for c in claims.get(pid, [])):
            report["unreferenced"].append(pid)
    names = labels_for(sorted(item_ids | set(report["unreferenced"])), a.lang)

    for k, v in ent.get("sitelinks", {}).items():
        report["sitelinks"][k] = v.get("title")

    if a.site:
        try:
            final_url, nodes, errors = site_org_nodes(a.site)
            linked = [n for n in nodes if any(item_url.replace("https://", "") in str(s) for s in n["sameAs"])
                      or (n["id"] and item_url.replace("https://", "") in str(n["id"]))]
            parent_linked = [n for n in nodes if item_url.replace("https://", "") in json.dumps(n.get("parentOrganization") or "")]
            p856_hosts = {host(v["value"]) for v in report["core"]["P856"]["values"]}
            report["site"] = {"url": a.site, "final_url": final_url, "org_nodes": nodes, "jsonld_parse_errors": errors,
                              "links_item_in_sameAs_or_id": bool(linked),
                              "links_item_via_parentOrganization": bool(parent_linked),
                              "p856_matches_site_host": host(final_url) in p856_hosts}
            if not nodes:
                report["problems"].append("no Organization-type JSON-LD on the site page")
            elif not linked and not parent_linked:
                report["problems"].append("site JSON-LD does not reference the Wikidata item (sameAs/@id/parentOrganization)")
            if not report["site"]["p856_matches_site_host"]:
                report["problems"].append("site host not in the item's official website (P856)")
        except Exception as e:  # noqa: BLE001 — report and continue
            report["site"] = {"url": a.site, "error": str(e)}
            report["problems"].append(f"site not checked: {e}")

    md = render_md(report, names)
    if a.out:
        os.makedirs(a.out, exist_ok=True)
        with open(os.path.join(a.out, "entity_check.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        with open(os.path.join(a.out, "entity_check.md"), "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Wrote {a.out}/entity_check.json and entity_check.md — {len(report['problems'])} problem(s).")
    else:
        sys.stdout.write(md)
    return 1 if report["problems"] else 0


def render_md(r, names):
    def show(v):
        s = str(v["value"])
        return f"{names.get(s, s)} ({s})" if re.fullmatch(r"Q\d+", s) else s

    out = [f"# Wikidata entity check — {r['qid']}", "", r["url"], ""]
    out += ["## Problems", ""] + ([f"- {p}" for p in r["problems"]] or ["- none"]) + [""]
    out += ["## Labels and descriptions", "", "| Lang | Label | Description | Aliases |", "|---|---|---|---|"]
    for L, t in r["terms"].items():
        out.append(f"| {L} | {t['label'] or '—'} | {t['description'] or '—'} | {', '.join(t['aliases']) or '—'} |")
    out += ["", "## Core statements", "", "| Property | Values (rank, references) |", "|---|---|"]
    for pid, d in list(r["core"].items()) + list(r["structure"].items()):
        shown = d["values"][:MAX_VALUES]
        vals = "; ".join(f"{show(v)} ({v['rank']}, {v['refs']} ref)" for v in shown) or "**missing**"
        if len(d["values"]) > MAX_VALUES:
            vals += f"; … {len(d['values']) - MAX_VALUES} more"
        out.append(f"| {pid} {d['name']} | {vals} |")
    out += ["", "## Identifiers", ""]
    for pid, d in r["identifiers"].items():
        urls = [v["url"] for v in d["values"]]
        vals = ", ".join(urls[:MAX_VALUES]) + (f", … {len(urls) - MAX_VALUES} more" if len(urls) > MAX_VALUES else "")
        out.append(f"- {pid} {d['name']}: {vals or '—'}")
    out += ["", "## Core statements with at least one unreferenced value", ""]
    out += [f"- {p} {names.get(p, '')}" for p in r["unreferenced"]] or ["- none"]
    wikis = {k: v for k, v in r["sitelinks"].items() if re.fullmatch(r"[a-z_]+wiki", k) and k != "commonswiki"}
    out += ["", f"## Sitelinks ({len(wikis)} Wikipedia editions)", ""]
    langs = list(r["terms"].keys())
    key = [f"- {L}wiki: {wikis[L + 'wiki']}" for L in langs if L + "wiki" in wikis]
    missing = [f"- {L}wiki: none" for L in langs if L + "wiki" not in wikis]
    out += key + missing or ["- none (notability then rests on serious public references)"]
    if r["site"]:
        s = r["site"]
        out += ["", "## Website JSON-LD", ""]
        if "error" in s:
            out.append(f"- NOT VERIFIED: {s['error']}")
        else:
            out.append(f"- Page: {s['final_url']} · Organization-type nodes: {len(s['org_nodes'])} · JSON-LD parse errors: {s['jsonld_parse_errors']}")
            out.append(f"- Item in sameAs/@id: {s['links_item_in_sameAs_or_id']} · via parentOrganization: {s['links_item_via_parentOrganization']}")
            out.append(f"- Site host in P856: {s['p856_matches_site_host']}")
            for n in s["org_nodes"]:
                out.append(f"  - {'/'.join(map(str, n['type']))} “{n['name']}” @id={n['id']} sameAs={len(n['sameAs'])}")
    out += ["", "Next steps → references/entity-authority-and-off-site.md §5 (disclose COI; reference every statement).", ""]
    return "\n".join(out)


if __name__ == "__main__":
    sys.exit(main())
