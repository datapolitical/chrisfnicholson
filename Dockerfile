FROM ubuntu:latest

LABEL version="2.0.1"
LABEL repository="https://github.com/helaili/jekyll-action"
LABEL homepage="https://github.com/helaili/jekyll-action"
LABEL maintainer="Alain Hélaïli <helaili@github.com>"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y build-essential && \
  apt-get install -y git && \
  apt-get install -y imagemagick && \
  apt-get install -y libmagickwand-dev && \
  apt-get install -y ruby && \
  apt-get install -y ruby-dev

RUN gem install rmagick
RUN gem install bundler

# debug
RUN bundle version
