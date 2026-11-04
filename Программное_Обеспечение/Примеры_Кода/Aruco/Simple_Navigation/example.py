from cam_control import *
import time
import os

DICT_NAME = "DICT_4X4_250"
IP = '10.56.131.92'
PORT = 12345

robot = RobotCam(DICT_NAME, IP, PORT)

def mission():
    robot.move_to((200, 240))
    robot.event.get()
    
    time.sleep(1)
  
    robot.move_to((500, 300))
    robot.event.get()
    robot.set_ang(90)
    robot.event.get()

robot.mission = mission
robot.start_mission()
