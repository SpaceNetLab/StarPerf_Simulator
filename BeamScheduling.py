import copy
import networkx as nx
import scipy.io as scio
import numpy as np
import math
import h3
import json
import pandas as pd
import time
import os
from get_SatPos_from_TLE import *
from geographiclib.geodesic import Geodesic
#The global parameters users can set
TLE=False#whether to use TLE data
IGNOREGSO=True#Whether to ignore GSO impact
provisionedRate=2#provision
SIMSPREAD=0#Number of beam tilts
STEERING_ANGLE=25
LIMITISLSATCAPACITY=False#Whether to limit ISL satellites' capacity,if True, ISL satllites' capacity/10
LIMITLINKS=False#Whether to limit gateway's antenna
GSOPROTECTION=10#GSO Protection‘parameter
GWMULTIPLIER=2#gateway's antenna multiplier
MINGWCAPACITY=25#The minimum gateway's capacity,unit is 'Gbps'
MAXGWCAPACITY=32#The maximum gateway's capacity
COUNTRY_LIST=['China']#Countries users want to sim
SIMMAXPOPULATION=20000#User-defined cell maximum population number in simulation
SIMMINPOPULATION=0#User-defined cell minimum population number in simulation
MAXBEAMCAPACITY=700#The maximum capacity of each beam, default 700Mbps
SIMTDM=1#time division multiplexing:1,0.75,0.5,0.25
SIMBEAMSPERCELL=1#The maximum beams assigned to each cell
MPDLSPOTBEASMS=0#After adding time division multiplexing, how many beams does each satellite have on the surface, in fact, a satellite has a maximum of 48 beams
SIMMODE='prio_nadir'#Simulation modes:'prio_slant'(from outside to inside) ,'prio_nadir'(from inside to outside)
#sat_station=[]
orbit_num=72#The number of constellation's orbit
sat_per_orbit=22#The number of satelltes on each orbit
time_in=0#simulation time slice(from 0 to cycle-1)

#global parameters
SIMCELLCOUNTS=0#The number of simulated cells
SIMACTIVECELLCOUNT=0#Actual number of cells being served
AVERAGECAPACITY=0#Actual average capacity
MAXCAPACITY=0#Actual max capacity
ACTMAXCELLCAPACITY=0#Actual max cell capacity
ACTMINCELLCAPACITY=1000000#Actual min cell capacity
MAXPOPULATION=0#Actual minimum population in simcells
MINPOPULATION=10000000#Actual maximum population in simcells,tha maximum is 10000000
BEAMCAPACITY=0#
MAXCELLCAPACITY=0
_MS_IN_A_DAY = 86400000
TIMESTAMP=1668235691621
RAANchangePerSec = -0.0000519575
node_num = orbit_num*sat_per_orbit
cycle=5731#satellite orbit period
R=6371#Earth radius(km)
#TLE=False
GRAPH_ISL=nx.Graph()#ISL graph
#TLE=True
ISL={}
ISLChains={}
isllinks={}
crossPlaneISL={}

sat=[]
Satellites={}
launch= {}
satelliteNames=set()
active_cells_info=[]#information from "[country].json"
simH3=set()#All h3ids in countries with resolution 5
simcells={}#The cells that need to be allocated beams are screened out according to the custom population range, and the h3id is obtained from '[country].json'，{'h3id':item['properties']['h3id'],'capacity':0,'uts':0,'simcell_num':count,'beamid':None,'beamcount':0,'serving_sats':None}
hexIntersect=set()#countries' boundaries' hex
simCellIDs=set()#parent h3id in simcells{} with resolution 3
simCellSats={}#cell's serving sats
simCellBeams={}#cell's beam count
simCellCapacity={}#cell's assigned capacity
simCellLinks={}#cell's serving links
simSats={}#serving sats
hexUpdates=set()#The no. of sats that can be served over the countries
haveGatewaysSats=set()#The number of sats that can be landed directly（connected to a certain gateway directly)
ISLsats=set()#The sats'no.(from 0-node_num-1) that cannot be directly landed in hexUpdates() but can serve through ISLs
simCelllocation_cbf={}#cells'location
simActiveCells=[]#Filtered cells that can be served

totalISLSats=0
#Pre work:load data
def load_country_json():
    for item in COUNTRY_LIST:
        file_name='.\\countries_json\\'+item+'.json'
        with open(file_name,'r') as fp:
            json_data=json.load(fp)
            global active_cells_info
            active_cells_info=copy.deepcopy(json_data['features'])
def load_launch_json():
    launch_path=".\\satellites_info_json\\launch.json"
    with open(launch_path,'r') as fp:
        json_data=json.load(fp)
        global launch
        for item in json_data:
            launch[item['launch']]=item
            #print(type(item['launch']))

#def load_station():

def load_hexIntersect():
    addcell=False
    count=0
    cellcount=0
    global MINPOPULATION,SIMCELLCOUNTS,SIMH3,SIMMAXPOPULATION,SIMMINPOPULATION,MAXPOPULATION,simcells,simCellSats,simCellBeams,simCellCapacity,simCellLinks,simCellIDs,hexIntersect,active_cells_info
    for item in active_cells_info:
        #print('item')
        addcell=False
        population=item['properties']['population']
        if population>=SIMMINPOPULATION and population<=SIMMAXPOPULATION:
            addcell=True
        if population>=SIMMINPOPULATION and SIMMAXPOPULATION==1000000:
            addcell=True
        if addcell:
            cellcount+=1
            h3id=item['properties']['h3id']
            if population>MAXPOPULATION:
                MAXPOPULATION=population
            if population<MINPOPULATION:
                MINPOPULATION=population
            tmp={'h3id':h3id,'capacity':0,'uts':0,'simcell_num':count,'beamid':None,'beamcount':0,'serving_sats':None}
            simcells[h3id]=tmp
            simH3.add(h3id)
            simCellSats[h3id]=[]
            simCellBeams[h3id]=0
            simCellCapacity[h3id]=0
            simCellLinks[h3id]=[]
            parent=h3.cell_to_parent(h3id,3)
            simCellIDs.add(parent)
            basecell=h3.cell_to_parent(h3id,1)
            hexIntersect.add(basecell)
        count+=1
    SIMCELLCOUNTS=cellcount

#load gateways'data
gateway_path='.\\starlink_gateway\\gw.txt'
gateway_file=open(gateway_path,'r')
gateway={}
count=1
file_count=0
tmp={}
for line in gateway_file:
    line=line.replace(' ','')
    line=line.replace('"','')
    line=line.replace(',','')
    line=line.replace('\n','')
    if count!=1 and count!=0:
        line=line.split(':')
        if line[0]=='numAntennas' or line[0]=='uplinkGhz' or line[0]=='downlinkGhz' or line[0]=='minElevation' or line[0]=='lat' or line[0]=='lng' or line[0]=='mincapacity' or line[0]=='maxcapacity' or line[0]=='cpd' or line[0]=='links':
            line[1]=float(line[1])
        tmp[line[0]]=line[1]
    if count==0:
        gateway[file_count]=tmp
        tmp={}
        file_count+=1
    count+=1
    count%=18
gw_pos=[]
for key,value in gateway.items():
    gw_pos.append([float(value['lat']),float(value['lng'])])
gw_length = len(gw_pos)


