#!/usr/bin/env bash
./scripts/download-blog-from-gdrive.sh
npm install -g mermaid.cli
bundle exec jekyll build