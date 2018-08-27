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

sys.path.append('../../python')
dir_path = os.path.dirname(os.path.realpath(__file__))

try:
    from openpose import openpose as op
    # from openpose import *
except:
    raise Exception('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')

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

def whatPosition(keypoints):
    if int(sum(keypoints[0,4]))!=0 & int(sum(keypoints[0,2]))!=0 & int(sum(keypoints[0,7]))!=0&int(sum(keypoints[0,5]))!=0:
        left_arm = keypoints[0,4] - keypoints[0,2]
        right_arm = keypoints[0,7] - keypoints[0,5]
        left_arm_vec = left_arm[[0,1]]
        right_arm_vec = right_arm[[0,1]]
        L_left = numpy.sqrt(left_arm_vec.dot(left_arm_vec))
        L_right = numpy.sqrt(right_arm_vec.dot(right_arm_vec))
        cos_angle = left_arm_vec.dot(right_arm_vec)/(L_left*L_right)

        angle = numpy.arccos(cos_angle)*180/numpy.pi
        return angle
        # if int(angle)>70&int(angle)<110:
        #     position = 'l'
        #     return position


def main():
    drone = tellopy.Tello()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)
        #drone.startControlCommand()
        #drone.takeoffsimplecontrol()
        #drone.takeoff()
        # sleep(3)
        #drone.land()
        # sleep(3)
        drone.set_video_encoder_rate(1)
        container = av.open(drone.get_video_stream())
        print('Start Video Stream**********************************')
        # skip first 300 frames
        frame_skip = 300

        while True:
            for frame in container.decode(video=0):

                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                start_time = time.time()

                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                #cv2.imshow('Original', image)

                keypoints, output_image = openpose.forward(image, True)
                cv2.imshow("output", output_image)
                # cv2.waitKey(1)
                if numpy.size(keypoints) > 1:
                    angle = whatPosition(keypoints)
                    print(str(angle)+'**************************')
                # if numpy.size(keypoints)>1:
                #     a = whatPosition(keypoints)
                #     if a=='l':
                #         print('hello***********************************************')
               #          drone.land()
               #          sleep(2)
               #
                waitkey_num = cv2.waitKeyEx()
               # cv2.imshow('Canny', cv2.Canny(image, 100, 200))


                if waitkey_num == ord('q'):
                    cv2.destroyWindow(output_image)
                    drone.land()
                    # drone.quitsimplecontrol()
                    sleep(1)
                if waitkey_num == ord('l'):
                    drone.land()
                    sleep(2)
                if waitkey_num == ord('w'):
                    drone.forwardsimplecontrol(20)
                    # sleep(1)
                if waitkey_num == ord('s'):
                    drone.backwardsimplecontrol(20)
                    sleep(1)
                if waitkey_num == ord('a'):
                    drone.leftsimplecontrol(20)
                    sleep(1)
                if waitkey_num == ord('d'):
                    drone.rightsimplecontrol(20)
                    sleep(1)
                if waitkey_num == ord('z'):
                    drone.clockwisesimplecontrol(20)
                    sleep(1)
                if waitkey_num == ord('c'):
                    drone.flip_rightsimplecontrol()
                    sleep(1)
                if waitkey_num == ord('t'):
                    drone.takeoffsimplecontrol()
                    sleep(2)
                if waitkey_num == ord('u'):
                    drone.upsimplecontrol(20)
                    sleep(1)
                if waitkey_num == ord('n'):
                    drone.downsimplecontrol(20)
                    sleep(1)
                if waitkey_num == ord('v'):
                    drone.contourclockwisesimplecontrol(20)
                    sleep(1)
                frame_skip = int((time.time() - start_time)/frame.time_base)

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
