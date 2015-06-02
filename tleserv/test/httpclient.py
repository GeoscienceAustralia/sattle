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
    Further more, comparison show that our TLE service has newer TLTs:
    
    Test:
    [fzhang@pe-test]$ vi tleserv/test/httpclient.py
    [fzhang@pe-test]$ python tleserv/test/httpclient.py 39084
    TLE Age in hours= 14.5175964561
    ('1 39084U 13008A   15152.50000000  .00000000  00000-0  93512-3 0    12', '2 39084  98.2294 222.5196 0001389  94.8942 192.0987 14.57089870122318', u'http://10.10.19.65:8000/sattle/tleserv/tles/952/')
    ""
    https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/NORAD_CAT_ID/39084/orderby/TLE_LINE1 ASC/format/tle
    [u'1 39084U 13008A   15152.23927176  .00000208  00000-0  56297-4 0  9990', u'2 39084 098.2292 222.2618 0001365 092.4729 267.6626 14.57095397122289']
    ['39084']
    '39084'

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
    res=None
    with requests.Session() as s:
        p = s.post(SPTRACK_LOGIN_URL, data=payload)
        # print the html returned or something more intelligent to see if it's a successful login page.
        #print p.text

        # An authorised request.
        qurl = QUERY_BASE_URL % (noradlist)
        print qurl
        r = s.get(qurl)  # A protected web page url'
        res=r.text

    return res

################################################################################
if __name__ == "__main__":
    
    print "USAGE: python httpclient.py [norad-numbers]"  # 25994 27424 39084

    tleclt = TleClient(RESTFUL_BASE_URL)
    if len(sys.argv) < 2:
        noradlist=tleclt.get_active_satellite_norad()
    else:
        noradlist= sys.argv[1:]

    for eachn in noradlist:
        tle = tleclt.get_latest_tle(eachn)
        print tle
        
        tle3rd=get_tle_from_spacetrack(eachn)
        print tle3rd.splitlines() # print in one line

    # get from website spacetrack
    print str(noradlist)
    norads= str(noradlist)[1:-1]
    print norads

    print get_tle_from_spacetrack(norads)
