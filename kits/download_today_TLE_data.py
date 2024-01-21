'''
Author : yunanhou

Date : 2023/11/26

Function : Download the current day's TLE data from the CelesTrak website
           https://celestrak.org/NORAD/elements/index.php?FORMAT=2le

Note: Note: These two download TLE data in two formats: 2LE and JSON.
      The standard TLE data format is as follows:

      STARLINK-1007
      1 44713U 19074A   23329.35222268  .00001777  00000+0  13823-3 0  9990
      2 44713  53.0554 336.5953 0001540  82.5266 277.5898 15.06386495222847

      The 2LE format omits the first line of standard TLE data and only retains the second and third lines, as follows:

      1 44713U 19074A   23329.35222268  .00001777  00000+0  13823-3 0  9990
      2 44713  53.0554 336.5953 0001540  82.5266 277.5898 15.06386495222847

      JSON format is the data after parsing standard TLE data into JSON format, as follows:

      [
        {
            "OBJECT_NAME": "STARLINK-1007",
            "OBJECT_ID": "2019-074A",
            "EPOCH": "2023-11-25T08:27:12.039552",
            "MEAN_MOTION": 15.06386495,
            "ECCENTRICITY": 0.000154,
            "INCLINATION": 53.0554,
            "RA_OF_ASC_NODE": 336.5953,
            "ARG_OF_PERICENTER": 82.5266,
            "MEAN_ANOMALY": 277.5898,
            "EPHEMERIS_TYPE": 0,
            "CLASSIFICATION_TYPE": "U",
            "NORAD_CAT_ID": 44713,
            "ELEMENT_SET_NO": 999,
            "REV_AT_EPOCH": 22284,
            "BSTAR": 0.00013823,
            "MEAN_MOTION_DOT": 1.777e-5,
            "MEAN_MOTION_DDOT": 0
        },
        ...
      ]

      Since h5 files cannot directly store data in JSON format, each JSON object needs to be converted into a string
      first and then stored in the h5 file. When reading data, the string needs to be converted into JSON before it can
      be used.
'''
import requests
import os
import h5py
from datetime import datetime
import json


# download the current day's TLE data from the CelesTrak website
def download_today_TLE_data(constellation_name):
    # h5 file path to save TLE data
    file_path = 'config/TLE_constellation/' + constellation_name + '/tle.h5'
    if not os.path.exists(file_path):
        with h5py.File(file_path, 'a') as file:
            pass
    # TLE data url
    url1 = "https://celestrak.org/NORAD/elements/gp.php?GROUP=" + constellation_name + "&FORMAT=2le"
    url2 = "https://celestrak.org/NORAD/elements/gp.php?GROUP=" + constellation_name + "&FORMAT=json"
    try:
        # send HTTP GET request
        response1 = requests.get(url1)
        # check if the request was successful
        response1.raise_for_status()
        # get web page TLE data and split the str by '\n'
        TLE = response1.text.split('\n')
        # delete the last row because it is a blank row with no data
        TLE.pop()

        response2 = requests.get(url2)
        if response2.status_code == 200:
            json_TLE = response2.json()
            # convert each JSON object to a string
            json_TLE = [json.dumps(item) for item in json_TLE]

        with h5py.File(file_path, 'a') as file:
            # get the current date and format it into 'yyyymmdd' format
            current_date = datetime.now()
            formatted_date = current_date.strftime('%Y%m%d')
            # if the group named with formatted_date does not exist, create a new group with the name
            # formatted_date, and write the obtained TLE data into the group.
            if file.get(formatted_date) is None:
                file.create_group(formatted_date)
                file[formatted_date].create_dataset(formatted_date + "-2LE", data=TLE)
                file[formatted_date].create_dataset(formatted_date + "-json", data=json_TLE)
                print("\t\t\t" , constellation_name + '\'s TLE data download was successful on ' + formatted_date + ' !')
            else:
                print('\t\t\tThe TLE data you downloaded already exists!')
    except requests.exceptions.RequestException as e:
        print(f"\t\t\tWhen downloading TLE data, an error occurred in the web page request: {e}")