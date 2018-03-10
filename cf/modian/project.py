import argparse

from . import api
from ..project import Project


def project_overview(project_id):
    r = api.get('/realtime/get_simple_product', params=dict(ids=project_id),
                logpath=f'projects/overview/{project_id}')
    link = f'https://zhongchou.modian.com/item/{project_id}.html'
    title = r.name
    start_time = api.parse_api_datetime(r.start_time)
    end_time = api.parse_api_datetime(r.end_time)
    amount = r.backer_money_rew
    backers = r.backer_count
    return Project('modian', project_id, link, title, start_time, end_time, amount, backers)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('project_id')
    args = parser.parse_args()

    print(project_overview(args.project_id))


if __name__ == '__main__':
    main()
