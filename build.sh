#!/bin/bash

pwd
cd $HOME/bin
wget "https://download.imagemagick.org/ImageMagick/download/binaries/magick"
chmod a+x magick
./magick -version
cd /opt/buildhome
bundle exec jekyll build --destination gh-pages