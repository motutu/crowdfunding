import json
import re
import time
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
    ntries = 4
    for ntry in range(ntries):
        try:
            full_url = '%s?%s' % (url, urllib.parse.urlencode(params))
            logger.info('GET %s', full_url)
            r = requests.get(url, params=params, timeout=5)
            break
        except (OSError, requests.RequestException) as e:
            logger.error('GET %s: %s: %s', full_url, type(e), e)
            time.sleep(2 ** ntry)
    else:
        raise RuntimeError('GET %s: failed after %d tries', full_url, ntries)
    assert r.status_code == 200
    m = re.match(r'^window\[decodeURIComponent\(\'\'\)\]\(\[(?P<json>.*)\]\);$', r.text)
    assert m
    obj = json.loads(m['json'])
    if logpath:
        log_raw_response(obj, 'modian/' + logpath)
    return attrdict.AttrDict(obj)
