# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 19:02:08 2020

@author: Катя
"""
import math
import pandas as pd
from utilities import getMTL
import datetime
from comparison import *
from MODIS import check_point
import numpy as np


def Max_Min_Lat_Lon(mtl):
    data =  getMTL(mtl)
    
    UL_LAT = float(data['CORNER_UL_LAT_PRODUCT'])
    UL_LON = float(data['CORNER_UL_LON_PRODUCT'])
    UR_LAT = float(data['CORNER_UR_LAT_PRODUCT'])
    UR_LON = float(data['CORNER_UR_LON_PRODUCT'])
    LL_LAT = float(data['CORNER_LL_LAT_PRODUCT'])
    LL_LON = float(data['CORNER_LL_LON_PRODUCT'])
    LR_LAT = float(data['CORNER_LR_LAT_PRODUCT'])
    LR_LON = float(data['CORNER_LR_LON_PRODUCT'])
    
    UL = (UL_LAT, UL_LON)
    LL = (LL_LAT, LL_LON)
    UR = (UR_LAT, UR_LON)
    LR = (LR_LAT, LR_LON)
    
    Max_lat = max(UL_LAT,UR_LAT,LL_LAT,LR_LAT)
    Min_lat = min(UL_LAT,UR_LAT,LL_LAT,LR_LAT)
    Max_lon = max(UL_LON,UR_LON,LL_LON,LR_LON)
    Min_lon = min(UL_LON,UR_LON,LL_LON,LR_LON)
    
    return (Max_lat, Min_lat, Max_lon, Min_lon)

def FIRMS_coordinates(folder, FIRMS, mtl, info):
    
    df = pd.read_csv(FIRMS, sep=',')
    
    columns = list(df.columns)
    print(columns)
    print()
    lat_lon = Max_Min_Lat_Lon(mtl)
    
    Max_lat = lat_lon[0]
    Min_lat = lat_lon[1]
    Max_lon = lat_lon[2]
    Min_lon = lat_lon[3]
    
    print(Min_lat, Max_lat, 'latitude snapshot')
    print(Min_lon, Max_lon, 'Longitude snapshot')
    
    z_lat  = (df.latitude >=  Min_lat) & (df.latitude <= Max_lat)
    z_lon  = (df.longitude >=  Min_lon) & (df.longitude <= Max_lon)
    z_coor = z_lat & z_lon
    
    
    
    date = str(datetime.date(int(info[7:11]),int(info[11:13]),int(info[13:15])))
    
    df_sort = df[(df.acq_date == date) & (df.daynight == 'D') & z_coor][['latitude', 'longitude','acq_date','confidence']]


    arr_lat  = np.array(df_sort['latitude'])
    arr_lon  = np.array(df_sort['longitude'])
    arr_conf = np.array(df_sort['confidence'])
    arr = []
    lat = []
    lon = []
    

    for i in range(arr_lat.shape[0]):
        if check_point(mtl, (arr_lat[i], arr_lon[i])) == True:
            arr.append((arr_lat[i], arr_lon[i], arr_conf[i]))
            lat.append(arr_lat[i])
            lon.append(arr_lon[i])
            
    lat = np.array(lat)
    lon = np.array(lon)
    
    np.save(folder+'\latarr_Firms_'+info, lat)
    np.save(folder+'\lonarr_Firms_'+info, lon)     
        
    print()
    print('FIRMS')    
    # print(arr)
    print()
    return arr
