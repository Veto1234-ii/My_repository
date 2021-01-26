import numpy as np
import math
import datetime
from comparison import *
from coordinates import index_corners
from utilities import getMTL


np_folder = r'result/'
Names_images = ['20140623', '20140522', '20140319', '20140215', '20131229']
E_diff = 1# km

def Print_Dict(d):
    print()
    print()
    for key,value in d.items():
        # print(key,value[2],' days')
        print(key,value[1],' points')
        

def Analysis(np_folder, Names_images, E_diff): 
    
    d2 ={}
    arr_coordinates = []
    for i in range(len(Names_images)):
        arr_coordinates.append(Lists_coordinates(np_folder, Names_images[i]))
        
    for i in range(len(arr_coordinates)-1):
        for j in range(i+1, len(arr_coordinates)):
            
            res = compare_coordinates_lists_2(arr_coordinates[i], arr_coordinates[j], E_diff)
            
            if len(res)!=0:
                d2[(Names_images[i],Names_images[j])] = (res, len(res))
    return d2

def comparison_comparison(d2, Names_images, E_diff):
    d3 = {}
    for key, value in d2.items():
        for i in range(len(Names_images)):
            if Names_images[i] in key:
                continue
            else:
                arr2 = Lists_coordinates(np_folder, Names_images[i])
                res = compare_coordinates_lists_2(value[0], arr2, E_diff)
                if len(res)!=0:
                    d3[key + (Names_images[i],)] = (res, len(res))
    return d3    


def Points_match_2_or_more(np_folder, Names_images, E_diff):
    arr_dict = []
    
    d = Analysis(np_folder, Names_images, E_diff)
    arr_dict.append(d)
    Print_Dict(d)
    
    k = len(Names_images) - 2
    for i in range(k):
        d = comparison_comparison(d, Names_images, E_diff)    
        Print_Dict(d)
        arr_dict.append(d)
        
    return arr_dict


def coordinates_points(np_folder, Names_images, E_diff):
    
    arr_dict = Points_match_2_or_more(np_folder, Names_images, E_diff)
    
    for i in range(len(arr_dict)-1, -1, -1):
        if len(arr_dict[i])!=0:
            break
    
    d = arr_dict[i]
    
    points = []
    for key,value in d.items():
        points.extend(value[0])
        
    points = set(points)
    points = list(points)
    
    result = []
    dist = []
    
    for i in range(len(points)):
        arr = []
        for j in range(i+1, len(points)):
            diff = length(points[i][0], points[i][1], points[j][0], points[j][1])
            dist.append((diff, i+1, j+1)) 
            
            if diff > E_diff:
                result.append((points[i][0], points[i][1]))
    
    images = list(d.keys())[0]        
    return (points, result, dist, images)

def FromCoordinatesToValue_b7(filepath, np_folder, info, lat, lon):
    b7 = np.load(np_folder + r'Landsat_' + info + '_B7.npy')
    mtl  = filepath + '_01_T1_MTL.txt'
    data = getMTL(mtl)

    UL_LAT = float(data['CORNER_UL_LAT_PRODUCT'])
    UL_LON = float(data['CORNER_UL_LON_PRODUCT'])
    UR_LAT = float(data['CORNER_UR_LAT_PRODUCT'])
    UR_LON = float(data['CORNER_UR_LON_PRODUCT'])
    LL_LAT = float(data['CORNER_LL_LAT_PRODUCT'])
    LL_LON = float(data['CORNER_LL_LON_PRODUCT'])
    LR_LAT = float(data['CORNER_LR_LAT_PRODUCT'])
    LR_LON = float(data['CORNER_LR_LON_PRODUCT'])
    
    Corners      = index_corners(b7)
#  (Max_ind_line, Min_ind_line, Max_ind_col, Min_ind_col)
    
    Max_ind_line = Corners[0]
    offsetY      = Corners[1]
    Max_ind_col  = Corners[2]
    offsetX      = Corners[3]
    
    Max_Lat = max(UL_LAT,UR_LAT,LL_LAT,LR_LAT)
    Min_lat = min(UL_LAT,UR_LAT,LL_LAT,LR_LAT)
    Max_lon = max(UL_LON,UR_LON,LL_LON,LR_LON)
    Min_lon = min(UL_LON,UR_LON,LL_LON,LR_LON)

    p_lat = abs((Max_Lat - Min_lat)/(Max_ind_line - offsetY))
    p_lon = abs((Max_lon - Min_lon)/(Max_ind_col - offsetX))

    Ind_Y = offsetY + math.ceil((Max_Lat - lat)/p_lat)
    Ind_X = offsetX + math.ceil((lon - Min_lon)/p_lon)
    
    val = b7[Ind_Y][Ind_X]
    
    return val 

coor_p = coordinates_points(np_folder, Names_images, E_diff)
points = coor_p[0]
result = coor_p[1]
dist   = coor_p[2]    
images = coor_p[3]

# print(points)        
print()
# print(dist)
print()
print(result)

print()
# print(images)