import collections

import jinja2


_PROJECT_TEMPLATE = jinja2.Template('''\
{% if p.platform == 'modian' %}摩点{% elif p.platform == 'owhat' %}Owhat{% endif %}：{{ p.title }}
{% if p.link -%}
{{ p.link }}
{% endif -%}
{% if p.start_time or p.end_time -%}
{% if p.start_time %}{{ p.start_time.strftime('%Y-%m-%d') }}{% else %}未知{% endif %}\
 -- \
{% if p.end_time %}{{ p.end_time.strftime('%Y-%m-%d') }}{% else %}未知{% endif %}
{% endif -%}
{% if p.amount is not none -%}
￥{{ '%.2f'|format(p.amount) }}\
{% if p.backers is not none %}\t{{ p.backers }}人{% endif %}
{% endif -%}
''')


class Project(collections.namedtuple('Project', 'platform project_id link title start_time end_time amount backers')):

    def __new__(cls, *args):
        platform, project_id, link, title, start_time, end_time, amount, backers = args
        if platform not in ('modian', 'owhat'):
            raise ValueError(f'{platform} is not a valid platform identifier, '
                             f'which should be either modian or owhat')
        if not project_id:
            raise ValueError('project_id is required')
        if not title:
            raise ValueError('title is required')
        self = super().__new__(cls, *args)
        return self

    def __str__(self):
        return _PROJECT_TEMPLATE.render(p=self)
