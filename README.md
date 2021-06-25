# AIoT SerBOT 주행

### 0. Blynk 화면
![image](https://user-images.githubusercontent.com/58851945/123362627-f0bd6500-d5ab-11eb-9bc6-08eb9c738814.png)
```
import BlynkLib
BLYNK_AUTH = 'y2Sg9eYorhQ9A7JDOBi0pLmIeb9hsrNU'
blynk = BlynkLib.Blynk(BLYNK_AUTH)
```
---
### 1. 수동조작
1) 조이스틱
```
if -100<x_pos<100 and y_pos>0:
    degree = 0
elif -100<x_pos<100 and y_pos<0:
    degree = 180
else:
    if x_pos > 0:
        degree = (90 - (math.atan((y_pos/x_pos)) * (180/math.pi)))%360
    else:
        degree = (90 - (math.atan((y_pos/x_pos)) * (180/math.pi)))%360 + 180
```

![image](https://user-images.githubusercontent.com/58851945/123344477-eccf1a00-d58e-11eb-9940-19cdf23a1687.png)

```
각도 = math.atan((y_pos/x_pos)) * (180/math.pi)
```
![image](https://user-images.githubusercontent.com/58851945/123344502-f6588200-d58e-11eb-9f58-1e9bcde517c9.png)

```
90-각도
```
![image](https://user-images.githubusercontent.com/58851945/123344534-02dcda80-d58f-11eb-9536-2b8dcee80945.png)

```
x>0 → 90-각도
x<0 → 90-각도+180
```

![image](https://user-images.githubusercontent.com/58851945/123344555-10926000-d58f-11eb-9153-b66896c85055.png)
  
```
분모인 x가 0에 가까우면 division 0 에러가 발생할 수 있으므로,
각도를 0(앞으로), 180(뒤로)으로 고정시킴
```
![image](https://user-images.githubusercontent.com/58851945/123344581-2142d600-d58f-11eb-8822-d3bace4038f7.png)

2) 속도 게이지 바 출력
```
@blynk.VIRTUAL_READ(8)              # 속력 표시
def guage():
    blynk.virtual_write(8,int(speed))
```
---
### 2. 버튼
1) 회전
```
@blynk.VIRTUAL_WRITE(0)             # 좌회전
def left_button(n):
    global speed
    if auto == 0:
        if int(n[0]) == 1:
            bot.turnLeft()
        else:
            bot.stop()
            speed = 0
```

2) 음성
```
from gtts import gTTS
tts = gTTS("감사합니다", lang='ko')
tts.save("thanks.mp3")
```
```
@blynk.VIRTUAL_WRITE(3)             # 음성(감사합니다)
def candy(n):
    if int(n[0])==1:
        with subprocess.Popen(['play', 'thanks.mp3']) as p:  
            p.wait()
```


3) 자율주행 - 수동조작 전환
- 조작버튼 클릭 시
```
@blynk.VIRTUAL_WRITE(5)             # 자율주행-수동조작 전환
def auto_switch(n):
    global auto

    if int(n[0])==1:
        auto = 1

    else:
        bot.stop()
        auto = 0
```
  
- Thread를 이용하여 자율주행이 항상 활성화되어있고, AUTO가 참일 때 주행
```
if auto==0:                 # 수동일 때, 무한루프에 가둬놓기
    bot.stop()
    while True:
        if auto==1:
            break
```

- 장애물 피하기
```
if collision:               # 충돌(장애물 발견)시 랜덤하게 회전
  dr = random.randint(1,20)
  bot.turnLeft() if dr%2==0 else bot.turnRight()
  time.sleep(dr*0.1)
  bot.stop()
```

4) 사진촬영
- 칼라사진으로 바꾸고, 뒤집혀 나오는 화면 회전
<img src = "https://user-images.githubusercontent.com/58851945/123364136-d6d15180-d5ae-11eb-8a7f-ce40e5e117da.png" width=450 height=450>

```
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
```

5) 종료
```
bot.stop()
lidar.stopMotor()
```

---

### 3. 기타

- 가속도 센서를 이용하여 충돌 혹은 급가속시 음성메세지 출력
- Thread를 이용하여 항상 활성화 시켜놓음

```
def impact():                       # 가속도센서 - 충격시 정지
    while True:
        value = bot.getAccel()

        if (value['x']**2 + value['y']**2)**(1/2) > 15500:
            bot.stop()
            with subprocess.Popen(['play', 'horn.mp3']) as p:  
                p.wait()
```