#load satellites'data
dataFile = '.\\matlab_code\\StarLink\\position.mat'
data = scio.loadmat(dataFile)
pos_all = data['position']
dataFile = '.\\matlab_code\\StarLink\\position.mat'
data = scio.loadmat(dataFile)
pos_cbf=data['position_cbf']
#load delay to construct ISLs
Delay=None
cycle=5760#can change
tle_satname=[]
tle_lat=[]
tle_lng=[]
tle_alt=[]
stations={}
shellOrientation={}
shellStats={}
shells={}
orbitalChartData={}
orbitalBarData={}
def load_delay(time_in):
    global Delay
    f_delay = scio.loadmat('.\\matlab_code\\StarLink\\delay\\' + str(time_in+1) + '.mat')
    data = f_delay['delay']
    Delay=data
def get_epochTimeStamp(tle1):
    components=tle1.split(' ')
    epochYear=int(components[3][0:2])
    epochDay=float(components[3][2:14])
    return dayOfYearToTimeStamp(epochDay,epochYear)
def dayOfYearToTimeStamp(epochDay,epochYear):
    yearStart=datetime.strptime("20"+str(epochYear)+ "-01-01 0:0:0", "%Y-%m-%d %H:%M:%S")
    yearStartMS=yearStart.timestamp()
    ts=math.floor(yearStartMS+(epochDay-1)*_MS_IN_A_DAY)
    return ts
def get_semiMagorAxis(motion):
    a=pow(398600441800000,1/3)/pow(2*math.pi*motion/86400,2/3)
    sMA=a/1000-6378.137
    return sMA
def loadShells():
    global shellOrientation,shellStats,orbitalBarData,orbitalChartData,shells
    shell_path='.\\satellites_info_json\\shells.json'
    with open(shell_path,'r') as f:
        json_data=json.load(f)
        for item in json_data:
            shellid=int(item['shellid'])
            shells[shellid]=item
            shellOrientation[shellid]={}
            shellStats[shellid]={}
            orbitalChartData[shellid]=[]
            orbitalBarData[shellid]=[]
        shell_len=len(shells)+1
        for i in range(1,shell_len):
            for j in range(0,361):
                shellOrientation[i][j]=[]
                shellStats[i][j]=[]


#------------------------------------------------Tool functions-------------------------------------------------------#
def to_cbf(lat_long,length):
    cbf=[]
    radius=6371
    for num in range(0,length):
        cbf_in=[]
        # d=radius*math.cos(math.radians(float(lat_long[num][0]))) # latitude\n",
        z=radius*math.sin(math.radians(float(lat_long[num][0])))
        x=radius*math.cos(math.radians(float(lat_long[num][0])))*math.cos(math.radians(float(lat_long[num][1])))
        y=radius*math.cos(math.radians(float(lat_long[num][0])))*math.sin(math.radians(float(lat_long[num][1])))
        cbf_in.append(x)
        cbf_in.append(y)
        cbf_in.append(z)
        cbf.append(cbf_in)
    return cbf
def cal_simcellslocation_cbf():
    global simCelllocation_cbf,active_cells_info
    location=[]
    for item in active_cells_info:
        tmp=[item['properties']['lat'],item['properties']['lng']]
        location.append(tmp)
    cbf=to_cbf(location,len(location))
    count=0
    for i in active_cells_info:
        simCelllocation_cbf[i['properties']['h3id']]={'lat':i['properties']['lat'],'lng':i['properties']['lng'],'x':cbf[count][0],'y':cbf[count][1],'z':cbf[count][2]}
        count+=1
def quadrant(satlat,satlng,eslat,eslng,az):
    pts=[]
    pts.append(satlat)
    pts.append(satlng)
    pte=[]
    pte.append(eslat)
    pte.append(eslng)
    xdiff=pte[0]-pts[0]
    ydiff=pte[1]-pts[1]
    if xdiff>=0 and ydiff>=0:
        return 180-az
    if xdiff>=0 and ydiff<0:
        return 360+az
    if xdiff<0 and ydiff>=0:
        return 180-az
    return az
def cal_lookAnglesNGSO(satlat,satlng,gwlat,gwlng,alt):
    R=6378.15
    Rn=R+alt
    alphag=math.radians(satlat)
    #delta_lng=satlng-gwlng
    delta_lamdag=math.radians(satlng-gwlng)
    delta_phig=satlat-gwlat
    phi=math.radians(gwlat)
    gammag=math.acos(math.sin(phi)*math.sin(alphag)+math.cos(phi)*math.cos(alphag)*math.cos(delta_lamdag))
    dg=math.sqrt(R*R+Rn*Rn-2*R*Rn*math.cos(gammag))
    look_elevation=math.degrees(math.acos(Rn/dg*math.sin(gammag)))
    look_azimuth=0
    look_azimuth=math.degrees(math.asin(math.cos(alphag)*math.sin(delta_lamdag)/math.sin(gammag)))
    corrected_look_azimuth=quadrant(satlat,satlng,gwlat,gwlng,look_azimuth)
    if corrected_look_azimuth<0:
        corrected_look_azimuth=corrected_look_azimuth+360
    ret= {}
    ret['az']=corrected_look_azimuth
    ret['el']=look_elevation
    return ret
def gsoLongitude(eslat,az):
    a=math.radians(eslat)
    azr=math.radians(az-100)
    bg=math.atan(math.tan(azr)*math.sin(a))
    return math.degrees(bg)
def lookAnglesGSODelta(satlng,eslat,eslng):
    if eslat==0:
        eslat=eslat+0.0001
    eslng=eslng*(-1)
    look_azimuth=math.acos(-math.tan(eslat*0.0174532925)/math.tan(math.acos(math.cos(eslat*0.0174532926)*math.cos(abs(satlng-eslng)*0.0174532925))))*57.2957795
    look_elevation = math.atan((math.cos(math.acos(math.cos(eslat * 0.0174532926) * math.cos(abs(satlng - eslng) * 0.0174532925))) - 0.15116) / math.sin(math.acos(math.cos(eslat * 0.0174532926) * math.cos(abs(satlng - eslng) * 0.0174532925)))) * 57.2957795
    if satlng-eslng>0:
        look_azimuth=360-look_azimuth
    if satlng-eslng>180:
        look_azimuth=360-look_azimuth
    if satlng-eslng<-180:
        look_azimuth=360-look_azimuth
    ret={'az':look_azimuth,'el':look_elevation}
    return ret
def lookAnglesGSO(satlng,eslat,eslng):
    ag=math.radians(satlng-eslng)
    b=math.radians(eslat)
    look_azimuth=180+math.degrees(math.atan(math.tan(ag)/math.sin(b)))
    if eslat<0:
        look_azimuth=look_azimuth-180
    if look_azimuth<0:
        look_azimuth=look_azimuth+360
    r1=1+35786/6378.15
    v1=r1*math.cos(b)*math.cos(ag)-1
    v2=r1*math.sqrt(1-math.cos(b)*math.cos(b)*math.cos(ag)*math.cos(ag))
    look_elevation=math.degrees(math.atan(v1/v2))
    ret={'az':look_azimuth,'el':look_elevation}
    return ret
