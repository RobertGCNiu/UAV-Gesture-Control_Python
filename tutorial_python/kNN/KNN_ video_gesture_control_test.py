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
import kNNtest
from sklearn.preprocessing import normalize

sys.path.append('../../../python')
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
params["default_model_folder"] = dir_path + "/../../../../models/"
# Construct OpenPose object allocates GPU memory
openpose = op.OpenPose(params)

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
        print('Start Video Stream**********************************')
        # skip first 10 frames

        frame_skip = 10
        count_frame = 10
        # count = 0
        flags = numpy.zeros((1, 4))
        while True:
            for frame in container.decode(video=0):
                # count+=1
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                # start_time = time.time()
                interupt = cv2.waitKey(10)
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                keypoints, output_image = openpose.forward(image, True)
                cv2.imshow("output", output_image)

                if numpy.size(keypoints) > 40:
                    (idx,dist_all) = kNNtest.implement_kNN(keypoints)

                    if dist_all[0]<0.7:
                        print('*****       Pose_Idx=%d       *****' % idx)
                        if idx==2: ###left
                            drone.takeoff()
                        elif idx==1:
                            drone.land()
                        elif idx==3:
                            drone.leftsimplecontrol(20)
                        elif idx==0:
                            drone.rightsimplecontrol(20)
                        elif idx==4:
                            drone.flip_leftsimplecontrol()
                            #drone.upsimplecontrol(20)
                        elif idx ==5:
                            drone.downsimplecontrol(20)


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
                count_frame = 10
                flags = numpy.zeros((1, 4)) # initial count of each gesture are all 0
                # print('*****       count_frame=%d       *****' % count_frame)
                # frame_skip = int((time.time() - start_time) / frame.time_base)
                frame_skip = 20

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
