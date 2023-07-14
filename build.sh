#!/bin/bash
#gem update --system --silent --no-document
whereis vips
whereis python3
vips -v
python3 --version
gem install bundler --no-document
python3 -m pip install --upgrade pip
python3 -m pip install beautifulsoup4
python3 -m pip install inlinehashes
export PATH=$PATH:/opt/buildhome/.asdf/installs/python/3.11.4/bin
source ~/.bashrc
mkdir -p gh-pages/assets/generated
cp -R _assets/generated/* gh-pages/assets/generated
bundle exec jekyll build
du -sh gh-pages
ls gh-pages
google_analytics="'sha256-7S8HHslrpUKGbGUmT/L2MgqW/dfTrlhZaY5GN8XhFqA='"
echo "/*" > _headers
echo "Report-To: {"group":"default","max_age":31536000,"endpoints":[{"url":"https://chrisfnicholson.report-uri.com/a/d/g"}],"include_subdomains":true}" >> _headers
echo -n "Content-Security-Policy-Report-Only: default-src 'none'; report-uri https://chrisfnicholson.report-uri.com/r/d/csp/reportOnly; report-to default; connect-src 'self' cloudflareinsights.com https://www.google-analytics.com www.google-analytics.com; img-src 'self'; base-uri 'self'; form-action https://chrisfnicholson-staticman.herokuapp.com 'self'; child-src crosshare.org; manifest-src 'self'; worker-src 'self'; script-src $google_analytics ajax.cloudflare.com static.cloudflareinsights.com 'self' 'report-sample'; font-src 'self';" >> _headers
echo -n "style-src " >> _headers
echo "INLINE HASH"
/opt/buildhome/.asdf/installs/python/3.11.4/bin/inlinehashes -h
/opt/buildhome/.asdf/installs/python/3.11.4/bin/inlinehashes gh-pages/index.html -o plain
echo "FOLDER opt"
ls /opt/buildhome/.asdf/installs/python/3.11.4/bin
python3 -m site --user-base
ls /opt/buildhome/.local/bin
echo $PATH
python3 criticalCSSparser.py | openssl sha256 -binary | openssl base64
inline_hash_v3=$(python3 criticalCSSparser.py | openssl sha256 -binary | openssl base64)
python3 CSPwriter.py
#echo -n "$inline_hash"
#echo -n "$inline_hash_v2"
echo -n "hash text is === $inline_hash_v3_text"
echo -n "hash equals === $inline_hash_v3"
echo -n "'sha256-$inline_hash_v3' " >> _headers
echo -n "'self' 'report-sample';" >> _headers
cp _headers gh-pages/

