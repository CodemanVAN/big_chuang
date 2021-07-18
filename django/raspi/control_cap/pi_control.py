
#import RPi.GPIO as GP
import os
import time


def start():
    os.system("sudo systemctl start motion")
    time.sleep(1)
    os.system('sudo motion')
def stop():
    os.system("sudo systemctl stop motion")
def del_video():
    os.system("rm -f ./record_video/*")
def down_rope(voltage):
    pass
    '''
    GP.setmode(GP.BOARD)
    GP.setup(11,GP.OUT)
    GP.output(11,voltage)
    '''