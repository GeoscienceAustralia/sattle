"""
Description:
    what does this script module do? How to do it.

Author: fei.zhang@ga.gov.au

Date:
"""
__author__ = 'u25656'

"""
Configuration Constants for this package
"""

import yaml
import os
import logging
import logging.handlers

# aws_mysql = {'user': 'rmsuser', 'host': 'localhost', 'dbname': 'rmsdb', 'password': 'rms@g.008c', }
if os.path.exists(os.path.expanduser('~/etc/fetch.conf.d/dbconf.yaml')):
    logging.getLogger().info("Use file: ~/etc/fetch.conf.d/dbconf.yaml")
    p2yamlf = os.path.expanduser('~/etc/fetch.conf.d/dbconf.yaml')
elif os.path.exists('/etc/fetch.conf.d/dbconf.yaml'):
    logging.getLogger().info("Use file: /etc/fetch.conf.d/dbconf.yaml")
    p2yamlf = '/etc/fetch.conf.d/dbconf.yaml'
else:
    logging.getLogger().error("You must have ~/etc/fetch.conf.ddbconf.yaml or /etc/fetch.conf.d/dbconf.yaml ")

with open(p2yamlf, 'r') as f: mydbs = yaml.load(f)

# get the db credential
MyCon = mydbs['mysqldb']  # default connection: a dictionary of db connection login cred

# more connections
PostCon = mydbs['postgresdb']

# python logging target file
LOG_FILENAME = os.path.expanduser(mydbs['pylogfile'])  # ("/data/fetch/TLE_loader.log")
# Python loggin Level, DEBUG for dev test envs, INFO or ERROR for production env
LOG_LEVEL = getattr(logging, mydbs['pyloglevel'].upper())  #
# logging.INFO for file handler: DEBUG, INFO, WARNING, ERROR and CRITICAL


def create_logger(loggerName):
    """ create a logger with a name"""

    logger = logging.getLogger(loggerName)

    logger.setLevel(LOG_LEVEL)
    # for file handler: DEBUG, INFO, WARNING, ERROR and CRITICAL

    # create file handler to the logger
    fhandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=2000000, backupCount=5)
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s :: %(levelname)s: %(message)s")

    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)

    # create an additional console handler for debug
    ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)  # add formatter to ch

    # add ch to logger
    logger.addHandler(ch)

    return logger


class MyYaml:
    """to handle yaml file.  @author: fzhang
    """

    def __init__(self, path2yamlfile):
        self.yamlfile = path2yamlfile
        # a dict
        MYSQL = {'user': 'rmsuser',
                 'host': 'localhost',
                 'dbname': 'rmsdb',
                 'password': 'mi_pwd'}

        POSTGRES = {'user': 'rmsuser', 'host': 'localhost', 'dbname': 'rmsdb',
                    'password': 'mi_pwd'}

        self.dictdata = {'mysqldb': MYSQL, 'postgresdb': POSTGRES}

    def write2file(self, p2file):
        """write template yaml file from dict"""

        config = self.dictdata  # {'key1': 'value1', 'key2': 'value2'}

        with open(p2file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

    def readin(self, p2file=None):
        """Read in data from a yaml  file
        """
        if p2file is None:
            yamlfile = self.yamlfile
        else:
            yamlfile = p2file

        with open(yamlfile, 'r') as f:
            config = yaml.load(f)

        # now we got a dictionary: config
        # print config.get('mysqldb')
        #print config.get('postgresdb')

        #print yaml.dump(config, None, default_flow_style=False)

        return config


class DatabaseConf:
    """
    This class takes a dictionary in constructire, and turn it into an object holding db connection login strings
    """
    def __init__(self, **kwargs):

        # print kwargs
        if kwargs == {}:  # case 1: default
            self.host = MyCon["host"]
            self.user = MyCon["user"]
            self.password = MyCon["password"]  # Cap4root rms@g.008c
            self.dbname = MyCon["dbname"]
            self.schema = ""
        else:  # construct from a dictionary
            self.host = kwargs.get("host")
            self.user = kwargs.get('user')
            self.password = kwargs.get('password')
            self.dbname = kwargs.get('dbname')
            # self.schema = kwargs.get('schema') # postgresql
            pass

    # -------------------
    def __str__(self):
        """A string representation of this object state"""
        return str(self.__dict__)


#####################################################################################
if __name__ == "__main__":
    # default db in yaml file
    dbconf = DatabaseConf()
    print dbconf


# ------------------------------------------------
# test yaml file handler class
if __name__ == "__main__22":
    # tesr yamle file handler

    myyaml = MyYaml('dbconf.yaml')
    yaml2dict = myyaml.readin()
    # case 2: provide a dictionary
    mydb = yaml2dict['mysqldb']

    dbconf2 = DatabaseConf(**mydb)
    print dbconf2

