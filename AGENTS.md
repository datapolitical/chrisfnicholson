# Agent notes — chrisfnicholson.com

## Deploy chain (verified 2026-09-30)
- **Pushing to `main` deploys the site.** Builds run via **Cloudflare Pages git integration** (project `chrisfnicholson`; domains chrisfnicholson.com + www). No local deploy step.
- The GitHub workflow `.github/workflows/new_build_jekyll.yml` ("Update External Data and Release") is **disabled_manually** — it is NOT the deploy path. `gh run list` shows nothing for deploys; don't use it to check.
- Cloudflare builds are **serialized** (one at a time); a push queues a build and production (`www`) flips a few minutes later (~30 min under load). The `rebuild:`-prefixed commits are deliberate deploy triggers.
- Verify a deploy: wrangler needs Node ≥22 on this box — `~/.nvm/versions/node/v24.13.1/bin/node ~/.npm/_npx/*/node_modules/wrangler/bin/wrangler.js pages deployment list --project-name=chrisfnicholson` (plain `npx wrangler` fails: the repo package.json pins an uninstalled version). Fastest tell: the page source comment `site: <sha>` matches the pushed commit once the build has flipped.
- Build config runs `./build.sh` → pip install -r requirements.txt → python data scripts → Jekyll build.

## Data pipelines
- `parserss.py` pulls the public Raindrop feeds (reads + press) into `_data/reads.json` / `_data/press.json`, cache-busted; items tagged `exclude` are filtered out.
- The press collection pipeline (sync script, curation tags, feed cap) is documented in `press/README.md`.

## Site serving
- Repo files are copied into the built site unless listed under `exclude:` in `_config.yml` — working files (`AGENTS.md`, `press/`, `python/`, `disabled_functions/`, scripts) are excluded; `.secrets/` never reaches the build (gitignored). Check any path with curl: missing paths serve a fallback copy of the homepage, so if the response isn't the file's own content, it's not served.