def lookAnglesNGSO(satlat,satlng,eslat,eslng,alt):
    Re=6378.15
    Rn=Re+alt
    ag=math.radians(satlat)
    bg=math.radians(satlng-eslng)
    cg=satlat-eslat
    e=math.radians(eslat)
    fg=math.acos(math.sin(e)*math.sin(ag)+math.cos(e)*math.cos(ag)*math.cos(bg))
    dg=math.sqrt(Re*Re-Rn*Rn-2*Re*Rn*math.cos(fg))
    look_elevation=math.degrees(math.acos(Rn/dg*math.sin(fg)))
    look_azimuth=0
    look_azimuth=math.degrees(math.asin(math.cos(ag)*math.sin(bg)/math.sin(fg)))
    corrected_look_azimuth=quadrant(satlat,satlng,eslat,eslng,look_azimuth)
    if corrected_look_azimuth<0:
        corrected_look_azimuth=corrected_look_azimuth+360
    ret={'az':corrected_look_azimuth,'el':look_elevation}
    return ret
def clarkInterference(eslat,eslng,az,el,pa,satlat,satlng):
    global IGNOREGSO
    if IGNOREGSO:
        return {'blocked':False,'gsolng':0,'gsoaz':0,'gsoel':0}
    blocked=False
    gsolng=0
    look_elevation=0
    look_azimuth=0
    gsolng=gsoLongitude(eslat,az)
    gsolng-=eslng
    la=lookAnglesGSODelta(gsolng,eslat,eslng)
    look_elevation=la['el']
    look_azimuth=la['az']
    azdiff=abs(round(look_azimuth-az))
    if look_elevation>7:
        if el<=look_elevation+pa and el>=look_elevation-pa and azdiff<18:
            blocked=True
        elif (el>look_elevation+pa or el<look_elevation-pa) and azdiff==0 and satlat>=15:
            return {'blocked':blocked,'gsolng':gsolng,'gsoaz':look_azimuth,'gsoel':look_elevation}
    if not blocked:
        gsolng=0
        delta=0.1
        direction='-'
        paz=1
        if eslat<15 and eslat>0:
            paz=10-eslat
        if eslat>-15 and eslat<0:
            paz=19-abs(eslat)
        if eslng>=satlng:
            direction='+'
        for h in range(1000):
            testlng=0
            if direction=='+':
                testlng=gsolng+delta*h
            else:
                testlng=gsolng=delta*h
            if testlng==0:
                testlng+=0.0001
            if testlng>100 or testlng<-100:
                break
            la=lookAnglesGSODelta(testlng,eslat,0)
            d_el=la['el']
            d_az=la['az']
            if d_el<7:
                break
            if d_el>=7:
                if el<=d_el+pa and el>=d_el-pa and az<=d_az+paz and az>=d_az-paz:
                    blocked=True
                    look_azimuth=d_az
                    look_elevation=d_el
                    break
            if abs(d_az-az)>5:
                delta=delta*1.1
    return {'blocked':blocked,'gsolng':gsolng,'gsoaz':look_azimuth,'gsoel':look_elevation}

def cal_distance(x1,y1,z1,x2,y2,z2):
    return math.sqrt(np.square(x1-x2)+np.square(y1-y2)+np.square(z1-z2))
def getDistance(lat1,lng1,lat2,lng2):
    R=6378.137
    radlat1=math.radians(lat1)
    radlat2=math.radians(lat2)
    a=radlat1-radlat2
    b=math.radians(lng1)-math.radians(lng2)
    s=2*math.asin(math.sqrt(pow(math.sin(a/2),2)+math.cos(radlat1)*math.cos(radlat2)*pow(math.sin(b/2),2)))
    s=s*R
    return s
COUNT=0
def isCellCovered(h3id,sid):
    if TLE==False:
        sid=sid
    else:
        sid=stations[sid]['index']
    lat1=sat[sid]['lat']
    lng1=sat[sid]['lng']
    lat2=simCelllocation_cbf[h3id]['lat']
    lng2=simCelllocation_cbf[h3id]['lng']
    #dis=cal_distance(x1,y1,z1,x2,y2,z2)
    dis=getDistance(lat1,lng1,lat2,lng2)
    if dis<sat[sid]['coverage']:
        la=cal_lookAnglesNGSO(sat[sid]['lat'],sat[sid]['lng'],simCelllocation_cbf[h3id]['lat'],simCelllocation_cbf[h3id]['lng'],sat[sid]['alt'])
        if la['el']>=STEERING_ANGLE:
            #有个clarkeInterference
            ci=clarkInterference(lat2,lng2,la['az'],la['el'],GSOPROTECTION,lat1,lng1)
            if not ci['blocked']:
                return {'az':la['az'],'el':la['el'],'distance':dis}
    return {}
def getSteeringAngle(altitude,angle):
    steering_angle=math.asin(R/(R+altitude)*math.cos(math.radians(angle)))
    return math.degrees(steering_angle)
def getSlant(altitude,steering_angle):
    a=math.radians(steering_angle)
    theta=math.asin(math.sin(a)*((R+altitude)/R))-a
    slant_distance=R*math.sin(theta)/math.sin(a)
    return slant_distance

def getHexRing(centerCell,ringCount):
    cells=None
    try:
        cells=h3.grid_ring(centerCell,ringCount)
    except:
        return None
def getCoverage(altitude,angle):
    steering_angle=math.asin(R/(R+altitude)*math.cos(math.radians(angle)))
    beta=math.radians(90)-steering_angle-math.radians(angle)
    area=2*math.pi*40589641*(1-math.cos(beta))#这里硬编码了个不知道啥玩意
    arc_distance=math.sqrt(area/math.pi)
    return arc_distance
def getSteeringCoverage(altitude,steering_angle):
    theta=math.asin(math.sin(math.radians(steering_angle)))
    theta_deg=math.degrees(theta)
    beta=math.radians(90)-math.radians(steering_angle)
    min_elevation=math.degrees(beta)
    arc_distance=theta*R
    return arc_distance
def generateSpotbeam(lat,lng,angle,beamwidth,alt=550,beam_azimuth=0,eccentricity=1,cell=False,celllat=0,celllng=0,stepsize=5):
    steering_angle=getSteeringAngle(alt,angle)
    coords=[]
    cp=[lat,lng]
    #generate ellipse points
    s=math.radians(steering_angle)
    alpha=math.radians(beamwidth/2)
    rEc=(R+alt)/R
    thetaNear=math.asin(math.sin(s-alpha)*rEc)-(s-alpha)
    thetaFar=math.asin(math.sin(s+alpha)*rEc)-(s+alpha)
    distNear=thetaNear*R
    distFar=thetaFar*R
    smaxAxis=(distFar-distNear)/2*(eccentricity*math.pow(1.007,steering_angle))
    slant=alt
    if steering_angle>0:
        slant=getSlant(alt,steering_angle)
    coverage=getSteeringCoverage(alt,steering_angle)
    sminAxis=getSteeringCoverage(slant,beamwidth)/2
    #calculate displacement
    b=math.radians(180-(90-steering_angle-beamwidth/2))
    a=slant/math.sin(b)*math.sin(alpha)
    adjust=smaxAxis-a
    divisor=eccentricity*math.pow(1.015,steering_angle)
    #get coverage latitude for distance correction
    geo_dict=Geodesic.WGS84.Direct(cp[0],cp[1],beam_azimuth,coverage*1000,1929)
    dstCp=[geo_dict['lat2'],geo_dict['lon2']]
    avgLat=(lat+dstCp[0])/2
    centerDelta=(coverage+adjust/divisor)/math.cos(math.radians(avgLat))
    #calculate the coordinates of the displaced point's center
    '''centerLat=OBESERVER_LAT
    centerlng=OBESERVER_LNG'''#这里全局变量，估计是显示在页面上，可以不用
    centerLat=41.5
    centerLng=1.9
    if cell:
        centerLat=celllat
        centerLng=celllng
    majorX=smaxAxis/(R*math.cos(math.pi*sminAxis/180))
    minorY=sminAxis/R
    newCp=[centerLat,centerLng]
    #generate the ellipse path
    for d in range(0,360,stepsize):
        x=sminAxis*math.cos(math.radians(d))*1000
        y=smaxAxis*math.sin(math.radians(d))*1000
        h=math.sqrt(x*x+y*y)
        if y==0:
            continue
        sa=math.degrees(math.atan(abs(x)/abs(y)))
        if d<90:
            sa=90-sa
        if d>=90 and d<180:
            sa+=90
        if d>=180 and d<270:
            sa=270-sa
        if d>=270 and d<360:
            sa=270+sa
        geo_dict=Geodesic.WGS84.Direct(newCp[0],newCp[1],sa,h,1929)
        pWpt=[geo_dict['lat2'],geo_dict['lon2']]
        plon=pWpt[1]
        plat=pWpt[0]
        coords.append([plon,plat])
    return coords

