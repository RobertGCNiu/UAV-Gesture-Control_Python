
from matplotlib import pyplot as plt
import numpy as np
import math
import scipy.io as sio
import os
#
#what of keypoints have multi-matirx?
def keypoints2Matrix(keypoints_need):
    vec_all = np.zeros([8,2])
    vec_all[0,:] = 0#(keypoints_need[1,:] - keypoints_need[2,:])/np.linalg.norm((keypoints_need[1,:] - keypoints_need[2,:]),ord=1) #1-2
    vec_all[1,:] = 0#(keypoints_need[1,:] - keypoints_need[5,:])/np.linalg.norm((keypoints_need[1,:] - keypoints_need[5,:]),ord=1) #1-5
    vec_all[2,:] = 0#(keypoints_need[1,:] - keypoints_need[8,:])/np.linalg.norm((keypoints_need[1,:] - keypoints_need[8,:]),ord=1) #1-8
    vec_all[3,:] = 0#(keypoints_need[1,:] - keypoints_need[0,:])/np.linalg.norm((keypoints_need[1,:] - keypoints_need[0,:]),ord=1) #1-0
    vec_all[4,:] = (keypoints_need[2,:] - keypoints_need[3,:])/np.linalg.norm((keypoints_need[2,:] - keypoints_need[3,:]),ord=1) #2-3
    vec_all[5,:] = (keypoints_need[3,:] - keypoints_need[4,:])/np.linalg.norm((keypoints_need[3,:] - keypoints_need[4,:]),ord=1) #3-4
    vec_all[6,:] = (keypoints_need[5,:] - keypoints_need[6,:])/np.linalg.norm((keypoints_need[5,:] - keypoints_need[6,:]),ord=1) #5-6
    vec_all[7,:] = (keypoints_need[6,:] - keypoints_need[7,:])/np.linalg.norm((keypoints_need[6,:] - keypoints_need[7,:]),ord=1) #6-7
    return vec_all

def Euclidean(vec1, vec2):
    npvec1, npvec2 = np.array(vec1), np.array(vec2)
    return np.linalg.norm((npvec1-npvec2),ord=2)
# def inner_product(vec1,vec2):
#     npvec1,npvec2 = np.array(vec1), np.array(vec2)
#     #print(np.size(npvec1),np.size(npvec2))
#     innerproduct_abs = abs(np.dot(npvec1 , np.transpose(npvec2)))
#     print(np.diag(innerproduct_abs))
#     return  sum(np.diag(innerproduct_abs))

def calculate_dist(keypoints_collection,input_Pose):
    keypoints = keypoints_collection.get('keypoints')
    new = np.reshape(keypoints,(pose_times,25,3))
    input_Pose = input_Pose[0,0:9,0:2]
    inputvec_all = keypoints2Matrix(input_Pose)
    #print(inputvec_all)
    #what if keypoints are larger than 1 matrix
    dist = np.zeros((pose_times))
    for pose_inx in range(pose_times):
        keypoints_pts = new[pose_inx,0:9,0:2]
        vec_all = keypoints2Matrix(keypoints_pts)
        dist[pose_inx] = Euclidean(vec_all,inputvec_all)
    return dist

def labeled_to_dist(dist,label):
    dist_all = np.zeros((pose_times, 2))
    dist_all[:, 0] = np.transpose(dist)
    dist_all[:, 1] = label
    return dist_all

def knn(dist_all):
    x_fre = np.zeros(pose_number)
    dist_sort_index = np.argsort(dist_all[:,0])
    k_min_index = dist_sort_index[0:k]
    l = dist_all[k_min_index,1]
    for i in range(pose_number):
        x_fre[i] = (l==i).sum()
    # print(x_fre)
    return np.argmax(x_fre), dist_all[k_min_index,0]


pose_times = 10
pose_number = 7#!!!!
k = 10
path1=os.path.abspath('')

def implement_kNN(input_Pose):
    #input_Pose = np.load('yogav.npy')

    keypoint_collection_1 = sio.loadmat(path1 + os.sep+'./action_uleft')
    keypoint_collection_2 = sio.loadmat(path1 + os.sep+'./action_right')
    keypoint_collection_3 = sio.loadmat(path1 + os.sep+'./action_left')
    keypoint_collection_4 = sio.loadmat(path1 + os.sep+'./action_uright')
    keypoint_collection_5 = sio.loadmat(path1 + os.sep+'./action_v')
    keypoint_collection_6 = sio.loadmat(path1 + os.sep+'./action_lr')
    keypoint_collection_7 = sio.loadmat(path1 + os.sep + './action_lrr')

    dist_1 = calculate_dist(keypoint_collection_1,input_Pose)
    dist_2 = calculate_dist(keypoint_collection_2,input_Pose)
    dist_3 = calculate_dist(keypoint_collection_3,input_Pose)
    dist_4 = calculate_dist(keypoint_collection_4,input_Pose)
    dist_5 = calculate_dist(keypoint_collection_5,input_Pose)
    dist_6 = calculate_dist(keypoint_collection_6,input_Pose)
    dist_7 = calculate_dist(keypoint_collection_7, input_Pose)

    dist_1_all = labeled_to_dist(dist_1,0)
    dist_2_all = labeled_to_dist(dist_2,1)
    dist_3_all = labeled_to_dist(dist_3,2)
    dist_4_all = labeled_to_dist(dist_4,3)
    dist_5_all = labeled_to_dist(dist_5,4)
    dist_6_all = labeled_to_dist(dist_6,5)
    dist_7_all = labeled_to_dist(dist_7, 6)

    dist_all = np.vstack((dist_1_all,dist_2_all,dist_3_all, dist_4_all, dist_5_all,dist_6_all,dist_7_all))
    dist_sort_index = np.argsort(dist_all[:,0])
    return knn(dist_all)


