#!/usr/bin/env python3
"""
site_check.py — read-only technical/on-page check for one or more sites (stdlib only).

What it does for each site:
  1. Redirects: first-hop status + full chain for http/https x apex/www variants.
  2. robots.txt: sitemap lines, AI-crawler groups (GPTBot, ClaudeBot, PerplexityBot,
     Google-Extended, Bingbot, Yeti, Daum), Disallow lines.
  3. Sitemap(s): collects URLs (follows sitemap indexes), samples or fetches all of them,
     and records status / title / description / H1 / canonical / lang / hreflang / JSON-LD types /
     phone numbers / forbidden words / <main> text length.
  4. Duplicate titles and descriptions across the fetched pages.

Output: one JSON file (full data) + one Markdown summary.

Usage:
  python3 site_check.py https://www.example.com https://www.example-2.com \
      --max-urls 200 --forbidden "free consultation,24 hours" --out ./audit-out

--forbidden takes phrases in the site's own language (e.g. the Korean words for
"free consultation" and "24-hour consultation" on a Korean site).

Use --max-urls 0 to fetch every sitemap URL (slow on big sites; be polite).
The script never sends anything except GET requests and never logs in.
"""
import argparse
import gzip
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; seo-geo-audit-fix/1.0; read-only audit)"
AI_BOTS = ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "Bingbot", "Yeti", "Daum"]
PHONE_RE = re.compile(r"(?<!\d)(0\d{1,2}-\d{3,4}-\d{4}|1[5-9]\d{2}-\d{4}|0\d{9,10})(?!\d)")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_noredir = urllib.request.build_opener(NoRedirect)