#----------------------------------------------------core functions-----------------------------------------------------#
def get_stations(t_s):#[lat,lon,height,lat,lon,height......]
    tle_path='.\\TLE\\satellites_TLE.txt'
    global satelliteNames,stations,shellStats,shellOrientation,shells
    with open(tle_path,'r') as fp:
        tle_line1=None
        tle_line2=None
        tmp=[]
        name=None
        for line in fp:
            if line[0:8]=='STARLINK':
                line=line.replace(' ','')
                line = line.replace('\n', '')
                satelliteNames.add(line)
                tmp=line.split('-')
                stations[tmp[1]]={}
                name=line
                #print(tmp)
                #continue
            #elif line[0] == '1':
                line=fp.readline()
                '''line=line.replace('   ',' ')
                line=line.replace('\n','')
                line=line.replace('  ',' ')'''
                tle_line1 = line
                #continue
            #elif line[0] == '2':
                line=fp.readline()
                '''line = line.replace('   ', ' ')
                line = line.replace('\n', '')
                line = line.replace('  ', ' ')'''
                tle_line2 = line
            else:
                tle_line1 = None
                tle_line2 = None
                tmp = []
                name = None
                continue
            sid = tmp[1]
            Satellite = EarthSatellite(tle_line1, tle_line2)#, 'ISS (ZARYA)')
            geocentric = Satellite.at(t_s)
            lat, lng = wgs84.latlon_of(geocentric)
            lat = lat.degrees
            lng = lng.degrees
            #print(type(lat), lng)
            alt = wgs84.height_of(geocentric).km
            if np.isnan(lat) or np.isnan(lng) or alt<0:
                continue
            stations[sid]['tle1'] = tle_line1
            stations[sid]['tle2'] = tle_line2
            tle_line1 = tle_line1.replace('   ', ' ')
            tle_line1 = tle_line1.replace('\n', '')
            tle_line1 = tle_line1.replace('  ', ' ')
            tle_line2 = tle_line2.replace('   ', ' ')
            tle_line2 = tle_line2.replace('\n', '')
            tle_line2 = tle_line2.replace('  ', ' ')

            line1=tle_line1.split(' ')
            launchID=line1[2][0:5]

            inclination=53.2
            satVersion='v1.5'
            satShell=0
            satGen=1
            #print(type(launch.keys()))
            if launchID in launch.keys():
                inclination=launch[launchID]['inclination']
                satVersion=launch[launchID]['version']
                satShell=launch[launchID]['shell']
                satGen=launch[launchID]['gen']

            hasFailed=False
            if satShell==0:
                continue#这里有个satShell=0的情况，下面别忘了判断

            stations[sid]['satnum'] = sid  # 字符串

            deltaShell=10000
            satType='normal'
            status='OPERATIONAL'
            if not hasFailed:
                components=tle_line2.split(' ')
                longitudeAscendingNode=float(components[3])
                argumentOfPerigee=float(components[5])
                anomaly=float(components[6])
                motion=float(components[7])
                semiMajorAxis=get_semiMagorAxis(motion)
                deltaShell=round(launch[launchID]['altitude']-semiMajorAxis,1)
                eccentricity=round(float('0.'+components[4])*10000,2)
                degPerSec=360*motion/86400
                epochTimeStamp=get_epochTimeStamp(tle_line1)
                secondsInPast=math.floor((TIMESTAMP-epochTimeStamp)/1000)
                cAPAN=(argumentOfPerigee+anomaly+degPerSec*secondsInPast+360)%360
                cLOAN=(longitudeAscendingNode+RAANchangePerSec*secondsInPast+360)%360
                cAPANr=math.floor(cAPAN)
                cLOANr=round(cLOAN)
                #这里可以有fakemode
                if deltaShell>15:
                    satType='off'
                    status='OUT OF ALTITUDE'
                elif abs(deltaShell)<=15 and abs(deltaShell)>4:
                    satType='off'
                    status='POSITIONING'
                orbitalEntry={'no':int(tmp[1][0:4]),'sat':name,'sid':sid,'cAPANr':cAPANr,'cAPAN':cAPAN,'alt':round(alt),'sMA':semiMajorAxis,'version':satVersion,'shell':satShell,'gen':satGen,'deltaShell':deltaShell,'ecc':eccentricity,'status':status,'type':satType}
                if cLOANr>=0 and satShell>0:
                    shellOrientation[satShell][cLOANr].append(orbitalEntry)
                    shellStats[satShell][cLOANr].append(cAPANr)
            else:
                satType='off'
                status='FAILED'
            if satVersion=='v1.5' or satVersion=='v2.0':
                global totalISLSats
                totalISLSats+=1
            if status=='OPERATIONAL':
                coverage=getCoverage(alt,STEERING_ANGLE)
                h3id=h3.latlng_to_cell(lat,lng,1)
                satMaker={'name':name,'satid':stations[sid]['satnum'],'lat':lat,'lng':lng,'altitude':alt,'coverage':coverage,'type':satType,'serving':'NO GATEWAY LINK','gatewayuuid':None,'gwslant':0,'utcoverage':False,'utslant':0,'utaz':0,'utel':0,'servingpt':None,'shell':satShell,'failed':hasFailed,'status':status,'loan':'N/A','apan':'N/A','geometry':None,'inclination':inclination,'version':satVersion,'launchid':launchID,'isl':0,'islchain':None,'islvia':None,'updated':ts,'visible':True,'active':False,'h3id':h3id,'h3cells':None,'capacity':0,'beams':0,'startring':None,'endring':None}
                stations[sid]=satMaker
            else:
                coverage=0
                h3id=h3.latlng_to_cell(lat,lng,1)
                satMaker={'name':name,'satid':stations[sid]['satnum'],'lat':lat,'lng':lng,'altitude':alt,'coverage':coverage,'type':satType,'serving':'NO GATEWAY LINK','gatewayuuid':None,'gwslant':0,'utcoverage':False,'utslant':0,'utaz':0,'utel':0,'servingpt':None,'shell':satShell,'failed':hasFailed,'status':status,'loan':'N/A','apan':'N/A','geometry':None,'inclination':inclination,'version':satVersion,'launchid':launchID,'isl':0,'islchain':None,'islvia':None,'updated':ts,'visible':True,'active':False,'h3id':h3id,'h3cells':None,'capacity':0,'beams':0,'startring':None,'endring':None}
                stations[sid]=satMaker
