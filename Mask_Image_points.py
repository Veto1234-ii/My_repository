import numpy as np
import matplotlib.pyplot as plt
import imageio
from PIL import Image

#def Reshape_image(path_res, shape, info):
#    
#    img = Image.open(path_res + '\LC08_L1TP_'+info+'_01_T1.jpg')
#    
#    newimg = img.resize(shape)
#    
#    newimg = newimg.save(path_res + '\LC08_L1TP_'+info+'_01_T1_2.jpg') 


def Save_image_points(firemask, info, path_res):
    
    res = np.load(firemask)
    shape = res.shape
    
    img = plt.imread(path_res + '\LC08_L1TP_'+info+'_01_T1_2.jpg')
    img = np.array(img)
    
    
    mx = np.max(img)
    mn = np.min(img)
    
    
    for i in range(shape[0]):
        for j in range(shape[1]):
            if res[i][j]!=0:
                img[i-50:i+51, j-50:j+51, 0] = mx
                img[i-50:i+51, j-50:j+51, 1] = mn
                img[i-50:i+51, j-50:j+51, 2] = mx
                
                
    imageio.imwrite(path_res + '\img_'+info+'.jpg', img)
    
