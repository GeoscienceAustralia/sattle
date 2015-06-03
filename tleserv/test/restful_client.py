"""
Description:    Get Latest TLE for satellite Norad_number, using http client to consume Restful web service APIs
Author:         Fei.Zhang@ga.gov.au
Date:           2015-06-01
"""

import sys
import time

import requests

from tleserv import TLEParser

# Anonymous readable Restful Service end-point base_url
RESTFUL_BASE_URL = r'http://10.10.19.65:8000/sattle/tleserv'
RESTFUL_BASE_URL = r'http://ec2-52-64-92-80.ap-southeast-2.compute.amazonaws.com/sattle/tleserv'
# OR connect to a proper http server
#RESTFUL_BASE_URL = r'http://127.0.0.1:80/sattle/tleserv'


class TleClient:
    def __init__(self, restful_burl):
        self.rest_base_url = restful_burl
        self.timenow=time.time()

    def get_active_satellite_norad(self):
        """
        Find all active satellites in the TLE system
        :return: a listbof norad numbers
        """
        sat_query_url = self.rest_base_url + "/satellites/?format=json&isactive=True"

        response = requests.get(sat_query_url)
        jdict = response.json()
        sat_res=jdict['results']

        norads=[]
        for each in sat_res:
            n= each['norad_number']
            norads.append(n)

        print norads

        return norads

    # http://stackoverflow.com/questions/7750557/how-do-i-get-json-data-from-restful-service-using-python
    def get_latest_tle(self, noradnums):
        """ Get the latest TLE  from Restful API
        :param noradnums: norad_numbers as comma-seps string
        :return: a TLE
        """

        tle_query_url = self.rest_base_url + "/tles/?format=json&norad_number=%s&ordering=-epochsec" % (noradnums)
        #debug print tle_query_url

        response = requests.get(tle_query_url)
        jdict = response.json()

        tle_res = jdict['results'][0]

        tle_age= (self.timenow - float(tle_res['epochsec']))/3600

        # print "TLE Age in hours= " + str(tle_age)

        #return (str(tle_res['line1']), str(tle_res['line2']), tle_res['url'])

        return (noradnums, str(tle_res['line1']), tle_age)



################################################################################
if __name__ == "__main__":
    
    print "USAGE: python restful_client.py [norad-numbers]"  # 25994 27424 39084

    tleclt = TleClient(RESTFUL_BASE_URL)
    if len(sys.argv) < 2:
        noradlist=tleclt.get_active_satellite_norad()
    else:
        noradlist= sys.argv[1:]

    for eachn in noradlist:
        tle = tleclt.get_latest_tle(eachn)
        print tle
