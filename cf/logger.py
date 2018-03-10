import json
import logging
import pathlib
import time

from . import config


logging.basicConfig(
    format='[%(levelname)s] %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger('crowdfunding')


HERE = pathlib.Path(__file__).resolve().parent
RAWDIR = config.datadir() / 'raw'
RAWDIR.mkdir(exist_ok=True, parents=True)


def log_raw_response(obj, reldir):
    timestamp_ms = int(time.time() * 1000)
    directory = RAWDIR.joinpath(reldir)
    directory.mkdir(exist_ok=True, parents=True)
    with open(directory / f'{timestamp_ms}.json', 'w', encoding='utf-8') as fp:
        json.dump(obj, fp, ensure_ascii=False, indent=2)
