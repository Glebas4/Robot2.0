import cv2 as cv
import numpy as np
from robot import Robot



MARKER_SIZE = 5

dist_coeffs = np.zeros((5, 1), dtype=np.float32)
cam_x, cam_y = 640, 360


camera_matrix = np.array([
    [1050.0, 0.0,    640.0],
    [0.0,    1050.0, 360.0],
    [0.0,    0.0,    1.0  ]
], dtype=np.float32)


obj_points = np.array([
        [-MARKER_SIZE/2,  MARKER_SIZE/2, 0],
        [ MARKER_SIZE/2,  MARKER_SIZE/2, 0],
        [ MARKER_SIZE/2, -MARKER_SIZE/2, 0],
        [-MARKER_SIZE/2, -MARKER_SIZE/2, 0]
    ], dtype=np.float32)



cap = cv.VideoCapture(0)

cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)


aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_250)
parameters = cv.aruco.DetectorParameters()
detector = cv.aruco.ArucoDetector(aruco_dict, parameters)



def calculate_signals(x: int) -> tuple:
    diff = x - cam_x
    sig  = 255 - int(abs(diff * 0.39))
    if diff > 0:
        right = sig
        left  = 255

    else:
        right = 255
        left  = sig

    return right, left




def main():
    rob = Robot()


    while True:
        ok, img_raw = cap.read()
        if not ok:
            print("err")
            break

        corners, ids, _ = detector.detectMarkers(img_raw)

        if ids is not None:

            for i in range(len(ids)):
                _, _, tvec = cv.solvePnP(obj_points, corners[i], camera_matrix, dist_coeffs)
            
                dist = np.linalg.norm(tvec)
                mark_x = int(np.mean(corners[i][0][:, 0]))
                #mark_y = int(np.mean(corners[i][0][:, 1]))
                
                if not(dist < 15):
                    r, l = calculate_signals(x=mark_x)
                    rob.set_motor(rob.R, rob.FWD, r)
                    rob.set_motor(rob.L, rob.FWD, l)


                #img_raw = cv.aruco.drawDetectedMarkers(img_raw, [corners[i]], ids[i])
                #img_raw = cv.arrowedLine(img_raw, (cam_x, cam_y), (mark_x, mark_y), (0, 0, 255), 3)
                #img_raw = cv.circle(img_raw, (x, y), 5, (0, 0, 255), -1)
                #img_raw = cv.putText(img_raw, distance)
                #print(int(distance), 'cm ',  ids[i], l, r)
            
        


if __name__ == '__main__':
    main()
