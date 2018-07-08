# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='labeler',
      version='0.1.0',
      packages=['labeler'],
      entry_points={
          'console_scripts': [
              'labeler = labeler.__main__:main'
          ]
      },
      )