import multiprocessing as mp
#import threading as th
from popAssist import *
import BlynkLib
from pop import Pilot, LiDAR
from pop import Camera, Util
from gtts import gTTS
import subprocess
import random
import time
import math
import cv2


tts = gTTS("사탕주세요", lang='ko')
tts.save("candy.mp3")

tts = gTTS("감사합니다", lang='ko')
tts.save("thanks.mp3")

tts = gTTS("빵빵 조심하세요", lang='ko')
tts.save("horn.mp3")


BLYNK_AUTH = 'y2Sg9eYorhQ9A7JDOBi0pLmIeb9hsrNU'
blynk = BlynkLib.Blynk(BLYNK_AUTH)  # server = '10.10.11.57, port=9443

x_pos = 0
y_pos = 0
speed = 0
auto = False

bot = Pilot.SerBot()
lidar = LiDAR.Rplidar()
lidar.connect()


@blynk.VIRTUAL_WRITE(0)             # 좌회전
def left_button(n):
    global speed
    if auto == False:
        if int(n[0]) == 1:
            bot.forward(10)
            bot.steering = -1.0
            speed = 10
            #print("왼쪽회전")
        else:
            bot.stop()
            #print("정지")
            speed = 0

@blynk.VIRTUAL_WRITE(1)             # 우회전
def right_button(n):
    global speed
    if auto == False:
        if int(n[0]) == 1:
            bot.forward(10)
            bot.steering = 1.0
            speed = 10
            #print("오른쪽회전")
        else:
            bot.stop()
            #print("정지")
            speed = 0


@blynk.VIRTUAL_WRITE(2)             # 음성(사탕주세요)
def candy(n):
    if int(n[0])==1:
        with subprocess.Popen(['play', 'candy.mp3']) as p:  
            p.wait()

@blynk.VIRTUAL_WRITE(3)             # 음성(감사합니다)
def candy(n):
    if int(n[0])==1:
        with subprocess.Popen(['play', 'thanks.mp3']) as p:  
            p.wait()

# @blynk.VIRTUAL_WRITE(10)            # 음성(빵빵)    - 
# def horn(n):
#     if int(n[0])==1:
#         with subprocess.Popen(['play', 'horn.mp3']) as p:  
#             p.wait()


@blynk.VIRTUAL_WRITE(4)                 # 사진촬영
def camv(n):
    if int(n[0])==1:
        with subprocess.Popen(['play', 'shutter.mp3']) as p:  
            p.wait()

        cam = Camera(width=1080, height=720)
        cv2.imwrite("picture.png", cam.value)
        imgColor = cv2.imread("picture.png", cv2.IMREAD_COLOR)
        imgColor = cv2.flip(imgColor,-1)
        cv2.imwrite("picture.png", imgColor)
        cv2.imshow("imgColor", imgColor)
        
    return

@blynk.VIRTUAL_WRITE(5)             # 자율주행-수동조작 전환
def auto_switch(n):
    global auto

    if int(n[0])==1:
        auto = True
        auto_move()
        time.sleep(5)
    else:
        bot.stop()
        lidar.stopMotor()
        auto = False
    #print(auto)


@blynk.VIRTUAL_WRITE(6)             # 조이스틱(x축)
def joystick1(n):
    global x_pos
    x_pos = int(n[0])-512
    move()

@blynk.VIRTUAL_WRITE(7)             # 조이스틱(y축)
def joystick2(n):
    global y_pos
    y_pos = int(n[0])-512
    move()

@blynk.VIRTUAL_READ(8)              # 속력 표시
def guage():
    blynk.virtual_write(8,int(speed))


# @blynk.VIRTUAL_READ(10)
# def cam():
    #Blynk.setProperty(V1, "url", "http://my_new_video_url");
    #blynk.setProperty(10, "https://youtu.be/PCz17d87W1E", "https://youtu.be/PCz17d87W1E")


