import json
import feedparser

feed = feedparser.parse("https://raindrop.io/collection/36448983/feed")

print(json.dumps(feed, indent=1))

file=open("_data/reads.json","w")
json.dump(feed.entries, file)
file.close()