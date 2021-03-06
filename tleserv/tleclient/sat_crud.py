#!/usr/bin/env python

import os
import sys
import django

if __name__ == "__main__":
    # setup django project
    #os.sys.path.append("/home/fzhang/PycharmProjects/sattle")
    os.sys.path.append("../..")

    print(os.sys.path)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sattle.settings")

    django.setup()
    ################################################
    from tleserv.models import Satellite

    print Satellite.objects.all()

    sat = Satellite(norad_number=99999, satname="LANDSAT-9")
    sat.rms_priority = 20
    sat.isactive = False #True 
    sat.save()
#todo: why duplicate norad_number=99999 no error?

    print sat.norad_number

    print "Inactive Satellites ......"
    sat0 = Satellite.objects.filter(isactive=False)
    print sat0

    print "Active Satellites ......"
    sat2 = Satellite.objects.filter(isactive='True')
    print sat2

    print "active satellite with given norad number"

    #sat_inst= Satellite.objects.filter(norad_number=37849)
    sat_inst = sat2.filter(norad_number=37849)
    print sat_inst


    print "LAND*  Satellites ......"
    landsats = Satellite.objects.filter(satname__startswith='LAND')
    print landsats

    print "Active Satellites ......"
    sat2 = Satellite.objects.filter(isactive='True')
    print sat2

    print "active satellite with given norad number"

    # sat_inst= Satellite.objects.filter(norad_number=37849)
    sat_inst = sat2.filter(norad_number=37849)
    print type(sat_inst) # QuerySet

    s = Satellite.objects.get(pk=37849) #get one object

    print s.tle_set.all()  # get related objects
    print ("Number of TLE for this Satellite", s.tle_set.count())

    ## t = s.tle_set.all()
    ## do not delete ! t.delete()