def generatePlaneStats():
    global orbitalChartData,stations,orbitalBarData
    length=len(shells)
    for ic in range(1,length):
        foundPos=0
        foundVal=0
        minVal=0
        filledPlanes=[]
        planeSlots=[]
        planeData=[]
        slotSpacing=shells[ic]['slotspacing']
        shellAlt=shells[ic]['altitude']
        maxsMA=shellAlt+4
        maxPos=shellAlt+15
        #get list of all planes with at least one satellite in
        for j in range(361):
            if len(shellStats[ic][j])>0:
                filledPlanes.append(j)
        for i in range(len(filledPlanes)-2):#这里有改了一下下标范围
            if (filledPlanes[i+2]-filledPlanes[i+1]==5) and (filledPlanes[i+1]-filledPlanes[i]==5):
                foundPos=i
                foundVal=filledPlanes[i]
                break
        for i2 in range(foundVal,0,-5):
            minVal=i2
        #generate slots
        for i3 in range(minVal,361,5):
            planeSlots.append(i3)
        for j1 in range(0,361):
            if len(shellStats[ic][j1])>0:
                oS=0
                oA=0
                OK=0
                PS=0
                shellStats[ic][j1].sort()
                #work out the standard deviation
                foundPos=0
                foundVal=0
                minVal=0
                orbitalSlots=[]
                count=len(shellStats[ic][j1])-1
                for i in range(count):
                    if shellStats[ic][j1][i+1]-shellStats[ic][j1][i]==slotSpacing:
                        foundPos=i
                        foundVal=shellStats[ic][j1][i]
                        break
                #find starting slot
                for i4 in range(foundVal,0,-slotSpacing):
                    minVal=i4
                #generate orbital slots for this plane
                for i5 in range(minVal,361,slotSpacing):
                    orbitalSlots.append(i5)
                #fakemode 不管
                for item in shellOrientation[ic][j1]:
                    operational='YES'
                    status='OUT OF SLOT'
                    #status='OPERATIONAL'
                    diff=0
                    if item['status']=='POSITIONING':
                        status='POSITIONING'
                    if item['status']=='OUT OF ALTITUDE':
                        status='OUT OF ALTITUDE'
                    if item['status']=='OPERATIONAL':
                        status='OPERATIONAL'
                        '''for slot in orbitalSlots:
                            diff=abs(item['cAPAN']-slot)
                            if diff<=2:
                                status='OPERATIONAL'
                                return False'''
                    status='OPERATIONAL'
                    entry={'x':j1,'y':item['cAPANr'],'value':1,'sat':item['sat'],'sid':item['sid'],'alt':item['alt'],'op':operational,'status':status}
                    orbitalChartData[ic].append(entry)
                    if item['sid'] in stations:#stations的键值是字符串
                        stations[item['sid']]['type']='normal'
                        stations[item['sid']]['status']=status
                        stations[item['sid']]['loan']=j1
                        stations[item['sid']]['apan']=item['cAPANr']
                    if status=='OUT OF SLOT':
                        oS+=1
                    if status=='OUT OF ALTITUDE':
                        oA+=1
                    if status=='OPERATIONAL':
                        OK+=1
                    if status=='POSITIONING':
                        PS+=1
                orbitalBarData[ic].append({'plane':j1,'ok':OK,'oa':oA,'os':oS,'ps':PS,'none':0})
        #print(len(orbitalChartData[ic]))
def generateISL():
    global orbitalChartData, stations, orbitalBarData,ISL,ISLChains,stations,ISLsats,isllinks,crossPlaneISL
    length = len(shells)
    for ic in range(1, length):
        idx=None
        for i1 in range(len(orbitalChartData[ic])):
            if orbitalChartData[ic][i1]['status']=='OPERATIONAL' or orbitalChartData[ic][i1]['status']=='OUT OF SLOT':
                idx=str(ic)+'_'+str(orbitalChartData[ic][i1]['x'])
                if idx not in ISL:
                    ISL[idx]=[]
                ISL[idx].append({'plane':orbitalChartData[ic][i1]['x'],'slot':orbitalChartData[ic][i1]['y'],'sid':orbitalChartData[ic][i1]['sid']})
                #print(orbitalChartData[ic][i1]['sid'],stations[ISL[ic][i1]['sid']]['version'])

        cc=0
        #update ISL links
        for key,value in ISL.items():
            arr=key.split('_')
            p=ISL[key]
            shell=int(arr[0])
            loan=int(arr[1])
            if shell!=ic:
                continue
            idx = str(ic) + '_' + str(cc)
            ISLChains[idx] = []
            plane=p
            plane.sort(key=lambda x:(x['slot']))
            len_plane=len(plane)
            #print(plane)
            for i in range(len_plane-1):#0 to 360
                #if i+1 in range(0,361):
                if plane[i+1]['slot']-plane[i]['slot']<=21:
                    if plane[i]['sid'] in stations and plane[i+1]['sid'] in stations:
                        if stations[plane[i]['sid']]['version']!='v1.0' and stations[plane[i+1]['sid']]['version']!='v1.0':
                            stations[plane[i]['sid']]['isl']=1
                            stations[plane[i+1]['sid']]['isl']=1
                            stations[plane[i]['sid']]['islchain']=idx
                            stations[plane[i+1]['sid']]['islchain']=idx
                            if plane[i]['sid'] not in ISLChains[idx]:
                                ISLChains[idx].append(plane[i]['sid'])
                            if plane[i+1]['sid'] not in ISLChains[idx]:
                                ISLChains[idx].append(plane[i+1]['sid'])
                            ISLsats.add(plane[i]['sid'])
                            ISLsats.add(plane[i+1]['sid'])
                            #Establish ISL link
                            sid=plane[i]['sid']+'_ip_'+plane[i+1]['sid']
                            islLink={'type':'isl_link','mode':'ip','name':sid,'loan':loan,'slot':plane[i]['slot'],'sata':plane[i]['sid'],'satb':plane[i+1]['sid'],'active':0,'planeid':idx}
                            isllinks[sid]=islLink
            #360 to 0
            i=len_plane-1
            if 360-plane[i]['slot']+plane[0]['slot']<=21:
                if plane[i]['sid'] in stations and plane[0]['sid'] in stations:
                    if stations[plane[i]['sid']]['version'] != 'v1.0' and stations[plane[0]['sid']]['version'] != 'v1.0':
                        stations[plane[i]['sid']]['isl']=1
                        stations[plane[0]['sid']]['isl']=1
                        if plane[i]['sid'] not in ISLChains[idx]:
                            ISLChains[idx].append(plane[i]['sid'])
                        if plane[0]['sid'] not in ISLChains[idx]:
                            ISLChains[idx].append(plane[0]['sid'])
                        ISLsats.add(plane[i]['sid'])
                        ISLsats.add(plane[0]['sid'])
                        sid=plane[i]['sid']+'_ip_'+plane[0]['sid']
                        islLink = {'type': 'isl_link', 'mode':'ip','name': sid, 'loan': loan, 'slot': plane[i]['slot'],
                                   'sata': plane[i]['sid'], 'satb': plane[0]['sid'], 'active': 0, 'planeid': idx}
                        isllinks[sid]=islLink
            cc+=1
        for key in list(ISLChains):
            if len(ISLChains[key])==0:
                del ISLChains[key]
        #check which chains can cross-plane
        for keyA,value in ISLChains.items():
            arr=keyA.split('_')
            shell=arr[0]
            k=int(arr[1])
            keyB=shell+'_'+str(k+1)
            if keyB in ISLChains:
                loanA=stations[ISLChains[keyA][0]]['loan']
                loanB=stations[ISLChains[keyB][0]]['loan']
                if loanB-loanA<6:
                    foundLink=False
                    satA=None
                    satB=None
                    for a in range(len(ISLChains[keyA])):
                        for b in range(len(ISLChains[keyB])):
                            apanA=stations[ISLChains[keyA][a]]['apan']
                            apanB=stations[ISLChains[keyB][b]]['apan']
                            if apanB>apanA and apanB-apanA<15:
                                satA=ISLChains[keyA][a]
                                satB=ISLChains[keyB][b]
                                foundLink=True
                                break
                        if foundLink:
                            break
                    if foundLink:
                        stations[satA]['isl']=1
                        stations[satB]['isl']=1
                        if satA not in ISLChains[keyA]:
                            ISLChains[keyA].append(satA)
                        if satB not in ISLChains[keyA]:
                            ISLChains[keyA].append(satB)
                        ISLsats.add(satA)
                        ISLsats.add(satB)
                        #establish ISL link
                        sid=satA+'_cp_'+satB
                        islLink = {'type': 'isl_link', 'mode':'cp','name': sid, 'loan': -1, 'slot': -1,
                                   'sata': satA, 'satb': satB, 'active': 0, 'planeid': idx}
                        isllinks[sid]=islLink
                        crossPlaneISL[keyA]=keyB

