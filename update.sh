#!/usr/bin/env bash
if which pyenv > /dev/null 2> /dev/null; then eval "$(pyenv init -)"; fi
pyenv activate femlibrary

echo "Crawl news..."
cd ../news-crawl
git pull
python crawl.py

echo "Categorize..."
cd ../femlibrary-src
git pull
python json2csv.py > _data/news.csv

echo "Download books..."
wget "https://docs.google.com/spreadsheets/d/1N9sUaBOqTMRzzecl5RHiBLUEBf9wJ-SjGkb3dtPNdr8/export?format=csv&id=1N9sUaBOqTMRzzecl5RHiBLUEBf9wJ-SjGkb3dtPNdr8&gid=270197918" --no-check-certificate -q -O _data/books.csv

echo "Generate site..."
jekyll b

echo "Push..."
cd ../femlibrary.github.io
git pull
cp -r ../femlibrary-src/_site/* .
git add .
git commit -m "Update news"
git push

cd ../femlibrary-src
echo "Done!"

