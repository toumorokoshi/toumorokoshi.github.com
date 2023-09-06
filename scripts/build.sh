#!/usr/bin/env bash
set -ex
pip install google-api-python-client
pip install google-auth
python ./scripts/download-blog-from-gdrive-2.py
npm install -g @mermaid-js/mermaid-cli
bundle install
bundle exec jekyll build
exit 0