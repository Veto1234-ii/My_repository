import numpy as np

path_modis = r'D:\MODIS\script\result\may2014_august2014\MOD14A1.A2014169.h12v10.006.2015288043634.hdf'

info_MOD = path_modis[-8:-4]
name = 'MOD14A1_' + info_MOD

folder = r'D:\MODIS\script\result\Article_coordinates'
info_Ld = '227069_20140624_20170421' 

def numpy_to_txt(folder, name):
    lat = np.load(folder+'\latarr_'+name+'.npy')
    lon = np.load(folder+'\lonarr_'+name+'.npy')
    
    
    file  = open(folder  +r'\coordinates_gdal_'+name+'.txt','w')
    for i in range(len(lat)):
        file.write( str(lat[i]) + ', '+ str(lon[i]) + '\n')
    file.close()
        
numpy_to_txt(folder, info_Ld)