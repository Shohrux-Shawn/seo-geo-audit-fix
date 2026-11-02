#!/usr/bin/env python3
"""
sitemap_validate.py — read-only validator for a sitemap or sitemap index (stdlib only).

Checks the sitemap files themselves:
  - fetch status, redirects, gzip (by Content-Encoding or file magic), XML parse errors
  - root element and namespace (http://www.sitemaps.org/schemas/sitemap/0.9)
  - follows <sitemapindex> children (nested indexes are reported: the protocol does not allow them)
  - limits: 50,000 entries and 50 MB (52,428,800 bytes) uncompressed per file;
    a warning at 10 MB because Naver rejects sitemap files of 10 MB or more
  - <loc>: absolute http(s), host equal to --host (or the sitemap's own host), scheme equal
    to the sitemap's scheme, duplicates across all files
  - <lastmod>: W3C datetime format, dates in the future, the same value on (almost) every
    URL or "today" on most URLs (signs of a fake lastmod)
  - hreflang alternates (<xhtml:link rel="alternate" hreflang=...>): code format, absolute
    href, self-reference present, reciprocity, duplicate codes, alternates missing from the
    sitemap (pages announced by hreflang but not offered)

Checks a sample (or all) of the listed URLs:
  - status of the first response, the redirect chain and the final status
  - X-Robots-Tag noindex header, <meta name="robots|googlebot"> noindex
  - <link rel="canonical"> missing or different from the URL (compared after
    percent-decoding + Unicode NFC, host lower-cased)
  - a "possible soft 404" hint (200 with a not-found title or almost no text)

Output: <out>/sitemap_validate.json (all data) and <out>/sitemap_validate.md (summary).
Exit code 0 = no errors, 1 = errors found, 2 = the sitemap itself could not be read.

Usage:
  python3 sitemap_validate.py https://www.example.com/sitemap.xml --host www.example.com \
      --max 500 --out ./sitemap-out
  python3 sitemap_validate.py https://www.example.com/sitemap.xml --max 0      # fetch every URL
  python3 sitemap_validate.py https://www.example.com/sitemap.xml --max -1     # no page fetches

Only GET requests are sent. Be polite on big sites: use --delay and a sample.
Local testing: set NO_PROXY=127.0.0.1,localhost if your shell uses an HTTP proxy.
"""
import argparse
import datetime as dt
import gzip
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; seo-geo-audit-fix/1.0; read-only sitemap check)"
SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
XHTML_NS = "http://www.w3.org/1999/xhtml"
MAX_URLS = 50000
MAX_BYTES = 52428800
NAVER_MAX_BYTES = 10 * 1024 * 1024
W3C_RE = re.compile(
    r"^\d{4}(-\d{2}(-\d{2}(T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2}))?)?)?$")
HREFLANG_RE = re.compile(r"^(x-default|[a-zA-Z]{2,3}(-[A-Za-z]{4})?(-([A-Za-z]{2}|\d{3}))?)$")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_noredir = urllib.request.build_opener(NoRedirect)


