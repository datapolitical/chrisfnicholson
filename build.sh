#!/bin/bash
#gem update --system --silent --no-document

gem install bundler --no-document

python3 -m pip install --upgrade pip
python3 -m pip install inlinehashes
python3 -m pip install feedparser
export PATH=$PATH:/opt/buildhome/.asdf/installs/python/3.11.4/bin
source ~/.bashrc
mkdir -p gh-pages/assets/generated
cp -R _assets/generated/* gh-pages/assets/generated

python3 parserss.py

bundle exec jekyll build

echo "INLINE HASH"
/opt/buildhome/.asdf/installs/python/3.11.4/bin/inlinehashes gh-pages/index.html -o plain

python3 CSPwriter.py
cat _headers
cp _headers gh-pages/


