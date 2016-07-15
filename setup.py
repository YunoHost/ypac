#!/usr/bin/python
# -*- coding:Utf-8 -*-

from setuptools import setup

setup(name='ypac',
      version='0.1',
      description='YPaC is Yunohost Package Creator',
      author='opi',
      long_description=open("README.md", "r").read(),
      author_email='opi@zeropi.net',
      url='https://github.com/opi/ypac',
      install_requires=open("requirements.txt", "r").read().split(),
      scripts=['ypac'],
      license= '',
      keywords='yunohost',
     )
