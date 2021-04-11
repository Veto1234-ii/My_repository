# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 19:33:14 2020

@author: Катя
"""
import gc
import numpy as np
import matplotlib.pyplot as plt
from Layer import Layer
import imageio

# fire = np.load(r'D:\MODIS\script\result\Article_coordinates\fire_mask_105069_20140805_20170420.npy')

# print(np.isclose(fire, 2).sum())

def detectFire(path_res, info):

    b_1s = np.load(path_res  + r'\Landsat_'+info+'_B1.npy')
    b_2s = np.load(path_res  + r'\Landsat_'+info+'_B2.npy')
    b_3s = np.load(path_res  + r'\Landsat_'+info+'_B3.npy')
    b_4s = np.load(path_res  + r'\Landsat_'+info+'_B4.npy')
    
    shape = b_1s.shape

    L1 = Layer(b_1s)
    L2 = Layer(b_2s)
    L3 = Layer(b_3s)
    L4 = Layer(b_4s)

    nw2 = L3 >> L2 | L1 >> L2 & L2 >> L3 & L3 >> L4

    L3.arr = None
    L3     = None
    L2.arr = None
    L2     = None
    gc.collect()
    
    b_5s = np.load(path_res + r'\Landsat_'+info+'_B5.npy')
    b_6s = np.load(path_res + r'\Landsat_'+info+'_B6.npy')
    b_7s = np.load(path_res + r'\Landsat_'+info+'_B7.npy')
    L5 = Layer(b_5s)
    L6 = Layer(b_6s)
    L7 = Layer(b_7s)

    Sub_1_7 = L1 - L7
    nw1 = L4 >> L5 & L5 >> L6 & L6 >> L7 & Sub_1_7 << 0.2

    L4.arr = None
    L4     = None
    Sub_1_7.arr = None
    Sub_1_7     = None
    gc.collect()

    z1 = nw1 & nw2
    not_water = ~z1 # logical not

    # z1.arr = None
    # z1 = None
    # gc.collect()

    result = np.zeros(shape,dtype = np.uint8)
    
    Div_7_6 = L7/L6
    Div_7_5 = L7/L5
    Sub_7_5 = L7 - L5

    # R75 > 1.8 && ρ7−ρ5 > 0.17
    test3 = np.zeros(shape,dtype = np.uint8)
    np.putmask(test3, ( Div_7_5 >> 1.8 & Sub_7_5 >> 0.17 & Div_7_6  >> 1.6 ).arr , 3)

    Div_7_6.arr = None
    Div_7_6     = None
    gc.collect()
    print("pre-test 3 done")

    # R75 > 2.5 && ρ7−ρ5 > 0.3 && ρ7 > 0.5
    np.putmask(result, (Div_7_5 >> 2.5 & Sub_7_5 >> 0.3 & L7 >> 0.5).arr, 1)

    Div_7_5.arr = None
    Div_7_5     = None
    Sub_7_5.arr = None
    Sub_7_5     = None
    gc.collect()
    
    print("test 1 done")
    # ===================================

    # ρ6 > 0.8 && ρ1 < 0.2 && ( ρ5 > 0.4 || p7 < 0.1 )
    np.putmask(result, ( L6 >> 0.8 & L1 << 0.2 & ( L5 >> 0.4 | L7 << 0.1 ) ).arr, 2)

    L1.arr = None
    L1     = None
    L6.arr = None
    L6     = None
    gc.collect()
    
    print("test 2 done")
    
    inf =  open(r'D:\Landsat\experiments\105069\class1.txt', 'w') 
    inf.write( 'Div_7_5' + ', '+ 'Sub_7_5' + ', ' + 'L7' + '\n')
        
    for i in range(shape[0]):
        for j in range(shape[1]):
            if result[i][j] == 1:
                inf.write( Div_7_5[i][j] + ', '+ Sub_7_5[i][j] + ', ' + L7[i][j] + '\n')
                    
                    
                    
    inf.close()
                
    # ====================================

path_res = 
info     =     
detectFire(path_res, info)
