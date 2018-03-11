import argparse
import collections
import textwrap
import time

import arrow
import jinja2

from . import config
from . import utils
from .modian import account as modian_account
from .modian import project as modian_project
from .owhat import account as owhat_account
from .owhat import project as owhat_project


PLATFORMS = [
    'modian',
    'owhat',
]

account_modules = {
    'modian': modian_account,
    'owhat': owhat_account,
}

project_modules = {
    'modian': modian_project,
    'owhat': owhat_project,
}

def _project_listing(platform, uid):
    return ((platform, uid), list(account_modules[platform].fetch_project_listing(uid)))


def fetch_new_projects():
    project_listing_args = [(platform, account.uid)
                            for platform in PLATFORMS
                            for account in config.accounts(platform)]
    project_listings = dict(utils.pool_starmap(_project_listing, project_listing_args))
    for platform in PLATFORMS:
        for account in config.accounts(platform):
            known_project_ids = set((account.get('project_ids') or []) +
                                    (account.get('irrelevant_project_ids') or []))
            new_projects = []
            for project in project_listings[(platform, account.uid)]:
                if project.project_id not in known_project_ids:
                    new_projects.append(project)
            if new_projects:
                print(account.name)
                print()
                for project in new_projects:
                    print(textwrap.indent(str(project), '  '))



def _project_overview(platform, faction, project_id):
    return (faction, project_modules[platform].project_overview(project_id))


def crawl_projects():
    project_overview_args = []
    for platform in PLATFORMS:
        for account in config.accounts(platform):
            for project_id in account.get('project_ids') or []:
                project_overview_args.append((platform, account.faction, project_id))

    faction_projects = collections.defaultdict(list)
    for faction, project in utils.pool_starmap(_project_overview, project_overview_args):
        faction_projects[faction].append(project)
    return [
        dict(
            faction=faction,
            projects=faction_projects[faction],
            total=sum(p.amount for p in faction_projects[faction]),
        ) for faction in config.factions()
    ]


_REPORT_TEMPLATE = jinja2.Template('''\
统计时间: {{ datetime.replace(microsecond=0).isoformat() }}

{% for entry in data -%}
{{ entry.faction }}
  总计: ￥{{ '%.2f'|format(entry.total) }}

{%- for project in entry.projects %}

  {{ project|string|trim|indent(2) }}
{%- endfor %}

{% endfor -%}
小结
{%- for entry in data %}
{{ entry.faction }}\t￥{{ '%.2f'|format(entry.total) }}
{%- endfor %}
''')


def projects_report(datetime, data):
    return _REPORT_TEMPLATE.render(datetime=datetime, data=data)


def newprojects_handler(args):
    fetch_new_projects()


def crawl_handler(args):
    now = arrow.now().to('Asia/Shanghai')
    timestamp_ms = int(now.float_timestamp * 1000)

    data = crawl_projects()

    reports_dir = config.datadir() / 'reports'
    json_reports_dir = reports_dir / 'json'
    text_reports_dir = reports_dir / 'text'
    json_reports_dir.mkdir(exist_ok=True, parents=True)
    text_reports_dir.mkdir(exist_ok=True, parents=True)

    utils.dump_json(collections.OrderedDict([('timestamp', timestamp_ms), ('data', data)]),
                    json_reports_dir / f'{timestamp_ms}.json')

    report = projects_report(now, data)
    with open(text_reports_dir / f'{timestamp_ms}.txt', 'w', encoding='utf-8') as fp:
        print(report, file=fp)

    print(report)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_newprojects = subparsers.add_parser('newprojects', help='check for new projects')
    parser_newprojects.set_defaults(handler=newprojects_handler)

    parser_crawl = subparsers.add_parser('crawl', help='crawl for stats of tracked projects')
    parser_crawl.set_defaults(handler=crawl_handler)

    args = parser.parse_args()

    args.handler(args)


main()
