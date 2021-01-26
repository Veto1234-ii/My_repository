# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 21:04:13 2020

@author: labgraph1
"""
import math
import imageio
import numpy as np
import matplotlib.pyplot as plt
from utilities import getMTL
from coordinates import index_corners

filepath = r'D:\VETOSHNIKOVA\Snapshots'
path_res = filepath + r'\result'
X = '175021_20180522_20180605'
mtl = filepath + '\LC08_L1TP_'+X+'_01_T1\LC08_L1TP_'+X+ '_01_T1_MTL.txt'

def Reading_data(path_res, X, mtl):
    
    firms       = np.load(path_res + r'/Firms_'+X+'.npy')
    print(firms)
    result      = np.load(path_res + r'/Algrorithm_'+X+'.npy')
    print(result)
    points_math = np.load(path_res + r'/Points_match_'+X+'.npy')
    print(points_math)

    b1 = np.load(path_res  + r'\Landsat_'+X+'_B1.npy')
    print(b1.shape, 'Shape')
    data = getMTL(mtl)
    
    return firms, result, points_math, b1, data  
 

def Offsets_Coord_p(b1, data):
    
    offsets   = index_corners(b1)
    
    x_offset  = offsets[3]
    print(x_offset, 'x_offset')
    
    y_offset  = offsets[1]
    print(y_offset, 'y_offset')
    
    Max_ind_line = offsets[0]
    print(Max_ind_line, 'Max_ind_line')
    
    Max_ind_col  = offsets[2]
    print(Max_ind_col, 'Max_ind_col')
    
    UL_LAT = float(data['CORNER_UL_LAT_PRODUCT'])
    UL_LON = float(data['CORNER_UL_LON_PRODUCT'])
    UR_LAT = float(data['CORNER_UR_LAT_PRODUCT'])
    UR_LON = float(data['CORNER_UR_LON_PRODUCT'])
    LL_LAT = float(data['CORNER_LL_LAT_PRODUCT'])
    LL_LON = float(data['CORNER_LL_LON_PRODUCT'])
    LR_LAT = float(data['CORNER_LR_LAT_PRODUCT'])
    LR_LON = float(data['CORNER_LR_LON_PRODUCT'])
    
    Max_lat = max(UL_LAT,UR_LAT,LL_LAT,LR_LAT)
    Min_lat = min(UL_LAT,UR_LAT,LL_LAT,LR_LAT)
    Max_lon = max(UL_LON,UR_LON,LL_LON,LR_LON)
    Min_lon = min(UL_LON,UR_LON,LL_LON,LR_LON)    
        
    p_lat = abs((Max_lat - Min_lat)/(Max_ind_line - y_offset))
    print(p_lat)
    p_lon = abs((Max_lon - Min_lon)/(Max_ind_col - x_offset))
    print(p_lon)
    
    return Max_lat, Min_lon, p_lat, p_lon, y_offset, x_offset 

    
def FromCoordTo_xy(Max_lat, Min_lon, p_lat, p_lon, y_offset, x_offset, lat, lon):
    i = math.ceil((Max_lat - lat)/p_lat + y_offset)
    j = math.ceil((lon - Min_lon)/p_lon + x_offset)
    
    return i,j

def Create_mask(path_res, X, mtl):
    
    r = Reading_data(path_res, X, mtl)
    
    firms       = r[0]
    result      = r[1]
    points_math = r[2]
    b1          = r[3]
    data        = r[4]  
    
    shape = b1.shape
    m = np.zeros(shape,dtype = np.uint8)
    
    f = Offsets_Coord_p(b1, data)
    
    Max_lat, Min_lon   = f[0], f[1]
    p_lat, p_lon       = f[2], f[3]
    y_offset, x_offset = f[4], f[5]
    
    lat = 55.91099
    lon = 42.70637
    
    i, j = FromCoordTo_xy(Max_lat, Min_lon, p_lat, p_lon, y_offset, x_offset, lat, lon)
        
    return i, j

#   
m = Create_mask(path_res, X, mtl)    
print(m)
#
#np.save(path_res + r'\mask_comparison'+X, m)
#plt.imshow(m)
#plt.show() 
#
#rgb  = imageio.imread(path_res + r'\rgb_'+X+'.jpg')
#st   = np.copy(rgb)
#
#st[:,:,2] = np.where(m == 1, st[:,:,2]*0.5 + 127, st[:,:,2]) #blue
#
#st[:,:,0] = np.where(m == 2, st[:,:,0]*0.5 + 127, st[:,:,0]) #red
#
#st[:,:,0] = np.where(m == 3, st[:,:,0]*0.5 + 127, st[:,:,0]) #red
#st[:,:,2] = np.where(m == 3, st[:,:,2]*0.5 + 127, st[:,:,2]) #blue
#
#imageio.imwrite(path_res + r'\mask_comparison'+X+'.jpg', st)
