# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 14:08:51 2020

@author: Катя
"""
import math
import numpy as np
import gc
import datetime
import matplotlib.pyplot as plt
# from Visualization_result_matplot import Visualization_nparray_coordinates, Visualization_arr
from utilities import getMTL


def time(a, b):
    date1 = datetime.date(int(a[0:4]),int(a[4:6]),int(a[6:]))
    date2 = datetime.date(int(b[0:4]),int(b[4:6]),int(b[6:]))
    days = abs(int(str(date1-date2).split()[0]))
    return days

def length(a1,b1,a2,b2):
    
    a1_r = (a1*math.pi)/180
    a2_r = (a2*math.pi)/180
    b1_r = (b1*math.pi)/180
    b2_r = (b2*math.pi)/180
    r = 6372795
    
    l_a = abs((a2_r - a1_r))/2
    l_b = abs((b2_r - b1_r))/2
    x = 2*math.asin( (math.sin(l_a)**2 + math.cos(a1_r)*math.cos(a2_r) * math.sin(l_b)**2 ) **0.5 )
    length = (x*r)/1000 # в км
    return length

def Minimum_Len_array(arr1, arr2):
    
    if len(arr1) < len(arr2):
        GT_coord = arr1
        Test_coord = arr2
    else:
        GT_coord = arr2
        Test_coord = arr1
        
    return (GT_coord, Test_coord)

def To_radians(x):
    R = (x * math.pi)/180
    return R

def Lists_coordinates(np_folder, info):
    
    arr_lat = np.load(np_folder + r'\latarr_'+info+'.npy')
    arr_lon = np.load(np_folder + r'\lonarr_'+info+'.npy')
    
    arr = []
   
    for i in range(arr_lat.shape[0]):
        arr.append((arr_lat[i], arr_lon[i]))
    
    
    return arr

def Minimum_distance(GT_coord, Test_coord, k):
    
    arr_minimum_d = []    
    arr_minimum_km = []

    for i in range(len(GT_coord)):
        arr_degrees = []
        arr_km = []
        for j in range(len(Test_coord)):
            
            diff_lat = abs(GT_coord[i][0] - Test_coord[j][0])
            diff_lon = abs(GT_coord[i][1] - Test_coord[j][1])
            
            diff_degrees = (diff_lat**2 + diff_lon**2)**0.5
            diff_km = length(GT_coord[i][0], GT_coord[i][1], Test_coord[j][0], Test_coord[j][1])
            
            arr_degrees.append(diff_degrees)
            arr_km.append(diff_km)
            
        arr_minimum_d.append(min(arr_degrees))
        arr_minimum_km.append(min(arr_km))
        
        
    arr_minimum_d = sorted(arr_minimum_d)
    arr_minimum_km = sorted(arr_minimum_km)

    return (arr_minimum_d[k-1], arr_minimum_km[k-1])

    
def Dist_GT_test(GT_coord, Test_coord):
    
    # GT_num   = [i for i in range(1, len(GT_coord) + 1)]
    # Test_num = [i for i in range(1, len(Test_coord) + 1)]
    

    dist_points = []
    
    for i in range(len(Test_coord)):
        arr_degrees = []
        for j in range(len(GT_coord)):
            
            diff_lat = abs(GT_coord[j][0] - Test_coord[i][0])
            diff_lon = abs(GT_coord[j][1] - Test_coord[i][1])
            
            diff_degrees = (diff_lat**2 + diff_lon**2)**0.5
            
            arr_degrees.append((diff_degrees, j+1))
            
        arr_degrees_sort = sorted(arr_degrees, key = lambda x: x[0])
        
        Min_dist_d = arr_degrees_sort[0][0] 
        ind_GT     = arr_degrees_sort[0][1]
        ind_test   = i+1 
        
        dist_points.append((Min_dist_d, ind_test, ind_GT))
    
    return dist_points

def Сalculation_E_diff_corners(filepath, np_filepath, info):
    
    b1 = np.load(np_filepath + r'Landsat_' + info + '_B1.npy')
    mtl  = filepath + '_01_T1_MTL.txt'
    data = getMTL(mtl)

    UL_LAT = float(data['CORNER_UL_LAT_PRODUCT'])
    UL_LON = float(data['CORNER_UL_LON_PRODUCT'])
    UR_LAT = float(data['CORNER_UR_LAT_PRODUCT'])
    UR_LON = float(data['CORNER_UR_LON_PRODUCT'])
    LL_LAT = float(data['CORNER_LL_LAT_PRODUCT'])
    LL_LON = float(data['CORNER_LL_LON_PRODUCT'])
    LR_LAT = float(data['CORNER_LR_LAT_PRODUCT'])
    LR_LON = float(data['CORNER_LR_LON_PRODUCT'])
    
    shape = b1.shape
    mask = np.zeros(shape)

    np.putmask(mask,b1!=b1[0][0],1)

    ind_lines = []
    for i in range(shape[0]):
       if np.sum(mask[i,:])<=5 and np.sum(mask[i,:])!=0:
           ind_lines.append(i)

    ind_columns = []
    for j in range(shape[1]):
       if np.sum(mask[:,j])<=5 and np.sum(mask[:,j])!=0:
           ind_columns.append(j)

    Max_ind_line = max(ind_lines)
    Min_ind_line = min(ind_lines)
    Max_ind_col = max(ind_columns)
    Min_ind_col = min(ind_columns)

    offsetX = Min_ind_col
    offsetY = Min_ind_line
    
    Max_Lat = max(UL_LAT,UR_LAT,LL_LAT,LR_LAT)
    Min_lat = min(UL_LAT,UR_LAT,LL_LAT,LR_LAT)
    Max_lon = max(UL_LON,UR_LON,LL_LON,LR_LON)
    Min_lon = min(UL_LON,UR_LON,LL_LON,LR_LON)
    
    p_lat = abs((Max_Lat - Min_lat)/(Max_ind_line - offsetY))
    p_lon = abs((Max_lon - Min_lon)/(Max_ind_col - offsetX))
    
    E_diff = (p_lat**2 + p_lon**2)**0.5
    return (p_lat, p_lon)

def Сalculation_E_diff_compare_coordinates(GT_coord, Test_coord):
    
    E_lat = 30/111134.86
    Gr3 = []
    for i in range(len(GT_coord)):
        
        Len = 40000 * math.cos(To_radians(GT_coord[i][0]))
        Degrees = (Len/360)*1000# m in 1 Degree
        E_lon = 30/Degrees 
        E_diff = (E_lat**2 + E_lon**2)**0.5
        arr = []     
        for j in range(len(Test_coord)):
            diff_lat = abs(GT_coord[i][0] - Test_coord[j][0])
            diff_lon = abs(GT_coord[i][1] - Test_coord[j][1])
            
            diff = (diff_lat**2 + diff_lon**2)**0.5
            arr.append(diff)
            
        
        if min(arr) <= E_diff:
            
            Gr3.append((GT_coord[i][0], GT_coord[i][1]))
            
    return Gr3



def compare_coordinates_lists_2(GT_coord, Test_coord, E_diff):
    
    Gr3 = []    
    for i in range(len(GT_coord)):
        arr = []
        for j in range(len(Test_coord)):
            
            diff = length(GT_coord[i][0], GT_coord[i][1], Test_coord[j][0], Test_coord[j][1])
            arr.append((diff, Test_coord[j][0], Test_coord[j][1]))
            
        arr_sort = sorted(arr, key = lambda x: x[0])

        
        if arr_sort[0][0] <= E_diff:
            Gr3.append((GT_coord[i][0], GT_coord[i][1], GT_coord[i][2]))
        

    return Gr3

def Grouping_points_confident(arr, g1, g2):
    k_unsure   = 0
    k_med_conf = 0
    k_conf     = 0
    
    for i in range(len(arr)):
        
        if int(arr[i][2]) < g1:
            k_unsure+=1
            
        if g1 <= int(arr[i][2]) <= g2:
            k_med_conf+=1
            
        if int(arr[i][2]) > g2:
            k_conf+=1
          
    return k_unsure, k_med_conf, k_conf

def Grouping_points_confident_VIIRS(arr):
    h = 0
    l = 0
    n = 0
    for i in range(len(arr)):
        if str(arr[i][2]) == 'h':
            h+=1
        if str(arr[i][2]) == 'l':
            l+=1
        if str(arr[i][2]) == 'n':
            n+=1
          
    return h, l, n
    

def compare_coordinates_lists(GT_coord, Test_coord, E_diff):
    
    Gr3 = []    
    for i in range(len(GT_coord)):
        arr = []
        for j in range(len(Test_coord)):
            
            diff_lat = abs(GT_coord[i][0] - Test_coord[j][0])
            diff_lon = abs(GT_coord[i][1] - Test_coord[j][1])
            
            diff = (diff_lat**2 + diff_lon**2)**0.5
            arr.append(diff)
            
        if min(arr) <= E_diff:
            Gr3.append((GT_coord[i][0], GT_coord[i][1]))
        

    return Gr3