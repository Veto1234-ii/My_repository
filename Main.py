# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 07:31:59 2020

@author: Alexandra
"""
from GeoTiff_to_reflectance_numpy_2 import DNtoReflectance
from Mask_true_false_borders import calculateBorders
from Algorithm import detectFire
from coordinates import FromMaskToCoords, Coordinates_gdal
from comparison import *
from open_sort_csv import FIRMS_coordinates
from rgb_points import Create_RGB, Save_image_points
from points_firms import Coord_To_Points_rgb
import numpy as np

def Main(X, filepath, FIRMS, mtl, path_res):
    print()
    print(X)
    print()
    
    E_diff = 1 # 1 km
    
    
    # firemask = path_res + r'\fire_mask_'+X+'.npy'
    
    # for i in range(1,8):
    #     DNtoReflectance(filepath, X, i, mtl, path_res)
     
    # k_alg = detectFire(path_res, X)
    # FromMaskToCoords(path_res, X, firemask, mtl)
    Coordinates_gdal(path_res, X)
    # print(k_alg, 'FIRE PIXELS')
    lat = np.load(path_res + r'\latarr_'+X+'.npy')
    k_alg = lat.shape[0]
##
# #    
    GT   = FIRMS_coordinates(path_res + FIRMS, mtl, X)
    np.save(path_res + r'/Firms_'+X, GT)
    print('Firms coordinates done')
    
    Test = Lists_coordinates(path_res, 'gdal_' + X)
    np.save(path_res + r'/Algrorithm_'+X, Test)
    print('Algrorithm coordinates done')
# #    
    Points_match = compare_coordinates_lists_km(GT, Test, E_diff)
    np.save(path_res + r'/Points_match_'+X, Points_match)
    print('Points match coordinates done') 
    
    k_unsure, k_med_conf, k_conf = Grouping_points_confident(Points_match, 40, 60)
#    
    Points = len(Points_match)
    
    Coord_To_Points_rgb(path_res, X, mtl)
    
    
    Create_RGB(path_res, X)
    Save_image_points(path_res, X)
    
    return k_alg, firms, k_unsure, k_med_conf, k_conf
        

    