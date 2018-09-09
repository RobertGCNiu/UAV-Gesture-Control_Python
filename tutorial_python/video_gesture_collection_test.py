import sys
import traceback
import threading
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import time
import os
from time import sleep
from sklearn.preprocessing import normalize
import scipy.io as sio

sys.path.append('../../python')
dir_path = os.path.dirname(os.path.realpath(__file__))

try:
    from openpose import openpose as op
    # from openpose import *
except:
    raise Exception(
        'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')

params = dict()
params["logging_level"] = 3
params["output_resolution"] = "-1x-1"
params["net_resolution"] = "-1x368"
params["model_pose"] = "BODY_25"
params["alpha_pose"] = 0.6
params["scale_gap"] = 0.3
params["scale_number"] = 1
params["render_threshold"] = 0.05
# If GPU version is built, and multiple GPUs are available, set the ID here
params["num_gpu_start"] = 0
params["disable_blending"] = False
# Ensure you point to the correct path where models are located
params["default_model_folder"] = dir_path + "/../../../models/"
# Construct OpenPose object allocates GPU memory
openpose = op.OpenPose(params)


def main():
    # drone = tellopy.Tello()

    try:

        # count_frame = 10
        # count = 0
        loop_init = 2
        image_count = 0
        keypoints_collection = numpy.empty((0, 3), float)
        # print(' the size of keypoints_collection is', numpy.shape(keypoints_collection))
        # flags = numpy.zeros((1, 4))
        # print('The path is:' + str(dir_path))
        filename = dir_path + "/action_1.mat"

        #  check if there's a action_1.mat file, we will create action_1.mat if it's not exists

        if not os.path.exists(filename):
            sio.savemat('./action_1', mdict={'keypoints': keypoints_collection}, oned_as='row')

        # # for each person's action we take his or her action gesture and restore in 4d array [1,image_count,25,3]
        keypoints_collection_import = sio.loadmat('./action_1')
        keypoints_collection = keypoints_collection_import.get('keypoints')
        if keypoints_collection.size == 0:
            keypoints_collection = keypoints_collection.reshape(0, 3)
        print(' the size of keypoints_collection is', numpy.shape(keypoints_collection))

        while loop_init:

            img = cv2.imread("../../../examples/media/police.jpg")
            keypoints, output_image = openpose.forward(img, True)
            # print(keypoints)
            cv2.imshow("output", output_image)
            cv2.waitKey(15000)

            if numpy.size(keypoints) != 0:
                image_count += 1
                keypoints = keypoints[0,:,:]
                keypoints_collection = numpy.vstack((keypoints_collection, keypoints))


            loop_init -=1

        sio.savemat('./action_1',mdict={'out': keypoints_collection}, oned_as='row')
        # action_collection.write(keypoints_collection)

        matdata = sio.loadmat('./action_1')
        print('size of keypoint_collection', numpy.shape(keypoints_collection))
        print(matdata)

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        # drone.quit()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
