import cv2
import numpy as np
import os
import time
import datetime
import threading

url=r'http://192.168.105.177:8081'
face_cascade=cv2.CascadeClassifier(r"C:\Users\ZYL\miniconda3\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml")
cap=cv2.VideoCapture(0)
orgFrame=None
ret=False
#################################################
# 智能监控
# 第一帧，用于比较
moving_last_gray = None
moving_first_flag = False  # 第一帧标志位
def move_obj_track(frame):
    global moving_first_flag
    global moving_last_gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = "Nobody_detected"
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if moving_first_flag and moving_last_gray is not None:
        # 计算当前帧和第一帧的不同
        cv2.accumulateWeighted(gray, moving_last_gray, 0.5)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(moving_last_gray))
        # cv2.imshow('frameDelta', frameDelta)
        thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
        # 扩展阀值图像填充孔洞，然后找到阀值图像上的轮廓
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts= cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        # 遍历轮廓
        for c in cnts:
            if cv2.contourArea(c) < 5000:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Obj detected"
            moving_first_flag = False
    # 保存上一帧
    moving_last_gray = gray.copy().astype("float")
    moving_first_flag = True
    # 在当前帧上写文字以及时间戳
def face_track(frame):

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor = 1.1,
        minNeighbors = 5,
        minSize = (5,5),
    )
    l=len(faces)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.putText(frame,'person',(w//2+x,y-h//5),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
    cv2.putText(frame,"face count",(20,60),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
    cv2.putText(frame,str(l),(230,60),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
    
def get_image():
    global orgFrame
    global cap
    global ret
    while True:
        if cap.isOpened():
            ret, orgFrame = cap.read()
        else:
            time.sleep(0.01)

def get_image2():
    global orgFrame
    global cap
    global ret
    while True:
        if cap.isOpened():
            ret, orgFrame = cap.read()
        else:
            time.sleep(0.01)

t = threading.Thread(target=get_image)
t.setDaemon(True)
t.start()

while True:

    if ret and orgFrame is not None:
        ret=False
        t1 = time.time()
        move_obj_track(orgFrame)

        fps = 1.0/(time.time()-t1)
        cv2.putText(orgFrame, "fps:" + str(int(fps)),
                (10, orgFrame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)#(0, 0, 255)BGR
        cv2.imshow("orgframe", orgFrame)
        cv2.waitKey(1)
    else:
        time.sleep(0.01)