"""
Description: import the base settings.py and modify the default database connection credentials

Author: fei.zhang@ga.gov.au

Date: 2015-07-09
"""

from settings import *
import yaml

## Local customisation in yaml file  (or environ setting)
with open('/etc/fetch.conf.d/dbconf.yaml', 'r') as f: mydbs = yaml.load(f)
# get the db credential
Mysql= mydbs['mysqldb']  # according to the config yaml file

#override the db credentials
DATABASES['default']['HOST'] = Mysql['host']
DATABASES['default']['NAME'] = Mysql['dbname']
DATABASES['default']['USER'] = Mysql['user']
DATABASES['default']['PASSWORD'] = Mysql['password']
