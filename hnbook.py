#!/usr/bin/env python3

# https://github.com/HackerNews/API

'''
Script gets list of recommended books in a HN story
'''

import argparse
import html
import requests
import logging

url = 'https://hacker-news.firebaseio.com/v0/item/{0}.json?print=pretty' # NOQA
SITE_URL = 'https://news.ycombinator.com/item?id={0}'

# https://news.ycombinator.com/item?id=14477851
# story = requests.get(url.format('13967350')).json()

logging.basicConfig(level=logging.DEBUG)
rq_log = logging.getLogger('requests')
rq_log.setLevel(logging.ERROR)

logger = logging.getLogger(__name__)


def get_books(story_id):
    story = requests.get(url.format(story_id)).json()
    fo = open('/tmp/hnbooks.txt', 'w')

    for comment_item in story['kids'][:-1]:
        item_url = url.format(comment_item)
        logger.debug(
            'Parsing comment: %s, API: %s',
            SITE_URL.format(comment_item), item_url
        )
        data = requests.get(item_url).json()
        user = data.get('by')
        s = data.get('text', '')
        s = s.replace('Mr.', 'Mr').replace('Mrs.', 'Mrs')
        sentences = s.split('.')
        books = [html.unescape(s.strip('<p>'))
                 for s in sentences if " by " in s]
        if not books:
            books = [html.unescape(sentences[0])]

        for book in books:
            logger.info('By %s: %s', user, book)
        fo.write('\n'.join(books) + '\n')


def main():
    import sys
    sys.argv.append('14477851')
    argp = argparse.ArgumentParser()
    argp.add_argument('StoryID', type=str, default='14477851')
    args = argp.parse_args()
    print(args)

    get_books(args.StoryID)
    print("See result in /tmp/hnbooks.txt")


if __name__ == "__main__":
    main()
