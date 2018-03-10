import json
import uuid

import attrdict
import requests
import urllib.parse

from ..logger import logger, log_raw_response


APIBASE = 'https://appo4.owhat.cn/api'


def post(cmd_m, cmd_s, data, *, logpath=None):
    deviceid = str(uuid.uuid4())
    client = json.dumps(dict(
        platform='ios',
        deviceid=str(uuid.uuid4()),
        channel='AppStore',
        version='4.4.4',
    ))
    payload = dict(
        client=client,
        cmd_m=cmd_m,
        cmd_s=cmd_s,
        data=json.dumps(data),
        v='1.0',
    )
    logger.info(f'POST {APIBASE} {urllib.parse.urlencode(payload)}')
    r = requests.post(APIBASE, data=payload)
    assert r.status_code == 200
    obj = r.json()
    if logpath:
        log_raw_response(obj, 'owhat/' + logpath)
    return attrdict.AttrDict(obj)
