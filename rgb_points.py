import numpy as np
import matplotlib.pyplot as plt
import imageio
from PIL import Image
import os

def  Create_path(path, info):

    firemask = path + r'/fire_mask_' + info + '.npy'
    path_rgb = path + '/rgb_'+info+'.jpg'
    path_res = path + '/img_'+info+'.jpg'
    
    return firemask, path_rgb, path_res

def range_0_255(a, band):
    b = a.ravel()# из b создает одномерный массив
#    print(b.shape)
    h = np.histogram(b,1000, range = (0, b.max()))
    
#    plt.plot(h[0])
#    plt.title("Histogram Band " + str(band))
#    plt.show()
    
    for i in range(2,1000):
        if sum(h[0][-i:-1]) > b.shape[0]*0.02 :
            mx = h[1][-i]
            break
        
    for i in range(2,1000):
        if sum(h[0][1:i]) > b.shape[0]*0.02 :
            mn = h[1][i]
            break
        
    
    a[a>mx] = mx 
    a[a<mn] = mn

    a = (a - mn)*255/(mx - mn)
    
    mx = np.max(a)
    mn = np.min(a)
    
    a = np.power(a, 0.5)
    
    mx = np.max(a)
    mn = np.min(a)
    
    a = (a - mn)*255/(mx - mn)

    return a

def Create_RGB(path, info):
    
    path_bands = path + '\Landsat_' + info +'_B'

    
    b2 = np.load(path_bands +'2.npy')
    b3 = np.load(path_bands +'3.npy')
    b4 = np.load(path_bands +'4.npy')
    
    b2 = range_0_255(b2, 2)
    b3 = range_0_255(b3, 3)
    b4 = range_0_255(b4, 4)
    
    
    rgb = np.dstack([b4, b3, b2])
    rgb = rgb.astype(np.uint8)
    
    
    imageio.imwrite(path + '/rgb_'+info+'.jpg', rgb)

def Save_image_points(path, info):
    
    firemask, path_rgb, path_res = Create_path(path, info)
    
    res = np.load(firemask)
    shape = res.shape
    
    img = plt.imread(path_rgb)
    img = np.array(img)
    
    
    mx = np.max(img)
    mn = np.min(img)
    
    
    for i in range(shape[0]):
        for j in range(shape[1]):
            if res[i][j]!=0:
                img[i-50:i+51, j-50:j+51, 0] = mx
                img[i-50:i+51, j-50:j+51, 1] = mn
                img[i-50:i+51, j-50:j+51, 2] = mx
                
                
    imageio.imwrite(path_res, img)




#path =  r'D:/VETOSHNIKOVA/Snapshots/result'   
#info =  '175021_20180623_20180703'
#
#Create_RGB(path, info)
#Save_image_points(path, info)





