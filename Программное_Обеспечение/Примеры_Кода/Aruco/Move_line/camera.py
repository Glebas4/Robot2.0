import cv2 as cv
import numpy as np
import socket
import math
import struct as st


DICT_NAME = "DICT_4X4_250"
KOEF = 10

GREEN = (0, 255, 0)
RED = (0, 0, 255)


IP = '10.56.131.92'
PORT = 12345


detector = cv.aruco.ArucoDetector(
    cv.aruco.getPredefinedDictionary(getattr(cv.aruco, DICT_NAME)), 
    cv.aruco.DetectorParameters()
    )



def calc_cords(pt1:tuple, pt2:tuple, dx:int, dy:int) -> tuple:
    pnt1 = (pt1[0] + dx * KOEF, pt1[1] + dy * KOEF)
    pnt2 = (pt2[0] - dx * KOEF, pt2[1] - dy * KOEF)

    return (pnt1, pnt2)



def get_glob_ang(dx:int, dy:int) -> int:
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




def get_pnt_mark_ang(pnt: tuple, pt1: list, pt2: list) -> tuple:  #(ang_degrees, direction)
    direct = 0
    
    a_sq = (pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2
    b_sq = (pnt[0] - pt2[0])**2 + (pnt[1] - pt2[1])**2
    c_sq = (pnt[0] - pt1[0])**2 + (pnt[1] - pt1[1])**2

    cos_a = (c_sq - a_sq - b_sq) / (-2*math.sqrt(a_sq)*math.sqrt(b_sq))

    try:
        ang_deg = 180 - int(math.degrees(math.acos(cos_a)))
    except:
        return (0, '')

    mark_vec = (pt2[0]-pt1[0], pt2[1]-pt1[1]) 
    pnt_vec = (pnt[0]-pt1[0], pnt[1]-pt1[1])

    d = pnt_vec[0]*mark_vec[1] - pnt_vec[1]*mark_vec[0]

    if d > 0:
        direct = 1

    return (ang_deg, direct) # CW = 0, CCW = 1



def signals(ang:int, direction: int) -> tuple: #(l_mot, r_mot) 180, -255   - значит BWD
    K = 1.5
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



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))

def main():
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)

    point = (0, 240)
    #first = True

    while True:
        _, img = cap.read()
        #if first:
        #    print(img.shape)
        #    first = False

        corners, ids, _ = detector.detectMarkers(img)
        l = r = 0

        if ids is not None:
            pt1 = [int(val) for val in corners[0][0][0].tolist()]
            pt2 = [int(val) for val in corners[0][0][3].tolist()]

            if math.sqrt((pt1[0] - point[0])**2 + (pt1[1] - point[1])**2) > 30:
                ang, direction = get_pnt_mark_ang(point, pt1, pt2)
                l, r = signals(ang, direction)

            img = cv.arrowedLine(img, pt1, point, (0, 255, 0), 2)
            img = cv.arrowedLine(img, pt1, pt2, (255, 0, 0), 2)

            #pt1, pt2 = calc_cords(pt1, pt2, pt1[0]-pt2[0], pt1[1]-pt2[1])

            #img = cv.line(img, pt1, (0,0), (0, 0, 255), 2)


        sock.sendall(st.pack('>hh', l, r))

        cv.imshow('result', img) 
     
        ch = cv.waitKey(5)
        if ch == 27:
            break



if __name__ == '__main__':
    main()
