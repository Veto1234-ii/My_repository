import math
import imageio
import numpy as np
import matplotlib.pyplot as plt
from utilities import getMTL
from coordinates import index_corners
from open_sort_csv import FIRMS_coordinates

def Reading_data(path_res, X, mtl):
    
    firms       = np.load(path_res + r'/Firms_'+X+'.npy')
    # print(firms)
    result      = np.load(path_res + r'/Algrorithm_'+X+'.npy')
    # print(result)
    points_math = np.load(path_res + r'/Points_match_'+X+'.npy')
    # print(points_math)
    
    
    b1 = np.load(path_res  + r'\Landsat_'+X+'_B1.npy')
    print(np.max(b1), np.min(b1))
    print(b1.shape, 'Shape')
    data = getMTL(mtl)
    
    return firms, result, points_math, b1, data
 
Reading_data(r'D:\MODIS\script\result\Article_coordinates','105069_20140805_20170420', r'D:\MODIS\script\result\Article_coordinates' + '\LC08_L1TP_'+'105069_20140805_20170420'+ '_01_T1_MTL.txt')
    

def Offsets_Coord_p(b1, data):
    
    offsets   = index_corners(b1)
    
    x_offset  = offsets[3]
    print(x_offset, 'x_offset')
    
    y_offset  = offsets[1]
    print(y_offset, 'y_offset')
    
    Max_ind_line = offsets[0]
    print(Max_ind_line, 'Max_ind_line')
    
    Max_ind_col  = offsets[2]
    print(Max_ind_col, 'Max_ind_col')
    
    UL_LAT = float(data['CORNER_UL_LAT_PRODUCT'])
    UL_LON = float(data['CORNER_UL_LON_PRODUCT'])
    UR_LAT = float(data['CORNER_UR_LAT_PRODUCT'])
    UR_LON = float(data['CORNER_UR_LON_PRODUCT'])
    LL_LAT = float(data['CORNER_LL_LAT_PRODUCT'])
    LL_LON = float(data['CORNER_LL_LON_PRODUCT'])
    LR_LAT = float(data['CORNER_LR_LAT_PRODUCT'])
    LR_LON = float(data['CORNER_LR_LON_PRODUCT'])
    
    Max_lat = max(UL_LAT,UR_LAT,LL_LAT,LR_LAT)
    Min_lat = min(UL_LAT,UR_LAT,LL_LAT,LR_LAT)
    Max_lon = max(UL_LON,UR_LON,LL_LON,LR_LON)
    Min_lon = min(UL_LON,UR_LON,LL_LON,LR_LON)    
        
    p_lat = abs((Max_lat - Min_lat)/(Max_ind_line - y_offset))
    print(p_lat)
    p_lon = abs((Max_lon - Min_lon)/(Max_ind_col - x_offset))
    print(p_lon)
    
    return Max_lat, Min_lon, p_lat, p_lon, y_offset, x_offset 

    
def FromCoordTo_xy(Max_lat, Min_lon, p_lat, p_lon, y_offset, x_offset, lat, lon):
    i = math.ceil((Max_lat - lat)/p_lat + y_offset)
    j = math.ceil((lon - Min_lon)/p_lon + x_offset)
    
    return i,j

def Create_mask(path_res, X, mtl):
    
    r = Reading_data(path_res, X, mtl)
    
    firms       = r[0]
    result      = r[1]
    points_math = r[2]
    b1          = r[3]
    data        = r[4]  
    
    
    shape = b1.shape
    
    mask_data = np.zeros(shape,dtype = np.uint8)
    np.putmask(mask_data, b1 != np.min(b1), 1)
    
    m = np.zeros(shape,dtype = np.uint8)
    
    f = Offsets_Coord_p(b1, data)
    
    Max_lat, Min_lon   = f[0], f[1]
    p_lat, p_lon       = f[2], f[3]
    y_offset, x_offset = f[4], f[5]
    
    for i in range(result.shape[0]):
        lat = result[i][0]
        lon = result[i][1]
        
        y,x = FromCoordTo_xy(Max_lat, Min_lon, p_lat, p_lon, y_offset, x_offset, lat, lon)
        
        
        m[y-44:y+45, x-44:x+45] = 1#выдал алгоритм
        m[y-24:y+25, x-24:x+25] = 4#выдал алгоритм
    kol_firms = 0    
    for i in range(firms.shape[0]):
        lat = firms[i][0]
        lon = firms[i][1]
        
        y,x = FromCoordTo_xy(Max_lat, Min_lon, p_lat, p_lon, y_offset, x_offset, lat, lon)
        if np.sum(mask_data[y-44:y+45, x-44:x+45]) + 250 >= 88*88 + 50:
            m[y-44:y+45, x-44:x+45] = 2# то что у фирмс
            kol_firms +=1
        
    for i in range(points_math.shape[0]):
        lat = points_math[i][0]
        lon = points_math[i][1]
        
        y,x = FromCoordTo_xy(Max_lat, Min_lon, p_lat, p_lon, y_offset, x_offset, lat, lon)
        
        m[y-44:y+45, x-44:x+45] = 3# что совпало
        
    return m, kol_firms

def Coord_To_Points_rgb(path_res, X, mtl):
    
    res       = Create_mask(path_res, X, mtl)   
    m         = res[0]
    kol_firms = res[1]
    
    print(kol_firms, 'FIRMS')
#    np.save(path_res + r'\mask_comparison'+X, m)
    plt.imshow(m)
    plt.show() 
    
    rgb  = imageio.imread(path_res + r'\rgb_'+X+'.jpg')
    st   = np.copy(rgb)
    
    st[:,:,0] = np.where(m == 1, 255, st[:,:,0]) #red
    st[:,:,2] = np.where(m == 1, 255, st[:,:,2]) #blue
    
    st[:,:,2] = np.where(m == 4, 255, st[:,:,2]) #blue
        
    st[:,:,0] = np.where(m == 2, 255, st[:,:,0]) #red  то что у фирмс
    
    st[:,:,2] = np.where(m == 3, 255, st[:,:,2]) #blue # что совпало

    
    imageio.imwrite(path_res + r'\mask_comparison'+X+'.jpg', st)

path_res = r'D:\MODIS\script\result\Article_coordinates'
X_arr = ['105069_20140805_20170420']
FIRMS = r'\fire_archive_M6_13348.csv'

for i in range(len(X_arr)):
    
    print()
    print(X_arr[i])
    print()
    mtl = path_res + '\LC08_L1TP_'+X_arr[i]+ '_01_T1_MTL.txt'
    
    GT   = FIRMS_coordinates(path_res, path_res + FIRMS, mtl, X_arr[i])
    np.save(path_res + r'/Firms_'+X_arr[i], GT)
    
    

    Coord_To_Points_rgb(path_res, X_arr[i], mtl)





