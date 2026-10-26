import cv2 as cv
import numpy as np
import socket
import math


DICT_NAME = "DICT_4X4_250"
KOEF = 10

GREEN = (0, 255, 0)
RED = (0, 0, 255)


IP = '10.217.123.92'
PORT = 12345


detector = cv.aruco.ArucoDetector(
    cv.aruco.getPredefinedDictionary(getattr(cv.aruco, DICT_NAME)), 
    cv.aruco.DetectorParameters()
    )



def calc_cords(pt1:tuple, pt2:tuple, dx:int, dy:int) -> tuple:
    pnt1 = (pt1[0] + dx * KOEF, pt1[1] + dy * KOEF)
    pnt2 = (pt2[0] - dx * KOEF, pt2[1] - dy * KOEF)

    return (pnt1, pnt2)


def calc_ang(dx:int, dy:int) -> int:
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

    




sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))

def main():
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)

    targ_ang = int(input('Какой угол удерживать ?'))

    while True:
        _, img = cap.read()
        msg = 2
        color = GREEN

        corners, ids, _ = detector.detectMarkers(img)
        

        if ids is not None:
            pt1 = [int(val) for val in corners[0][0][0].tolist()]
            pt2 = [int(val) for val in corners[0][0][3].tolist()]

            dx = pt1[0] - pt2[0]
            dy = pt1[1] - pt2[1]

            curr_ang = calc_ang(dx, dy)

            if abs(curr_ang - targ_ang) > 5:
                color = RED
                if curr_ang < targ_ang or curr_ang > 180 + targ_ang:
                    msg = 0

                else:
                    msg = 1

                 

            #img = cv.line(img, (pt1[0], pt1[1]), (pt2[0], pt1[1]), RED, 2)
            #img = cv.line(img, (pt1[0], pt2[1]), (pt2[0], pt2[1]), RED, 2)
            #img = cv.line(img, (pt2[0], pt1[1]), (pt2[0], pt2[1]), (255, 255, 255), 2)
            #img = cv.line(img, (pt1[0], pt1[1]), (pt1[0], pt2[1]), (255, 255, 255), 2)
            #img = cv.line(img, (0, pt2[1]), (720, pt2[1]), (255, 150, 255), 2)

            img = cv.line(img, (0, pt2[1]), (720, pt2[1]), (0, 127, 255), 2)
            pt1, pt2 = calc_cords(pt1, pt2, dx, dy)
            img = cv.line(img, pt1, pt2, color, 2)
            img = cv.putText(img, str(curr_ang), (500, 70), cv.FONT_HERSHEY_SIMPLEX, 2, color, 2, cv.LINE_AA)

            #img = cv.line(img, (pt1[0], pt1[1]), (pt2[0], pt1[1]), color, 2)


 
        sock.send(str(msg).encode('utf-8'))

        cv.imshow('result', img) 
     
    
        ch = cv.waitKey(5)
        if ch == 27:
            break



if __name__ == '__main__':
    main()

