#!/bin/bash

pwd
echo $PATH
mogrify -version
sudo apt-get install fuse
cd $HOME
wget --no-check-certificate "https://download.imagemagick.org/ImageMagick/download/binaries/magick"
chmod a+x magick
./magick -version
cd /opt/buildhome/repo
bundle exec jekyll build --destination gh-pages