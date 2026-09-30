import json
import sys
import time

import feedparser
import requests

FEEDS = (
    ("https://raindrop.io/collection/36448983/feed", "_data/reads.json"),
    ("https://datapolitical.raindrop.page/press-75641856/feed", "_data/press.json"),
)
FIELDS = ("title", "link", "summary")
EXCLUDE_TAG = "exclude"


def fetch_feed(feed_url, out_path):
    # Raindrop feeds sit behind an edge cache; the cache-busting parameter makes
    # every run see the feed's current version instead of a frozen copy.
    bust = ("&" if "?" in feed_url else "?") + f"_={int(time.time())}"
    try:
        r = requests.get(feed_url + bust, timeout=30, allow_redirects=True)
        r.raise_for_status()
    except Exception as e:
        print(f"parserss: fetch failed for {out_path}:", repr(e))
        print(f"parserss: keeping existing {out_path} (if any)")
        return False

    feed = feedparser.parse(r.content)
    if feed.bozo:
        print("parserss: parse warning:", repr(getattr(feed, "bozo_exception", None)))

    if not feed.entries:
        print(f"parserss: no entries for {out_path}; keeping existing file")
        return False

    entries, hidden = [], 0
    for e in feed.entries:
        tags = [t.get("term", "") for t in e.get("tags", [])]
        if EXCLUDE_TAG in tags:
            hidden += 1
            continue
        entry = {**{k: str(e.get(k, "")) for k in FIELDS}, "tags": tags}
        entries.append(entry)

    with open(out_path, "w") as f:
        json.dump(entries, f, ensure_ascii=False, indent=1)
    msg = f"parserss: wrote {len(entries)} entries to {out_path}"
    if hidden:
        msg += f" ({hidden} hidden by tag '{EXCLUDE_TAG}')"
    print(msg)
    return True


def main():
    ok = True
    for feed_url, out_path in FEEDS:
        if not fetch_feed(feed_url, out_path):
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
