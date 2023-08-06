#!/bin/bash
#gem update --system --silent --no-document

gem install bundler --no-document

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
export PATH=$PATH:/opt/buildhome/.asdf/installs/python/3.11.4/bin
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


bundle exec jekyll build

echo "INLINE HASH"
/opt/buildhome/.asdf/installs/python/3.11.4/bin/inlinehashes gh-pages/index.html -o plain

python3 CSPwriter.py
cat _headers
cp _headers gh-pages/


