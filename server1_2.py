#server1.py
from time import sleep
import socket
import time
import datetime as dt
import cv2
import pickle
import struct
import cv2
from gpiozero import MotionSensor
from flask import Flask

cam = cv2.VideoCapture(0)
pir = MotionSensor(4)
ret, image = cam.read()

host = '131.128.51.187'
port = 8600 #change to other port if this one is occupied
s = socket.socket()
s.bind((host, port))
s.listen(10)
#cam = cv2.VideoCapture(1)
i = 0
#app = Flask(__name__)
#@app.route('/')
#def index():
#    return 'Hello world'
#if __name__ == '__main__':
#    app.run(debug=True, port=80, host='131.128.51.187')
    
def takepic():
    global i
    i = i + 1
    cv2.imshow('Imagetest',image)
    cam = cv2.VideoCapture(1)
    cv2.imwrite('/home/pi/Desktop/image%s.jpg' % i, image)
    cam.release()
    cv2.destroyAllWindows()
while True:
    pir.wait_for_motion()
    print("You moved")
    takepic()
    pir.wait_for_no_motion()
while True:
    try:
        conn, addr = s.accept()
        if conn:
            print("Connection established, from: %s"%str(addr))
            while True:
                file = open('/home/pi/testimage.jpg', 'rb')
                image_data = file.read(2048)
                while image_data:
                    s.send(image_data)
                    image_data = file.read(2048)
                file.close()
                s.close()
                data = conn.recv(20)
                print("recvdata:{0}".format(data.decode('ascii')))
                time.sleep(1)
        else:
                time.sleep(1)
    except:
        s.close()
    cam.release()