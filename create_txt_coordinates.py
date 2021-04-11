import numpy as np
from comparison import *


Xl = '026048_20140507_20170306'
Xm = '2317'
info_MOD = '2317'
name_MOD = 'MOD14A1_' + info_MOD
# name_firms = 'FIRMS_' + X 

folder = r'D:\MODIS\script\result\Article_coordinates'
# info_Ld = 'Firms_'+ 

# def numpy_to_txt(folder, name):
#     lat = np.load(folder+'\latarr_'+name+'.npy')
#     lon = np.load(folder+'\lonarr_'+name+'.npy')
    
#     latlon = np.load(folder+'\MODIS_'+name+'.npy')
    
#     file  = open(folder  +r'\coordinates_'+name+'.txt','w')
#     for i in range(len(lat)):
#         file.write( str(lat[i]) + ', '+ str(lon[i]) + '\n')
#     file.close()
        

def numpy_to_txt(folder, name):
   
    latlon = np.load(folder+'\FIRMS_'+name+'.npy')
    print(latlon)
    
    file  = open(folder  +r'\FIRMS_'+name+'.txt','w')
    for i in range(len(latlon)):
        file.write( str(latlon[i][0]) + ', '+ str(latlon[i][1]) + '\n')
    file.close()

numpy_to_txt(folder, Xl)

# E_diff = 1

# path_res = r'D:\MODIS\Result_MODIS'

# MOD14A1 = Lists_coordinates(path_res, 'MOD14A1_' + Xm)

# np.save(path_res + r'/MOD14A1_'+Xm, MOD14A1)
 
# Test = np.load(path_res + r'/Algrorithm_'+Xl+ '.npy')

# Points_match = compare_coordinates_lists_km(MOD14A1, Test, E_diff)

# np.save(path_res + r'/MODIS_'+Xl, Points_match)

# print('Points match coordinates done') 





