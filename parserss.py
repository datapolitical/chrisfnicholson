import yaml
import feedparser

feed = feedparser.parse("https://raindrop.io/collection/36448983/feed")

file=open("_/data/reads.yaml","w')
yaml.dump(feed, file)
file.close()