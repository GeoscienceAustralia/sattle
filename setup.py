#!/usr/bin/env python2.7
"""
Description:
    Standard setup.py for python packaging. Not really useful for django projects!

Author: fei.zhang@ga.gov.au

Date: 2015-06-30
Example Run:  python2.7 ./setup.py bdist_rpm  --fix-python

"""

from __future__ import print_function
from distutils.core import setup
import os

version = '1.1.0'

# Append TeamCity build number if it gives us one.
if 'TC_BUILD_NUMBER' in os.environ and version.endswith('b'):
    version += '-' + os.environ['TC_BUILD_NUMBER']

setupconfig = {
    'name': 'sattle',
    'url': 'https://github.com/GeoscienceAustralia/sattle',
    'maintainer': 'Fei Zhang',
    'maintainer_email': 'fei.zhang@ga.gov.au',
    'version': version,
    'description': 'Satellite TLE Service',
    'packages': ['sattle', 'tleserv' ],
    #'package_dir': [''], #dir where the packages will be found, ''==current-rootdir
    'scripts': ['bin/tleloader.bash', ],
    'requires': ['psycopg2','Django','djangorestframework',]  # [ 'mysql-python27', ]
}

setup(**setupconfig)
