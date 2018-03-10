import functools
import pathlib

import attrdict
import yaml


config_file = None
config = None


def load_config(path=None):
    global config_file
    global config

    if not path:
        path = pathlib.Path('config.yml')

    config_file = path
    with open(path, encoding='utf-8') as fp:
        config = attrdict.AttrDict(yaml.load(fp.read()))


def ensure_config(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if config is None:
            load_config()
        return f(*args, **kwargs)
    return wrapper


@ensure_config
def accounts(platform):
    if platform not in ('modian', 'owhat'):
        raise ValueError(f'{platform} is not a valid platform identifier, '
                         f'which should be either modian or owhat')
    if platform in config:
        return config(platform)
    else:
        return []


@ensure_config
def factions():
    return config.factions


@ensure_config
def datadir():
    s = config.datadir
    if s.startswith('/'):
        dir_ = pathlib.Path(s)
    elif s.startswith('~'):
        dir_ = pathlib.Path(s).expanduser()
    else:
        dir_ = config_file.parent.joinpath(s)
    assert dir_.is_dir(), f'{dir_} is not a directory'
    return dir_
