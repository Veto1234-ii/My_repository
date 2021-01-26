# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 10:55:51 2020

@author: Катя
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 23:07:03 2019

@author: Alexandra
"""

import tifffile
import numpy as np
from utilities import getMTL 

def DNtoTCelsium(filepath, info, n_band, resultfolder):
    num_band = str(n_band)
    band = filepath + '_01_T1_B' + num_band +'.tif'
    mtl  = filepath + '_01_T1_MTL.txt'
    data = getMTL(mtl)
    
    # Open the file:
    Band = tifffile.imread(band, key=0)
    
    RADIANCE_MULT_BAND = float(data['RADIANCE_MULT_BAND_'+ num_band])
    RADIANCE_ADD_BAND  = float(data['RADIANCE_ADD_BAND_' + num_band])
    K2_CONSTANT_BAND   = float(data['K2_CONSTANT_BAND_'  + num_band])
    K1_CONSTANT_BAND   = float(data['K1_CONSTANT_BAND_'  + num_band])
    
    TOARadiance = RADIANCE_MULT_BAND * Band + RADIANCE_ADD_BAND
    
    band_log = np.log(K1_CONSTANT_BAND/TOARadiance + 1)
    band_t = K2_CONSTANT_BAND / band_log - 273.15
    
    print(np.max(band_t), ' Max Temperature')
    print(np.min(band_t), ' Min Temperature')
    
    Band_T_float32 = np.array(band_t, dtype = np.float32)
    
    np.save(resultfolder + 'Temperature_Band_' + str(n_band) +'_'+info, Band_T_float32 )
    print('Temperature_Band_' + num_band +'_' + info + ' done')



