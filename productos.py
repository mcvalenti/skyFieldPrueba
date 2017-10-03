'''
Created on 22 sep. 2017

@author: ceci
'''

import numpy as np
from datetime import datetime
from globals import *




def newton(x,f,fp):
    x1=x-(float(f)/float(fp))
    dif=np.abs(x-x1)
    return x1,dif

def calculates_earth_rotation(epoch):
    """
    Recibe una fecha en UT y calcula el tiempo sidereo en Greenwich 
    para esa fecha y hora. 
    El mismo representa la rotacion de la tierra respecto al equinoccio vernal.
    ES APARENTE O SIDEREO ??? REVISAR!!
    -------------------------------------------
    output:
        GMST: tiempo sidereo medio en Greenwich [grados] - (float)
    """
    j0=367*epoch.year-int(7*(epoch.year+int((epoch.month+9)/12))/4)+int(275*epoch.month/9)+epoch.day+1721013.5
    t0=(j0-2451545.5)/36525
    sidereal_time_G0hs=100.4606184+36000.77004*t0+0.000387933*t0*t0-0.000000002583*t0*t0*t0
    univesal_time_hs=epoch.hour+epoch.minute/60.0+epoch.second/3600.0
    GMST=sidereal_time_G0hs+360.98564724*univesal_time_hs/24.0
    GMST=GMST%360
    
    return GMST

def transform_to_RA_DEC(r):
    """
    Recibe un vector en el sistema cartesiano inercial
    y lo transforma a sus coordenadas Ascesion Recta y Declinacion. 
    -------------------------------------------------
    outputs
        ar, dec: angulos de asc. recta y declinacion [rad] - (floats)
    """
    r_module=np.sqrt(np.dot(r,r))
    r_xprime=r[0]/r_module
    r_yprime=r[1]/r_module
    r_zprime=r[2]/r_module
    
    r_prime = np.array([[r_xprime],[r_yprime],[r_zprime]])
    declination=np.arcsin(r_zprime)
    if r_yprime > 0:
        right_ascention=(np.arccos(r_xprime/np.cos(declination)))
    else:
        right_ascention=2*np.pi-(np.arccos(r_xprime/np.cos(declination)))
        
    return right_ascention, declination

def transform_to_ECEF(GMST,r_x):
    """
    Recibe un vector en el sistema inercial ECI.
    Devuelve el vector en el sistema rotante.
    Fecha ? - mejorar 
    """
    theta=GMST*rad
    #theta=11.281*rad
    matriz_rotante=np.array([[np.cos(theta),np.sin(theta),0],[-np.sin(theta),np.cos(theta),0],[0,0,1]])
    r_xrot=np.dot(matriz_rotante,r_x)
#     print 'matriz rotante = ', matriz_rotante
#     print '----------------------------------'
#     print 'vector rotado = ', r_xrot
    return r_xrot

def generate_groudtrack(self):
    pass

epoch=datetime(2004,3,3,4,30,0)
ts_Greenwich=calculates_earth_rotation(epoch)
n_veces=int(ts_Greenwich/360.0)
ts_mod=ts_Greenwich-n_veces*360.0

print ts_mod
# eccentricity=0.0089312
# semimajor_axis=6718.0
# inclination=51.43*rad
# node_longitude_punto=-(3.0/2.0)*(np.sqrt(mu_earth)*J2*earth_radius*earth_radius/((1-eccentricity*eccentricity)*(1-eccentricity*eccentricity)*(semimajor_axis)**(7.0/2.0)))*np.cos(inclination)
# perigee_argument_punto=(node_longitude_punto/np.cos(inclination))*((5.0/2.0)*np.sin(inclination)*np.sin(inclination)-2.0)
# 
# print 'Deriva de la Longitud del Nodo [rad/s]= ', round(node_longitude_punto,11)
# print 'Deriva del Argumento del Perigeo [rad/s]= ', round(perigee_argument_punto,11)
# 
# r_x=np.array([3212.6,-2250.5,5568.6])
# r_prime=transforma_al_sist_rotante(r_x)
# #r_prime=np.array([-5368.0,-1784.0,3691.0])
# delta, alfa=transforma_a_RA_DEC(r_prime)
# 
# print '----------------------------------'
# print '----------------------------------'
# print 'alfa, delta = ', alfa*180.0/np.pi,delta*180.0/np.pi