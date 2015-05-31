#!/usr/bin/env python
__author__ = 'fzhang'
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

################################################
def get_satellite_norad_numbers():
    """
    get a list of active satellite Norad_numbers
    :return:
    """
    #Active Satellites
    sat2 = Satellite.objects.filter(isactive='True')

    norad_numbers=[]
    for s in sat2:
        norad_numbers.append(s.norad_number)

    return norad_numbers

def get_tle_by_norad(number):
    """
    Get all TLE of a given satellite norad_number
    :param number: satellite norad_number
    :return: a set of TLE records-objects
    """
    s = Satellite.objects.get(pk=number) #get one object

    related_tles = s.tle_set.all()  # get related objects

    order_tles = related_tles.order_by("-epochsec")  # -epochsec for descend

    print order_tles[:3]  #take the first three as latest 3.

    return order_tles  #related_tles

#http://stackoverflow.com/questions/7750557/how-do-i-get-json-data-from-restful-service-using-python
def get_latest_tle_from_restapi(number):
    """
    :param number: get the latest TLE  from Restful API
    :return: a TLE

    """


def create_tle_entry(line1, line2):
    """ define a new tle record and insert into the table
    """

    a_tle = Tle()
    a_tle.line1 = "1 37849U 11061A   15138.00000000  .00000000  00000-0  45447-5 2    02"
    a_tle.line2 = "2 37849 098.6970 077.8602 0001252 092.0306 348.7111 14.19552114184104"

    a_tle.norad_number = sat_inst[0]
    a_tle.status = True
    a_tle.epochsec = 1431907200.0000000000
    a_tle.md5sum = "97d1bdc6f3a150977d7eeefdea56723g"
    a_tle.path2file = "/data/ephemeris/source/nasa/20150519.drl.tle"
    a_tle.tle_dt_utc = "2015-05-18 00:00:00+00"
    a_tle.tle_source = 0
    a_tle.inp_dt_utc = timezone.now()  # OK "2015-05-19 10:40:02.685394+00"
    # todo: make default timesatmp ?
    print a_tle

    a_tle.save()

    print a_tle.tleid, a_tle.inp_dt_utc

if __name__ == "__main__":
    # setup django project
    # os.sys.path.append("/home/fzhang/PycharmProjects/sattle")
    os.sys.path.append("../..")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sattle.settings")

    django.setup()
    ################################################
    from tleserv.models import Satellite
    from tleserv.models import Tle

    norad_list=get_satellite_norad_numbers()
    print norad_list

    for noradn in norad_list:
        tles = get_tle_by_norad(noradn)
        print ("The Satellite %s has %s TLE records " %(noradn, tles.count()))
        try:
            print ("The Satellite %s has this LATEST TLE %s " %(noradn, tles[0]))
        except IndexError as indexe:
            print indexe.message


# define a new tle record and insert into the table
    #create_tle_entry("line1","line2")