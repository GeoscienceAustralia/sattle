#!/bin/env python2.7
"""
Description:
    Use Django models and settings.py to insert new TLE data from file to DB targets.

Author: fei.zhang@ga.gov.au

Date: 2015-06-04
"""
__author__ = 'u25656'


import os
import sys
import django
from django.utils import timezone

# The next 3 lines are essential to setup django project with DB connection
# os.sys.path.append("/home/fzhang/PycharmProjects/sattle")
os.sys.path.append("../..")
os.environ["DJANGO_SETTINGS_MODULE"] = "sattle.settings"
django.setup()

from tleserv.models import Satellite
from tleserv.models import Tle

from TLEParser import TLE
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


    def parse_tle_file(self, tlefile):
        """
        parse an input TLE file to produce a list of records
        :param tlefile:
        :return: TLE list
        """

        try:
            fp = open(tlefile, "r")
            lines = fp.readlines()
        except IOError:
            self.logger.error("Error: failed to find the file %s or read data", tlefile)
        finally:
            fp.close()

        tle_list = []  # to be returned

        line1 = None
        line2 = None
        for aline in lines:
            if aline.startswith("1 ") and len(
                    aline) >= 69:  # the length of a TLE line is 70 including the trailing newline char \n
                line1 = aline
            elif aline.startswith("2 ") and len(
                    aline) >= 69:  # the length of a TLE line is 70 including the trailing newline char \n
                line2 = aline
            else:
                # This line is a satellite name descrip for example: ISS (ZARYA)
                # self.logger.debug("TLE subject line: %s", aline)
                pass

            if line1 is not None and line2 is not None:  # got a pair of tle
                tle = (line1.strip('\r\n '), line2.strip('\r\n '))  # strip leading and trailng \r or \n or white space
                tle_list.append(tle)
                self.logger.debug("A TLE pair is found: %s", tle)

                # reset the 2 line holders
                line1 = None
                line2 = None

        return tle_list

    def get_meta_tle(self, tlefile, sfilter=None):
        """
        parse and extract metatdata from a tlefile => a list of TLE pairs;
        Filter them according to norad number.
        Each pair would be a row into the database table.
        :param a list of tlepair tuples:
        :return: a list of TLE objects of the TLEParser.TLE type
        """
        tlepairs = self.parse_tle_file(tlefile)  # all the TLE pairs from the file

        self.logger.info("Total number of TLE pairs from the downloaded file is %s", len(tlepairs))

        tlelist = []  # TLE objects
        for atle in tlepairs:
            tleobj = TLE(atle, tlefile)
            if sfilter is None:  # no filter is applied, all tle will be ingested
                tlelist.append(tleobj)
            elif tleobj.noradid in sfilter:
                tlelist.append(tleobj)

            else:  # the noradid is not active, not interested to us.
                pass

        return tlelist

    def create_tle_record(self, atleobj):
        """Create a Django model instance of Tle type
        :param atleobj: encaptulation of TLE and full metadata
        :return: Django ModelTle instances ready to be saved into DB
        """
        self.logger.debug( str(atleobj))

        #try to see if the same TLE already exists?
        tle=Tle.objects.get(md5sum=atleobj.md5sum)
        self.logger.info(str(tle))
        self.logger.info(type(tle))

        if not tle:
            print "This TLE has not been in DB yet, to do insert"
        else:
            print "skip insert, will return -1"
            return -1


        sat_inst = Satellite.objects.get(pk=atleobj.noradid) #get one object

        TleModelObj = Tle()

        TleModelObj.line1 = atleobj.line1
        TleModelObj.line2 = atleobj.line2

        TleModelObj.norad_number = sat_inst
        TleModelObj.status = True
        TleModelObj.epochsec =  atleobj.epoc_seconds
        TleModelObj.md5sum = atleobj.md5sum
        TleModelObj.path2file = atleobj.path2file  #"/data/ephemeris/source/nasa/20150519.drl.tle"
        TleModelObj.tle_dt_utc = atleobj.tledt   #"2015-05-18 00:00:00+00"
        TleModelObj.tle_source = 0
        TleModelObj.inp_dt_utc = timezone.now()  # OK "2015-05-19 10:40:02.685394+00"
        # todo: make default timesatmp in model and leave this unpoulated?

        new_tleid=-1
        try:
            TleModelObj.save()
            self.logger.info("Successful TLE save() into DB: %s", str(TleModelObj))
            new_tleid = TleModelObj.tleid
        except Exception , why:
            self.logger.error("Django save Tle failed because: %s", str(why))
        finally:
            # do what?
            pass

        return new_tleid

    def get_satellite_norads(self, db=None):
        """
        get a list of active satellite Norad_numbers
        :return:list_of_norad
        """
        self.logger.info("**********************  Get satellites from  %s", str(db))

        #Active Satellites
        sat2 = Satellite.objects.filter(isactive='True')

        norad_numbers=[]
        for s in sat2:
            norad_numbers.append(s.norad_number)

        return norad_numbers

    # --------------------------------------------------------------------
    def load(self, tlefile, dbtargets=None):
        """Given a tlefile, parse it to get the TLE pairs, derive the required metadata and save the tle into dbtargets
        :param tlefile: a file with TLE/3LEs typically downloaded from providers.
        :param dbtargets: MySQL and/or Postgres configures in django settings.py
        :return:
        """

        tle_source = 0  # deprecated: downloading source: CELESTRAC, USGS, NASA are in the path2/filename
        for db in dbtargets:
            print db
            # A list of Norad Number, corresponding to RMS active satellites in the table satellite
            # ((25682L, 'LANDSAT-7'), (39084L, 'LANDSAT-8'), (27424L, 'AQUA'), (25994L, 'TERRA'),
            # (25338L, 'NOAA-15'), (28654L, 'NOAA-18'), (33591L, 'NOAA-19'), (37849L, 'SUOMI-NPP'))
            # sat_filter = [25338, 25682, 25994, 27424, 28654,33591,  37849,  39084  ]

            sat_filter = self.get_satellite_norads()

            # parse TLE file and filter for what we want according to NORA_ID of active satellite
            tle_list = self.get_meta_tle(tlefile, sat_filter)

            self.logger.info("After applying the filter, %s TLEs to be inserted into DB", len(tle_list))

            # make tle dj-model obj, and save it
            for atle in tle_list:
                new_tleid=self.create_tle_record(atle)
                if new_tleid>0:
                    self.logger.info("new TLE record was created with tleid=%s", str(new_tleid))
                else:
                    self.logger.info("No TLE record was created  !!!!!!! duplicate exists already")

        return 0


################################################################################################################
# How to insert many TLE files:
# [ads@pe-test tle2db]$ python tle_loader.py /eoancillarydata/sensor-specific/CELESTRAK_TLE/*.txt &>> /tmp/my.log
# OR   find /eoancillarydata -name "*.txt"  -exec ./tle_loader.py {} \; &> stdoe.log
#
if __name__ == "__main__":

    aloader = TLELoader()

    if len(sys.argv) == 1:
        norads = aloader.get_satellite_norads()  # testing the get_satellite_norads function
        print norads
    else:
        print "To load TLE data from files into DB: %s %s" % (sys.argv[0], str(sys.argv[1:]))
        for tlefile in sys.argv[1:]:
            print "Processing " + tlefile
            aloader.load(tlefile,["postgres"])  # this will load tle into db



