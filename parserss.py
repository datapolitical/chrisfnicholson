import json
import sys

import feedparser
import requests

FEED_URL = "https://raindrop.io/collection/36448983/feed"
FIELDS = ("title", "link", "summary")


def main():
    try:
        r = requests.get(FEED_URL, timeout=30, allow_redirects=True)
        r.raise_for_status()
    except Exception as e:
        print("parserss: fetch failed:", repr(e))
        print("parserss: keeping existing _data/reads.json (if any)")
        return 1

    feed = feedparser.parse(r.content)
    if feed.bozo:
        print("parserss: parse warning:", repr(getattr(feed, "bozo_exception", None)))

    if not feed.entries:
        print("parserss: no entries in feed; keeping existing _data/reads.json")
        return 1

    entries = [{k: str(e.get(k, "")) for k in FIELDS} for e in feed.entries]
    with open("_data/reads.json", "w") as f:
        json.dump(entries, f, ensure_ascii=False, indent=1)
    print(f"parserss: wrote {len(entries)} entries to _data/reads.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
