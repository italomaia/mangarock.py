#!/usr/bin/env python3

from distutils.core import setup


setup(
    name='Mangarock',
    version='1.0',
    description='Script to download mangarock comics',
    author='Italo Maia',
    author_email='',
    install_requires=[
        'python-slugify==2.0.1',
        'requests==2.19.1',
        'Werkzeug==0.14.1',
    ],
    scripts=['mangarock.py']
)