def fetch(url, timeout=20, follow=True):
    """Return (status, final_url, headers, body_bytes). Never raises on HTTP errors."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    opener = urllib.request.build_opener() if follow else _noredir
    try:
        resp = opener.open(req, timeout=timeout)
        body = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            body = gzip.decompress(body)
        return resp.status, resp.geturl(), dict(resp.headers), body
    except urllib.error.HTTPError as e:
        body = e.read() if hasattr(e, "read") else b""
        return e.code, url, dict(e.headers or {}), body
    except Exception as e:  # network error, DNS, TLS
        return None, url, {"error": f"{type(e).__name__}: {e}"}, b""


def redirect_chain(url, max_hops=6):
    chain = []
    cur = url
    for _ in range(max_hops):
        status, _, headers, _ = fetch(cur, follow=False)
        loc = headers.get("Location") or headers.get("location")
        chain.append({"url": cur, "status": status, "location": loc, "error": headers.get("error")})
        if status in (301, 302, 303, 307, 308) and loc:
            cur = urllib.parse.urljoin(cur, loc)
            continue
        break
    return chain


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.meta = {}
        self.canonical = None
        self.hreflang = []
        self.lang = None
        self.h1 = []
        self._in_h1 = False
        self._h1_buf = ""
        self.jsonld_raw = []
        self._in_jsonld = False
        self._jsonld_buf = ""
        self._main_depth = 0
        self.main_text = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html" and a.get("lang"):
            self.lang = a["lang"]
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link":
            rel = a.get("rel", "").lower()
            if rel == "canonical":
                self.canonical = a.get("href")
            elif rel == "alternate" and a.get("hreflang"):
                self.hreflang.append((a["hreflang"], a.get("href")))
        elif tag == "h1":
            self._in_h1 = True
            self._h1_buf = ""
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._in_jsonld = True
            self._jsonld_buf = ""
        elif tag == "main":
            self._main_depth += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1" and self._in_h1:
            self._in_h1 = False
            self.h1.append(re.sub(r"\s+", " ", self._h1_buf).strip())
        elif tag == "script" and self._in_jsonld:
            self._in_jsonld = False
            self.jsonld_raw.append(self._jsonld_buf)
        elif tag == "main" and self._main_depth:
            self._main_depth -= 1

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_h1:
            self._h1_buf += data
        if self._in_jsonld:
            self._jsonld_buf += data
            return
        if self._main_depth:
            self.main_text.append(data)
        self.text.append(data)


def jsonld_types(raw_blocks):
    types, errors = [], 0
    def walk(node):
        if isinstance(node, dict):
            t = node.get("@type")
            if t:
                types.extend(t if isinstance(t, list) else [t])
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    for raw in raw_blocks:
        try:
            walk(json.loads(raw))
        except Exception:
            errors += 1
    return sorted(set(map(str, types))), errors


def analyse_page(url, forbidden):
    status, final, headers, body = fetch(url)
    row = {"url": url, "status": status, "final_url": final if final != url else None,
           "error": headers.get("error")}
    if not body or status is None or status >= 400:
        return row
    html = body.decode("utf-8", errors="replace")
    p = PageParser()
    try:
        p.feed(html)
    except Exception as e:
        row["parse_error"] = str(e)
        return row
    text = re.sub(r"\s+", " ", " ".join(p.text))
    main_text = re.sub(r"\s+", " ", " ".join(p.main_text)).strip()
    types, ld_err = jsonld_types(p.jsonld_raw)
    row.update({
        "title": p.title.strip(),
        "description": p.meta.get("description", ""),
        "robots_meta": p.meta.get("robots", ""),
        "h1": p.h1,
        "canonical": p.canonical,
        "lang": p.lang,
        "hreflang": p.hreflang,
        "og_image": p.meta.get("og:image"),
        "jsonld_types": types,
        "jsonld_parse_errors": ld_err,
        "phones_visible": sorted(set(PHONE_RE.findall(text))),
        "main_chars": len(main_text),
        "forbidden_hits_visible": [w for w in forbidden if w and w in text],
        "forbidden_hits_raw_html": [w for w in forbidden if w and w in html],
        "utm_links": len(re.findall(r'href="[^"]*utm_[a-z]+=', html)),
    })
    return row


def parse_robots(body):
    lines = body.decode("utf-8", errors="replace").splitlines()
    groups, cur_agents, sitemaps = defaultdict(list), [], []
    last_was_agent = False
    for line in lines:
        line = line.split("#", 1)[0].strip() if not line.strip().startswith("#DaumWebMasterTool") else line.strip()
        if not line or ":" not in line:
            continue
        k, v = [s.strip() for s in line.split(":", 1)]
        kl = k.lower()
        if kl == "user-agent":
            if not last_was_agent:
                cur_agents = []
            cur_agents.append(v)
            groups.setdefault(v, [])
            last_was_agent = True
            continue
        last_was_agent = False
        if kl == "sitemap":
            sitemaps.append(v)
        elif kl in ("allow", "disallow"):
            for ag in cur_agents:
                groups[ag].append(f"{k}: {v}")
    ai = {}
    for bot in AI_BOTS:
        own = [g for g in groups if g.lower() == bot.lower()]
        if own:
            rules = groups[own[0]]
            ai[bot] = {"own_group": True, "blocked_root": "Disallow: /" in rules, "rules": rules}
        else:
            star = groups.get("*", [])
            ai[bot] = {"own_group": False, "blocked_root": "Disallow: /" in star}
    daum = [l.strip() for l in lines if l.strip().startswith("#DaumWebMasterTool")]
    return {"sitemaps": sitemaps, "groups": dict(groups), "ai_bots": ai, "daum_verification": daum}


def collect_sitemap_urls(url, seen=None, limit_maps=200):
    seen = seen if seen is not None else set()
    if url in seen or len(seen) >= limit_maps:
        return []
    seen.add(url)
    status, _, _, body = fetch(url)
    if status != 200 or not body:
        return []
    xml = body.decode("utf-8", errors="replace")
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
    if "<sitemapindex" in xml:
        out = []
        for child in locs:
            out.extend(collect_sitemap_urls(child, seen, limit_maps))
        return out
    return locs


def check_site(base, max_urls, forbidden, delay):
    parsed = urllib.parse.urlparse(base)
    host = parsed.netloc
    apex = host[4:] if host.startswith("www.") else host
    variants = [f"{s}://{h}/" for s in ("http", "https") for h in (apex, "www." + apex)]
    result = {"site": base, "redirects": {v: redirect_chain(v) for v in variants}}

    status, _, _, body = fetch(urllib.parse.urljoin(base, "/robots.txt"))
    result["robots_status"] = status
    robots = parse_robots(body) if status == 200 else {"sitemaps": [], "ai_bots": {}}
    result["robots"] = robots

    s, _, _, b = fetch(urllib.parse.urljoin(base, "/llms.txt"))
    result["llms_txt"] = {"status": s, "chars": len(b.decode("utf-8", "replace")) if s == 200 else 0}

    sitemap_list = robots.get("sitemaps") or [urllib.parse.urljoin(base, "/sitemap.xml")]
    urls = []
    for sm in sitemap_list:
        urls.extend(collect_sitemap_urls(sm))
    urls = list(dict.fromkeys(urls))
    result["sitemap_url_count"] = len(urls)

    to_fetch = [base] + [u for u in urls if u.rstrip("/") != base.rstrip("/")]
    if max_urls:
        to_fetch = to_fetch[:max_urls]
    pages = []
    for i, u in enumerate(to_fetch, 1):
        pages.append(analyse_page(u, forbidden))
        if delay:
            time.sleep(delay)
        if i % 50 == 0:
            print(f"  {base}: {i}/{len(to_fetch)} pages", file=sys.stderr)
    result["pages"] = pages

    dup_t, dup_d = defaultdict(list), defaultdict(list)
    for p in pages:
        if p.get("title"):
            dup_t[p["title"]].append(p["url"])
        if p.get("description"):
            dup_d[p["description"]].append(p["url"])
    result["duplicate_titles"] = {k: v for k, v in dup_t.items() if len(v) > 1}
    result["duplicate_descriptions"] = {k: v for k, v in dup_d.items() if len(v) > 1}
    return result


def summarize(results):
    out = ["# site_check summary", ""]
    for r in results:
        out.append(f"## {r['site']}")
        out.append("")
        out.append("**Redirects** (variant → hops → final status)")
        for v, chain in r["redirects"].items():
            hops = len(chain) - 1
            last = chain[-1]
            flag = "" if hops <= 1 else " ⚠️ multi-hop"
            out.append(f"- {v} → {hops} hop(s) → {last['status'] or last['error']}{flag}")
        rb = r["robots"]
        out.append("")
        out.append(f"**robots.txt** status {r['robots_status']}; sitemaps: {len(rb.get('sitemaps', []))}; "
                   f"Daum verification lines: {len(rb.get('daum_verification', []))}")
        for bot, info in rb.get("ai_bots", {}).items():
            note = "own group (does NOT inherit * rules)" if info["own_group"] else "uses * group"
            out.append(f"- {bot}: {'BLOCKED' if info['blocked_root'] else 'allowed'}; {note}")
        out.append(f"\n**llms.txt** status {r['llms_txt']['status']}, {r['llms_txt']['chars']} chars")
        pages = r["pages"]
        bad = [p for p in pages if p.get("status") != 200]
        out.append(f"\n**Pages** sitemap URLs: {r['sitemap_url_count']}; fetched: {len(pages)}; non-200: {len(bad)}")
        for p in bad[:20]:
            out.append(f"- {p['status']} {p['url']} {p.get('error') or ''}")
        home = pages[0] if pages else {}
        if home.get("status") == 200:
            out.append(f"\n**Home** title: {home.get('title')!r}")
            out.append(f"- H1: {home.get('h1')}")
            out.append(f"- canonical: {home.get('canonical')}; lang: {home.get('lang')}; hreflang: {len(home.get('hreflang', []))}")
            out.append(f"- JSON-LD types: {', '.join(home.get('jsonld_types', [])) or 'none'}")
            out.append(f"- phones visible: {', '.join(home.get('phones_visible', [])) or 'none'}")
        no_h1 = [p["url"] for p in pages if p.get("status") == 200 and not p.get("h1")]
        multi_h1 = [p["url"] for p in pages if len(p.get("h1") or []) > 1]
        no_ld = [p["url"] for p in pages if p.get("status") == 200 and not p.get("jsonld_types")]
        thin = [(p["main_chars"], p["url"]) for p in pages if p.get("status") == 200 and p.get("main_chars", 9999) < 300]
        forb = [(p["url"], p["forbidden_hits_raw_html"]) for p in pages if p.get("forbidden_hits_raw_html")]
        utm = [p["url"] for p in pages if p.get("utm_links")]
        out.append(f"\n- pages without H1: {len(no_h1)}; with >1 H1: {len(multi_h1)}; without JSON-LD: {len(no_ld)}")
        out.append(f"- thin <main> (<300 chars): {len(thin)}" + "".join(f"\n  - {c} chars {u}" for c, u in sorted(thin)[:10]))
        out.append(f"- forbidden wording (raw HTML): {len(forb)}" + "".join(f"\n  - {u}: {w}" for u, w in forb[:10]))
        out.append(f"- pages with UTM links: {len(utm)}")
        out.append(f"- duplicate title groups: {len(r['duplicate_titles'])}; duplicate description groups: {len(r['duplicate_descriptions'])}")
        for t, us in list(r["duplicate_titles"].items())[:10]:
            out.append(f"  - {t!r} ×{len(us)}")
        out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sites", nargs="+", help="Canonical base URLs, e.g. https://www.example.com")
    ap.add_argument("--max-urls", type=int, default=100, help="Pages per site to fetch (0 = all sitemap URLs)")
    ap.add_argument("--forbidden", default="", help="Comma-separated phrases to flag (searched in visible text and raw HTML)")
    ap.add_argument("--delay", type=float, default=0.3, help="Seconds between page fetches")
    ap.add_argument("--out", default="./site-check-out", help="Output directory")
    args = ap.parse_args()

    import os
    os.makedirs(args.out, exist_ok=True)
    forbidden = [w.strip() for w in args.forbidden.split(",") if w.strip()]
    results = []
    for s in args.sites:
        print(f"Checking {s} ...", file=sys.stderr)
        results.append(check_site(s.rstrip("/") + "/", args.max_urls, forbidden, args.delay))
    with open(os.path.join(args.out, "site_check.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    md = summarize(results)
    with open(os.path.join(args.out, "site_check.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(md)


if __name__ == "__main__":
    main()
