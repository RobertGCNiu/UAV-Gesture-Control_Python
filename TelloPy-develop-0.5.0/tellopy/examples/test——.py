import sys
import traceback
import tellopy
#import av
import opencv as cv2  # for avoidance of pylint error
import numpy
import time

def handler(event, sender, data, **args):
    drone2 = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)

def test():
    drone2 = tellopy.Tello()
    try:
        drone2.subscribe(drone.EVENT_FLIGHT_DATA, handler)
        drone2.connect()
        drone2.wait_for_connection(60.0)
        drone2.takeoff()
        sleep(3)
        drone2.down(30)
        sleep(3)
        drone2.flip_backleft()
        sleep(3)
        drone2.backward(30)
        sleep(3)
        drone2.land()
# original data is 5

    except Exception as ex:
        print(ex)
    finally:
        drone2.quit()


def main():
    drone = tellopy.Tello()
    try:
        drone.connect()
        drone.wait_for_connection(60.0)

        container = av.open(drone.get_video_stream())
        # skip first 300 frames
        frame_skip = 300
        while True:
            for frame in container.decode(video=0):
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                start_time = time.time()
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2GRAY)
                cv2.imshow('Original', image)
                cv2.imshow('Canny', cv2.Canny(image, 100, 200))
                cv2.waitKey(1)
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
    if ret==True:
        frame = cv2.flip(frame,0)

        # write the flipped frame
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