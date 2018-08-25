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
               # cv2.imshow('Canny', cv2.Canny(image, 100, 200))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyWindow(output_image)
                    drone.landsimplecontrol()
                    # drone.quitsimplecontrol()
                    sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('l'):
                    drone.land()
                    sleep(2)
                if cv2.waitKey(1) & 0xFF == ord('w'):
                    drone.forwardsimplecontrol(10)
                    # sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    drone.backwardsimplecontrol(10)
                    sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('a'):
                    drone.leftsimplecontrol(10)
                    sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('d'):
                    drone.rightsimplecontrol(10)
                    sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('z'):
                    drone.clockwisesimplecontrol(10)
                    sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('c'):
                    drone.flip_rightsimplecontrol()
                    sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('t'):
                    drone.takeoffsimplecontrol()
                    sleep(2)
                if cv2.waitKey(1) & 0xFF == ord('u'):
                    drone.upsimplecontrol(10)
                    sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('n'):
                    drone.downsimplecontrol(10)
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
