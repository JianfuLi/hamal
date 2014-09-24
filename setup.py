# -*- coding: utf-8 -*-


import sys
from distutils.core import setup

sys.path.append('./src')

setup(name='hamal',
      version='1.0.0',
      description='mysql全文索引同步中间件',
      long_description='',
      author='lijf',
      author_email='me@ljf.me',
      packages=['hamal'],
      package_dir={'hamal': 'src'},
      package_data={'hamal': ['stuff']},
      license="MIT",
      platforms=["any"],
      url='https://github.com/jianphu/hamal')