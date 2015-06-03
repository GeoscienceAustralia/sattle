"""
TLE parser utility class to handle a pair of strings (ie, TLE data) and extract info from them
"""
import sys
import hashlib
import datetime
import time


class TLE:
    """
    TLE data parser to extract metadata
    """

    def __init__(self, tles, path2tlefile=None):
        """
        :param tles: =(line1, line2) tupple.
        :param path2tlefile: the file where the tle pair is from
        :return:
        """
        self.line1 = tles[0]
        self.line2 = tles[1]

        self.path2file = path2tlefile  # prepend  $HOSTNAME:

        if self._check(self.line1) and self._check(self.line2):
            pass  # good TLE
        else:
            raise Exception("This TLE %s %s has a problem with check sums." % (tles[0], tles[1]))

        self._parse_line1()
        self._parse_line2()
        self._md5sum()
        self.get_epoc_seconds()
        self.get_datetime()

    # -------------------
    def __str__(self):
        """A string representation of the TLE"""
        return str(self.__dict__)

    def _check(self, line):
        """
        Verify the check sum of the line:
        The checksum for each line is calculated by adding the all numerical digits on that line, including the line number.
        One is added to the checksum for each negative sign - on that line. All other non-digit characters are ignored.
        :return: True if both line OK; False is either line is not OK.
        """

        sum = 0
        for ch in line[:-1]:
            if ch in '0123456789':
                sum = sum + int(ch)
            elif ch == '-':
                sum = sum + 1
            else:
                pass

        sum1mod10 = sum % 10

        # tested works very well.
        # print "line %s checksum is %s" % (line, str(sum1mod10))

        return int(line[-1]) == sum1mod10

    def _md5sum(self):
        """
        md5 checksum of the string lin1+line2, where line1 and line2 are the two line elements without trailing \n
        echo -n "1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  29272 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537" | md5sum
        :return: 32chars alphanumerics, eg 8b997ecb09edecf8d500e5b58fd6aa27
        """
        twolines = self.line1 + self.line2
        md5 = hashlib.md5()
        md5.update(twolines.encode())

        self.md5sum = md5.hexdigest()

        return self.md5sum


    def _parse_line1(self):
        """Parse the first line of the TLE:
        1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
        """

        line = self.line1

        self.noradid = int(line[2:7])  # self.satelliteNumber 5 digit sequential number started from 00001
        self.classification = line[7]
        self.intDesgination = line[9:17]
        self.epochYear = line[18:20]
        self.epochDay = float(line[20:32])
        self.firstDeriv = float(line[33:43])
        self.secondDeriv = (float(line[44:50]) / 100000.0) * (10.0 ** int(line[50:52]))
        self.bStarDrag = (float(line[53:59]) / 100000.0) * (10.0 ** int(line[59:61]))
        self.elementSetType = line[62]
        self.elementNumber = int(line[64:68])  # interesting
        return

    def _parse_line2(self):
        """Parse the second line of the TLE:
        2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
        """
        line = self.line2
        self.satelliteNumber = line[2:7]  # == self.noradid
        self.inclination = float(line[8:16])  # * SatId.radians_per_degree
        self.ra = float(line[17:25])  # * SatId.radians_per_degree
        self.eccentricity = float("0." + line[26:33])
        self.perigee = float(line[34:42])  # * SatId.radians_per_degree
        self.anomaly = float(line[43:51])  # * SatId.radians_per_degree
        self.meanMotion = float(line[52:63])
        self.revolutions = int(line[63:68])
        return

    def get_epoc_seconds(self, year=None, epocdoy=None):
        """ Beaware, The date time thing may have issues with timezone day light saving time etc. If in doubt trust UTC setting.
        this function has been tested for UTC and localtime setting of host Linux system. with datetime from both summer and winter.
        python under default local time setting.
        >>> time.timezone
        >>> -36000
        >>> import os; os.environ['TZ'] = 'UTC'  # to alter the TZ for it to be UTC
        >>> time.tzset()
        >>> time.timezone
        >>>0

        :param year: 08
        :param epocdoy:
        :return: unix epoc seconds since 1920 Jan 01.
        """
        if year is None:
            year = self.epochYear

        if epocdoy is None:
            epocdoy = self.epochDay

        iyear = int(year)

        if iyear < 57:  # https://celestrak.com/columns/v04n03/  good until year 2056
            eyear = iyear + 2000
        else:
            eyear = iyear + 1900

        # this works well and correctly for Python2.7 but not for python2.6
        # year_sec = (datetime.datetime(eyear, 1, 1, 0, 0, 0, 0) - datetime.datetime(1970, 1, 1)).total_seconds()

        tstring = '%s-01-01 00:00:00' % (eyear)  # get the epock seconds until the very start of the eyear
        year_sec = int(time.mktime(time.strptime(tstring, '%Y-%m-%d %H:%M:%S'))) - time.altzone
        # - time.timezone have problem in winter datetime

        # print year_sec

        # see the interpretation of https://celestrak.com/columns/v04n03/
        self.epoc_seconds = year_sec + (epocdoy - 1) * 24 * 3600  # take into account of the offset -1 for doy

        return self.epoc_seconds

    # update tle set tle_utc_dt=to_timestamp('2015-04-01T15:36:38', 'yyyy-mm-ddThh24:mi:ss') where tleid=1;
    def get_datetime(self):
        """ converts  self.epoc_seconds (eg, 1428296478.06) into a UTC date time string.
        :param epoc_seconds:
        :return: A datetime string like: 2015-04-06T05:01:18
        to be inserted into the tle table for human read.
        """
        self.tledt = time.strftime("%Y-%m-%dT%H:%M:%S +0000", time.gmtime(self.epoc_seconds))  # +0000 is the UTC offset

        return self.tledt

    def get_tle_age_hours(self):
        self.age= (time.time() - self.epoc_seconds)/3600

        print self.age

        return self.age

def parse_tle_lines(self, lines):
    """
    parse an input TLE file to produce a list of TLE tupples records
    :param tlefile:
    :return: TLE list
    """

    # try: # if input is a file
    #     fp = open(tlefile, "r")
    #     lines = fp.readlines()
    # except IOError:
    #     self.logger.error("Error: failed to find the file %s or read data", tlefile)
    # finally:
    #     fp.close()

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


###########################################################################################
# Test data and Description:
# http://en.wikipedia.org/wiki/Two-line_element_set
# http://joyfulcoder.net/tle/
# Usage:
# [ads@pe-test tle2db]$ python2.7 TLE.py "1 39084U 13008A   15103.50000000  .00000000  00000-0  72108-3 0    16" "2 39084  98.1853 174.2713 0001235 101.5451 342.0006 14.57106792115186"
# [ads@pe-test tle2db]$ python2.7 TLE.py "1 39084U 13008A   15025.50000000  .00000000  00000-0  87277-3 0    12"  "2 39084  98.1974  97.5562 0001346  96.0913  30.3906 14.57105315103827"
#####################################################################################################################
if __name__ == "__main__":
    line1 = sys.argv[1]
    line2 = sys.argv[2]
    tle = (line1, line2)

    # print tle

    tleobj = TLE(tle)

    print str(tleobj)