def cal_gw_candidate(gw_cbf,gw_length,time_in,gw_pos):
    sat_candidate={}
    R=6371
    a=math.radians(25)
    b=math.radians(56.5)
    for i in range(0,len(sat)):
        tmp={}
        for j in range(0,gw_length):
            lat1=sat[i]['lat']
            lat2=gateway[j]['lat']
            lng1=sat[i]['lng']
            lng2=gateway[j]['lng']
            #dist=math.sqrt(np.square(x1-x2)+np.square(y1-y2)+np.square(z1-z2))
            dist=getDistance(lat1,lng1,lat2,lng2)
            if dist<=sat[i]['coverage']:
                if gateway[j]['enabled']==False:
                    continue
                gwlat = float(gateway[j]['lat'])
                gwlng = float(gateway[j]['lng'])
                satlat = lat1#pos_all[i][0][0][time_in]
                satlon = lng1#pos_all[i][0][1][time_in]
                satalt = sat[i]['alt']#pos_all[i][0][2][time_in]
                la = cal_lookAnglesNGSO(satlat, satlon, gwlat, gwlng, satalt)
                az = la['az']
                el = la['el']
                if el >= gateway[j]['minElevation']:
                    ci=clarkInterference(gwlat,gwlng,az,el,GSOPROTECTION,satlat,satlon)
                    if not ci['blocked']:
                        tmp[j]={'gwDistance':dist,'az':az,'el':el}
                #tmp[j]['gw_sat_dis']=dist
        if tmp !={}:
            tmp=sorted(tmp.items(),key=lambda x:x[1]['gwDistance'])
        sat_candidate[i]=tmp
    return sat_candidate

def init_sat(time_in):
    global STEERING_ANGLE,sat
    #sat=[]
    if TLE==False:
        for i in range(node_num):
            tmp={'satid':i,'satname':i,'lat':pos_all[i][0][0][time_in],'lng':pos_all[i][0][1][time_in],'alt':pos_all[i][0][2][time_in]/1000,'coverage':0.0,'serving':'NO GATEWAY LINK','gatewayuuid':None,'gw_num':-1,'capacity':0,'beams':0,'h3id':None,'h3cells':[],'islvia':False}
            tmp['h3id']=h3.latlng_to_cell(tmp['lat'],tmp['lng'],1)
            tmp['coverage']=getCoverage(tmp['alt'],STEERING_ANGLE)
            #get H3 cells around satellite
            cells=h3.grid_disk(tmp['h3id'],1)
            tmp['h3cells'].extend({tmp['h3id']})
            cells.remove(tmp['h3id'])#保证顺序是从内到外
            h3cells=cells
            tmp['h3cells'].extend(h3cells)
            sat.append(tmp)
    else:
        global stations
        load_launch_json()
        loadShells()
        get_stations(t_s)
        #print(stations)
        index=0
        for key,satrec in stations.items():
            if satrec!={}:
                #print(satrec)
                tmp={'satid':satrec['satid'],'satname':satrec['name'],'lat':satrec['lat'],'lng':satrec['lng'],'alt':satrec['altitude'],'coverage':0.0,'serving':'NO GATEWAY LINK','gatewayuuid':None,'gw_num':-1,'capacity':0,'beams':0,'h3id':None,'h3cells':[],'islvia':False}
                tmp['h3id'] = h3.latlng_to_cell(tmp['lat'], tmp['lng'], 1)
                tmp['coverage'] = getCoverage(tmp['alt'], STEERING_ANGLE)
                cells = h3.grid_disk(tmp['h3id'], 1)
                tmp['h3cells'].extend({tmp['h3id']})
                cells.remove(tmp['h3id'])  # 保证顺序是从内到外
                h3cells = cells
                tmp['h3cells'].extend(h3cells)
                sat.append(tmp)
                satrec['index']=index#stations对应sat中的下标
                index+=1
        '''#load_tle(time_in)
        no=0
        count=0
        name_exist=set()
        for satrec in tle_satname:
            if satrec not in name_exist:
                name_exist.add(satrec)
                tmp={'satid':no,'satname':satrec[0:13],'lat':tle_lat[count],'lng':tle_lng[count],'alt':tle_alt[count],'coverage':0.0,'serving':'NO GATEWAY LINK','gatewayuuid':None,'gw_num':-1,'capacity':0,'beams':0,'h3id':None,'h3cells':[],'islvia':False}
                tmp['h3id'] = h3.latlng_to_cell(tmp['lat'], tmp['lng'], 1)
                tmp['coverage'] = getCoverage(tmp['alt'], STEERING_ANGLE)
                # get H3 cells around satellite
                cells = h3.grid_disk(tmp['h3id'], 1)
                tmp['h3cells'].extend({tmp['h3id']})
                cells.remove(tmp['h3id'])  # 保证顺序是从内到外
                h3cells = cells
                tmp['h3cells'].extend(h3cells)
                sat.append(tmp)
                no+=1
            count+=1'''
    #return sat
def init_gateways():
    gw_len=len(gateway)
    global MINGWCAPACITY,MAXGWCAPACITY
    for i in range(gw_len):
        gateway[i]['h3id']=h3.latlng_to_cell(gateway[i]['lat'],gateway[i]['lng'],1)
        mincapacity=MINGWCAPACITY*1000/2.1*gateway[i]['uplinkGhz']#硬编码了
        maxcapacity=MAXGWCAPACITY*1000/2.1*gateway[i]['uplinkGhz']#硬编码了
        gateway[i]['mincapacity']=mincapacity
        gateway[i]['maxcapacity']=maxcapacity
        gateway[i]['cpd']=(maxcapacity-mincapacity)/65



