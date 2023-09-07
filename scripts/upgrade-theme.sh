#!/usr/bin/env bash
# upgrade the minima theme
rm -rf /tmp/minima
git clone https://github.com/jekyll/minima.git /tmp/minima
for dir in "_includes" "_layouts" "_sass" "assets"
do
    cp -r /tmp/minima/$dir/* $dir
done
# files to keep because they're heavily modified
git checkout _includes/disqus_comments.html
git checkout _includes/header.html
git checkout _includes/footer.html
git checkout _layouts/post.html