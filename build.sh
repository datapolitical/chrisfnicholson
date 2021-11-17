#!/bin/bash

pwd
echo $PATH
mogrify -version
cd $HOME
wget --no-check-certificate "https://download.imagemagick.org/ImageMagick/download/binaries/magick"
chmod a+x magick
export MAGICK_HOME="/opt/buildhome"
./magick --appimage-extract
cd /opt/buildhome/repo
bundle exec jekyll build --destination gh-pages