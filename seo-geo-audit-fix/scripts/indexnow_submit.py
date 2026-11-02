#!/usr/bin/env python3
"""
indexnow_submit.py — check an IndexNow key file and (only with --apply) submit URLs (stdlib only).

Steps:
  1. Reads the key from an environment variable (default INDEXNOW_KEY). The key is never
     printed in full. Format rule: 8-128 characters from a-z, A-Z, 0-9 and "-".
  2. Reads URLs from a file (one per line; blank lines and lines starting with # ignored),
     de-duplicates them and rejects URLs whose host differs from --host (the engine would
     answer 422). With --key-location, URLs must also sit under that file's directory.
  3. Verifies the key file: GET https://<host>/<key>.txt (or --key-location) must return 200
     without redirects and contain exactly the key. If it doesn't, nothing is sent.
  4. Splits the URLs into batches of up to 10,000 (the protocol limit per POST).
  5. Without --apply (default): prints the payload summary only (dry run).
     With --apply: POSTs each batch as JSON to the endpoint and prints the response codes.

Endpoint default: https://api.indexnow.org/indexnow (shared with all participating engines;
on 2026-11-02 indexnow.org listed Bing, Yandex, Seznam, Naver, Yep, Internet Archive and
Amazonbot). Google does not participate.

Usage:
  export INDEXNOW_KEY=<your key>
  python3 indexnow_submit.py --host www.example.com --urls-file changed.txt            # dry run
  python3 indexnow_submit.py --host www.example.com --urls-file changed.txt --apply    # send
  python3 indexnow_submit.py --host www.example.com --urls-file changed.txt \
      --key-location https://www.example.com/keys/indexnow-key.txt --apply

Send only URLs that were added, updated or deleted (404/410/redirect) since your last
submission — never the whole site on a schedule.
Local testing: set NO_PROXY=127.0.0.1,localhost if your shell uses an HTTP proxy.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_ENDPOINT = "https://api.indexnow.org/indexnow"
KEY_RE = re.compile(r"^[A-Za-z0-9-]{8,128}$")
BATCH_MAX = 10000
UA = "Mozilla/5.0 (compatible; seo-geo-audit-fix/1.0; indexnow-submit)"
MEANING = {200: "OK — URLs received", 202: "Accepted — key validation pending",
           400: "Bad request — invalid format", 403: "Forbidden — key not valid (file missing or content wrong)",
           422: "Unprocessable — URLs don't belong to the host or key doesn't match",
           429: "Too many requests — slow down"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def mask(key):
    return key[:4] + "…" + key[-2:] if len(key) > 8 else "…"


def check_key_file(url, key, timeout):
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        resp = opener.open(req, timeout=timeout)
        status, body = resp.status, resp.read(4096)
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code} (redirects and errors are not accepted)"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"
    text = body.decode("utf-8-sig", "replace").strip()
    if status != 200:
        return False, f"HTTP {status}"
    if text != key:
        return False, "HTTP 200 but the file content is not exactly the key"
    return True, "HTTP 200, content matches the key"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", required=True, help="Host of every URL, e.g. www.example.com (host[:port])")
    ap.add_argument("--key-env", default="INDEXNOW_KEY", help="Environment variable holding the key (default INDEXNOW_KEY)")
    ap.add_argument("--urls-file", required=True, help="Text file with one URL per line")
    ap.add_argument("--key-location", help="Full URL of the key file if it is not https://<host>/<key>.txt")
    ap.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help=f"IndexNow endpoint (default {DEFAULT_ENDPOINT})")
    ap.add_argument("--batch-size", type=int, default=BATCH_MAX, help="URLs per POST, max 10000 (default 10000)")
    ap.add_argument("--timeout", type=float, default=20, help="Request timeout in seconds")
    ap.add_argument("--apply", action="store_true", help="Actually POST to the endpoint (default: dry run)")
    args = ap.parse_args()

    key = os.environ.get(args.key_env, "").strip()
    if not key:
        print(f"ERROR: environment variable {args.key_env} is empty or not set.", file=sys.stderr)
        return 2
    if not KEY_RE.match(key):
        print("ERROR: the key must be 8-128 characters from a-z, A-Z, 0-9 and '-'.", file=sys.stderr)
        return 2
    host = args.host.lower().strip().rstrip("/")
    if "://" in host:
        print("ERROR: --host takes a host name (www.example.com), not a URL.", file=sys.stderr)
        return 2
    batch_size = max(1, min(args.batch_size, BATCH_MAX))

    with open(args.urls_file, encoding="utf-8-sig") as f:
        raw = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
    urls, rejected = [], []
    scope = None
    if args.key_location:
        kl = urllib.parse.urlsplit(args.key_location)
        if kl.netloc.lower() != host:
            print(f"ERROR: --key-location host {kl.netloc} differs from --host {host}.", file=sys.stderr)
            return 2
        scope = args.key_location.rsplit("/", 1)[0] + "/"
    for u in dict.fromkeys(raw):
        p = urllib.parse.urlsplit(u)
        if p.scheme not in ("http", "https") or not p.netloc:
            rejected.append((u, "not an absolute http(s) URL"))
        elif p.netloc.lower() != host:
            rejected.append((u, f"host {p.netloc} != {host}"))
        elif scope and not u.startswith(scope):
            rejected.append((u, f"outside the key file's directory {scope}"))
        else:
            urls.append(u)

    if args.key_location:
        key_url = args.key_location
    else:
        scheme = urllib.parse.urlsplit(urls[0]).scheme if urls else "https"
        key_url = f"{scheme}://{host}/{key}.txt"
    shown_key_url = key_url.replace(key, mask(key))
    ok, why = check_key_file(key_url, key, args.timeout)

    batches = [urls[i:i + batch_size] for i in range(0, len(urls), batch_size)]
    print("IndexNow submission " + ("(APPLY)" if args.apply else "(dry run — nothing sent)"))
    print(f"  endpoint:     {args.endpoint}")
    print(f"  host:         {host}")
    print(f"  key:          {mask(key)} (from ${args.key_env})")
    print(f"  key file:     {shown_key_url} -> {'OK' if ok else 'FAIL'}: {why}")
    print(f"  URLs:         {len(raw)} read, {len(urls)} valid, {len(rejected)} rejected, {len(raw) - len(set(raw))} duplicates dropped")
    print(f"  batches:      {len(batches)} (≤ {batch_size} URLs each)")
    for u, r in rejected[:10]:
        print(f"  rejected:     {u} — {r}")
    for u in urls[:3]:
        print(f"  sample:       {u}")
    payload_keys = ["host", "key", "urlList"] + (["keyLocation"] if args.key_location else [])
    print(f"  payload keys: {', '.join(payload_keys)}")

    if not ok:
        print("STOP: the key file check failed; fix it before submitting (engines would answer 403).", file=sys.stderr)
        return 3
    if not urls:
        print("Nothing to submit.")
        return 0
    if not args.apply:
        print("Dry run complete. Re-run with --apply to send.")
        return 0

    failures = 0
    for i, batch in enumerate(batches, 1):
        payload = {"host": host, "key": key, "urlList": batch}
        if args.key_location:
            payload["keyLocation"] = args.key_location
        req = urllib.request.Request(args.endpoint, data=json.dumps(payload).encode("utf-8"), method="POST",
                                     headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": UA})
        try:
            resp = urllib.request.urlopen(req, timeout=args.timeout)
            code = resp.status
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:
            code = None
            print(f"  batch {i}: network error {type(e).__name__}: {e}")
        if code is not None:
            print(f"  batch {i}: HTTP {code} — {MEANING.get(code, 'see the engine documentation')}")
        if code not in (200, 202):
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
