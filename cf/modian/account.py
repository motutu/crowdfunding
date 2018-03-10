import argparse
import logging
import pathlib
import re

import bs4
import requests

from ..logger import logger
from ..project import Project


def parse_project_listing(html):
    soup = bs4.BeautifulSoup(html, 'html5lib')
    for proj in soup.select('.project'):
        link = proj.a['href']
        project_id = int(pathlib.Path(link).stem)
        title = proj.h4.text.strip()
        m = re.search(r'支持者：(?P<backers>\d+).*'
                      r'¥(?P<amount>[0-9,.]+)\s*已众筹.*',
                      proj.text, re.S)
        assert m
        backers = int(m['backers'])
        amount = float(m['amount'].replace(',', ''))
        yield Project('modian', project_id, link, title, None, None, amount, backers)


def fetch_project_listing(uid):
    url = f'https://me.modian.com/user?type=index&id={uid}'
    logger.info(f'GET {url}')
    r = requests.get(url)
    assert r.status_code == 200
    return parse_project_listing(r.text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('uid', help='user id of the creator')
    args = parser.parse_args()

    for project in fetch_project_listing(args.uid):
        print(project)


if __name__ == '__main__':
    main()
