#!/bin/bash

pwd
echo $PATH
#!export PATH = "/opt/buildhome/squashfs-root/usr/bin:$PATH"
sudo apt-get install fuse
mogrify -version
cd $HOME
wget --no-check-certificate "https://download.imagemagick.org/ImageMagick/download/binaries/magick"
chmod a+x magick
./magick --version
echo "zero"
ls -l
cd /opt/buildhome/repo
bundle exec jekyll build --destination gh-pages