def updateGateways(satCandidate):
    global haveGatewaysSats
    for i in range(len(sat)):
        gatewayUUID=None
        for j in range(len(satCandidate[i])):
            candidate=satCandidate[i][j][0]
            elevation=satCandidate[i][j][1]['el']
            gw=gateway[candidate]
            if LIMITLINKS:
                if gw['links']<gw['numAntennas']*GWMULTIPLIER/2:
                    #calculate capacity
                    capacity=gw['mincapacity']+gw['cpd']*(elevation-25)#25这里硬编码了
                    #assign gateway
                    sat[i]['serving']=gw['town']
                    sat[i]['capacity']=capacity
                    sat[i]['gatewayuuid']=gw['uuid']
                    sat[i]['gw_num']=candidate
                    gw['links']+=1
                    haveGatewaysSats.add(i)
                    gatewayUUID=gw['uuid']
                    break
            else:
                capacity = gw['mincapacity'] + gw['cpd'] * (elevation - 25.0)  # 25这里硬编码了
                sat[i]['serving'] = gw['town']
                sat[i]['capacity'] = capacity
                sat[i]['gatewayuuid'] = gw['uuid']
                sat[i]['gw_num'] = candidate
                haveGatewaysSats.add(i)
                gatewayUUID = gw['uuid']
                break

def serving_sats():
    global hexUpdates,simSats
    for i in range(len(sat)):
        h3cells=sat[i]['h3cells']
        for item in h3cells:
            if item in hexIntersect:
                hexUpdates.add(sat[i]['satid'])
                '''tmp={'satid':i,'used':0,'beams':{}}
                simSats[i]=tmp'''
def init_ISL(byhop=False):
    if TLE==False:
        global GRAPH_ISL
        edge=[]
        GRAPH_ISL.add_nodes_from(range(node_num))
        for i in range(node_num):
            for j in range(i+1,node_num):
                if Delay[i][j]>0:
                    if byhop:
                        Delay[i][j]=1
                    edge.append((i,j,Delay[i][j]))
        GRAPH_ISL.add_weighted_edges_from(edge)
    else:
        global ISL
        length=len(shells)
        #for ic in range(1,length):
        generatePlaneStats()
        generateISL()
def updateISLGw():
    global ISLsats
    if TLE==False:
        #havegwsats = []
        for sid in hexUpdates:
            if sat[sid]['gatewayuuid']==None:
                ISLsats.add(sid)
            '''else:
                havegwsats.append(sid)'''
        for sid in ISLsats:
            #print(sid)
            satno=-1
            distance = 1000000
            for lid in haveGatewaysSats:
                if nx.has_path(GRAPH_ISL,source=sid,target=lid):
                    dis=nx.dijkstra_path_length(GRAPH_ISL,source=sid,target=lid)
                    if dis<distance:
                        distance=dis
                        satno=lid
            if satno!=-1:
                sat[sid]['gatewayuuid']=sat[satno]['gatewayuuid']
                sat[sid]['gw_num']=sat[satno]['gw_num']
                sat[sid]['islvia']=True
                sat[sid]['serving']=sat[satno]['serving']+"(ISL)"
                if LIMITISLSATCAPACITY:
                    sat[sid]['capacity']=sat[satno]['capacity']/10#这里硬编码
                else:
                    sat[sid]['capacity']=sat[satno]['capacity']
    else:
        doneSats=set()
        doneChains=[]
        for sid in hexUpdates:
            aSat = stations[sid]
            gatewayuuid = sat[aSat['index']]['gatewayuuid']
            if gatewayuuid!=None:
                if sid not in doneSats:
                    doneSats.add(sid)
                    islUpdates=[]
                    chain=None
                    chainID=None
                    if aSat['islchain']!=None:
                        chainID=aSat['islchain']
                        chain=ISLChains[chainID]
                        for k in range(len(chain)):
                            if chain[k] not in doneSats:
                                if sat[stations[chain[k]]['index']]['gatewayuuid']==None:
                                    islUpdates.append(chain[k])
                                doneSats.add(chain[k])
                        cpKeys=crossPlaneISL.keys()
                        if chainID in cpKeys and chainID not in doneChains:
                            doneChains.append(chainID)
                            while chainID in cpKeys:
                                chainID=crossPlaneISL[chainID]
                                if chainID not in doneChains:
                                    doneChains.append(chainID)
                                    cpChain=ISLChains[chainID]
                                    for k in range(len(cpChain)):
                                        if cpChain[k] not in doneSats:
                                            if sat[stations[cpChain[k]]['index']]['gatewayuuid']==None:
                                                islUpdates.append(cpChain[k])
                                            doneSats.add(cpChain[k])
                        for n in range(len(islUpdates)):
                            lid=islUpdates[n]
                            sata=sat[stations[lid]['index']]
                            satb=sat[stations[sid]['index']]

                            sata['serving']=satb['serving']+'(ISL)'
                            sata['gatewayuuid']=satb['gatewayuuid']
                            sata['gw_num']=satb['gw_num']
                            sata['islvia']=sid
                            if LIMITISLSATCAPACITY:
                                sata['capacity']=satb['capacity']/10
                            else:
                                sata['capacity'] = satb['capacity']

