import numpy as np
from utilities import getMTL
import rasterio
import pyproj

def Coordinates_gdal(folder, info):
    
    localname = folder+ '/LC08_L1TP_'+info+'_01_T1_B6.TIF'
    folder_firemask = folder + '\fire_mask_'+info+'.npy'
    
    firemask = np.load(folder_firemask)

    with rasterio.open(localname, mode='r') as src:
        p = pyproj.Proj(src.crs)
        
        height = src.height
        width  = src.width
        
        lonarr = []
        latarr = []
        
        for i in range(height):
            for j in range(width):
                
                if (i == height//2) and (j == width//2):
                    x_center, y_center = src.xy(i, j)
                    lon_center, lat_center = p(x_center, y_center, inverse=True) 
                    
                if firemask[i][j]!=0:
                    x, y = src.xy(i, j)
                    lon, lat = p(x,y,inverse=True) 
                    
                    latarr.append(lat)
                    lonarr.append(lon)
                        
                
                    
        
        lonarr=np.array(lonarr)
        latarr=np.array(latarr)
        
        np.save(folder+'\latarr_gdal_'+info, latarr)
        np.save(folder+'\lonarr_gdal_'+info, lonarr)         
        print('coords done')
        
def index_corners(b):
    shape = b.shape
    mask = np.zeros(shape)

    np.putmask(mask,b!=b[0][0],1)

    ind_lines = []
    for i in range(shape[0]):
       if np.sum(mask[i,:])<=5 and np.sum(mask[i,:])!=0:
           ind_lines.append(i)

    ind_columns = []
    for j in range(shape[1]):
       if np.sum(mask[:,j])<=5 and np.sum(mask[:,j])!=0:
           ind_columns.append(j)

    Max_ind_line = max(ind_lines)
    Min_ind_line = min(ind_lines)
    Max_ind_col = max(ind_columns)
    Min_ind_col = min(ind_columns)

    return  (Max_ind_line, Min_ind_line, Max_ind_col, Min_ind_col)

def Coordinates(i, j, Min_lat, Max_Lat, Min_lon, Max_lon, Max_ind_line, Min_ind_line, Max_ind_col, Min_ind_col):

    offsetX = Min_ind_col
    offsetY = Min_ind_line

    p_lat = abs((Max_Lat - Min_lat)/(Max_ind_line - offsetY))
    print(p_lat)
    p_lon = abs((Max_lon - Min_lon)/(Max_ind_col - offsetX))
    print(p_lon)

    res_lat1 = Max_Lat - (i - offsetY) * p_lat

    res_lon = Min_lon + (j - offsetX) * p_lon

    return (res_lat1,res_lon)

def FromMaskToCoords(path_res, info, firemask, mtl):
    b1 = np.load(path_res + r'\Landsat_' + info + '_B1.npy')
    data = getMTL(mtl)

    UL_LAT = float(data['CORNER_UL_LAT_PRODUCT'])
    UL_LON = float(data['CORNER_UL_LON_PRODUCT'])
    UR_LAT = float(data['CORNER_UR_LAT_PRODUCT'])
    UR_LON = float(data['CORNER_UR_LON_PRODUCT'])
    LL_LAT = float(data['CORNER_LL_LAT_PRODUCT'])
    LL_LON = float(data['CORNER_LL_LON_PRODUCT'])
    LR_LAT = float(data['CORNER_LR_LAT_PRODUCT'])
    LR_LON = float(data['CORNER_LR_LON_PRODUCT'])
    
    Corners = index_corners(b1)
    Max_ind_line = Corners[0]
    Min_ind_line = Corners[1]
    Max_ind_col =  Corners[2]
    Min_ind_col =  Corners[3]
    
    Max_Lat = max(UL_LAT,UR_LAT,LL_LAT,LR_LAT)
    Min_lat = min(UL_LAT,UR_LAT,LL_LAT,LR_LAT)
    Max_lon = max(UL_LON,UR_LON,LL_LON,LR_LON)
    Min_lon = min(UL_LON,UR_LON,LL_LON,LR_LON)

    result = np.load(firemask)
    shape = result.shape

    height = shape[0]
    width = shape[1]

    lonarr = []
    latarr = []

    for i in range(height):
            for j in range(width):
                if result[i][j]!=0:
                    lon_lat = Coordinates(i,j,Min_lat, Max_Lat, Min_lon, Max_lon, Max_ind_line, Min_ind_line, Max_ind_col, Min_ind_col)
                    latarr.append(lon_lat[0])
                    lonarr.append(lon_lat[1])


    lonarr=np.array(lonarr)
    latarr=np.array(latarr)

    print(len(lonarr))
    np.save(path_res + r'\lonarr_'+info,lonarr)
    np.save(path_res + r'\latarr_'+info,latarr)
    print('coords done')