def move():
    global speed
    if auto == False:
        if x_pos**2 >10000 or y_pos**2 >10000:
            if -100<x_pos<100 and y_pos>0:
                degree = 0
            elif -100<x_pos<100 and y_pos<0:
                degree = 180
            else:
                if x_pos > 0:
                    degree = (90 - (math.atan((y_pos/x_pos)) * (180/math.pi)))%360
                else:
                    degree = (90 - (math.atan((y_pos/x_pos)) * (180/math.pi)))%360 + 180

            speed = int(((x_pos**2 + y_pos**2)**(1/2))) /10 *1.1
            bot.move(degree, speed)
            #print ("각도 = %.2f, 속력 = %.2f" %(degree, speed))

        if x_pos**2 < 500 and y_pos**2 < 500:
            speed = 0
            bot.stop()
            #print("정지")
        
        # value = bot.getGyro()    # 회전각 측정
        # print(value)


def auto_move():
    #auto = False
    lidar.startMotor()
    direction = 0

    bot.move(direction, 40)

    collision = True


    while collision:
        collision = False
        vectors = lidar.getVectors()
        
        

        for v in vectors:
            degree = v[0]    # 각도
            distance = v[1]  # 거리

            left_hand = (direction-35)%360   # 360을 넘어서지 않도록
            right_hand = (direction+35)%360

            disc = None
            if left_hand > right_hand:      # 진행방향쪽의 거리만 사용하기위함
                disc = degree >= left_hand or degree <= right_hand
            else:
                disc = degree >= left_hand and degree <= right_hand

            if disc:
                if distance <= 350:
                    collision = True
                    bot.stop()
                    break
        
        if collision:
            direction += 40
            direction %= 360
    
    
        


def impact():                       # 가속도센서 - 충격시 정지
    while True:
        value = bot.getAccel()
        #print ((value['x']**2 + value['y']**2)**(1/2))

        if (value['x']**2 + value['y']**2)**(1/2) > 12000:
            bot.stop()
            lidar.stopMotor()
            with subprocess.Popen(['play', 'horn.mp3']) as p:  
                p.wait()

# def xy():                           # 자이로센서
#     while True:
#         value = bot.getGyro()
#         print(value)


# def avi():
#     Util.enable_imshow()

#     cam = Util.gstrmer(width=640, height=480)
#     camera = cv2.VideoCapture(cam, cv2.CAP_GSTREAMER)
#     if not camera.isOpened():
#         print("Not found camera")

#     fourcc = cv2.VideoWriter_fourcc(*"PIM1")
#     out = cv2.VideoWriter("soda.avi", fourcc, 30, (640,480))

#     #for _ in range(120):
#     while True:
#         ret, frame = camera.read()
#         frame = cv2.flip(frame,-1)
#         framGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         out.write(frame)
#         cv2.imshow("soda", framGray)



# def userAction(text):                              # gassist 
#     action = False 
#     print(text)

#     if text.find("앞으로") != -1:
#         bot.forward() 
#         action = True 
#     elif text.find("뒤로") != -1:
#         bot.backward() 
#         action = True 
#     elif text.find("정지") != -1:
#         bot.stop() 
#         action = True    

#     return action

# stream = create_conversation_stream()
# ga = GAssistant(stream, local_device_handler=userAction)

# def onStart():
#     print(">>> Start recording...")

# def gassist():                                     # 구글 어시스턴트
#     while True:
#         ga.assist(onStart)


# def main():
#     try:
#         while True:
#             blynk.run()
#     except:
#         pass

def blynk_():
    while True:
        blynk.run()

if __name__ == '__main__':
#     main()
    p1 = mp.Process(target=blynk_)
    # # p1 = mp.Process(target=main)
    p2 = mp.Process(target=impact)
    #p1 = th.Thread(target=blynk_)
    #p2 = th.Thread(target=impact)
    #p3 = mp.Process(target=avi)
    #p3 = mp.Process(target=gassist)
    #p3 = mp.Process(target=xy)
    

    p1.start()
    p2.start()
    #p3.start()

    p1.join()
    p2.join()
    #p3.join()
