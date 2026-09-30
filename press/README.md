# press — Chris Nicholson media coverage archive

Compiled 2026-09-30. Inventory of verified press coverage naming **Chris Nicholson, RTD Board Director, District A** (Denver).

## Files
- `press-inventory-chris-nicholson-2026-09-30.md` — the inventory: 82 listed items across 20 outlets; every item fetch-verified (mention counts + excerpts), plus a coverage-gaps section. `[n]` numbers match the citation ledger.
- `fetch_report.txt` — raw fetch log: per-article URL/date/mention counts/snippets for ~85 candidate articles.
- `final_urls.txt` — all 87 source URLs as registered in the ledger.
- `ledger.json` — citation ledger (canonical; ids match `[n]` refs in the inventory).
- `gen_dossier.py` — generator that (re)builds the inventory from the fetch log + ledger.
- `sync_raindrop.py` — syncs the ledger URLs into the Raindrop.io "press" collection. Dry run by default; `--apply` to write. (Token: `.secrets/raindrop.env`, gitignored — never commit.)

## Website integration (chrisfnicholson.com)
The collection's public feed (`https://datapolitical.raindrop.page/press-75641856/feed`) is pulled at build time by `../parserss.py` into `../_data/press.json`; the homepage renders the newest entries as "Recent Press" (`press_count` in `index.md` sets how many).
- Tag an item `exclude` in Raindrop to keep it off the site list — it stays in the archive. Currently excluded: Ballotpedia profile, Denver Post author page, the two op-ed reposts (Daily Camera, Mass Transit), SoS press release, 2024 forum video.
- Raindrop feeds are edge-cached; `parserss.py` cache-busts so builds always see the current feed.
- The feed carries at most 50 items, so the site list draws from the newest 50 only.

## Method
Publisher site searches + web search + Google News RSS sweep across Denver outlets (Denver Post, Westword, CPR, Denverite, Denver Gazette, Denver7, CBS Colorado, Axios Denver, Colorado Politics, Newsline, Longmont Times-Call / Daily Camera, trade press). Every candidate article was fetched and confirmed to name him before inclusion. Raw page captures (~20 MB) are held locally, not in this repo.

## Not included
Social media posts, advocacy pages, official RTD/government comms (Ballotpedia profile and the 2024 SoS press release are listed as adjacent references in the inventory).
