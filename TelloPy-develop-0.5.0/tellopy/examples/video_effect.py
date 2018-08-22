import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import time
from time import sleep


def main():
    drone = tellopy.Tello()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)
        # drone.takeoff()
        # sleep(3)
        # drone.land()
        # sleep(3)
        container = av.open(drone.get_video_stream())
        # skip first 300 frames
        frame_skip = 300
        while True:
            for frame in container.decode(video=0):
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                start_time = time.time()
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                cv2.imshow('Original', image)
               # cv2.imshow('Canny', cv2.Canny(image, 100, 200))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyWindow(image)
                    drone.land()
                    sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('l'):
                    drone.land()
                    sleep(2)
                if cv2.waitKey(1) & 0xFF == ord('w'):
                    drone.forward(10)
                    sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    drone.backward(10)
                    sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('a'):
                    drone.left(10)
                    sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('d'):
                    drone.right(10)
                    sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('z'):
                    drone.clockwise(10)
                    sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('c'):
                    drone.flip_right()
                    sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('t'):
                    drone.takeoff()
                    sleep(2)
                if cv2.waitKey(1) & 0xFF == ord('u'):
                    drone.up(10)
                    sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('n'):
                    drone.down(10)
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
