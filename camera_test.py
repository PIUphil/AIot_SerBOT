import cv2
from pop import Util

Util.enable_imshow()

cam = Util.gstrmer(width=640, height=480)
camera = cv2.VideoCapture(cam, cv2.CAP_GSTREAMER)
if not camera.isOpened():
    print("Not found camera")

fourcc = cv2.VideoWriter_fourcc(*"PIM1")
out = cv2.VideoWriter("soda.avi", fourcc, 30, (640,480))

#for _ in range(120):
while True:
    ret, frame = camera.read()
    frame = cv2.flip(frame,-1)
    framGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    out.write(frame)
    
    cv2.imshow("soda", framGray)

#camera.release()

#cv2.destroyAllWindows()
