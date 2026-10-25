import cv2 as cv
import numpy as np
import socket
import math


DICT_NAME = "DICT_4X4_250"
KOEF = 10


detector = cv.aruco.ArucoDetector(
    cv.aruco.getPredefinedDictionary(getattr(cv.aruco, DICT_NAME)), 
    cv.aruco.DetectorParameters()
    )



def calc_cords(pt1:tuple, pt2:tuple, dx:int, dy:int) -> tuple:
    pnt1 = (pt1[0] + dx * KOEF, pt1[1] + dy * KOEF)
    pnt2 = (pt2[0] - dx * KOEF, pt2[1] - dy * KOEF)

    return (pnt1, pnt2)



def main():
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)

    ip = input('ip: ')
    port = int(input('port: '))

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((ip, port))

    while True:
        _, img = cap.read()
        msg = 2

        corners, ids, _ = detector.detectMarkers(img)
        

        if ids is not None:
            pt1 = [int(val) for val in corners[0][0][0].tolist()]
            pt2 = [int(val) for val in corners[0][0][3].tolist()]

            dx = pt1[0] - pt2[0]
            dy = pt1[1] - pt2[1]

            if dy:
                ang = int(abs(math.degrees(math.atan(dx/dy))))
                #print(ang)

                if dx > 0:
                    if dy < 0:
                        ang = 360 - ang

                    else:
                        ang = 180 + ang

                else:
                    if dy < 0:
                        pass

                    else:      
                        ang = 180 - ang

            

                if abs(360 - ang) > 5:
                    if ang < 180:
                        msg = 1
                    else:
                        msg = 0
                        

            pt1, pt2 = calc_cords(pt1, pt2, dx, dy)
            img = cv.line(img, pt1, pt2, (0,0,255), 2)

 
        socket.send(str(msg).encode('utf-8'))

        img = cv.line(img, (100, 0), (100, 200), (0, 255, 0))


        cv.imshow('result', img) 
    
        ch = cv.waitKey(5)
        if ch == 27:
            break



if __name__ == '__main__':
    main()
