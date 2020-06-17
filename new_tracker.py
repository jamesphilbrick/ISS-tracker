# AUTHOR: James Philbrick
# 15/06/2020

# NOTES:
# Might wanna make it so that the actual request for the TLE happens a lot less frequently than then pos. calculation
# Also might be a good idea to impliment error handling for the web scraping indipendent of the pos. calculation.
#
# can also add functionality to get names of ISS crew from https://www.nasa.gov/mission_pages/station/expeditions/index.html 

# It should be noted that the Vector Time (GMT) displayed
# represents the most recent TLE string posted by NASA and
# not the date at which it was sourced

# If running on LINUX:
# might be worth looking at https://stackoverflow.com/questions/21322948/beautifulsoup-wont-recognize-lxml

import ephem #*
import math
import time
from datetime import datetime
from bs4 import BeautifulSoup #*
import requests #*

# global input vars
obs_lon = 0.5406
obs_lat = 53.2307
obs_elevation = 75 # elevation in m
update_delay = 60 # delay between each data scrape in seconds
timeout_delay = 10 # url access timeout delay in seconds

def tle_source():
    # for the below line see: https://github.com/psf/requests/issues/4023
    source = requests.get('https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html', headers = {'connection': 'close'}, timeout = timeout_delay).text
    soup = BeautifulSoup(source, 'lxml')
    text = (soup.find('pre')).prettify() # prettify function converts to str datatype
    lines = text.splitlines()
    indices = [i for i, x in enumerate(lines) if x == '    ISS']
    last_iss_index = (indices[len(indices) - 1]) # get the line number for the last instance of 'ISS'
    # not really sure about how the above line works - sourced from https://stackoverflow.com/questions/6294179/how-to-find-all-occurrences-of-an-element-in-a-list
    date = lines[last_iss_index - 42]
    motion = lines[last_iss_index + 14]
    tle_1 = lines[last_iss_index + 1]
    tle_2 = lines[last_iss_index + 2]
    # above lines fetch lines from text by being called a set number of lines away from last 'ISS' line, kinda janky but hey ho oh well, effort
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
        print('ERROR: unable to source TLE from spaceflight.nasa.gov\n...either that or NASA changed their format or something ¯\_(ツ)_/¯')
    alt, az = calc_alt_az(tle_1, tle_2)

    # presentation
    div_line = ('-' * len(date.strip()))
    print(div_line)
    print('Last updated: ', datetime.utcnow())
    print(div_line)
    print('Elevation and Azimuth (DEG):')
    print(alt, ' ', az)
    print(div_line)
    print(date.strip())
    print(div_line)
    print(motion.strip())
    print(div_line + '\n')

# difine observer
observer = ephem.Observer()
observer.lon = obs_lon
observer.lat = obs_lat
observer.elevation = 75

while True:
    main()
    time.sleep(update_delay)
