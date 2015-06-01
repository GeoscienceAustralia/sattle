"""
Description:    http client to consume Restful web service API
Author:         Fei.Zhang@ga.gov.au
Date:           2015-06-01
"""

import requests

RESTFUL_BASE_URL = r'http://10.10.19.65:8000/sattle/tleserv'

# http://stackoverflow.com/questions/7750557/how-do-i-get-json-data-from-restful-service-using-python
def get_latest_tle(noradnumber):
    """ Get the latest TLE  from Restful API
    :param noradnumber: norad_number
    :return: a TLE
    """

    tle_query_url = RESTFUL_BASE_URL + "/tles/?format=json&norad_number=%s&ordering=-epochsec" % (noradnumber)
    print tle_query_url

    response = requests.get(tle_query_url)
    jdict = response.json()

    return jdict['results'][0]


def get_active_satellite_norad():
    sat_query_url = RESTFUL_BASE_URL + "/satellites/?format=json"

    response = requests.get(sat_query_url)
    jdict = response.json()

    print jdict


def get_tle_from_spacetrack():
    # http://stackoverflow.com/questions/11892729/how-to-log-in-to-a-website-using-pythons-requests-module
    # Fill in your details here to be posted to the login form.
    LOGIN_URL='https://www.space-track.org/ajaxauth/login'
    payload = {
        'identity': 'fei.zhang@ga.gov.au',
        'password': '$Password'
    }

    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        p = s.post(LOGIN_URL, data=payload)
    # print the html returned or something more intelligent to see if it's a successful login page.
        print p.text

    # An authorised request.
        URL="https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/NORAD_CAT_ID/25994/orderby/TLE_LINE1%20ASC/format/tle"
        r = s.get( URL) # A protected web page url'
        print r.text


if __name__ == "__main__":
    # print get_latest_tle(25682)
    #
    # print get_latest_tle(27424)
    #
    # get_active_satellite_norad()

    get_tle_from_spacetrack()

