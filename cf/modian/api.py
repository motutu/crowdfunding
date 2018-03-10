import json
import re
import urllib.parse

import arrow
import attrdict
import requests

from ..logger import logger, log_raw_response


APIBASE = 'https://zhongchou.modian.com/'


def parse_api_datetime(s):
    # API datetime format: ISO 8601 without timezone info, i.e., YYYY-MM-DD HH:MM:SS
    assert re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', s)
    return arrow.get(s + '+08:00')


def get(endpoint, params, *, logpath=None):
    params = params.copy()
    params['jsonpcallback'] = ''
    url = urllib.parse.urljoin(APIBASE, endpoint)
    logger.info('GET %s?%s', url, urllib.parse.urlencode(params))
    r = requests.get(url, params=params)
    assert r.status_code == 200
    m = re.match(r'^window\[decodeURIComponent\(\'\'\)\]\(\[(?P<json>.*)\]\);$', r.text)
    assert m
    obj = json.loads(m['json'])
    if logpath:
        log_raw_response(obj, 'modian/' + logpath)
    return attrdict.AttrDict(obj)
