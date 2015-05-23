#!/usr/bin/env python

import os
import sys
import django

if __name__ == "__main__":

# setup django project 
    os.sys.path.append("/path2/restle/proj")
    	
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resttle.settings")

    django.setup()
################################################    
    from tleserv.models import Satellite, Tle

    print Satellite.objects.all()
    print Tle.objects.all()

    sat=Satellite(norad_number=99999, satname="LANDSAT-9")
    sat.rms_priority=20
    sat.isactive=True
    sat.save()

    print sat.norad_number

    print "Inactive Satellites ......"
    sat0=Satellite.objects.filter(isactive=False)
    print sat0

    print "Active Satellites ......"
    sat2=Satellite.objects.filter(isactive='True')
    print sat2

    print "LAND*  Satellites ......"
    landsats=Satellite.objects.filter(satname__startswith='LAND')
    print landsats