# print(knn(dist_all,10))
#
# # print(dist_all)
# print(dist_all[dist_sort_index,:])


# keypoint_collection_2 = sio.loadmat('./action_5')
# keypoint2 = keypoint_collection_2.get('keypoints')
# print(keypoint2[0:25,:])
#
# np.save('predict3',keypoint2[0:25,:])
# print(keypoint2)
#keypoints = np.array(keypoints)
# keypoints_cpts = collect_0_9_keypoints(keypoints)
# #print(keypoints)
#
# keypoints = keypoints[249,:][0:2]
# new = np.zeros([1,2,2])
# new[0,0,:] = keypoints
# new[0,1,:] = keypoints
# print(new)




# keypoints = np.load('policeman.txt.npy')
# label_A = 'A'
# keypoints_new = np.load('policeman_pose.npy')
# label_B = 'B'
# #print(New_all)
# keypoints = keypoints[0,:,:]
# keypoints_new = keypoints_new[0,:,:]
# #print(keypoints)
# keypoints_need = keypoints[0:9,0:2]
# new_keypoints_need = keypoints_new[0:9,0:2]
# #print(keypoints_need)

# #print(vec_all)
#
# def Euclidean(vec1, vec2):
#     npvec1, npvec2 = np.array(vec1), np.array(vec2)
#     return np.linalg.norm((npvec1-npvec2),ord=2)
#
# vec_all = keypoints2Matrix(keypoints_need)
# New_vec_all = keypoints2Matrix(new_keypoints_need)
#
# for New_vec_all in matrix_all:
#     x = Euclidean(vec_all,New_vec_all)
# np.min(x)





# # 定义四个点的坐标
# a1 = np.array([1, 1])
# a2 = np.array([1, 2])
# b1 = np.array([3, 3])
# b2 = np.array([3, 4])
# c = np.array([2, 1])
#
# # 四个点坐标分别赋值给X,Y
# X1, Y1 = a1
# X2, Y2 = a2
# X3, Y3 = b1
# X4, Y4 = b2
# X5, Y5 = c
#
# plt.title('show data')
# plt.scatter(X1, Y1, color="blue", label="a1")
# plt.scatter(X2, Y2, color="blue", label="a2")
# plt.scatter(X3, Y3, color="red", label="b1")
# plt.scatter(X4, Y4, color="red", label="b2")
# plt.scatter(X5, Y5, color="yellow", label="c")
#
# plt.annotate(r'a1(1,1)', xy=(X1, Y1), xycoords='data', xytext=(+10, +20), textcoords='offset points',fontsize=12, arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
# plt.annotate(r'a2(1,2)', xy=(X2, Y2), xycoords='data', xytext=(+10, +20), textcoords='offset points',fontsize=12, arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
# plt.annotate(r'b1(3,3)', xy=(X3, Y3), xycoords='data', xytext=(+10, +20), textcoords='offset points',fontsize=12, arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
# plt.annotate(r'b2(3,4)', xy=(X4, Y4), xycoords='data', xytext=(+10, +20), textcoords='offset points', fontsize=12, arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
#
# plt.annotate(r'c(2,1)', xy=(X5, Y5), xycoords='data', xytext=(+30, 0), textcoords='offset points', fontsize=12, arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
#
#
# def Euclidean(vec1, vec2):
#     npvec1, npvec2 = np.array(vec1), np.array(vec2)
#     return math.sqrt(((npvec1-npvec2)**2).sum())
#
# # 显示距离
# def show_distance(exit_point, c):
#     line_point = np.array([exit_point, c])
#     x = (line_point.T)[0]
#     y = (line_point.T)[1]
#     o_dis = round(Euclidean(exit_point, c), 2)  # 计算距离
#     mi_x, mi_y = (exit_point+c)/2  # 计算中点位置，来显示“distance=xx”这个标签
#     plt.annotate('distance=%s' % str(o_dis), xy=(mi_x, mi_y), xycoords='data', xytext=(+10, 0), textcoords='offset points', fontsize=10, arrowprops=dict(arrowstyle="-", connectionstyle="arc3,rad=.2"))
#     return plt.plot(x, y, linestyle="--", color='black', lw=1)
#
# show_distance(a1, c)
# show_distance(a2, c)
# show_distance(b1, c)
# show_distance(b2, c)
# plt.show()