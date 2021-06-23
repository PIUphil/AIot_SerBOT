import BlynkLib
from pop import Pilot, LiDAR
from gtts import gTTS
import subprocess
import random
import time
import math


tts = gTTS("사탕주세요", lang='ko')
tts.save("candy.mp3")

tts = gTTS("저 li B 켜", lang='en')
tts.save("horn.mp3")


BLYNK_AUTH = 'y2Sg9eYorhQ9A7JDOBi0pLmIeb9hsrNU'
blynk = BlynkLib.Blynk(BLYNK_AUTH)  # server = '10.10.11.57, port=9443

x_pos = 0
y_pos = 0
speed = 0

bot = Pilot.SerBot()


@blynk.VIRTUAL_WRITE(0)
def back_button(n):
    global speed
    if int(n[0]) == 1:
        bot.forward(10)
        bot.steering = -1.0
        speed = 10
        print("왼쪽회전")
    else:
        bot.stop()
        print("정지")
        speed = 0

@blynk.VIRTUAL_WRITE(1)
def go_button(n):
    global speed
    if int(n[0]) == 1:
        bot.forward(10)
        bot.steering = 1.0
        speed = 10
        print("오른쪽회전")
    else:
        bot.stop()
        print("정지")
        speed = 0



@blynk.VIRTUAL_WRITE(2)
def candy(n):
    if int(n[0])==1:
        with subprocess.Popen(['play', 'candy.mp3']) as p:  
            p.wait()

@blynk.VIRTUAL_WRITE(3)
def horn(n):
    if int(n[0])==1:
        with subprocess.Popen(['play', 'horn.mp3']) as p:  
            p.wait()

# @blynk.VIRTUAL_READ(4)
# def led(n):
#     led1 = WidgetLED()
#     if speed <= 50:
#         led1 = on
#     else:
#         led1 = off

@blynk.VIRTUAL_READ(5)
def guage():
    #print (speed)
    blynk.virtual_write(5,int(speed))


@blynk.VIRTUAL_WRITE(6)
def joystick1(n):
    global x_pos
    x_pos = int(n[0])-512
    move()

@blynk.VIRTUAL_WRITE(7)
def joystick2(n):
    global y_pos
    y_pos = int(n[0])-512
    move()


def move():
    global speed

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
        print ("각도 = %.2f, 속력 = %.2f" %(degree, speed))

    if x_pos**2 < 500 and y_pos**2 < 500:
        speed = 0
        bot.stop()
        print("정지")
        

while True:
    try:
        blynk.run()

    except IOError:
        pass
