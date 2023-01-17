import os
import scipy.io as scio
import pandas as pd
from tqdm import tqdm
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
import numpy as np
import math
from skyfield.api import EarthSatellite,load, wgs84
from skyfield.elementslib import osculating_elements_of
from pytz import timezone
from matplotlib.colors import cnames
from multiprocessing import Pool
import statsmodels.api as sm
from matplotlib.pyplot import MultipleLocator
from multiprocessing import Pool
import matplotlib.dates as mdates
from utils import *
import random
rand=math.floor(random.random()*10000000)+1000
date=datetime.now().timestamp()
#print(date)
pos_path='.\\satellites_pos\\'
UTC = timezone('UTC')
d=3600
starttime = datetime.strptime("2021-12-1 0:0:0", "%Y-%m-%d %H:%M:%S")
endtime = datetime.strptime("2021-12-5 2:0:0", "%Y-%m-%d %H:%M:%S")
#print(starttime.timestamp())
delta_time = (endtime - starttime).days * 24 * 3600 + (endtime - starttime).seconds
t = starttime  # + timedelta(seconds=seconds)
ts = load.timescale()
t = UTC.localize(t)
t_s = ts.from_datetime(t)
#t_s=
#print(t_s)
INF = 99999
from functools import cmp_to_key


'''def get_pos_per_sat():
    tle='.\\TLE\\test'
    heights, lat_, lng_ = [], [], []
    for root, dirs, files in os.walk(tle):
        for file in files:
            print(file)
            sattle = pd.read_csv(tle+"\\"+file)
            sattle['EPOCH'] = sattle['EPOCH'].astype('datetime64[ns]')
            sattle = sattle.sort_values(by="EPOCH")
            #with open(file,'r') as f:
            file=file.split('.')
            fname=pos_path+file[0]+'.txt'
            with open(fname,'w',encoding='UTF-8') as pos_file:
                for seconds in range(0, delta_time, d):
                    t = starttime + timedelta(seconds=seconds)
                    temp = sattle[(sattle['EPOCH'] < t)]
                    if len(temp) == 0:
                        s = str(INF) + ',' + str(INF) + ',' + str(INF) + '\n'
                        print('sat: ', file[0], 'time: ', t, 's: ', s, ', the sat is not exist in this time slot...')
                        pos_file.write(s)
                        continue
                    temp = temp.sort_values(by="EPOCH")
                    begin_tle = temp.loc[temp.index[-1]]
                    #print('t = ', t, )
                    Satellite = EarthSatellite(str(begin_tle['TLE_LINE1']), str(begin_tle['TLE_LINE2']), 'ISS (ZARYA)', ts)
                    t = UTC.localize(t)
                    t_s = ts.from_datetime(t)
                    geocentric = Satellite.at(t_s)
                    height = wgs84.height_of(geocentric)
                    heights.append(height.km)
                    lat, lon = wgs84.latlon_of(geocentric)
                    lat_.append(lat.degrees)
                    lng_.append(lon.degrees)
                    s = str(lat.degrees) + ',' + str(lon.degrees) + ',' + str(height.km) + ','
                    pos_file.write(s)
                pos_file.close()
get_pos_per_sat()'''
'''    with open(tle_path,'r') as tle_file:
        heights, lat_, lng_ = [], [], []
        #sattle = pd.read_csv(tlepath + str(sat) + '.csv')
        #sattle['EPOCH'] = sattle['EPOCH'].astype('datetime64[ns]')
       # sattle = sattle.sort_values(by="EPOCH")


        s = ''
        #fname = open('.\\satellites_pos\\pos.txt','w',encoding='UTF-8')
        fname=None
        with open(tle_path, 'r') as f:
            name=None
            tle_line1=None
            tle_line2=None
            for line in f:
                if line[0]!='1' and line[0]!='2':
                    name=line[0:-1]
                    fname=open('.\\satellites_pos\\'+name+'_pos.txt','w',encoding='UTF-8')
                    #fname.write(name)
                    #fname.write('\n')
                    continue
                if line[0]=='1':
                    tle_line1=line
                    continue
                else:
                    tle_line2=line
                Satellite = EarthSatellite(tle_line1, tle_line2,'ISS (ZARYA)', ts)
                for seconds in range(0, delta_time, d):
                    t = starttime + timedelta(seconds=seconds)
                    t = UTC.localize(t)
                    t_s = ts.from_datetime(t)
                    geocentric = Satellite.at(t_s)
                    height = wgs84.height_of(geocentric)
                    heights.append(height.km)
                    lat, lon = wgs84.latlon_of(geocentric)
                    lat_.append(lat.degrees)
                    lng_.append(lon.degrees)
                    s=str(lat.degrees)+','+str(lon.degrees)+','+str(height.km)+','
                    fname.write(s)
                #fname.write('\n')
                fname.close()
            f.close()
'''

'''fname='.\\satellites_pos'
for root,dirs,files in os.walk(fname):
    for file in files:
        if file=='BLUEWALKER 3 _pos.txt':
            print(file)'''