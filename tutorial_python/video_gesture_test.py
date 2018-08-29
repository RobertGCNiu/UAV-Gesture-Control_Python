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


def gesture_recognize(keypoints,flags):  # define function to recognize gesture
    # flags = numpy.zeros((1, 4))  # initial count of each gesture are all 0
    v_56 = keypoints[6, 0:2] - keypoints[5, 0:2]  # left shoulder and arm
    # v_67 = keypoints[7, 0:2] - keypoints[6, 0:2]  # left arm and hand
    v_15 = keypoints[5, 0:2] - keypoints[1, 0:2]  # neck and left shoulder
    v_12 = keypoints[2, 0:2] - keypoints[1, 0:2]  # neck and right shoulder
    v_23 = keypoints[3, 0:2] - keypoints[2, 0:2]  # right shoulder and arm
    v_17 = keypoints[7, 0:2] - keypoints[1, 0:2]  # neck and left hand
    v_14 = keypoints[4, 0:2] - keypoints[1, 0:2]  # neck and right hand
    # normalize vector
    nv_56 = v_56 / numpy.linalg.norm(v_56, ord=1)
    # nv_67 = v_67 / numpy.linalg.norm(v_67, ord=1)
    nv_15 = v_15 / numpy.linalg.norm(v_15, ord=1)
    nv_12 = v_12 / numpy.linalg.norm(v_12, ord=1)
    nv_23 = v_23 / numpy.linalg.norm(v_23, ord=1)
    nv_17 = v_17 / numpy.linalg.norm(v_17, ord=1)
    nv_14 = v_14 / numpy.linalg.norm(v_14, ord=1)
    dv_15_56 = numpy.vdot(nv_15, nv_56)
    # print('dv_15_56 = %f' %dv_15_56)
    dv_12_23 = numpy.vdot(nv_12, nv_23)
    # print('dv_12_23 = %f' % dv_12_23)
    dv_v_17 = numpy.vdot([0,1], nv_17)  # dot product of positive vertical line and the v_17,
                                        # if we lift left hand it should be positive
    dv_v_14 = numpy.vdot([0, 1], nv_14) # dot product of positive vertical line and the v_14,
                                        # if we lift right hand it should be positive
    # if (dv_15_56 >= 0 and dv_15_56 <= 0.7 and dv_v_17 > 0 and dv_v_14 <= 0):  # the angle btw arm_shoulder
    if (dv_12_23 >= 0 and dv_12_23 <= 0.7 and dv_v_14 > 0 and dv_v_17 <= 0):
        flags[0, 0] = flags[0, 0] + 1  # and the neck_arm is 90-135 degree
    # elif (dv_12_23 >= 0 and dv_12_23 <= 0.7 and dv_v_14 > 0 and dv_v_17 <= 0):  # the angle btw arm_shoulder
    elif (dv_15_56 >= 0 and dv_15_56 <= 0.7 and dv_v_17 > 0 and dv_v_14 <= 0):
        flags[0, 1] = flags[0, 1] + 1  # and the neck_arm is 90-135 degree
    print(flags)
    return flags


def main():
    drone = tellopy.Tello()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)
        # drone.startControlCommand()
        # drone.takeoffsimplecontrol()
        # drone.takeoff()
        # sleep(3)
        # drone.land()
        # sleep(3)
        drone.set_video_encoder_rate(1)
        container = av.open(drone.get_video_stream())
        # print('Start Video Stream**********************************')
        # skip first 300 frames
        frame_skip = 300
        count_frame = 10
        # count = 0
        flags = numpy.zeros((1, 4))
        while True:
            for frame in container.decode(video=0):
                # count+=1
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                start_time = time.time()
                interupt = cv2.waitKey(10)
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                keypoints, output_image = openpose.forward(image, True)
                # print(keypoints)
                cv2.imshow("output", output_image)

                if numpy.size(keypoints) != 0:
                    keypoints = keypoints[0,:,:]
                    # print('*********************************************************************************')
                    # print('the shape of output keypoints is ', numpy.shape(keypoints))
                    flags = gesture_recognize(keypoints,flags)  # let each image compare with keypoints transfered vector and
                                                    # accumualte counts in every 20 frames

                    # if count%count_frame!=0:   # look for 20 continuous frame and recognize the gesture in every 20 frames
                    #     continue
                    if 0 < count_frame:
                        count_frame = count_frame - 1
                        continue
                    # print('*****       count_frame=%d       *****' %count_frame)
                    idx = numpy.argmax(flags)
                    print('*****       index=%d       *****' %idx)
                    if flags[0,idx] >=5:
                        print(idx)
                        if idx==0:
                            drone.takeoff()
                        if idx==1:
                            drone.land()
                        if idx==2:
                            drone.leftsimplecontrol(20)
                        if idx==3:
                            drone.rightsimplecontrol(20)
                    # else:


                elif interupt & 0xFF == ord('q'):
                    cv2.destroyWindow(output_image)
                    drone.land()
                    # drone.quitsimplecontrol()
                    sleep(1)
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
                count_frame = 10
                flags = numpy.zeros((1, 4)) # initial count of each gesture are all 0
                # print('*****       count_frame=%d       *****' % count_frame)
                # frame_skip = int((time.time() - start_time) / frame.time_base)
                frame_skip = 100

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
