#!/bin/bash

pwd
echo $PATH
export PATH = "/opt/buildhome/squashfs-root/:$PATH"
mogrify -version
cd $HOME
wget --no-check-certificate "https://download.imagemagick.org/ImageMagick/download/binaries/magick"
chmod a+x magick
export MAGICK_HOME="/opt/buildhome/squashfs-root/"
./magick --appimage-extract
echo "zero"
cd /opt/buildhome
pwd
cd /opt/buildhome/repo
echo "one
/opt/buildhome/squashfs-root/mogrify -version
echo "two"
mogrify -version
bundle exec jekyll build --destination gh-pages