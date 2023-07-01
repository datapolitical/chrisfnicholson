#!/bin/bash
#gem update --system --silent --no-document
gem install bundler --no-document
gem install nokogiri
python3 -m pip install beautifulsoup4
go get github.com/ericchiang/pup
sudo apt install cargo
cargo install htmlq
export PATH="$PATH:$HOME/.cargo/bin"
# gem install ffi -- --disable-system-libffi
# mkdir assets/css/
# touch assets/css/generated-critical.css
mkdir -p gh-pages/assets/generated
cp -R _assets/generated/* gh-pages/assets/generated
bundle exec jekyll build
pwd
ls
# npm i crittr
# node contrast_theme_node.js
# bundle exec jekyll build
# wget https://ajax.cloudflare.com/cdn-cgi/scripts/cloudflare-static/rocket-loader.min.js
# rocket_hash=$(echo `cat rocket-loader.min.js` | openssl dgst -binary -sha256 | base64)
# rocket_hash="'sha256-7S8HHslrpUKGbGUmT/L2MgqW/dfTrlhZaY5GN8XhFqA='"
google_analytics="'sha256-7S8HHslrpUKGbGUmT/L2MgqW/dfTrlhZaY5GN8XhFqA='"
echo "/*" > _headers
echo "Report-To: {"group":"default","max_age":31536000,"endpoints":[{"url":"https://chrisfnicholson.report-uri.com/a/d/g"}],"include_subdomains":true}" >> _headers
echo -n "Content-Security-Policy-Report-Only: default-src 'none'; report-uri https://chrisfnicholson.report-uri.com/r/d/csp/reportOnly; report-to default; connect-src 'self' cloudflareinsights.com https://www.google-analytics.com www.google-analytics.com; img-src 'self'; base-uri 'self'; form-action https://chrisfnicholson-staticman.herokuapp.com 'self'; child-src crosshare.org; manifest-src 'self'; worker-src 'self'; script-src $google_analytics ajax.cloudflare.com static.cloudflareinsights.com 'self' 'report-sample'; font-src 'self';" >> _headers
echo -n "style-src " >> _headers
#inline_hash=$(echo `cat gh-pages/index.html | hxselect -i -c style | shasum -a 256 | cut -d' ' -f1 | xxd -r -p | base64`)
#inline_hash_v2=$(echo `cat gh-pages/index.html | hxselect -i -c style | openssl sha256 -binary | openssl base64`)
python3 criticalCSSparser.py
echo -n `cat gh-pages/index.html | htmlq --attribute style.[0]`
cat gh-pages/index.html | pup 'style:first-of-type'
echo "nokogiri raw output"
cat gh-pages/index.html | nokogiri -e 'puts $_.css("style")[0].text'
inline_hash_v3_text=$(echo -n `cat gh-pages/index.html | nokogiri -e 'puts $_.css("style")[0].text'`)
inline_hash_v3=$(echo -n `echo -n "$inline_hash_v3_text" | openssl sha256 -binary | openssl base64`)
#echo -n "$inline_hash"
#echo -n "$inline_hash_v2"
echo -n "hash text is === $inline_hash_v3_text"
echo -n "hash equals === $inline_hash_v3"
echo -n "'sha256-$inline_hash_v3' " >> _headers
echo -n "'self' 'report-sample';" >> _headers
cp _headers gh-pages/
