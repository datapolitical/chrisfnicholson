import json
import feedparser

feed = feedparser.parse("https://raindrop.io/collection/36448983/feed")

file=open("_data/reads.yaml","w")
json.dump(feed, file)
file.close()