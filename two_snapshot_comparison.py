from comparison import *

X_1 = '188034_20140623_20170421'
X_2 = '188034_20140522_20180527'
k = 1 # нужное кол-во точек

# 188034_20140623_20170421
# 188034_20140522_20180527
# 188034_20140215_20170425
# 188034_20140319_20170425
# 188034_20131229_20170427

filepath = r'F:\Gis\188034\LC08_L1TP_'+X_1+'_01_T1\Image\LC08_L1TP_'+X_1
np_filepath = r'result/'

snapshot1 = X_1[7:15]
snapshot2 = X_2[7:15]

arr1 = Lists_coordinates(np_filepath, snapshot1)
arr2 = Lists_coordinates(np_filepath, snapshot2)

arrays = Minimum_Len_array(arr1, arr2)
Test_sample_coord = arrays[1]
GT_coord = arrays[0]

print(len(Test_sample_coord), 'Points Test_sample')
print(len(GT_coord), 'Points Ground truth')

days = time(snapshot1, snapshot2)
print(days, 'days')


func = Minimum_distance(GT_coord, Test_sample_coord, k)
E_diff_d = func[0]
E_diff_km = func[1]
print('min E_diff in degrees', E_diff_d)
print('min E_diff in kilometers', E_diff_km)

dist_points = Dist_GT_test(GT_coord, Test_sample_coord)
dist_points_sort = sorted(dist_points, key = lambda x: x[0])
print()
# print(dist_points_sort)


res = compare_coordinates_lists_2(GT_coord, Test_sample_coord, 0.03)
print(len(res), 'points')
print(res)

func = Сalculation_E_diff_corners(filepath, np_filepath, X_1)
p_lat = func[0]
p_lon = func[1]

print(p_lat,'degrees of latitude in 30 m')
print(p_lon,'degrees of longitude in 30 m')
# Visualization_arr(res, snapshot1+'_'+snapshot2, 'green')
# file.close()