def fetch(url, timeout=20, max_bytes=60 * 1024 * 1024):
    """One GET without following redirects. Returns (status, headers, body) — never raises."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    try:
        resp = _noredir.open(req, timeout=timeout)
        status, headers, body = resp.status, resp.headers, resp.read(max_bytes)
    except urllib.error.HTTPError as e:
        status, headers = e.code, e.headers
        try:
            body = e.read(max_bytes)
        except Exception:
            body = b""
    except Exception as e:  # DNS, TLS, timeout, refused
        return None, {"error": f"{type(e).__name__}: {e}"}, b""
    hdrs = {k.lower(): v for k, v in (headers.items() if headers else [])}
    if hdrs.get("content-encoding", "").lower() == "gzip" and body[:2] == b"\x1f\x8b":
        try:
            body = gzip.decompress(body)
        except Exception:
            pass
    return status, hdrs, body


def fetch_follow(url, timeout=20, max_hops=5):
    """Follow redirects manually. Returns (chain, final_status, final_headers, final_body)."""
    chain, cur = [], url
    for _ in range(max_hops + 1):
        status, hdrs, body = fetch(cur, timeout)
        chain.append({"url": cur, "status": status, "error": hdrs.get("error")})
        loc = hdrs.get("location")
        if status in (301, 302, 303, 307, 308) and loc:
            cur = urllib.parse.urljoin(cur, loc)
            continue
        return chain, status, hdrs, body
    return chain, None, {}, b""


def norm_url(u):
    if not u:
        return ""
    p = urllib.parse.urlsplit(u.strip())
    path = unicodedata.normalize("NFC", urllib.parse.unquote(p.path or "/"))
    query = unicodedata.normalize("NFC", urllib.parse.unquote(p.query))
    return urllib.parse.urlunsplit((p.scheme.lower(), p.netloc.lower(), path, query, ""))


def parse_lastmod(v):
    v = v.strip()
    if not W3C_RE.match(v):
        return None
    s = v.replace("Z", "+00:00")
    for fmt in ("%Y", "%Y-%m", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(s, fmt).replace(tzinfo=dt.timezone.utc)
        except ValueError:
            pass
    if re.search(r"T\d{2}:\d{2}[+-]", s):  # hh:mm without seconds
        s = re.sub(r"(T\d{2}:\d{2})([+-])", r"\1:00\2", s)
    try:
        return dt.datetime.fromisoformat(s)
    except ValueError:
        return None


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonicals, self.robots, self.title, self._t, self.text_len = [], [], "", False, 0
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonicals.append(a.get("href", ""))
        elif tag == "meta" and a.get("name", "").lower() in ("robots", "googlebot"):
            self.robots.append(a.get("content", ""))
        elif tag == "title":
            self._t = True
        elif tag in ("script", "style", "noscript"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._t = False
        elif tag in ("script", "style", "noscript") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._t:
            self.title += data
        elif not self._skip:
            self.text_len += len(data.strip())


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, code, msg, url=None):
        self.errors.append({"code": code, "msg": msg, "url": url})

    def warn(self, code, msg, url=None):
        self.warnings.append({"code": code, "msg": msg, "url": url})


def read_sitemap(url, rep, timeout):
    """Fetch + parse one sitemap file. Returns (kind, entries, info) or (None, [], info)."""
    chain, status, hdrs, body = fetch_follow(url, timeout)
    info = {"url": url, "status": status, "redirects": len(chain) - 1,
            "content_type": hdrs.get("content-type"), "bytes_uncompressed": 0, "entries": 0}
    if len(chain) > 1:
        rep.warn("sitemap_redirect", f"sitemap redirects ({len(chain) - 1} hop(s)) to {chain[-1]['url']}; submit the final URL", url)
    if status != 200 or not body:
        rep.err("sitemap_fetch", f"sitemap returned {status or chain[-1].get('error')}", url)
        return None, [], info
    if body[:2] == b"\x1f\x8b":
        try:
            body = gzip.decompress(body)
        except Exception as e:
            rep.err("sitemap_gzip", f"gzip decode failed: {e}", url)
            return None, [], info
    info["bytes_uncompressed"] = len(body)
    if len(body) > MAX_BYTES:
        rep.err("sitemap_size", f"{len(body):,} bytes uncompressed > 50 MB limit", url)
    elif len(body) >= NAVER_MAX_BYTES:
        rep.warn("sitemap_size_naver", f"{len(body):,} bytes ≥ 10 MB: Naver rejects this file; split it", url)
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        snippet = body[:80].decode("utf-8", "replace").replace("\n", " ")
        rep.err("sitemap_xml", f"XML parse error: {e} (starts with: {snippet!r})", url)
        return None, [], info
    m = re.match(r"\{(.*)\}(.*)", root.tag)
    ns, local = (m.group(1), m.group(2)) if m else ("", root.tag)
    if ns != SM_NS:
        rep.err("sitemap_namespace", f"root namespace is {ns or '(none)'!r}, expected {SM_NS}", url)
    if local not in ("urlset", "sitemapindex"):
        rep.err("sitemap_root", f"root element <{local}> is neither <urlset> nor <sitemapindex>", url)
        return None, [], info
    entries = []
    child_tag = "sitemap" if local == "sitemapindex" else "url"
    for el in root.iter():
        if not el.tag.endswith("}" + child_tag) and el.tag != child_tag:
            continue
        loc = lastmod = None
        alts = []
        for c in el:
            t = c.tag.split("}")[-1]
            if t == "loc":
                loc = (c.text or "").strip()
            elif t == "lastmod":
                lastmod = (c.text or "").strip()
            elif t == "link" and c.tag.startswith("{" + XHTML_NS):
                if c.get("rel", "") == "alternate":
                    alts.append((c.get("hreflang", ""), (c.get("href") or "").strip()))
        entries.append({"loc": loc, "lastmod": lastmod, "alternates": alts, "sitemap": url})
    info["entries"] = len(entries)
    if len(entries) > MAX_URLS:
        rep.err("sitemap_count", f"{len(entries):,} entries > 50,000 limit", url)
    if not entries:
        rep.warn("sitemap_empty", "sitemap has no entries (an empty 200 often means a failed data source)", url)
    return local, entries, info


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sitemap", help="URL of a sitemap or sitemap index")
    ap.add_argument("--host", help="Expected host of every <loc>, e.g. www.example.com (default: the sitemap's host)")
    ap.add_argument("--max", type=int, default=500, help="URLs to fetch: N = evenly spaced sample, 0 = all, -1 = none (default 500)")
    ap.add_argument("--max-sitemaps", type=int, default=500, help="Stop after this many sitemap files (default 500)")
    ap.add_argument("--delay", type=float, default=0.2, help="Seconds between page fetches (default 0.2)")
    ap.add_argument("--timeout", type=float, default=20, help="Per-request timeout in seconds (default 20)")
    ap.add_argument("--out", default="./sitemap-validate-out", help="Output directory")
    args = ap.parse_args()

    rep = Report()
    start = urllib.parse.urlsplit(args.sitemap)
    host = (args.host or start.netloc).lower()
    scheme = start.scheme.lower()

    # 1. walk the sitemap tree
    files, urls, queue, seen = [], [], [(args.sitemap, 0)], set()
    while queue and len(seen) < args.max_sitemaps:
        sm, depth = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        kind, entries, info = read_sitemap(sm, rep, args.timeout)
        info["kind"] = kind
        files.append(info)
        if kind == "sitemapindex":
            if depth > 0:
                rep.err("nested_index", "a sitemap index lists another sitemap index (not allowed by the protocol)", sm)
            for e in entries:
                if e["loc"]:
                    if urllib.parse.urlsplit(e["loc"]).netloc.lower() != start.netloc.lower():
                        rep.warn("child_host", f"child sitemap on another host: {e['loc']}", sm)
                    queue.append((e["loc"], depth + 1))
                if e["lastmod"] and not parse_lastmod(e["lastmod"]):
                    rep.err("lastmod_format", f"child lastmod {e['lastmod']!r} is not W3C datetime", sm)
        elif kind == "urlset":
            urls.extend(entries)
    if queue:
        rep.warn("sitemap_limit", f"stopped after {len(seen)} sitemap files (--max-sitemaps)")
    if not files or files[0]["status"] != 200 or files[0].get("kind") is None:
        write_out(args, host, files, urls, [], rep)
        return 2

    # 2. URL-level checks
    now = dt.datetime.now(dt.timezone.utc)
    loc_count = Counter(u["loc"] for u in urls if u["loc"])
    for loc, n in loc_count.items():
        if n > 1:
            rep.err("duplicate_url", f"listed {n} times", loc)
    lastmods, parsed_dates = [], []
    for u in urls:
        loc = u["loc"]
        if not loc:
            rep.err("loc_missing", "<url> without <loc>", u["sitemap"])
            continue
        p = urllib.parse.urlsplit(loc)
        if p.scheme not in ("http", "https") or not p.netloc:
            rep.err("loc_not_absolute", "loc is not an absolute http(s) URL", loc)
            continue
        if p.netloc.lower() != host:
            rep.err("host_mismatch", f"host {p.netloc} != expected {host}", loc)
        elif p.scheme.lower() != scheme:
            rep.warn("scheme_mismatch", f"scheme {p.scheme} differs from the sitemap's {scheme}", loc)
        if re.search(r"[?&](utm_[a-z]+|gclid|fbclid|sessionid|sid)=", loc, re.I):
            rep.warn("tracking_param", "tracking/session parameter in loc", loc)
        if u["lastmod"] is not None:
            lastmods.append(u["lastmod"])
            d = parse_lastmod(u["lastmod"])
            if not d:
                rep.err("lastmod_format", f"lastmod {u['lastmod']!r} is not W3C datetime", loc)
            else:
                if d.tzinfo is None:
                    d = d.replace(tzinfo=dt.timezone.utc)
                parsed_dates.append(d)
                if d > now + dt.timedelta(days=1):
                    rep.err("lastmod_future", f"lastmod {u['lastmod']} is in the future", loc)
    if len(lastmods) >= 20:
        top, n = Counter(lastmods).most_common(1)[0]
        if n == len(lastmods):
            rep.warn("lastmod_identical", f"all {n} URLs share lastmod {top!r} — likely build/request time, not content dates")
        elif n / len(lastmods) >= 0.9:
            rep.warn("lastmod_mostly_identical", f"{n}/{len(lastmods)} URLs share lastmod {top!r}")
        today = sum(1 for d in parsed_dates if d.date() == now.date())
        if today / len(lastmods) >= 0.5:
            rep.warn("lastmod_today", f"{today}/{len(lastmods)} lastmod values are today — 'lastmod = now'?")
    elif urls and not lastmods:
        rep.warn("lastmod_absent", "no lastmod at all (fine if unknown; Google and Bing use it when accurate)")

    # 3. hreflang alternates
    url_set = {norm_url(u["loc"]) for u in urls if u["loc"]}
    alt_map = {}
    for u in urls:
        if not u["alternates"] or not u["loc"]:
            continue
        me = norm_url(u["loc"])
        codes = defaultdict(set)
        for code, href in u["alternates"]:
            if not HREFLANG_RE.match(code or ""):
                rep.err("hreflang_code", f"invalid hreflang code {code!r}", u["loc"])
            if not urllib.parse.urlsplit(href).netloc:
                rep.err("hreflang_href", f"alternate href not absolute: {href!r}", u["loc"])
                continue
            codes[code.lower()].add(norm_url(href))
        for code, hrefs in codes.items():
            if len(hrefs) > 1:
                rep.err("hreflang_duplicate_code", f"hreflang {code} points to {len(hrefs)} different URLs", u["loc"])
        targets = {h for hs in codes.values() for h in hs}
        if me not in targets:
            rep.err("hreflang_no_self", "the URL's alternates don't include the URL itself", u["loc"])
        alt_map[me] = targets
    for me, targets in alt_map.items():
        for t in targets:
            if t == me:
                continue
            if t not in url_set:
                rep.warn("hreflang_not_in_sitemap", f"alternate {t} is announced but not offered in the sitemap", me)
            elif t in alt_map and me not in alt_map[t]:
                rep.err("hreflang_not_reciprocal", f"{t} does not link back", me)

    # 4. fetch a sample of pages
    pages = []
    locs = [u["loc"] for u in urls if u["loc"]]
    locs = list(dict.fromkeys(locs))
    if args.max == 0:
        sample = locs
    elif args.max < 0:
        sample = []
    elif len(locs) <= args.max:
        sample = locs
    else:
        step = len(locs) / args.max
        sample = [locs[int(i * step)] for i in range(args.max)]
    for i, loc in enumerate(sample, 1):
        chain, status, hdrs, body = fetch_follow(loc, args.timeout)
        row = {"url": loc, "first_status": chain[0]["status"], "final_status": status,
               "final_url": chain[-1]["url"] if len(chain) > 1 else None, "hops": len(chain) - 1,
               "error": chain[-1].get("error")}
        if len(chain) > 1:
            rep.err("url_redirects", f"{chain[0]['status']} → {chain[-1]['url']} ({len(chain) - 1} hop(s)); list the final URL", loc)
        if status != 200:
            rep.err("url_status", f"final status {status or row['error']}", loc)
        else:
            xrt = hdrs.get("x-robots-tag", "")
            row["x_robots_tag"] = xrt
            if "noindex" in xrt.lower() or "none" in [t.strip().lower() for t in xrt.split(",")]:
                rep.err("url_noindex_header", f"X-Robots-Tag: {xrt}", loc)
            ctype = hdrs.get("content-type", "")
            if "html" in ctype or body[:200].lstrip().lower().startswith((b"<!doctype html", b"<html")):
                pp = PageParser()
                try:
                    pp.feed(body.decode("utf-8", "replace"))
                except Exception:
                    pass
                row.update({"canonical": pp.canonicals, "meta_robots": pp.robots,
                            "title": pp.title.strip()[:120], "text_chars": pp.text_len})
                if any("noindex" in r.lower() or r.strip().lower() == "none" for r in pp.robots):
                    rep.err("url_noindex_meta", f"meta robots: {pp.robots}", loc)
                if not pp.canonicals:
                    rep.warn("canonical_missing", "no rel=canonical", loc)
                else:
                    if len(set(pp.canonicals)) > 1:
                        rep.err("canonical_multiple", f"{len(pp.canonicals)} different canonicals", loc)
                    canon = urllib.parse.urljoin(chain[-1]["url"], pp.canonicals[0])
                    target = chain[-1]["url"]  # after a redirect, compare with the final URL
                    if norm_url(canon) != norm_url(target):
                        rep.err("canonical_mismatch", f"canonical is {canon}", loc)
                if re.search(r"\b(404|not found|page not found)\b", pp.title, re.I) or pp.text_len < 50:
                    rep.warn("possible_soft_404", f"200 with title {pp.title.strip()[:60]!r} and {pp.text_len} text chars", loc)
        pages.append(row)
        if args.delay:
            time.sleep(args.delay)
        if i % 100 == 0:
            print(f"  fetched {i}/{len(sample)}", file=sys.stderr)

    write_out(args, host, files, urls, pages, rep)
    return 1 if rep.errors else 0


def write_out(args, host, files, urls, pages, rep):
    os.makedirs(args.out, exist_ok=True)
    data = {"sitemap": args.sitemap, "expected_host": host,
            "checked_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "files": files, "url_count": len(urls), "pages_fetched": len(pages),
            "errors": rep.errors, "warnings": rep.warnings, "pages": pages,
            "urls": [{"loc": u["loc"], "lastmod": u["lastmod"], "sitemap": u["sitemap"], "alternates": len(u["alternates"])} for u in urls]}
    with open(os.path.join(args.out, "sitemap_validate.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    md = ["# sitemap_validate summary", "",
          f"- Sitemap: {args.sitemap}", f"- Expected host: {host}", f"- Checked: {data['checked_at']}",
          f"- Files read: {len(files)}; URLs listed: {len(urls)}; pages fetched: {len(pages)}",
          f"- **Errors: {len(rep.errors)}**; warnings: {len(rep.warnings)}", "", "## Files", "",
          "| File | Kind | Status | Entries | Bytes (uncompressed) |", "|---|---|---|---|---|"]
    for f_ in files:
        md.append(f"| {f_['url']} | {f_.get('kind')} | {f_['status']} | {f_['entries']} | {f_['bytes_uncompressed']:,} |")
    for title, items in (("Errors", rep.errors), ("Warnings", rep.warnings)):
        md += ["", f"## {title}", ""]
        if not items:
            md.append("None.")
            continue
        by = defaultdict(list)
        for it in items:
            by[it["code"]].append(it)
        for code, its in sorted(by.items(), key=lambda kv: -len(kv[1])):
            md.append(f"### {code} ({len(its)})")
            for it in its[:15]:
                md.append(f"- {it['url'] or ''} — {it['msg']}" if it["url"] else f"- {it['msg']}")
            if len(its) > 15:
                md.append(f"- … {len(its) - 15} more in the JSON")
    text = "\n".join(md) + "\n"
    with open(os.path.join(args.out, "sitemap_validate.md"), "w", encoding="utf-8") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    sys.exit(main())