def CapSim():
    global ACTMAXCELLCAPACITY,ACTMINCELLCAPACITY,simActiveCells,SIMACTIVECELLCOUNT,simSats,BEAMCAPACITY,MAXBEAMCAPACITY,MAXCELLCAPACITY,SIMBEAMSPERCELL,SIMTDM,MPDLSPOTBEASMS
    BEAMCAPACITY=MAXBEAMCAPACITY/SIMTDM
    MAXCELLCAPACITY=BEAMCAPACITY/SIMBEAMSPERCELL
    for key,value in simcells.items():
        simCellSats[key]=[]
        simCellBeams[key]=0
        simCellCapacity[key]=0
        simCellLinks[key]=[]
    maxBeams=len(simcells)*SIMBEAMSPERCELL
    assignedBeams=0
    usedBeams=0
    servingSats=0
    totalSatCapacity=0
    totalUsedCapacity=0
    totalCells=0
    isfull=0
    #act_count=0
    for sid in hexUpdates:
        if TLE==False:
            lat=sat[sid]['lat']
            lng=sat[sid]['lng']
            alt=sat[sid]['alt']
            coverage=sat[sid]['coverage']
            parents = sat[sid]['h3cells']
            capacity=sat[sid]['capacity']
        else:
            lat = sat[stations[sid]['index']]['lat']
            lng = sat[stations[sid]['index']]['lng']
            alt = sat[stations[sid]['index']]['alt']
            coverage = sat[stations[sid]['index']]['coverage']
            parents = sat[stations[sid]['index']]['h3cells']
            capacity=sat[stations[sid]['index']]['capacity']
        simSats[sid]={}
        simSats[sid]['sid']=sid
        simSats[sid]['used']=0
        simSats[sid]['position']=[lat,lng]
        simSats[sid]['capacity']=capacity
        simSats[sid]['beams']={}
        MPDLSPOTBEASMS=48*SIMTDM#硬编码了波束个数
        beamID=0
        actStartRing=None
        actEndRings=None
        #coverage=sat[sid]['coverage']
        centerCell=h3.latlng_to_cell(lat,lng,5)
        cells=[]
        candidates=[]
        if SIMMODE=='prio_slant':
            tmp=parents[1:]
            for r in tmp:#range(1,7):
                children=h3.cell_to_children(r,5)
                candidates.extend(children)
            children=h3.cell_to_children(parents[0],5)
            candidates.extend(children)
        if SIMMODE=='prio_nadir':
            for r in parents:
                children=h3.cell_to_children(r,5)
                candidates.extend(children)
        if len(candidates)==0:
            continue
        candidates_len=len(candidates)
        for r in range(candidates_len):
            cell=candidates[r]
            if cell in simH3:
                if sid in simCellSats[cell]:
                    continue
                if simCellBeams[cell]>=SIMBEAMSPERCELL:
                    continue
                cells.append(cell)
        checked=0
        skipped=0
        cells_len=len(cells)
        for j in range(cells_len):
            checked+=1
            if simSats[sid]['used']>=MPDLSPOTBEASMS:
                break
            if assignedBeams>=maxBeams:
                break
            cellID=cells[j]
            if sid in simCellSats[cellID]:
                skipped+=1
                continue
            if simCellBeams[cellID]>=SIMBEAMSPERCELL:
                skipped+=1
                continue
            isCovered=isCellCovered(cellID,sid)
            if isCovered!={}:
                simSats[sid]['used']+=1
                simSats[sid]['beams'][beamID]=[]
                simSats[sid]['beams'][beamID].append(cellID)
                simCellBeams[cellID]+=1
                assignedBeams+=1
                if not (cellID in simActiveCells):
                    simActiveCells.append(cellID)
                    SIMACTIVECELLCOUNT+=1
                simCellSats[cellID].append(sid)
                if SIMSPREAD>1:
                    sb=generateSpotbeam(lat,lng,isCovered['el'],2.984,alt,isCovered['az'],1.128,True,simCelllocation_cbf[cellID]['lat'],simCelllocation_cbf[cellID]['lng'],20)
                    poly=[]
                    for t in range(len(sb)):
                        poly.append([sb[t][1],sb[t][0]])
                    poly=h3.Polygon(poly)
                    cellRing=h3.polygon_to_cells(poly,5)
                    doneCells=0
                    for r in cellRing:
                        if not r in simH3:
                            skipped+=1
                            continue
                        if simCellBeams[r]>=SIMBEAMSPERCELL:
                            skipped+=1
                            continue
                        if r==cellID:
                            skipped+=1
                            continue
                        if sid in simCellSats[r]:
                            skipped+=1
                            continue
                        if not r in simActiveCells:
                            simActiveCells.append(r)
                            SIMACTIVECELLCOUNT+=1
                        simCellSats[r].append(sid)
                        simSats[sid]['beams'][beamID].append(r)
                        simCellBeams[r]+=1
                        assignedBeams+=1
                        doneCells+=1
                        beamLink = {'name': str(r) + '_' + str(sid), 'sid': sid, 'active': 0, 'primary': 1,
                                    'capacity': 0, 'type': 'simlink'}
                        simCellLinks[r]={}
                        simCellLinks[r][sid]=beamLink
                        if doneCells>=SIMSPREAD:
                            break
                beamID+=1
                beamLink={'name':str(cellID)+'_'+str(sid),'sid':sid,'active':0,'primary':1,'capacity':0,'type':'simlink'}
                simCellLinks[cellID]={}
                simCellLinks[cellID][sid]=beamLink
        if simSats[sid]['used']>0:
            servingSats+=1
            usedSatBeams=(48 if simSats[sid]['used']>48 else simSats[sid]['used'])
            if TLE==False:
                sat[sid]['beams']=usedSatBeams
            else:
                sat[stations[sid]['index']]['beams']=usedSatBeams
            usedBeams+=usedSatBeams
            totalSatCapacity+=simSats[sid]['capacity']
            #Assign bandwidth to each cell we caught
            beamCapacity=simSats[sid]['capacity']/simSats[sid]['used']
            if beamCapacity>MAXBEAMCAPACITY:
                beamCapacity=MAXBEAMCAPACITY
            for i in range(simSats[sid]['used']):
                beamCells=simSats[sid]['beams'][i]
                beamSplit=len(beamCells)
                cellCapacity=beamCapacity/beamSplit
                for k in range(beamSplit):
                    simCellCapacity[beamCells[k]]+=cellCapacity
                    simCellLinks[beamCells[k]][sid]['capacity']=cellCapacity
        if assignedBeams>=maxBeams:
            break
    for key,value in simCellCapacity.items():
        cap=value
        beams=simCellBeams[key]
        if cap>0:
            totalCells+=1
            totalUsedCapacity+=cap
            simcells[key]['capacity']=cap
            simcells[key]['beamcount']=beams
            simcells[key]['uts']=math.floor(cap/provisionedRate)
            simcells[key]['serving_sats']=[]
            simcells[key]['serving_sats'].append(sid)
            if cap>ACTMAXCELLCAPACITY:
                ACTMAXCELLCAPACITY=cap
            if cap<ACTMINCELLCAPACITY:
                ACTMINCELLCAPACITY=cap

    totalUsedCapacity=totalUsedCapacity/1000
    usedCapacityPct=str(round(totalUsedCapacity*1000/(totalSatCapacity)*100))+"%"
    averageCapacity=totalUsedCapacity/totalCells
    totalTerminals=math.floor(totalUsedCapacity*1000/(provisionedRate))
    AVERAGECAPACITY=averageCapacity*1000
    MAXCAPACITY=averageCapacity+(averageCapacity-ACTMINCELLCAPACITY)
    if SIMACTIVECELLCOUNT==0 or totalUsedCapacity==0:
        averageCapacity=0
        totalTerminals=0
        usedCapacityPct='-'
    print('TOTAL CELLS: ',SIMCELLCOUNTS)
    if SIMCELLCOUNTS>0:
        print('COVERD CELLS: ',SIMACTIVECELLCOUNT,"(",round(SIMACTIVECELLCOUNT/SIMCELLCOUNTS*100),')%')
    else:
        print('COVERED CELLS: 0 (0%)')
    print('USED SATS: ',servingSats)
    print('USED BEAMS: ',round(usedBeams))
    print('TOTAL CAP: ',totalUsedCapacity,'Gbps',"(",usedCapacityPct,')')
    print('MAX CELL CAP: ',ACTMAXCELLCAPACITY,'Mbps')
    print('AVG CELL CAP: ',AVERAGECAPACITY,'Mbps')
    print('TERMINALS: ',totalTerminals,'@',provisionedRate,'Mbps')


#-------------------------------------main function----------------------------------#
print("SIM COUNTRIES: ",COUNTRY_LIST)
load_country_json()
load_hexIntersect()
load_delay(time_in)
init_ISL(True)
init_sat(time_in)
init_gateways()
gw_cbf=to_cbf(gw_pos,gw_length)
sat_candidate=cal_gw_candidate(gw_cbf,gw_length,0,gw_pos)
updateGateways(sat_candidate)
serving_sats()
updateISLGw()
cal_simcellslocation_cbf()
CapSim()


'''print("SIM COUNTRIES: ",COUNTRY_LIST)
load_country_json()
load_hexIntersect()
init_sat(time_in)
init_ISL()
init_gateways()
gw_cbf=to_cbf(gw_pos,gw_length)
sat_candidate=cal_gw_candidate(gw_cbf,gw_length,0,gw_pos)
updateGateways(sat_candidate)
serving_sats()
updateISLGw()
cal_simcellslocation_cbf()
CapSim()
print(len(isllinks),isllinks)'''


