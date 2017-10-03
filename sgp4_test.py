'''
Created on 30 sep. 2017
@author: ceci
'''
import numpy as np
from datetime import datetime
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
import ephem
from ephem import degree
from skyfield.api import load, EarthSatellite, utc

text = """
SAC-D
1 37673U 11024A   17067.96328249 +.00000142 +00000-0 +30125-4 0  9990
2 37673 098.0124 076.9906 0001747 116.5869 298.3150 14.72659834308721
"""

"""
-----------------------------------------------------------------------
                        SGP 4 
-----------------------------------------------------------------------
"""
whichconst=wgs72
lines = text.strip().splitlines()
satrec = twoline2rv(lines[1], lines[2], whichconst)
d=satrec.epoch
pos, vel=satrec.propagate(d.year, d.month, d.day,d.hour, d.minute,d.second)
print 'SGP4:   ',d,pos

"""
-----------------------------------------------------------------------
                       STK 
-----------------------------------------------------------------------
"""
print 'STK:      8 Mar 2017 23:07:07.607    1691,436557    3763,226781    5685,813614'

"""
-----------------------------------------------------------------------
                       PyEphem 
-----------------------------------------------------------------------
"""
sacD = ephem.readtle(lines[0], lines[1], lines[2])
sacD.compute('2017/3/8 23:07:07.607135')
r = 6378.16 + sacD.elevation / 1000.0
x = r * np.cos(sacD.ra) * np.cos(sacD.dec)
y = r * np.sin(sacD.ra) * np.cos(sacD.dec)
z = r * np.sin(sacD.dec)
print 'PyEphem:   2017-3-8 23:07:07.607    ', x, y, z
"""
-----------------------------------------------------------------------
                       Skyfield 
-----------------------------------------------------------------------
"""
sat=EarthSatellite(lines[1], lines[2], lines[0])
geocentric = sat.at(sat.epoch)
print 'Skyfield: ',sat.epoch.utc_strftime('%Y-%m-%d %H:%M:%S    '),geocentric.position.km



