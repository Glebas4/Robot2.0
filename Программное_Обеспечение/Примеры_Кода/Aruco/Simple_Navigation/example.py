from cam_control import *
import time

DICT_NAME = 'DICT_4X4_250'
IP = '10.56.131.92'
PORT = 12345

robot = RobotCam(DICT_NAME, IP, PORT)

def mission():
    robot.move_to((200, 200), tolerance_px=30, wait=True)
    time.sleep(2)
    robot.set_ang(90, wait=True)
    time.sleep(2)

    robot.move_to((500, 200), tolerance_px=30, wait=True)
    time.sleep(2)
    robot.set_ang(135, wait=True)
    time.sleep(2)

robot.mission = mission
robot.start_mission()
