import numpy as np
import tifffile
import math
import gc
from utilities import getMTL

def DNtoReflectance(filepath, info, n_band, resultfolder):
    num_band = str(n_band)
    band = filepath + '_01_T1_B' + num_band +'.tif'
    mtl  = filepath + '_01_T1_MTL.txt'

    data = getMTL(mtl)

    SUN_ELEVATION      = float(data['SUN_ELEVATION'])
    SUN_ELEVATION_Rad  = SUN_ELEVATION * math.pi/180
    EARTH_SUN_DISTANCE = float(data['EARTH_SUN_DISTANCE'])

    image = tifffile.imread(band, key=0)
    DN = np.array(image)

    RADIANCE_MAXIMUM_BAND =    float(data['RADIANCE_MAXIMUM_BAND_'    + num_band])
    REFLECTANCE_MAXIMUM_BAND = float(data['REFLECTANCE_MAXIMUM_BAND_' + num_band])
    RADIANCE_MULT_BAND =       float(data['RADIANCE_MULT_BAND_'       + num_band])
    RADIANCE_ADD_BAND =        float(data['RADIANCE_ADD_BAND_'        + num_band])

    Radiance = DN * RADIANCE_MULT_BAND + RADIANCE_ADD_BAND
    Sun_radiance = ((math.pi*EARTH_SUN_DISTANCE**2)**2*RADIANCE_MAXIMUM_BAND*np.sin(SUN_ELEVATION_Rad))/REFLECTANCE_MAXIMUM_BAND
    Reflectance = Radiance/Sun_radiance

    b = np.array(Reflectance,dtype = np.float32)
    np.save(resultfolder + 'Landsat_'+ info +'_B' + num_band, b)
    Reflectance = None
    b = None
    gc.collect()
    print("save "+ 'Landsat_'+ info +'_B' + num_band)
