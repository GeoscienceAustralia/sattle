#!/usr/bin/env python
__author__ = 'fzhang'
import os
import sys
import django

if __name__ == "__main__":
    # setup django project
    #os.sys.path.append("/home/fzhang/PycharmProjects/sattle")
    os.sys.path.append("../..")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sattle.settings")

    django.setup()
    ################################################
    from tleserv.models import Satellite
    from tleserv.models import Tle

    print "Active Satellites ......"
    sat2 = Satellite.objects.filter(isactive='True')
    print sat2

    print "active satellite with given norad number"

    #sat_inst= Satellite.objects.filter(norad_number=37849)
    sat_inst = sat2.filter(norad_number=37849)
    print type(sat_inst)

####
    all_tle=Tle.objects.all()
    print "Number of TLE records==" #+ all_tle[-1]
    print len(all_tle)

    a_tle = Tle()
    a_tle.line1 = "1 37849U 11061A   15138.00000000  .00000000  00000-0  45447-5 2    02"
    a_tle.line2 = "2 37849 098.6970 077.8602 0001252 092.0306 348.7111 14.19552114184104"

    a_tle.norad_number = sat_inst[0]
    a_tle.status = True
    a_tle.epochsec = 1431907200.0000000000
    a_tle.md5sum="97d1bdc6f3a150977d7eeefdea56723c"
    a_tle.path2file = "/data/ephemeris/source/nasa/20150519.drl.tle"
    a_tle.tle_dt_utc = "2015-05-18 00:00:00+00"
    a_tle.tle_source = 0
    a_tle.inp_dt_utc="2015-05-19 10:40:02.685394+00"

    a_tle.save()

    print a_tle.tleid
