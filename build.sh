#!/bin/bash

gem install bundler:2.3.4
bundle exec jekyll build
echo "/*" > _headers
echo -n "Content-Security-Policy-Report-Only: default-src 'none'; connect-src 'self' cloudflareinsights.com https://www.google-analytics.com www.google-analytics.com; img-src 'self'; base-uri 'self'; form-action https://chrisfnicholson-staticman.herokuapp.com 'self'; child-src crosshare.org; manifest-src 'self'; worker-src 'self'; font-src 'self';" >> _headers
echo -n "style-src " >> _headers
inline_hash=$(echo `cat gh-pages/assets/css/generated-critical.css` | openssl dgst -binary -sha256 | base64)
echo -n "'sha256-$inline_hash' " >> _headers
echo -n "'self';" >> _headers
cp _headers gh-pages/
