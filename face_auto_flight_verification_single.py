import numpy
import math
import scipy.io as sio
import os
import sys
import traceback
import threading
import tellopy
import av
import cv2.cv2 as cv2
import face_recognition
import time
from time import sleep


## Supposed to be able to complete: auto flight, face verification, and adjustment. (One drone)



known_distance = 47.24  # for face, inches. or 120cm.
known_length = 6.6      # for face, inches. or 17cm.
focal_length = 1073.6

f_left = 0
f_bottom=0
f_right=0
f_top=0
w = 0
d = 0
xp = 0
yp = 0
end1 = 0
vid = True
flight = True

drone = tellopy.Tello()

def distance_to_camera(known, focal, pixel):
    return (known*focal)/pixel


def adjust(distance,h_distance,error):
    global vid
    m=1
    if error-distance<0:
        m=-1
    degree0 = math.atan(abs(error-distance)/h_distance)
    degree0 = math.degrees(degree0)
    degree = round(90+m*degree0)
    e = abs(distance-error)/math.sin(degree0)
    e = round(e,2)
    print(degree,e)
    drone.cw(degree)
    sleep(3)
    if e>1:
        drone.forward(round(100*(e-1)))
        sleep(4)
    print('*******************FINISH ADJUSTING******************')
    
        
def coordinate(t1,t2):
    time=[t1,t2]
    x=[]
    y=[]
    line_li=[]
    length = 4
    v = 0.8
    s = v*(t2-t1)
    for t in time:
        line = t//(5+5+4)+1
        line -= 4*(line//4)
        part = t%(5+5+4)
        line_li.append(line)
        if 0<part<10:
            length = round(v*part,2)
        point = [1,length,0,2,4,length,3,4-length,4,4,0,4-length]
        l = 3*line-3
        x.append(point[l+1])
        y.append(point[l+2])
    print('The coordinate of the drone when an unknown face is detected is:',(x[0],y[0])
           ,'when the drone stop is:',(x[1],y[1]))
    l1 = 3*line_li[0]-3
    person = [1,x[0]+d,w,2,4-w,y[0]+d,3,x[0]-d,4-w,4,w,y[0]-d]
    xp = person[l1+1]
    yp = person[l1+2]
    print('The person coordinate (xp,yp) is: ',(xp,yp))
    sleep(1)
    adjust(d,w,s)


def auto_flight():
    global flight,end1,vid
    print('**********************START AUTO FLIGHT THREAD*********************')
    n = 0
    sleep(17)
    drone.takeoff()
    sleep(6)
    drone.up(50)
    sleep(5)
    start = time.time()
    while n>=0:
        n+=1
        drone.forward(200)
        sleep(5)
        print('forward 2m ',n)
        if flight==False:
            end2=time.time()
            break
        if n%2==0:
            drone.cw(90)
            sleep(4)
            print('*********** counterclockwise: 90 degrees *************')
            if flight==False:
                end2=time.time()
                break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            sleep(1)
            drone.quit()
            vid=False
        
    sleep(1)
    detect_time = round(end1-start,1)
    auto_time = round(end2-start,1)
    if d!=0:
        coordinate(detect_time,auto_time)
    # sleep(2)
    # drone.land()
    # sleep(1)
    # drone.quit()
    # vid=False

    print('**********************EXIT AUTO FLIGHT THREAD*********************')


def face_detect():
    global vid,flight,end1,d,w
    print('**********************START FACE RECOGNITION THREAD*********************')
    # start = time.time()
    try:
        drone.connect()
        container = av.open(drone.get_video_stream())

        jenny_image = face_recognition.load_image_file('her.jpg')
        jenny_face_encoding = face_recognition.face_encodings(jenny_image)[0]
        known_face_encodings = [
            jenny_face_encoding
        ]
        known_face_names = [
            "Hermione"
        ]

        process_this_frame = True
        face_locations = []
        face_encodings = []
        i=0
        timef = 10

        for frame in container.decode(video=0):  
            i+=1
            image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
           # image = cv2.resize(image, (550, 400))
            small_frame = cv2.resize(numpy.array(frame.to_image()), (0, 0), fx=0.5, fy=0.5)

            if i>100 and i%timef==0:

                cv2.imshow('drone',image)
                if process_this_frame:
                    face_locations = face_recognition.face_locations(small_frame)
                    face_encodings = face_recognition.face_encodings(small_frame,face_locations)
                    face_names = []

                    for face_encoding in face_encodings:
                        matches = face_recognition.compare_faces(known_face_encodings,face_encoding,0.4)
                        name = 'Unknown'

                        if True in matches:
                            first_match_index = matches.index(True)
                            name = known_face_names[first_match_index]
                        face_names.append(name)

                process_this_frame = not process_this_frame

                for (top,right,bottom,left),name in zip(face_locations,face_names):
                    
                    f_top = top*2
                    f_right = right*2
                    f_bottom = bottom*2
                    f_left = left*2

                    cv2.rectangle(image, (f_left, f_top), (f_right, f_bottom), (0, 255, 255), 2)
                    cv2.rectangle(image,(f_left,f_bottom-35),(f_right,f_bottom),(0,255,255),cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(image,name,(f_left+6,f_bottom-6),font,1.0,(255,255,255),1)

                    if len(face_locations)!=0 and face_names[-1]=='Unknown':
                        d = distance_to_camera(known_length,focal_length,(bottom-top))  #inch
                        d = round(2.54*d*0.01,2)  #m
                        w = abs((left+right)/2-480)*6.6/150  #inch
                        w = round(2.54*w*0.01,2)  #m

                        print('FACE DETECTED')
                        cv2.putText(image, "distance: {} m".format(d),(image.shape[1]-900,image.shape[0]-40),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),3)
                        
                        if flight==True:
                            flight = False
                            end1 = time.time()
                            print('Adjust**************************************')                      

                cv2.imshow('drone',image)
            
            # if len(face_locations) != 0:
            #     print('FACE DETECTED')
            #     # face = True
            #     drone.forcedstop()
            #     print('FORCE STOP**************************************')
            #     flight = False

            if cv2.waitKey(1)&0xFF == ord('q'):
                drone.land()
                print("******NOW exiting the video trans after interuption quit*****")
                flight = False
                cv2.destroyWindow(image)
                cv2.destroyAllWindows()
            if vid == False:
                print("******NOW exiting the video trans as vid is False*****")
                cv2.destroyWindow(image)
                cv2.destroyAllWindows()
                
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()
    print('****************EXITING FACE RECOGNITION THREAD**************')
    # end = time.time()
    # print("The face_recognition module has been running for:",round(end-start,3),' seconds')



threading.Thread(target=face_detect).start()
threading.Thread(target=auto_flight).start()

