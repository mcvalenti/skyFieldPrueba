'''
Created on 19 sep. 2017

@author: ceci
'''
from skyfield.api import Topos, load, EarthSatellite, utc
from datetime import datetime, timedelta
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import csv
from globals import *
from productos import calculates_earth_rotation, transform_to_ECEF, transform_to_RA_DEC
from sist_deCoordenadas import teme2tod

# stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
# satellites = load.tle('stations.txt')
# satellite = satellites['ISS (ZARYA)']
# print(satellite)
# 
# 
# planets = load('de421.bsp')
# earth, mars= planets['earth'], planets['mars']


# t = ts.now()


# GOCE
# 1 34602U 09013A   13314.96046236  .14220718  20669-5  50412-4 0   930
# 2 34602 096.5717 344.5256 0009826 296.2811 064.0942 16.58673376272979
 
text = """
SAC-D
1 37673U 11024A   17067.96328249 +.00000142 +00000-0 +30125-4 0  9990
2 37673 098.0124 076.9906 0001747 116.5869 298.3150 14.72659834308721
"""

lines = text.strip().splitlines()
sat = EarthSatellite(lines[1], lines[2], lines[0])
ts = load.timescale()
sat_epoch=sat.epoch
sat_epoch_datetime=sat_epoch.utc_datetime()
start_epoch_datetime=datetime(sat_epoch_datetime.year, sat_epoch_datetime.month,sat_epoch_datetime.day,sat_epoch_datetime.hour,sat_epoch_datetime.minute,0).replace(tzinfo=utc) 
stop_epoch_datetime=start_epoch_datetime+timedelta(hours=3)
#sat_epoch_datetime=sat_epoch_datetime+timedelta(hours=2)
sat_epoch_list=[]
ra_list=[]
dec_list=[]

while start_epoch_datetime < stop_epoch_datetime:
#for dt in range(300):
    start_epoch_datetime=start_epoch_datetime+timedelta(minutes=1)
    sat_epoch_list.append(start_epoch_datetime)
    
earth_oblat=0.000335

with open('validaciones/sacDskyfield.csv', 'w') as csvfile: #csv
        fieldnames = ['Epoca','Latitud','Longitud'] #csv 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)   #csv 
        writer.writeheader()       #csv
        for sepoch in sat_epoch_list:
            gmst_angle=calculates_earth_rotation(sepoch)
            se_skf=ts.utc(sepoch)
            geocentric = sat.at(se_skf)            
            r_xtot=transform_to_ECEF(gmst_angle, geocentric.position.km)
            r_teme=np.array([r_xtot[0],r_xtot[1],r_xtot[2]])
            r_tod=teme2tod(sepoch, r_teme)
      #      print sepoch,r_teme,r_tod
#             r_xtot=np.array(r_tod[0])
#             r_xtot1=r_xtot[0]
            ra, dec=transform_to_RA_DEC(r_xtot)
            dec1=np.arctan(np.tan(dec)/((1.0-earth_oblat)*(1.0-earth_oblat)))
            if ra*deg > 180.0:
                ra=-360.0+ra*deg
            else:
                ra=ra*deg
            ra_list.append(ra)
            dec_list.append(dec1*deg)
            print sepoch,geocentric.position.km, ra, dec*deg
            writer.writerow({'Epoca': sepoch.strftime('%Y-%m-%d %H:%M:%S'), 'Latitud': dec*deg, 'Longitud':ra}) #csv
#           print gmst_angle, geocentric.position.km, r_xtot, ar*deg, dec*deg
      
"""
Grafico
"""  
m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
m.drawcoastlines()
m.fillcontinents(color='green',lake_color='aqua',zorder=0)
# draw parallels and meridians.
m.drawparallels(np.arange(-90.,91.,30.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='blue')
for k in range(len(ra_list)):
    x, y = m(ra_list[k],dec_list[k])
 #   m.plot(ra_list[k],dec_list[k],'bo')
    m.scatter(x,y,3,marker='o',color='yellow')
plt.title('Tracks')
plt.show()

cett = Topos('31.5241 S', '64.4635 W')


# difference=sat-cett
# topocentric = difference.at(t)
# print(topocentric.position.km)
# alt, az, distance = topocentric.altaz()
# print(alt)
# print(az)
# print(distance.km)


