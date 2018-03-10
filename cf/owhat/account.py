import argparse

import arrow

from . import api
from ..project import Project


def fetch_project_listing(uid):
    r = api.post('home', 'userindex', dict(userid=uid, pagenum=1, pagesize=50),
                 logpath=f'accounts/{uid}')
    for item in r.data.useractivity:
        # columnid:
        # - 1: 商品
        # - 2: 活动
        # - 3: 应援（集资）
        if item.columnid != 3:
            continue
        project_id = item.entityid
        link = f'https://www.owhat.cn/shop/supportdetail.html?id={project_id}'
        title = item.title
        start_time = arrow.get(item.publishtime / 1000)
        end_time = arrow.get(item.fundingendtime / 1000)
        amount = float(item.fundingtotalamount)
        yield Project('owhat', project_id, link, title, start_time, end_time, amount, None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('uid', help='user id of the creator')
    args = parser.parse_args()

    for project in fetch_project_listing(args.uid):
        print(project)


if __name__ == '__main__':
    main()
