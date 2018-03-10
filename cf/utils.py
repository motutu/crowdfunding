import json
import multiprocessing.pool

import arrow


MAXJOBS = 16


def pool_starmap(func, iterable, chunksize=1):
    argslist = list(iterable)
    if not argslist:
        return []
    with multiprocessing.pool.Pool(min(len(argslist), MAXJOBS)) as pool:
        return pool.starmap(func, argslist, chunksize=chunksize)


class ExtendedJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, arrow.Arrow):
            return o.to('Asia/Shanghai').isoformat()
        else:
            return super().default(o)


def dump_json(obj, path):
    with open(path, 'w', encoding='utf-8') as fp:
        json.dump(obj, fp, cls=ExtendedJSONEncoder, ensure_ascii=False, indent=2)
