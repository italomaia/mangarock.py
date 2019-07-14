#!/usr/bin/env python

from setuptools import setup


setup(
    name='Mangarock',
    version='1.3',
    description='Script to download mangarock comics',
    author='Italo Maia',
    author_email='',
    packages=['mangarock'],
    install_requires=[
        'python-slugify==2.0.1',
        'requests>=2.20.0',
        'Werkzeug==0.14.1',
    ],
    entry_points={
        'console_scripts': ['mangarock = mangarock.main:main']
    }
)
