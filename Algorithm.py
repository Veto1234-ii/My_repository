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
    # ====================================

    for i in range(shape[0]):
        for j in range(shape[1]):
            if test3[i][j] == 3:

                b_5_61 = b_5s[i-30:i+31, j-30:j+31]
                b_7_61 = b_7s[i-30:i+31, j-30:j+31]
                not_water61 = not_water[i-30:i+31, j-30:j+31]
                test3_61    = test3[i-30:i+31, j-30:j+31]

                shape61 = b_5_61.shape
                arr_7 = []
                arr_5 = []

                for x in range(shape61[0]):
                    for y in range(shape61[1]):
                        if b_7_61[x][y] > 0 and not_water61[x][y] and test3_61[x][y] == 0:
                            arr_7.append(b_7_61[x][y])
                            arr_5.append(b_5_61[x][y])

                arr_7 = np.array(arr_7)
                arr_5 = np.array(arr_5)

                Div_7_5 = arr_7 / arr_5
    #            print(R75)
                Sr_7 = np.mean(arr_7)
                Sr_5 = np.mean(arr_5)

                Div_Sr7_Sr5 = Sr_7/Sr_5
                
                STD_7  = np.std(arr_7)
                STD_75 = np.std(Div_7_5)
                
                if (L7[i][j] > Sr_7 + max(3*STD_7, 0.08)) and (L7[i][j] / L5[i][j] > Div_Sr7_Sr5 + max(3*STD_75, 0.8)):
                        result[i][j]=3
    #===============================================================================

    np.save(path_res + r'\fire_mask_'+info, result)
    mask = np.zeros(shape, dtype = np.uint8)
    np.putmask(mask,result!=0, 1)
    k = np.sum(mask)
    print(k, 'Points')
    
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if mask[i][j]==1:
                mask[i-50:i+51, j-50:j+51] = 10
                
    imageio.imwrite(path_res + r'\mask_'+info+'.jpg', mask)
     
    plt.title("result")
    plt.imshow(mask,cmap='gray')
       
    return k
    