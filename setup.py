#!/usr/bin/env python3

import setuptools


setuptools.setup(
    name='crowdfunding',
    author='KSH',
    author_email='i@momo0v0.club',
    version='0.1dev',
    packages=['cf'],
    install_requires=[
        'Jinja2',
        'PyYAML',
        'arrow',
        'attrdict',
        'bs4',
        'html5lib',
        'requests',
    ],
    entry_points={
        'console_scripts': [
        ],
    },
)
