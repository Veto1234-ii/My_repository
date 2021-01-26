import numpy as np

def calculateBorders( np_filepath, info, resultpath, border_width = 40):
    b1 = np.load(np_filepath + r'Landsat_' + info + '_B1.npy')
    
    min_val = b1[0][0] 
    shape = b1.shape
    res1 = np.full(shape, False, dtype=bool)
    np.putmask(res1, b1 != min_val , True)
    result = np.copy(res1)
    
    for i in range(2, shape[0]-2):
        for j in range(2, shape[1]-2):
            if res1[i][j]== True:
                arr = res1[i-border_width:i+border_width,j-border_width:j+border_width]
                count = arr.shape[0]*arr.shape[1]
                if np.sum(arr) < count:
                    result[i][j] = False
                          
    np.save(resultpath + 'clip_'+ info, result)
    print("borders done" + str(np.sum(result)))



