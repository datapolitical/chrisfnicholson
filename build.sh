#!/bin/bash
#gem update --system --silent --no-document
gem install bundler --no-document
python3 -m pip install beautifulsoup4

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

python3 criticalCSSparser.py | openssl sha256 -binary | openssl base64
inline_hash_v3=$(python3 criticalCSSparser.py | openssl sha256 -binary | openssl base64)
#echo -n "$inline_hash"
#echo -n "$inline_hash_v2"
echo -n "hash text is === $inline_hash_v3_text"
echo -n "hash equals === $inline_hash_v3"
echo -n "'sha256-$inline_hash_v3' " >> _headers
echo -n "'self' 'report-sample';" >> _headers
cp _headers gh-pages/

