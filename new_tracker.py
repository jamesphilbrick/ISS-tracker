# AUTHOR: James Philbrick
# Initially created 15/06/2020

# NOTES:
# Can add functionality to get names of ISS crew from https://www.nasa.gov/mission_pages/station/expeditions/index.html

# It should be noted that the Vector Time (GMT) displayed represents the most recent TLE string posted by NASA and
# not the date at which it was sourced.

# If running on LINUX:
# might be worth looking at https://stackoverflow.com/questions/21322948/beautifulsoup-wont-recognize-lxml

import ephem
import math
import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests 

OBS_LON = 0.5406     # observer latitude
OBS_LAT = 53.2307    # observer longitude
OBS_ELEVATION = 75   # elevation in m
UPDATE_DELAY = 60    # delay between each data scrape in seconds
TIMEOUT_DELAY = 10   # url access timeout delay in seconds

def tle_source():
    # NASA has changed their site - this function will need to be updated to allow for automatic collection of the most recent TLE data available.
    # For now, data is hard-coded at the expense of accuracy.
    tle_1 = '1 25544U 98067A   22220.55122723  .00004662  00000-0  88788-4 0  9996'
    tle_2 = '2 25544  51.6445  77.1862 0005231  97.2571 342.7527 15.50269549353300'
    date = '08/08/2022'
    motion = 'motion'

    return tle_1, tle_2, date, motion

def calc_alt_az(tle_1, tle_2):
    # calculate altitude and azimuth
    observer.date = datetime.utcnow()
    iss_loc = ephem.readtle('ISS', tle_1, tle_2)
    iss_loc.compute(observer)
    alt = (iss_loc.alt * 180/math.pi)
    az = (iss_loc.az * 180/math.pi)

    return alt, az

def main():
    # source data and then get altitude and azimuth
    try:
        tle_1, tle_2, date, motion = tle_source()
    except:
        print('ERROR: unable to source TLE from spaceflight.nasa.gov \n Perhaps there has been a format change on the source page.')
    alt, az = calc_alt_az(tle_1, tle_2)

    # display information
    print('Last updated: ', datetime.utcnow())
    print('Elevation and Azimuth (DEG): {} {}'.format(alt, az))
    print('{} \n {} \n'.format(date.strip(), motion.strip()))


if __name__ == '__main__':
    # difine observer
    observer = ephem.Observer()
    observer.lon = OBS_LON
    observer.lat = OBS_LAT
    observer.elevation = 75

    while True:
        main()
        time.sleep(UPDATE_DELAY)
