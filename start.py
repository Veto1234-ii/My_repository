from Main import Main
import os

def Loading_processing(filepath, X_arr, FIRMS, nameFile, path_res):

    # file = open(path_res + nameFile + '.txt','w')
    # file.write('Snapshot, Fire algorithm output pixels, FIRMS, Points coincided with firms, unsure, medium confident, confident')
    
    
    for i in range(len(X_arr)):
        
        
        mtl = filepath + '\LC08_L1TP_'+X_arr[i]+ '_01_T1_MTL.txt'
#        print('MTL',mtl)
        
        main  = Main(X_arr[i], filepath, FIRMS, mtl, path_res)
        

        k_alg      = main[0]# Fire algorithm output pixels
        print(k_alg, 'FIRE PIXELS')
        
        # firms      = main[1]# всего у firms  за тот период
        # Points     = main[2]# совпало с ландсатом
        # k_unsure   = main[3]
        # k_med_conf = main[4]
        # k_conf     = main[5]
        
    #     fileStr = 'LC08_L1TP_'+X_arr[i]+'_01_T1, ' + str(k_alg)+', '+str(firms)+', '+str(Points)+', '+str(k_unsure)+', '+str(k_med_conf)+', '+str(k_conf)
        
    #     file.write('\n' + fileStr + '\n')
    # file.close()    
    # print('file close')    

        

path_res = r'D:\MODIS\script\result\Article_coordinates'

FIRMS = r'\fire_archive_M6_13348.csv'
nameFile = '\Snapshot_article'

# list_files = os.listdir(filepath)
# X_arr = [list_files[i][10:34] for i in range(len(list_files) - 1)]
# X_arr = ['023034_20140518_20180131','188034_20140623_20170421', 
        # '026048_20140507_20170306', '105069_20140805_20170420',
        # '226069_20140820_20170420', '227069_20140624_20170421']
X_arr = ['105069_20140805_20170420']


print()
print(X_arr)
print()

Loading_processing(path_res, X_arr, FIRMS, nameFile, path_res)
    
