#!/usr/bin/env bash
bash -c "sleep 5 && xdg-open http://localhost:4000" &
exec bundle exec jekyll serve