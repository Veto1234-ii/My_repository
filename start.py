from Main import Main
import os

def Loading_processing(filepath, X_arr, FIRMS, nameFile, path_res):

#    file = open(filepath + r"/result/" + nameFile + '.txt','w')
#    file.write('Snapshot, Fire algorithm output pixels, Points coincided with firms, unsure, medium confident, confident')
    
    
    for i in range(len(X_arr)):
        
        
        mtl = filepath + '\LC08_L1TP_'+X_arr[i]+'_01_T1\LC08_L1TP_'+X_arr[i]+ '_01_T1_MTL.txt'
#        print('MTL',mtl)
        
        main = Main(X_arr[i], filepath, FIRMS, mtl, path_res)
#        k_alg      = main[0]# Fire algorithm output pixels
#        firms      = main[1]# match with firms
#        k_unsure   = main[2]
#        k_med_conf = main[3]
#        k_conf     = main[4]
        
#        fileStr = 'LC08_L1TP_'+X_arr[i]+'_01_T1, ' + str(k_alg)+', '+str(firms)+', '+str(k_unsure)+', '+str(k_med_conf)+', '+str(k_conf)
        
#        file.write('\n' + fileStr + '\n')
        
#    file.close()    
        

filepath = r'D:\VETOSHNIKOVA\Snapshots'

FIRMS = r'\fire_archive_M6_120507.csv'
nameFile = 'Snapshot174020'
path_res = filepath + r'\result'

list_files = os.listdir(filepath)
X_arr = [list_files[i][10:34] for i in range(len(list_files) - 1)]

print()
print(X_arr)
print()

Loading_processing(filepath, X_arr, FIRMS, nameFile, path_res)
    