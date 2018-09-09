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
    drone = tellopy.Tello()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)
        # drone.takeoff()
        # sleep(3)
        # drone.land()
        # sleep(3)
        drone.set_video_encoder_rate(1)
        container = av.open(drone.get_video_stream())
        print('Start Video Stream**********************************')
        # skip first 10 frames

        frame_skip = 10
        # loop_init = 400
        image_count = 0
        count = 0
        keypoints_collection = numpy.empty((0, 3), float)

        # print('The path is:' + str(dir_path))
        filename = dir_path + "/lrr.mat"

        #  check if there's a action_1.mat file, we will create action_1.mat if not exists

        if not os.path.exists(filename):
            sio.savemat('./lrr', mdict={'keypoints': keypoints_collection}, oned_as='row')

        # for each person's action we take his or her action gesture and restore in 4d array [1,image_count,25,3]
        keypoints_collection_import = sio.loadmat('./lrr')
        keypoints_collection = keypoints_collection_import.get('keypoints')
        if numpy.size(keypoints_collection) == 0:
            keypoints_collection = keypoints_collection.reshape(0, 3)
        # print(' the size of keypoints_collection is', numpy.shape(keypoints_collection))
        while True:
            count += 1
            for frame in container.decode(video=0):
                # skip the required nomber frames
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                # start_time = time.time()
                interupt = cv2.waitKey(10)
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                keypoints, output_image = openpose.forward(image, True)
                cv2.imshow("output", output_image)
                # # for test image
                # img = cv2.imread("../../../examples/media/police.jpg")
                # keypoints, output_image = openpose.forward(img, True)
                # print(keypoints)


                if numpy.size(keypoints) > 40:
                    image_count += 1
                    print('count',image_count)
                    keypoints = keypoints[0,:,:]
                    keypoints_collection = numpy.vstack((keypoints_collection, keypoints))
                    # keypoints_collection = numpy.append(keypoints_collection, keypoints, axis=0)

                    # print('*********************************************************************************')
                    # print('the shape of output keypoints is ', numpy.shape(keypoints))
                    # flags = gesture_recognize(keypoints,flags)  # let each image compare with keypoints transfered vector and
                                                    # accumualte counts in every 20 frames

                    # if count%count_frame!=0:   # look for 20 continuous frame and recognize the gesture in every 20 frames
                    #     continue

                    # if 0 < count_frame:
                    #     count_frame = count_frame - 1
                    #     continue
                    # print('*****       count_frame=%d       *****' %count_frame)
                    # idx = numpy.argmax(flags)
                    # print('*****       index=%d       *****' %idx)
                    # if flags[0,idx] >=5:
                    #     print(idx)
                    #     if idx==0:
                    #         drone.takeoff()
                    #     if idx==1:
                    #         drone.land()
                    #     if idx==2:
                    #         drone.leftsimplecontrol(20)
                    #     if idx==3:
                    #         drone.rightsimplecontrol(20)
                    # else:


                elif interupt & 0xFF == ord('q'):
                    cv2.destroyWindow(output_image)
                    drone.land()
                    # drone.quitsimplecontrol()
                    # sleep(1)
                # if interupt & 0xFF == ord('l'):
                #     drone.land()
                #     sleep(2)
                # if interupt & 0xFF == ord('w'):
                #     drone.forwardsimplecontrol(20)
                #     # sleep(1)
                # if interupt & 0xFF == ord('s'):
                #     drone.backwardsimplecontrol(20)
                #     sleep(1)
                # if interupt & 0xFF == ord('a'):
                #     drone.leftsimplecontrol(20)
                #     sleep(1)
                # if interupt & 0xFF == ord('d'):
                #     drone.rightsimplecontrol(20)
                #     sleep(1)
                # if interupt & 0xFF == ord('z'):
                #     drone.clockwisesimplecontrol(20)
                #     sleep(1)
                # if interupt & 0xFF == ord('c'):
                #     drone.flip_rightsimplecontrol()
                #     sleep(1)
                # if interupt & 0xFF == ord('t'):
                #     drone.takeoff()
                #     sleep(2)
                # if interupt & 0xFF == ord('u'):
                #     drone.upsimplecontrol(20)
                #     sleep(1)
                # if interupt & 0xFF == ord('n'):
                #     drone.downsimplecontrol(20)
                #     sleep(1)
                # if interupt & 0xFF == ord('v'):
                #     drone.contourclockwisesimplecontrol(20)
                #     sleep(1)
                # if interupt & 0xFF == ord('b'):
                #     drone.flip_leftsimplecontrol()
                #     sleep(1)
                # count_frame = 10
                # flags = numpy.zeros((1, 4)) # initial count of each gesture are all 0
                # print('*****       count_frame=%d       *****' % count_frame)
                # frame_skip = int((time.time() - start_time) / frame.time_base)
                frame_skip = 100
                if image_count >= 10:  # image_count that record each person's gesture
                    break
                sleep(2)
            if count ==1:
                break

        sio.savemat('./lrr',mdict={'keypoints': keypoints_collection}, oned_as='row')
        # action_collection.write(keypoints_collection)

        # matdata = sio.loadmat('./action_1')
        print('size of keypoint_collection', numpy.shape(keypoints_collection))
        # print(matdata)

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
