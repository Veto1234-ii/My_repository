# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 17:59:42 2020

@author: Катя
"""

from GeoTiff_to_Temperature import DNtoTCelsium
from histogram import threshold_selection
from Threshold_mask_thermal import Thermal_mask
from Thermal_coordinates import FromMaskToCoords
from Thermal_Visualization import Visualization

X = '119041_20140807_20170420'
filepath = r'E:\Gis\LC08_L1TP_'+X+'_01_T1\LC08_L1TP_'+X

# X = '188034_20140623_20170421'
# filepath = r'F:\Gis\LC08_L1TP_'+X+'_01_T1\Image\LC08_L1TP_'+X

Count = 176
N = 500
band = 10

DNtoTCelsium(filepath, X, band, "result/")

threshold = threshold_selection("result/", band, X, N, Count)

Thermal_mask(threshold, "result/", band, X)

thermal_mask_file = r'result/Thermal_mask_'+X+'.npy'

FromMaskToCoords(filepath, "result/", X, band, thermal_mask_file)
Visualization("result/", X, band)

