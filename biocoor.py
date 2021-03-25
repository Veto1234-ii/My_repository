import numpy as np
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
        
    
    
    
p1 = (-11.96569, -55.68193)
p2 =(-12.32898, -53.96557)
p3 = (-14.04923, -54.35316)
Vec2i_P = (-12.71244, -54.89999)


print(barycentric(p1, p2, p3, Vec2i_P))