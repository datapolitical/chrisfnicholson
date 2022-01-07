#!/bin/bash

gem install bundler:2.3.4
bundle exec jekyll build
cp _headers gh-pages/
