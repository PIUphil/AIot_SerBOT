import BlynkLib
from pop import Pilot, LiDAR
import random
import time

BLYNK_AUTH = 'y2Sg9eYorhQ9A7JDOBi0pLmIeb9hsrNU'
blynk = BlynkLib.Blynk(BLYNK_AUTH)  # server = '10.10.11.57, port=9443

SPEED = 30

bot = Pilot.SerBot()

@blynk.VIRTUAL_WRITE(0)
def go_button(n):
    for i in n:
        if i == '0'or i == '1':
            bot.forward(10)
            bot.steering = 1.0
            print("오른쪽회전")

@blynk.VIRTUAL_WRITE(1)
def back_button(n):
    for i in n:
        if i == '0'or i == '1':
            bot.forward(10)
            bot.steering = -1.0
            print("왼쪽회전")


@blynk.VIRTUAL_WRITE(2)
def slider(n):
    global SPEED

    #print(int(n[0]))
    SPEED = int(n[0]) *8 /60

# @blynk.VIRTUAL_WRITE(2)
# def left_button(n):
#     for i in n:
#         if i == '0'or i == '1':
#             bot.move(270, 40)
#             print("왼쪽")


@blynk.VIRTUAL_WRITE(6)
def joystick1(n):
    #print(int(n[0]))
    if (int(n[0]) < 300):
        bot.move(270, int(n[0])*(-0.2)+60)
        print("왼쪽")
    elif (int(n[0]) > 700):
        bot.move(90, (int(n[0])-700) * 0.18)
        print("오른쪽")
    elif (508<int(n[0])<515):
        bot.stop()
        print("정지")

@blynk.VIRTUAL_WRITE(7)
def joystick2(n):
    if (int(n[0])<300):
        bot.move(180, int(n[0])*(-0.2)+60)
        print("뒤로")
    elif (int(n[0])>700):
        bot.move(0, (int(n[0])-700) * 0.18)
        print("앞으로")
    elif (508<int(n[0])<515):
        bot.stop()
        print("정지")



while True:
    try:
        blynk.run()
    except IOError:
        pass
