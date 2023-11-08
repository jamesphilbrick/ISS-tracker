# AUTHOR: James Philbrick
# Initially created 15/06/2020, updated 08/11/2023

import urllib.request
import time
import math
from datetime import datetime
import ephem

SATELLITE_NAME = "ISS (ZARYA)"
TLE_SOURCE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle"
TLE_SOURCE_INTERVAL_HRS = 12
TLE_SOURCE_INTERVAL_SEC = float(60 * 60 * TLE_SOURCE_INTERVAL_HRS)
STORED_TLE = ("1 25544U 98067A   23312.38093591  .00013945  00000+0  24951-3 0  9994",
              "2 25544  51.6428 334.3064 0001085 100.8606  30.1667 15.50269558424151")
OBS_LON =  0.5406
OBS_LAT = 53.2307
OBS_ELEVATION = 75

def log(msg):
    print("[{}] {}".format(time.ctime(time.time()), msg))

def get_tle_url_status() -> str:
    req = urllib.request.Request(url=TLE_SOURCE_URL, headers={"User-Agent': 'Mozilla/5.0"})
    return urllib.request.urlopen(req).getcode()

def get_tle() -> tuple:
    req = urllib.request.Request(url=TLE_SOURCE_URL, headers={"User-Agent': 'Mozilla/5.0"})
    _ = urllib.request.urlopen(req)
    url_byte_array = _.read()
    _.close()
    url_content = url_byte_array.decode("utf8")
    url_content = url_content.splitlines(False)
    for idx, line in enumerate(url_content): 
        url_content[idx] = line.rstrip(" ")
    sat_idx = url_content.index(SATELLITE_NAME)
    tle_1 = url_content[sat_idx + 1]
    tle_2 = url_content[sat_idx + 2]

    return (tle_1, tle_2)

def varify_tle(tle: tuple) -> bool: # Function not currently used. 
    if (len(tle[0]) == 69) and (len(tle[1]) == 69):
        return True
    else: 
        return False


def calc_alt_az(tle: tuple) -> tuple:
    observer.date = datetime.utcnow()
    iss_loc = ephem.readtle(SATELLITE_NAME, tle[0], tle[1])
    iss_loc.compute(observer)
    alt = (iss_loc.alt * 180/math.pi)
    az = (iss_loc.az * 180/math.pi)

    return (alt, az)

def main():
    try:
        url_status = get_tle_url_status()
        log("Status = {}".format(url_status))
    except:
        log("Warning: Status exception when contacting {}".format(TLE_SOURCE_URL))

    log("Obtaining TLE from celestrak.org...")
    try: 
        tle = get_tle()
        log("TLE successfully obtained for {}".format(SATELLITE_NAME))
        log("Line 1 = {}".format(tle[0]))
        log("Line 2 = {}".format(tle[1]))
    except:
        log("Warning: Unable to source or parse TLE from {}".format(TLE_SOURCE_URL))
        try: 
            tle
            log("Warning: TLE not updated.")
            log(str(tle))
        except: 
            tle = STORED_TLE
            log("Warning: Using default TLE values: {}. Calculated position likely to be highly inaccurate.".format(STORED_TLE))
    
    alt_az = calc_alt_az(tle)
    log("Elevation & Azumith = {} & {} respectively (DEG).".format(alt_az[0], alt_az[1]))
    

if __name__ == "__main__":
    # difine observer
    observer = ephem.Observer()
    observer.lon = OBS_LON
    observer.lat = OBS_LAT
    observer.elevation = OBS_ELEVATION


    while True:
        main()
        time.sleep(TLE_SOURCE_INTERVAL_SEC - time.time() % TLE_SOURCE_INTERVAL_SEC)