from pyhdf.SD import SD,SDC
import numpy as np
import datetime
import math
import shapefile
from comparison import *
from utilities import getMTL


def barycentric(p1, p2, p3, Vec2i_P):
    u = np.cross(np.array([ p3[0]-p1[0], p2[0]-p1[0], p1[0]-Vec2i_P[0] ]), np.array([ p3[1]-p1[1], p2[1]-p1[1], p1[1]-Vec2i_P[1] ]))
    if (abs(u[2])<1): 
            return False # triangle is degenerate, in this case return smth with negative coordinates
    u = np.array([1-(u[0]+u[1])/u[2], u[1]/u[2], u[0]/u[2]])
    return (u[0] > 0) and (u[1] > 0) and (u[2] > 0) 


def check_point_modis(mtl, modis_lat_lon):
    data = getMTL(mtl)
    
    UL_LAT = float(data['CORNER_UL_LAT_PRODUCT'])
    UL_LON = float(data['CORNER_UL_LON_PRODUCT'])
    UR_LAT = float(data['CORNER_UR_LAT_PRODUCT'])
    UR_LON = float(data['CORNER_UR_LON_PRODUCT'])
    LL_LAT = float(data['CORNER_LL_LAT_PRODUCT'])
    LL_LON = float(data['CORNER_LL_LON_PRODUCT'])
    LR_LAT = float(data['CORNER_LR_LAT_PRODUCT'])
    LR_LON = float(data['CORNER_LR_LON_PRODUCT'])
    
    UL = (UL_LAT, UL_LON)
    LL = (LL_LAT, LL_LON)
    UR = (UR_LAT, UR_LON)
    LR = (LR_LAT, LR_LON)
    
    return (barycentric(UL, UR, LR, modis_lat_lon)) or (barycentric(UL, LL, LR, modis_lat_lon))
        
    



def Gr_Tile(H,V):
   with open('D:\MODIS\manuals\Tile.txt','r')  as file:
       for line in file:
           arr_l = line.split()
           if len(arr_l) != 0:
               if arr_l[0] == str(V) and arr_l[1] == str(H):
                   lon_min = float(arr_l[2])
                   lon_max = float(arr_l[3])
                   lat_min = float(arr_l[4])
                   lat_max = float(arr_l[5])
                   
   return lon_min, lon_max, lat_min, lat_max
  


def Index_date_Mod14_A1(a,b):
    # a startdate MOD14A1
    # b date Landsat
    date1 = datetime.date(int(a[0:4]), int(a[5:7]), int(a[8:10]))
    date2 = datetime.date(int(b[0:4]), int(b[5:7]), int(b[8:10]))
    
    if str(date2 - date1) == '0:00:00':
        days = 0
    else:    
        days = abs(int(str(date1-date2).split()[0]))
    
    
    return days
    


def ConversionCoordinates(H, V, i, j):
    R =6371007.181 #радиус в м
    T = 1111950# высота и ширина каждой плитки MODIS в плоскости проекции в м
    Xmin = -20015109# западная граница плоскости проекции в м
    Ymax = 10007555# северная граница плоскости проекции;

    w = T/1200
    
    x = (j + 0.5)*w + H*T + Xmin
    y = Ymax - (i + 0.5)*w - V*T
    
    lat = y/R
    
    lon = x/(R*np.cos(lat))
    
    return lat, lon
  
def MaskToShapefile(arr, H, V):
   

    w = shapefile.Writer(shapefile.POINT)
    
    shape = arr.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            if arr[i][j] == 9:
                lat_r, lon_r = ConversionCoordinates(H, V, i, j)# радианы
                
                lat = lat_r*180/math.pi
                lon = lon_r*180/math.pi
                
                w.point(lon, lat)
                

    w.save('result\shapefiles')                
    
 

def MaskToCoord(arr, H, V, info, folder, mtl):
    lat_arr = []
    lon_arr = []
    
    shape = arr.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            if (arr[i][j] == 7) or (arr[i][j] == 8) or (arr[i][j] == 9):
                
                value_mask = arr[i][j] 
                lat_r, lon_r = ConversionCoordinates(H, V, i, j)# радианы
                
                lat = lat_r*180/math.pi
                lon = lon_r*180/math.pi
                
                modis_lat_lon = (lat, lon)
                
                if check_point_modis(mtl, modis_lat_lon) == True:
                    
                    lat_arr.append(lat)
                    lon_arr.append(lon) 
                
    print('POINT MODIS',len(lat_arr))
            
    lat_arr = np.array(lat_arr)
    lon_arr = np.array(lon_arr)
    
    np.save(folder+'\coordinates_pointmodis_landsat'+'\latarr_MOD14A1_'+info, lat_arr)
    np.save(folder+'\coordinates_pointmodis_landsat'+'\lonarr_MOD14A1_'+info, lon_arr)



