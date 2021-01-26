import matplotlib.pyplot as plt
import numpy as np

def Visualization(np_folder,info,n_band):
    
    latarr = np.load(np_folder + r'latarr_Temperature_Band_'+str(n_band)+'_'+info+'.npy')
    lonarr = np.load(np_folder + r'lonarr_Temperature_Band_'+str(n_band)+'_'+info+'.npy')
    print(latarr.shape)
    file  = open(r'Thermal_'+info+'.txt','w')
    for i in range(len(lonarr)):
        file.write( str(latarr[i]) + ', '+ str(lonarr[i]) + '\n')
    file.close()
    
    y = latarr
    x = lonarr
    
    fig, ax = plt.subplots()
    
    ax.scatter(x, y, c = 'red') 
      
    ax.set_facecolor('white')     #  цвет области Axes
    
    fig.set_figwidth(10)     #  ширина и
    fig.set_figheight(10)    #  высота "Figure"
    
    plt.show()




            

