import arrow

from . import api
from ..project import Project


def project_overview(project_id):
    r = api.post('findgoodsbyid', 'shop.goods', dict(goodsid=project_id),
                 logpath=f'projects/overview/{project_id}').data
    link = f'https://www.owhat.cn/shop/supportdetail.html?id={project_id}'
    title = r.title
    start_time = arrow.get(r.salestartat / 1000)
    end_time = arrow.get(r.saleendat / 1000)
    amount = float(r.fundingdto.saleamount)
    return Project('owhat', project_id, link, title, start_time, end_time, amount, None)
