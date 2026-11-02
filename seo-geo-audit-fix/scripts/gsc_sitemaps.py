#!/usr/bin/env python3
"""
gsc_sitemaps.py — list or submit sitemaps in Google Search Console with a service account.

Needs (not stdlib):  pip install --upgrade google-api-python-client google-auth

Credentials: the path to a Google Cloud service-account JSON key in the environment variable
GOOGLE_APPLICATION_CREDENTIALS. Never commit that file and never paste its content anywhere.

One-time setup:
  1. Google Cloud console: create (or pick) a project, enable the "Google Search Console API",
     create a service account and download a JSON key for it.
  2. Search Console → Settings → Users and permissions → Add user: the service account's
     e-mail (…@….iam.gserviceaccount.com). Permission: "Full" (or Owner) to submit sitemaps;
     "Restricted" is enough for `list`.
  3. export GOOGLE_APPLICATION_CREDENTIALS=/secure/path/service-account.json

Usage:
  python3 gsc_sitemaps.py list   --site sc-domain:example.com
  python3 gsc_sitemaps.py list   --site https://www.example.com/ --sitemap https://www.example.com/sitemap.xml
  python3 gsc_sitemaps.py submit --site sc-domain:example.com --sitemap https://www.example.com/sitemap.xml          # dry run
  python3 gsc_sitemaps.py submit --site sc-domain:example.com --sitemap https://www.example.com/sitemap.xml --apply  # submits

--site is the property exactly as Search Console names it: "sc-domain:example.com" for a Domain
property, or the URL-prefix with its trailing slash ("https://www.example.com/").
`list` is read-only (scope webmasters.readonly). `submit` changes the property and runs only
with --apply (scope webmasters). Re-submit only after a real change to the sitemap.
For indexed counts per sitemap use the Search Console UI (Sitemaps and Page indexing reports).
"""
import argparse
import os
import sys

PIP = "pip install --upgrade google-api-python-client google-auth"
SCOPE_RO = "https://www.googleapis.com/auth/webmasters.readonly"
SCOPE_RW = "https://www.googleapis.com/auth/webmasters"


def load_libs():
    try:
        from google.oauth2 import service_account  # noqa: F401
        from googleapiclient.discovery import build  # noqa: F401
        from googleapiclient.errors import HttpError  # noqa: F401
    except ImportError:
        print("Missing libraries. Install them with:\n  " + PIP, file=sys.stderr)
        sys.exit(3)
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    return service_account, build, HttpError


def service(scope):
    path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
    if not path or not os.path.isfile(path):
        print("ERROR: set GOOGLE_APPLICATION_CREDENTIALS to the service-account JSON key file path.", file=sys.stderr)
        sys.exit(2)
    service_account, build, HttpError = load_libs()
    creds = service_account.Credentials.from_service_account_file(path, scopes=[scope])
    print(f"Service account: {creds.service_account_email}")
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False), HttpError


def explain(err, site):
    status = getattr(getattr(err, "resp", None), "status", None)
    if status in (401, 403):
        print(f"HTTP {status}: the service account has no access to {site!r}. Add its e-mail in Search Console → "
              "Settings → Users and permissions (Full or Owner to submit; Restricted to list), and check that "
              "--site matches the property name exactly.", file=sys.stderr)
    elif status == 404:
        print(f"HTTP 404: property or sitemap not found for {site!r}.", file=sys.stderr)
    else:
        print(f"API error: {err}", file=sys.stderr)


def cmd_list(args):
    svc, HttpError = service(SCOPE_RO)
    try:
        if args.sitemap:
            items = [svc.sitemaps().get(siteUrl=args.site, feedpath=args.sitemap).execute()]
        else:
            items = svc.sitemaps().list(siteUrl=args.site).execute().get("sitemap", [])
    except HttpError as e:
        explain(e, args.site)
        return 1
    if not items:
        print("No sitemaps submitted for this property.")
        return 0
    print(f"| Sitemap | Index? | Last submitted | Last downloaded | Pending | Errors | Warnings | Submitted URLs |")
    print("|---|---|---|---|---|---|---|---|")
    for s in items:
        submitted = sum(int(c.get("submitted", 0) or 0) for c in s.get("contents", []))
        print(f"| {s.get('path')} | {s.get('isSitemapsIndex', False)} | {s.get('lastSubmitted', '—')} | "
              f"{s.get('lastDownloaded', '—')} | {s.get('isPending', False)} | {s.get('errors', 0)} | "
              f"{s.get('warnings', 0)} | {submitted} |")
    return 0


def cmd_submit(args):
    if not args.sitemap:
        print("ERROR: submit needs --sitemap URL.", file=sys.stderr)
        return 2
    if not args.apply:
        print("Dry run — nothing sent.")
        print(f"  would call: sitemaps.submit(siteUrl={args.site!r}, feedpath={args.sitemap!r})")
        print(f"  HTTP: PUT https://www.googleapis.com/webmasters/v3/sites/<siteUrl>/sitemaps/<feedpath> (scope {SCOPE_RW})")
        print("  Re-run with --apply after the owner approves.")
        return 0
    svc, HttpError = service(SCOPE_RW)
    try:
        svc.sitemaps().submit(siteUrl=args.site, feedpath=args.sitemap).execute()
        s = svc.sitemaps().get(siteUrl=args.site, feedpath=args.sitemap).execute()
    except HttpError as e:
        explain(e, args.site)
        return 1
    print(f"Submitted. lastSubmitted={s.get('lastSubmitted')} isPending={s.get('isPending')} "
          f"errors={s.get('errors', 0)} warnings={s.get('warnings', 0)}")
    print("Check the Sitemaps report the next day for the fetch status.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["list", "submit"], help="list (read-only) or submit (needs --apply)")
    ap.add_argument("--site", required=True, help='Property: "sc-domain:example.com" or "https://www.example.com/"')
    ap.add_argument("--sitemap", help="Sitemap URL (required for submit; optional filter for list)")
    ap.add_argument("--apply", action="store_true", help="Actually submit (default: dry run)")
    args = ap.parse_args()
    return cmd_list(args) if args.command == "list" else cmd_submit(args)


if __name__ == "__main__":
    sys.exit(main())
