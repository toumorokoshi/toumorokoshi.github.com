#!/usr/bin/env bash
set -e
pip install google-api-python-client
pip install google-auth
python ./scripts/download-blog-from-gdrive-2.py
npm install -g @mermaid-js/mermaid-cli
bundle exec jekyll build