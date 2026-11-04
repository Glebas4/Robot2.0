import cv2 as cv
import socket
import math
import struct as st
import threading
import queue



class RobotCam():
    def __init__(self, aruco_dict, rob_ip, rob_port) -> None:
        self.aruco_dict = aruco_dict
        self.rob_ip = rob_ip
        self.rob_port = rob_port


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.rob_ip, self.rob_port)) 
        print(f'connected to {rob_ip}, {rob_port}')


        self.detector = cv.aruco.ArucoDetector(
        cv.aruco.getPredefinedDictionary(getattr(cv.aruco, self.aruco_dict)), 
        cv.aruco.DetectorParameters()
        )

        self.cam = cv.VideoCapture(0, cv.CAP_DSHOW)
        self.window_name = 'result'

        self._move_to_flag = False
        self._move_to_cords = [0, 0]
        self._move_to_tolerance = 0

        self._set_ang_flag = False
        self._set_ang_val = 0

        self.DONE = 1

        self.event = queue.Queue()

        self.mission = None



    def start_mission(self) -> None:
        if self.mission is not None:
            self.thread = threading.Thread(target=self.mission, daemon=True)
            self.thread.start()
        self.proc()



    @staticmethod
    def get_dist(pt1: tuple, pt2: tuple) -> int: #расстояние в пикселях
        return math.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)



    @staticmethod
    def get_glob_ang(pt1: tuple, pt2: tuple) -> int:
        dx = pt2[0] - pt1[0]
        dy = pt2[1] - pt1[1]

        if dx and dy:
            ang = int(math.degrees(math.atan(abs(dy)/abs(dx))))
            if dx > 0:
                if dy > 0:
                    return 360 - ang

                return ang

            else:
                if dy > 0:
                    return ang + 180

                return 180 - ang

        elif not dx:
            if dy > 0:
                return 270

            return 90

        if dx > 0:
            return 0

        return 180



    @staticmethod
    def get_pnt_mark_ang(pnt: tuple, pt1: list, pt2: list) -> tuple:  #(ang_degrees, direction)
        direct = 0
        
        a_sq = (pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2
        b_sq = (pnt[0] - pt2[0])**2 + (pnt[1] - pt2[1])**2
        c_sq = (pnt[0] - pt1[0])**2 + (pnt[1] - pt1[1])**2

        cos_a = (c_sq - a_sq - b_sq) / (-2*math.sqrt(a_sq)*math.sqrt(b_sq))

        try:
            ang_deg = 180 - int(math.degrees(math.acos(cos_a)))
        except:
            return (0, 0)

        mark_vec = (pt2[0]-pt1[0], pt2[1]-pt1[1]) 
        pnt_vec = (pnt[0]-pt1[0], pnt[1]-pt1[1])

        d = pnt_vec[0]*mark_vec[1] - pnt_vec[1]*mark_vec[0]

        if d > 0:
            direct = 1

        return (ang_deg, direct) # CW = 0, CCW = 1



    def get_mark_cords(self, img) -> tuple: #pt1, pt2
        corners, ids, rejected = self.detector.detectMarkers(img)
        pt1 = None
        pt2 = None

        if ids is not None:
            pt1 = [int(val) for val in corners[0][0][0].tolist()]
            pt2 = [int(val) for val in corners[0][0][3].tolist()]

        return (pt1, pt2)



    @staticmethod
    def signals_line(ang: int, direction: int) -> tuple: #(l_mot, r_mot) 180, -255   - значит BWD
        K = 1.4
        if ang > 90:
            if direction == 0: # CW
                return (130, -130)

            return (-130, 130)


        l = r = 150
        dif = int(ang * K)

        if direction == 0:
            r -= dif

        else:
            l -= dif

        return (l, r)



    def send_motors(self, l: int, r: int) -> None:
        data = st.pack('>hh', l, r)
        self.sock.sendall(data)



    def move_to(self, cords: tuple, tolerance_px: int = 30) -> None:
        self._move_to_flag = True
        self._move_to_cords = cords
        self._move_to_tolerance = tolerance_px



    def set_ang(self, ang: int) -> None:
        self._set_ang_flag = True
        self._set_ang_val = ang



    def proc(self) -> bool:    
        while True:
            img_flag, img = self.cam.read()
    
            if not img_flag:
                raise Exception('А Где картинка алё')


            elif self._move_to_flag:
                pt1, pt2 = self.get_mark_cords(img)

                if pt1 == None:
                   self.send_motors(0, 0) 
                   continue
                   
                    
                elif self.get_dist(pt1, self._move_to_cords) < self._move_to_tolerance:
                    self._move_to_flag = False
                    self.send_motors(0, 0)
                    self.event.put(self.DONE)
                        
                else:
                    ang, direction = self.get_pnt_mark_ang(self._move_to_cords, pt1, pt2)
                    l, r = self.signals_line(ang, direction)
                    self.send_motors(l, r)
                    img = cv.arrowedLine(img, pt1, self._move_to_cords, (0, 255, 0), 2)
                    img = cv.arrowedLine(img, pt1, pt2, (255, 0, 0), 2)


            elif self._set_ang_flag:
                #stab_cnt = 0

                pt1, pt2 = self.get_mark_cords(img)
                
                if pt1 is None: 
                    self.send_motors(0, 0) 
                    continue

                curr_ang = self.get_glob_ang(pt1, pt2)

                if abs(curr_ang - self._set_ang_val) > 5:
                    if curr_ang < self._set_ang_val or curr_ang > 180 + self._set_ang_val:
                        self.send_motors(-95, 95)

                    else:
                        self.send_motors(95, -95)

                else:
                    #stab_cnt += 1
                    self.send_motors(0, 0)
                    self.event.put(self.DONE)

#                if stab_cnt == 20:
#                    self.send_motors(0, 0)
#                    self._set_ang_flag = False
#                    self.event.put(self.DONE)


            cv.imshow('result', img)
            ch = cv.waitKey(5)
            if ch == 27:
                break
