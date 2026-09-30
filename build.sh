#!/bin/bash
#gem update --system --silent --no-document

gem install bundler --no-document

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
PYDIR="$(dirname "$(command -v python3)")"
export PATH=$PATH:$PYDIR
source ~/.bashrc
mkdir -p gh-pages/assets/generated
cp -R _assets/generated/* gh-pages/assets/generated

python3 parserss.py
python3 -m papexp
python3 -m mndexp
mv recent_food.yml _data/recent_food.yml
mv steps.yml _data/steps.yml
md5sum _data/recipes.yaml > recipes.md5
md5sum _data/recent_food.yml > recent_food.md5
md5sum _data/reads.json > reads.md5

bundle exec jekyll build > /tmp/jekyll_build.log 2>&1
JEKYLL_EXIT=$?
echo "=== jekyll exit: $JEKYLL_EXIT ==="
if [ $JEKYLL_EXIT -ne 0 ]; then
  echo "=== Jekyll failed; last 100 lines of its output ==="
  tail -n 100 /tmp/jekyll_build.log
  echo "=== ABORTING build; production keeps the last good deployment ==="
  exit 1
fi
MISSING=0
for f in index.html sitemap.xml feed.xml; do
  if [ ! -f "gh-pages/$f" ]; then
    echo "=== BUILD SANITY FAILED: gh-pages/$f missing after a successful jekyll run ==="
    MISSING=1
  fi
done
if [ $MISSING -ne 0 ]; then
  echo "=== gh-pages top level ==="
  ls gh-pages | head -40
  echo "=== ABORTING build; production keeps the last good deployment ==="
  exit 1
fi
echo "jekyll: $(tail -n 2 /tmp/jekyll_build.log | head -n 1)"
rm -f /tmp/jekyll_build.log

echo "INLINE HASH"
"$PYDIR/inlinehashes" gh-pages/index.html -o plain

python3 CSPwriter.py
cat _headers
cp _headers gh-pages/
