import time
from socket import *

high = 0


#   By Q.Z.Lin  Do not use for commercial purposes!
#   If you have any advice, please send an email to 13439402428@163.com

class tello:
    def take_off(self):
        global high
        self.send_data("takeoff")
        high = 1
        time.sleep(5)

    def land(self):
        global high
        self.send_data("land")
        high = 0
        time.sleep(8)

    def up(self, distance):
        global high
        self.send_data("up" + " " + str(distance))
        high += distance / 100
        time.sleep(int(distance * 0.05))

    def down(self, distance):
        global high
        self.send_data("down" + " " + str(distance))
        high -= distance / 100
        time.sleep(int(distance * 0.05))

    def left(self, distance):
        self.send_data("left" + " " + str(distance))
        time.sleep(int(distance * 0.05))

    def right(self, distance):
        self.send_data("right" + " " + str(distance))
        time.sleep(int(distance * 0.05))

    def forward(self, distance):
        self.send_data("forward" + " " + str(distance))
        time.sleep(int(distance * 0.05))

    def back(self, distance):
        self.send_data("back" + " " + str(distance))
        time.sleep(int(distance * 0.05))

    def cw(self, angle):
        self.send_data("cw" + " " + str(angle))
        time.sleep(int(angle * 0.02))

    def ccw(self, angle):
        self.send_data("ccw" + " " + str(angle))
        time.sleep(int(angle * 0.02))

    def flip(self, direction):
        self.send_data("flip" + " " + direction)
        time.sleep(3)

    def set_speed(self, speed):
        self.send_data("speed" + " " + str(speed))

    def delay(self, s):
        print("Delay: ", s, " s")
        time.sleep(s)

    def send_data(self, data):
        try:
            data = data.encode(encoding="utf-8")
            self.udpClient.sendto(data, self.addr)
            print("Send Command:" + " " + data.decode(encoding="utf-8"))
        except:
            print("Error")

    def end(self):
        self.udpClient.close()
        print("Program Stop")

    def __init__(self):
        self.host = "192.168.10.1"  # Host ip address
        self.port = 8889  # port
        self.bufsize = 1024
        #
        self.addr = (self.host, self.port)
        self.udpClient = socket(AF_INET, SOCK_DGRAM)
        print("=" * 20, "tello_withPython By Q.Z.Lin", "=" * 20)
        print("If you have any advice, please send an email to 13439402428@163.com\n")

#   By Q.Z.Lin  Do not use for commercial purposes!
#   By Q.Z.Lin  Do not use for commercial purposes!
#   By Q.Z.Lin  Do not use for commercial purposes!
#   By Q.Z.Lin  Do not use for commercial purposes!
#   By Q.Z.Lin  Do not use for commercial purposes!
#   By Q.Z.Lin  Do not use for commercial purposes!
#   By Q.Z.Lin  Do not use for commercial purposes!
#   By Q.Z.Lin  Do not use for commercial purposes!