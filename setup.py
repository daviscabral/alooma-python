#!/usr/bin/env python
try:
      from pip.req import parse_requirements
except ImportError:
      from pip._internal.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session=False)

reqs = [str(ir.req) for ir in install_reqs]

from distutils.core import setup

setup(name='alooma',
      version='0.3.21',
      description='Alooma python API',
      author='Yonatan Kiron',
      author_email='yonatan@alooma.io',
      packages=['alooma'],
      install_requires=reqs,
      keywords=['alooma']
      )
