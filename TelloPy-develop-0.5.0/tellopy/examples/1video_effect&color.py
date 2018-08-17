import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import time
from collections import deque



redLower = np.array([170, 100, 100])
redUpper = np.array([179, 255, 255])
mybuffer = 64
pts = deque(maxlen=mybuffer)


def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)


def main():
    drone = tellopy.Tello()
    try:
        drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
        drone.connect()
        drone.wait_for_connection(30.0)
        # 设置连接等待的时间，若超时则抛出错误

        drone.takeoff()
        time.sleep(3)

        container = av.open(drone.get_video_stream())
        # skip first 300 frames
        frame_skip = 300
        while True:

            for frame in container.decode(video=0):

                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue

                start_time = time.time()
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, redLower, redUpper)
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

                if len(cnts) > 0:
                    c = max(cnts, key=cv2.contourArea)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    if radius > 10:
                        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                        cv2.circle(frame, center, 5, (0, 0, 255), -1)
                        pts.appendleft(center)
                else:
                    pts.clear()

                length = len(pts)
                for i in range(1, length):
                    if pts[i - 1] is None or pts[i] is None:
                        continue
                    thickness = int(np.sqrt(mybuffer / float(i + 1)) * 2.5)
                    cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
                cv2.imshow('Frame', frame)
                image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2GRAY)
                cv2.imshow('Original', image)
                # cv2.imshow('Canny', cv2.Canny(image, 100, 200))

                interrupt = cv2.waitKey(10)
                if interrupt & 0xFF == ord('q'):
                    drone.down(30)
                    time.sleep(3)
                    drone.land()
                    time.sleep(3)
                    print('successfully land!')
                    break
                frame_skip = int((time.time() - start_time)/frame.time_base)

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()

cap = cv2.VideoCapture(0)
if __name__ == '__main__':
    main()

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    # read有结果时，ret的返回值是True
    if ret:
        frame = cv2.flip(frame,0)

        #write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
