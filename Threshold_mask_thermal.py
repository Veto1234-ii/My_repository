# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 17:14:07 2020

@author: Катя
"""
import numpy as np

def Thermal_mask(threshold, np_folder, n_band, info):

    T = np.load(np_folder + r'Temperature_Band_' + str(n_band) +'_'+info + '.npy')
    shape = T.shape
    mask = np.zeros(shape, dtype = np.uint8)
    np.putmask(mask, T > threshold, 1)
    print(np.sum(mask))
    np.save(np_folder + r'Thermal_mask_'+info, mask)
