#!/bin/env python2.7
"""
Description:
    A entry script to check every aspects of the deployment:
    get Satellites, Tles
    Get latest Tle for each active satellite.
    from Restful json and direct DB access.

Author: fei.zhang@ga.gov.au

Date:   2015-06-05
"""

import getopt
import os
import sys
import logging
import unittest
import config


class MyTester:
    """ class TLE loader
     """

    def __init__(self):
        """
        database target
        :return:
        """
        logname = self.__class__.__name__
        self.logger = config.create_logger(logname)




#######################################################
if __name__ == "__main__":

    print("todo")