def Read_MOD14_A1(path):
    
    
    d_MOD14_A1 = SD(path, SDC.READ)
    metadata = d_MOD14_A1.attributes()
    
    StartDate = metadata['StartDate']
    print(StartDate, 'StartDate')
    
    EndDate = metadata['EndDate']
    print(EndDate, 'EndDate')
    
   
    H = metadata['HorizontalTileNumber']
    
    V = metadata['VerticalTileNumber']     
    
    
        
    return H, V, StartDate, d_MOD14_A1



def MODIS_save_coordinates(path_modis, path_landsat_coor, Date_Landsat, info_MOD, mtl):
    
    H, V, StartDate_MODIS, d_MOD14_A1 = Read_MOD14_A1(path_modis)
    
    idx = Index_date_Mod14_A1(StartDate_MODIS, Date_Landsat)
    
    print('IDX' ,idx)
   
    
    FireMask_8day = d_MOD14_A1.select('FireMask').get()
    
    Mask = FireMask_8day[idx]
    
    
    lon_min, lon_max, lat_min, lat_max = Gr_Tile(H,V) 
    print()  
    print(lon_min,'lon_min')
    print(lon_max, 'lon_max') 
    print(lat_min, 'lat_min')
    print(lat_max, 'lat_max')
        
    MaskToCoord(Mask, H, V, info_MOD, path_landsat_coor, mtl)
    
def Landsat_MODIS(path_landsat_coor, info_MOD, info_Ld, E_diff_km, E_diff_degrees, mtl):
    
    Coord_Mod14_A1 = Lists_coordinates(path_landsat_coor, 'MOD14A1_' + info_MOD)
    print( 'POINT MODIS', len(Coord_Mod14_A1))
    Coord_Mod14_A1_sort_lat = sorted(Coord_Mod14_A1, key = lambda x: x[0])
    Coord_Mod14_A1_sort_lon = sorted(Coord_Mod14_A1, key = lambda x: x[1])
    
    
    
    Coord_Ld          = Lists_coordinates(path_landsat_coor, info_Ld)
    print( 'POINT LANDSAT', len(Coord_Ld))
    Coord_Ld_sort_lat = sorted(Coord_Ld, key = lambda x: x[0])
    Coord_Ld_sort_lon = sorted(Coord_Ld, key = lambda x: x[1])
    
   
    
    if len(Coord_Mod14_A1_sort_lat)!=0 and len(Coord_Ld_sort_lat)!=0:
        Result_km      = compare_coordinates_lists_km(Coord_Mod14_A1, Coord_Ld, E_diff_km)
        Result_degrees = compare_coordinates_lists_degrees(Coord_Mod14_A1, Coord_Ld, E_diff_degrees)
        print('Result')
        print(Result_degrees)
    else:
        print('Landsat or MODIS are empty')
        
def numpy_to_txt(folder, name):
    lat = np.load(folder+'\latarr_'+name+'.npy')
    lon = np.load(folder+'\lonarr_'+name+'.npy')
    
    
    file  = open(folder  +r'\coordinates_'+name+'.txt','w')
    for i in range(len(lat)):
        file.write( str(lat[i]) + ', '+ str(lon[i]) + '\n')
    file.close()


E_diff_km      = 1 # 1 km 
E_diff_degrees = 2.740169953384774e-05


path_modis = r'D:\MODIS\script\result\may2014_august2014\MOD14A1.A2014169.h12v10.006.2015288043634.hdf'
path_landsat_coor = r'D:\MODIS\script\result\Article_coordinates'
folder = r'D:\MODIS\script\result\Article_coordinates\coordinates_pointmodis_landsat'


info_Ld = '226069_20140820_20170420' 
info_MOD = path_modis[-8:-4]

Date_Landsat = info_Ld[7:11]+'-'+info_Ld[11:13]+'-'+info_Ld[13:15]   
mtl = path_landsat_coor + '\LC08_L1TP_'+info_Ld+ '_01_T1_MTL.txt'

print('Data Landsat', Date_Landsat)
print()
Landsat_MODIS(path_landsat_coor, info_MOD, info_Ld, E_diff_km, E_diff_degrees, mtl)

# MODIS_save_coordinates(path_modis, path_landsat_coor, Date_Landsat, info_MOD, mtl)
# numpy_to_txt(folder, 'MOD14A1_' + info_MOD)



