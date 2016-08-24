import os
import re
import csv
import sys
import json


def main():
    csvout = csv.DictWriter(sys.stdout, fieldnames=[
        'date',
        'category',
        'tags',
        'provider',
        'comments',
        'title',
        'summary',
        'articleUrl',
        'imageUrl'
    ])

    csvout.writeheader()

    for a in list_articles():
        tags = extract_tags(a)
        if len(tags) == 0:
            continue

        csvout.writerow({
            'date': a['regDt'],
            'category': a['category'],
            'tags': '|'.join(tags),
            'provider': a['cpKorName'],
            'comments': a['ucccount'],
            'title': a['title'],
            'summary': a['summary'],
            'articleUrl': a['url'],
            'imageUrl': a['imageUrl'],
        })


def list_articles():
    for filename in os.listdir('../news-crawl/data/'):
        with open('../news-crawl/data/' + filename, 'r') as f:
            obj = json.load(f)
            yield from obj['bestreplyNewsList']


WHITELIST = (
    (['강간', '범죄'], r'(강간|윤간)'),
    (['낙태', '임신'], r'(낙태|중절)'),
    (['범죄', '성폭행', '폭행',], r'성폭행'),
)

def extract_tags(a):
    matching_tags = []
    for tags, pattern in WHITELIST:
        if re.search(pattern, '%s %s' % (a['title'], a['summary'])) is not None:
            matching_tags += tags
    return sorted(list(set(matching_tags)))


if __name__ == '__main__':
    main()
