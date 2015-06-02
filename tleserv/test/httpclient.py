"""
Description:    Get Latest TLE for satellite Norad_number, using http client to consume Restful web service APIs
Author:         Fei.Zhang@ga.gov.au
Date:           2015-06-01
"""

import sys
import time

import requests

# Anonymous readable Restful Service end-point base_url
RESTFUL_BASE_URL = r'http://10.10.19.65:8000/sattle/tleserv'


class TleClient:
    def __init__(self, restful_burl):
        self.rest_base_url = restful_burl
        self.timenow=time.time()

    def get_active_satellite_norad(self):
        """
        Find all active satellites in the TLE system
        :return: a listbof norad numbers
        """
        sat_query_url = self.rest_base_url + "/satellites/?format=json&isactive=rue"

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

        print "TLE Age in hours= " + str(tle_age)

        return (str(tle_res['line1']), str(tle_res['line2']), tle_res['url'])


# this function is included for comparison purpose
def get_tle_from_spacetrack( noradlist ):
    """
    :param noradlist: one or more comma separated norad numbers: 39084 OR "25994, 27424, 39084"
    :return: TLE for each norad
    Pre-condition: users have to register a login account with space-track: https://www.space-track.org/
    Pitfall: what if this site is down?
    Ref: http://stackoverflow.com/questions/11892729/how-to-log-in-to-a-website-using-pythons-requests-module
    """
    QUERY_BASE_URL = "https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/NORAD_CAT_ID/%s/orderby/TLE_LINE1 ASC/format/tle"
    # QUERY_BASE_URL="https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/NORAD_CAT_ID/25994, 27424, 39084/orderby/TLE_LINE1 ASC/format/tle"

    # Fill in your details here to be posted to the login form.
    SPTRACK_LOGIN_URL = 'https://www.space-track.org/ajaxauth/login'
    payload = {
        'identity': 'fei.zhang@ga.gov.au',
        'password': '$PASSWORD'  # not revealed in gitpub
    }

    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        p = s.post(SPTRACK_LOGIN_URL, data=payload)
        # print the html returned or something more intelligent to see if it's a successful login page.
        print p.text

        # An authorised request.
        qurl = QUERY_BASE_URL % (noradlist)
        print qurl
        r = s.get(qurl)  # A protected web page url'
        print r.text

################################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "USAGE: python httpclient.py norad numbers"  # 25994 27424 39084
        sys.exit(1)

    tleclt = TleClient(RESTFUL_BASE_URL)

    noradlist=tleclt.get_active_satellite_norad()
    # noradlist= sys.argv[1:]

    for eachn in noradlist:
        tle = tleclt.get_latest_tle(eachn)
        print tle

    # get from third party site spacetrack
    print str(noradlist)
    norads= str(noradlist)[1:-1]
    print norads

    # get_tle_from_spacetrack(norads)
