import numpy as np

keypoints = np.load('policeman.txt.npy')
left_arm = keypoints[0,4] - keypoints[0,2]
right_arm = keypoints[0,7] - keypoints[0,5]
left_arm_vec = left_arm[[0,1]]
right_arm_vec = right_arm[[0,1]]
L_left = np.sqrt(left_arm_vec.dot(left_arm_vec))
L_right = np.sqrt(right_arm_vec.dot(right_arm_vec))
cos_angle = left_arm_vec.dot(right_arm_vec)/(L_left*L_right)

angle = np.arccos(cos_angle)*180/np.pi
if int(angle)>70&int(angle)<110:
    print('ok')

if sum(keypoints[0,2])!=0:
    print(keypoints)