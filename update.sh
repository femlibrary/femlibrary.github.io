#!/usr/bin/env bash
if which pyenv > /dev/null 2> /dev/null; then eval "$(pyenv init -)"; fi
pyenv activate femlibrary

echo "Crawl..."
cd ../news-crawl
git pull
python crawl.py

echo "Categorize..."
cd ../femlibrary-src
git pull
python json2csv.py > _data/news.csv

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

