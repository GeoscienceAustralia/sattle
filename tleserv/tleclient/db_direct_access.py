#!/bin/env python2.7
"""
Description:
    Direct access of the TLE database tables using traditional way, django, running SQL queries:
    get Satellites, Tles
    Get latest Tle for each active satellite.
    So that we can compare with retrieved from Restful json.

Author: fei.zhang@ga.gov.au

Date:   2015-06-05
"""

import getopt
import os
import sys
import psycopg2
import MySQLdb
import logging

from TLE import TLE
import config


class TLELoader:
    """ class TLE loader
     """

    def __init__(self):
        """
        database target
        :return:
        """
        logname = self.__class__.__name__
        self.logger = config.create_logger(logname)





    # ----------------------------------------------------------------------
    def postgres_get_satellite_norads(self, targetdb):
        """
        get a list of the actively-tracked satellites NORAD_Number from targetdb = config.DatabaseConf()
        :return: list_of_noradID
        """
        self.logger.info("**********************  Get satellites from  %s", str(targetdb))

        db = None
        try:
            db = psycopg2.connect(**targetdb)
        except Exception, why:
            self.logger.error("!!! Connection Failed Error %s !!!: ", str(why))
            sys.exit(1)

        cursor = db.cursor()
        sql = "SELECT norad_number, satname FROM satellite where isactive=true"

        try:
            cursor.execute(sql)
            satellites = cursor.fetchall()
        except Exception, why:
            self.logger.error("!! Failed because: %s", str(why))
        finally:
            # disconnect from server
            if db is not None: db.close()

        self.logger.debug("Active satellites retrieved from DB: %s", satellites)

        norads = []
        for sat in satellites:
            norads.append(int(sat[0]))

        return norads



    def get_satellite_norads(self, targetdb):
        """
        get a list of the actively-tracked satellites NORAD_Number from targetdb = config.DatabaseConf()
        :return: list_of_noradID
        """
        self.logger.info("**********************  Get satellites from  %s", str(targetdb))

        db = None
        try:
            db = MySQLdb.connect(host=targetdb.host,  # db host, name or ip, usually localhost
                                 user=targetdb.user,  # db username
                                 passwd=targetdb.password,  # db password
                                 db=targetdb.dbname)  # name of the data base
            # prepare a cursor object using cursor() method
        except Exception, why:
            self.logger.error("!!! Connection Failed Error %s !!!: ", str(why))
            sys.exit(1)

        cursor = db.cursor()
        sql = "SELECT norad_number, satname FROM satellite where isactive=1"

        try:
            cursor.execute(sql)
            satellites = cursor.fetchall()
        except Exception, why:
            self.logger.error("!! Failed because: %s", str(why))
        finally:
            # disconnect from server
            if db is not None: db.close()

        self.logger.debug("Active satellites retrieved from DB: %s", satellites)

        norads = []
        for sat in satellites:
            norads.append(int(sat[0]))

        return norads

#######################################################
if __name__ == "__main__":

    aloader = TLELoader()

    if len(sys.argv) == 1:
        norads = aloader.get_satellite_norads(config.DatabaseConf())  # testing the get_satellite_norads function
        print norads
    else:
        pass


