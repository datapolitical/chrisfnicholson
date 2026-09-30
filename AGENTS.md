# Agent notes — chrisfnicholson.com

## Deploy chain (verified 2026-09-30)
- **Pushing to `main` deploys the site.** Builds run via **Cloudflare Pages git integration** (project `chrisfnicholson`; domains chrisfnicholson.com + www). No local deploy step.
- The GitHub workflow `.github/workflows/new_build_jekyll.yml` ("Update External Data and Release") is **disabled_manually** — it is NOT the deploy path. `gh run list` shows nothing for deploys; don't use it to check.
- Cloudflare builds are **serialized** (one at a time) and take several minutes each; a push queues a build and production (`www`) flips a few minutes later. The `rebuild:`-prefixed commits are deliberate deploy triggers.
- Verify a deploy: `npx wrangler pages deployment list --project-name=chrisfnicholson` (Source column = commit; a deployment URL 404s until its build finishes) — or just curl the live page for the change.
- Build config runs `./build.sh` → pip install -r requirements.txt → python data scripts → Jekyll build.

## Data pipelines
- `parserss.py` pulls the public Raindrop feeds (reads + press) into `_data/reads.json` / `_data/press.json`, cache-busted; items tagged `exclude` are filtered out.
- The press collection pipeline (sync script, curation tags, feed cap) is documented in `press/README.md`.

## Site serving
- Repo files are copied into the built site unless listed under `exclude:` in `_config.yml` — working files (`AGENTS.md`, `press/`, `python/`, `disabled_functions/`, scripts) are excluded; `.secrets/` never reaches the build (gitignored). Check any path with curl: the 404 page means it's not served.
