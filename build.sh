#!/bin/bash

pwd
echo $PATH
export PATH = "/opt/buildhome/squashfs-root/usr/bin:$PATH"
mogrify -version
cd $HOME
wget --no-check-certificate "https://download.imagemagick.org/ImageMagick/download/binaries/magick"
chmod a+x magick
export MAGICK_HOME="/opt/buildhome/squashfs-root/usr"
export LD_LIBRARY_PATH=$MAGICK_HOME/lib:$LD_LIBRARY_PATH"
./magick --appimage-extract
echo "zero"
cd /opt/buildhome
ls -l
cd /opt/buildhome/repo
echo "one"
/opt/buildhome/squashfs-root/usr/bin/mogrify -version
echo "two"
mogrify -version
bundle exec jekyll build --destination gh-pages