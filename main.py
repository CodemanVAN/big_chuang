import cv2
import numpy as np
import dachuang_ui
from PyQt5 import QtWidgets
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
import datetime
import threading
import client
face_cascade=cv2.CascadeClassifier(r'C:\Users\18249\AppData\Local\Programs\Python\Python38-32\Lib\site-packages\cv2\data\haarcascade_frontalface_alt.xml')

cap=cv2.VideoCapture(0)

def connect_yuying():
    yuyin_client=client.connect_to_server()
    QtWidgets.QMessageBox.about(MainWindow,'连接结果',yuyin_client.state)
def face_track(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor = 1.1,
        minNeighbors = 5,
        minSize = (5,5),
    )
    l=len(faces)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame,'person',(w//2+x,y-h//5),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
    cv2.putText(frame,"face count",(20,60),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
    cv2.putText(frame,str(l),(230,60),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
    return frame

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
            if cv2.contourArea(c) < 8000:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Obj detected"
            moving_first_flag = False
    # 保存上一帧
    moving_last_gray = gray.copy().astype("float")
    moving_first_flag = True
    return frame

def water_track(pic):
    wtl=(100,43,43)
    wth=(120,255,255)
    hsv=cv2.cvtColor(pic,cv2.COLOR_BGR2HSV)
    wt=cv2.inRange(hsv,wtl,wth)
    (cnts,hi)=cv2.findContours(wt, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i in cnts:
        if cv2.contourArea(i)>2000:
            ((wx,wy),r)=cv2.minEnclosingCircle(i)
            cv2.circle(pic,(int(wx),int(wy)),int(r),(255, 0, 0),2)
    return pic
def updata_pic():
	global ui,cap
	while True:
		ret,pic=cap.read()
		if ret:
			pic=move_obj_track(pic)
			pic=face_track(pic)
			pic=water_track(pic)
			ui.frame.setPixmap(set_frame(pic))
		else:
			time.sleep(0.01)

def set_frame(pic):
	shrink = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
	QtImg = QImage(shrink.data,
								shrink.shape[1],
								shrink.shape[0],
								shrink.shape[1] * 3,
								QImage.Format_RGB888)
	return QPixmap.fromImage(QtImg)
if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = dachuang_ui.Ui_main_wd()
	ui.setupUi(MainWindow)
	ui.pushButton_3.clicked.connect(connect_yuying)
	t = threading.Thread(target=updata_pic)
	t.setDaemon(True)
	t.start()
	MainWindow.show()
	sys.exit(app.exec_()) 
