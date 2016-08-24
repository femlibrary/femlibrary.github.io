#!/usr/bin/env bash
if which pyenv > /dev/null 2> /dev/null; then eval "$(pyenv init -)"; fi
pyenv activate femlibrary

echo "Crawling news..."
cd ../news-crawl
git pull
python crawl.py

