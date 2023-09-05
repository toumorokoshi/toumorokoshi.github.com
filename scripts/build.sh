#!/usr/bin/env bash
set -e
./scripts/download-blog-from-gdrive.sh
npm install -g @mermaid-js/mermaid-cli
bundle exec jekyll build