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
    (['강간', '범죄',], r'(강간|윤간)'),
    (['낙태', '임신', '산부인과'], r'(낙태|중절)'),
    (['범죄', '성폭행', '폭행',], r'(성폭행)'),
    (['메갈리안', '커뮤니티',], r'(메갈리안|메갈리아|메갈)'),
    (['몰카', '범죄',], r'(몰카|몰래\s*카메라|도촬)'),
    (['생리', '산부인과',], r'(생리|월경)'),
    (['성매매',], r'(성매매|집창촌|윤락가|윤락녀|윤락여성|매춘|단란주점)'),
    (['성폭력', '범죄',], r'(성폭력)'),
    (['성폭행', '범죄',], r'(성폭행)'),
    (['성추행', '범죄',], r'(성추행)'),
    (['성희롱', '범죄',], r'(성희롱)'),
    (['소라넷', '커뮤니티', '범죄', '여성혐오',], r'(소라넷)'),
    (['여성혐오',], r'(미소지니|misogyny|여성\s*혐오|..녀)'),
    (['육아',], r'(육아|모유|보육|기저귀|이유식|태아)'),
    (['일베', '커뮤니티', '여성혐오'], r'(일베|일간\s*베스트|베충)'),
    (['인권',], r'(인권|기본권)'),
    (['임신', '산부인과',], r'(임신|산후)'),
    (['차별'], r'(성차별|유리\s*천장|남녀차별)'),
    (['추행',], r'(추행)'),
    (['페미니즘',], r'(페미니즘|여성주의)'),
    (['피임', '산부인과',], r'(피임|콘돔)'),
    (['혐오',], r'(혐오)'),
)

def extract_tags(a):
    matching_tags = []
    for tags, pattern in WHITELIST:
        if re.search(pattern, '%s %s' % (a['title'], a['summary'])) is not None:
            matching_tags += tags
    return sorted(list(set(matching_tags)))


if __name__ == '__main__':
    main()
