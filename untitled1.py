import numpy as np

folder = r'D:\MODIS\script\result\Article_coordinates'

info = ['188034_20140623_20170421', 
        '026048_20140507_20170306', '105069_20140805_20170420',
        '226069_20140820_20170420', '227069_20140624_20170421']

for x in info:
    latarr = np.load(folder + r'\latarr_gdal_'+x+'.npy')
    lonarr = np.load(folder + r'\lonarr_gdal_'+x+'.npy')
    print(x)
    print('latarr')
    print(latarr)
    print()
    print('lonarr')
    print(lonarr)
    print()
 