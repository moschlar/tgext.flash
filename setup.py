#This is just a work-around for a Python2.7 issue causing
#interpreter crash at exit when trying to log an info message.
try:
    import logging
    import multiprocessing
except:
    pass

import sys

from setuptools import setup, find_packages


setup(name='tgext.flash',
      version='0.1',
      description="Advanced Flash Extension for TG2",
      long_description=open('README.md').read(),
      author='Moritz Schlarb',
      author_email='moschlar@metalabs.de',
      url='https://github.com/moschlar/tgext.flash',
      keywords='turbogears2.extension, TG2, flash',
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      license='BSD-2',
      packages=find_packages(),
      namespace_packages=['tgext'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'TurboGears2 >= 2.2.0',
      ],
#      entry_points="""
#      # -*- Entry points: -*-
#      """,
      )