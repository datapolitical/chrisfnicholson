#!/usr/bin/env python3
"""Sync the verified press archive into a Raindrop.io collection.

Source of truth : ledger.json     (canonical citation ledger; see README.md)
Dates           : fetch_report.txt + press-inventory-*.md + URL patterns.
                  Each bookmark's date is set to the article's publication date
                  (and manual sort order = newest first), so the collection
                  reads chronologically with most recent coverage on top.
Credential      : .secrets/raindrop.env  ->  RAINDROP_TOKEN=<Raindrop API token>

Usage:
  python3 sync_raindrop.py                      # dry run: show the plan, write nothing
  python3 sync_raindrop.py --apply              # create collection + add missing bookmarks
  python3 sync_raindrop.py --collection press   # target a different collection title

Idempotent: bookmarks already in the target collection (matched by normalized
URL) are skipped, so re-running after ledger.json grows only inserts the new
items. The token is read from disk and never printed.
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.raindrop.io/rest/v1"
HERE = Path(__file__).resolve().parent
LEDGER = HERE / "ledger.json"
ENVFILE = HERE / ".secrets" / "raindrop.env"
TAGS = ["press"]
TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid", "igshid"}
MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def load_token() -> str:
    if not ENVFILE.is_file():
        sys.exit(f"error: {ENVFILE} not found — see .secrets/README.md")
    for line in ENVFILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        if key.strip() == "RAINDROP_TOKEN":
            value = value.strip().strip("'\"")
            if value:
                return value
    sys.exit(f"error: RAINDROP_TOKEN missing or empty in {ENVFILE}")


def request(token: str, method: str, path: str, body=None) -> dict:
    url = f"{API}/{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("User-Agent", "press-sync/1.0 (chrisfnicholson press archive)")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    last_err = None
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode())
            if isinstance(payload, dict) and payload.get("result") is False:
                sys.exit(f"error: API refused {method} /{path}: {payload.get('errorMessage') or payload}")
            return payload
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:300]
            if e.code == 429:
                wait = 15 * attempt
                print(f"rate limited; sleeping {wait}s ...")
                time.sleep(wait)
            elif e.code >= 500:
                time.sleep(3 * attempt)
            else:
                sys.exit(f"error: HTTP {e.code} on {method} /{path}: {detail}")
            last_err = f"HTTP {e.code}: {detail}"
        except OSError as e:
            reason = getattr(e, "reason", e)
            time.sleep(3 * attempt)
            last_err = f"network error: {reason}"
    sys.exit(f"error: giving up on {method} /{path} ({last_err})")


def normalize(url: str) -> str:
    """Canonical form for comparison: no www, no fragment, no tracking params, no trailing slash."""
    parts = urllib.parse.urlsplit(url.strip())
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    query = [
        (k, v)
        for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
        if not k.startswith("utm_") and k not in TRACKING_KEYS
    ]
    path = re.sub(r"/+$", "", parts.path) or "/"
    return urllib.parse.urlunsplit((parts.scheme.lower(), host, path, urllib.parse.urlencode(query), ""))


def url_date(url: str):
    """Publication date guess from URL patterns: /YYYY/MM/DD/, month-name slugs, SoS PR files."""
    m = re.search(r"/((?:19|20)\d{2})/(\d{1,2})/(\d{1,2})(?:/|$)", url)
    if m:
        y, mo, d = m.groups()
        if 1 <= int(mo) <= 12 and 1 <= int(d) <= 31:
            return f"{y}-{int(mo):02d}-{int(d):02d}"
    m = re.search(r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[- ](\d{1,2})[- ,]+((?:19|20)\d{2})", url, re.I)
    if m and m.group(1).lower()[:3] in MONTHS:
        return f"{m.group(3)}-{MONTHS[m.group(1).lower()[:3]]:02d}-{int(m.group(2)):02d}"
    m = re.search(r"PR((?:19|20)\d{2})(\d{2})(\d{2})", url)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return None


def parse_dates() -> dict:
    """Map normalized URL -> 'YYYY-MM-DD' publication date, from the fetch log and the inventory."""
    dates = {}
    report = HERE / "fetch_report.txt"
    if report.is_file():
        pending = None
        for line in report.read_text(encoding="utf-8").splitlines():
            if line.startswith("### "):
                parts = [p.strip() for p in line[4:].split("|")]
                pending = parts[1] if len(parts) > 1 else None
            elif pending and line.strip().startswith("URL:"):
                u = line.split("URL:", 1)[1].strip()
                if re.fullmatch(r"\d{4}-\d{2}-\d{2}", pending):
                    dates.setdefault(normalize(u), pending)
                pending = None
    inventories = sorted(HERE.glob("press-inventory-*.md"))
    if inventories:
        for line in inventories[-1].read_text(encoding="utf-8").splitlines():
            m = re.match(r"- \*\*([^*]+)\*\*\s*·.*?\]\((https?://[^)]+)\)", line)
            if not m:
                continue
            raw, url = m.group(1).strip(), m.group(2)
            d = None
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
                d = raw
            else:
                mm = re.match(r"([A-Za-z]+)\s+(\d{4})", raw)
                if mm and mm.group(1).lower() in MONTHS:
                    d = f"{mm.group(2)}-{MONTHS[mm.group(1).lower()]:02d}-01"
            if d:
                dates.setdefault(normalize(url), d)
    return dates


def load_ledger(dates: dict):
    """Return (items, dated, undated); items carry date + manual sort order (newest first)."""
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    items, seen = [], set()
    for src in data.get("sources") or []:
        url = (src.get("url") or "").strip()
        if not url.lower().startswith(("http://", "https://")):
            continue
        key = normalize(url)
        if key in seen:
            continue
        seen.add(key)
        items.append({"id": src.get("id"), "url": url, "date": dates.get(key) or url_date(url)})
    dated = sorted((it for it in items if it["date"]), key=lambda it: it["date"], reverse=True)
    undated = [it for it in items if not it["date"]]
    for i, it in enumerate(dated + undated):
        it["order"] = i
    return items, dated, undated


def find_collection(token: str, name: str):
    name_l = name.strip().lower()
    for endpoint in ("collections", "collections/childrens"):
        payload = request(token, "GET", endpoint)
        for col in payload.get("items") or []:
            if (col.get("title") or "").strip().lower() == name_l:
                return col.get("_id")
    return None


def list_collection(token: str, cid):
    out, page = [], 0
    while True:
        payload = request(token, "GET", f"raindrops/{cid}?perpage=50&page={page}")
        page_items = payload.get("items") or []
        out.extend(page_items)
        if len(page_items) < 50:
            return out
        page += 1


def collection_links(token: str, cid):
    return {normalize(i["link"]) for i in list_collection(token, cid) if i.get("link")}


def mk_item(item, cid):
    obj = {
        "link": item["url"],
        "collection": {"$id": cid},
        "tags": TAGS,
        "order": item["order"],
        "pleaseParse": {},
    }
    if item.get("date"):
        obj["created"] = f"{item['date']}T12:00:00.000Z"  # noon UTC = same calendar day in Denver
    return obj


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="actually write to Raindrop (default: dry run)")
    ap.add_argument("--collection", default="press", help="target collection title (default: press)")
    args = ap.parse_args()

    token = load_token()
    dates = parse_dates()
    items, dated, undated = load_ledger(dates)
    if not items:
        sys.exit("error: no usable URLs found in ledger.json")
    print(f"ledger: {len(items)} unique URLs — {len(dated)} dated, {len(undated)} without a date")
    if dated:
        print(f"date range: {dated[-1]['date']} .. {dated[0]['date']} (oldest .. newest)")
    for it in undated:
        print(f"  undated: #{it['id']} {it['url']}")

    cid = find_collection(token, args.collection)
    if cid is None:
        print(f"collection '{args.collection}': not found (will be created)")
        pending = items
    else:
        print(f"collection '{args.collection}': id {cid}")
        seen = collection_links(token, cid)
        pending = [it for it in items if normalize(it["url"]) not in seen]
        print(f"already in collection: {len(items) - len(pending)}; to add: {len(pending)}")

    if not pending:
        print("nothing to do.")
        return

    pending.sort(key=lambda it: it["date"] or "0000", reverse=True)

    if not args.apply:
        action = (
            f"create collection '{args.collection}' and add {len(pending)} bookmarks"
            if cid is None
            else f"add {len(pending)} bookmarks"
        )
        print(f"\nDRY RUN — would {action} (newest first):")
        for it in pending[:5]:
            print(f"  #{it['id']:>3}  {it['date'] or '(no date)':<10}  {it['url']}")
        if len(pending) > 5:
            print(f"  ... and {len(pending) - 5} more")
        print("\nre-run with --apply to execute")
        return

    if cid is None:
        cid = request(token, "POST", "collection", {"title": args.collection})["item"]["_id"]
        print(f"created collection '{args.collection}' (id {cid})")

    # Probe one item first to confirm batch collection targeting works as documented.
    probe = pending[0]
    probe_resp = request(token, "POST", "raindrops", {"items": [mk_item(probe, cid)]})
    landed = False
    for _ in range(3):
        time.sleep(1.5)
        if normalize(probe["url"]) in collection_links(token, cid):
            landed = True
            break
    if landed:
        rest = pending[1:]
        if rest:
            request(token, "POST", "raindrops", {"items": [mk_item(it, cid) for it in rest]})
        print(f"added {len(pending)} bookmarks")
    else:
        print("probe did not land in the target collection; falling back to single-item adds")
        stray = (probe_resp.get("items") or [{}])[0].get("_id")
        if stray:
            request(token, "DELETE", f"raindrop/{stray}")
        for i, it in enumerate(pending, 1):
            request(token, "POST", "raindrop", mk_item(it, cid))
            if i % 20 == 0:
                print(f"  added {i}/{len(pending)}")
            time.sleep(0.65)
        print(f"added {len(pending)} bookmarks (single mode)")

    final = list_collection(token, cid)
    links = {normalize(i["link"]) for i in final if i.get("link")}
    missing = [it for it in items if normalize(it["url"]) not in links]
    createds = sorted(i["created"] for i in final if i.get("created"))
    print(f"verify: '{args.collection}' now holds {len(links)} bookmarks; {len(missing)} ledger URL(s) missing")
    if createds:
        print(f"created-date range in collection: {createds[0]} .. {createds[-1]}")
    print(f"collection URL: https://app.raindrop.io/collection/{cid}")
    if missing:
        for it in missing[:10]:
            print(f"  missing #{it['id']}  {it['url']}")
        sys.exit(1)
    print("done. re-running this script is safe (idempotent).")


if __name__ == "__main__":
    main()
