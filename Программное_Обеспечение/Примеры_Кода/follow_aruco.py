import cv2 as cv
import numpy as np
from robot import Robot


MARKER_SIZE = 5

dist_coeffs = np.zeros((5, 1), dtype=np.float32)
cam_x, cam_y = 320, 240


camera_matrix = np.array([
    [1430.0, 0,      640.0],
    [0,      1430.0, 360.0],
    [0,      0,      1    ]
    ], dtype=np.float32)


obj_points = np.array([
        [-MARKER_SIZE/2,  MARKER_SIZE/2, 0],
        [ MARKER_SIZE/2,  MARKER_SIZE/2, 0],
        [ MARKER_SIZE/2, -MARKER_SIZE/2, 0],
        [-MARKER_SIZE/2, -MARKER_SIZE/2, 0]
    ], dtype=np.float32)


aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
parameters = cv.aruco.DetectorParameters()
detector = cv.aruco.ArucoDetector(aruco_dict, parameters)


def compute_signals(x: int) -> tuple:
    diff = x - cam_x
    sig  = int(255 - abs(diff * 0.7))
    if diff > 0:
        right = 255
        left  = sig

    else:
        right = sig
        left  = 255

    return right, left




def main():
    rob = Robot()

    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    print('Capture started')

    while True:
        ok, img_raw = cap.read()
        if not ok:
            print("err")
            break
        
        corners, ids, _ = detector.detectMarkers(img_raw)

        if ids is not None:
            for i in range(len(ids)):
                if ids[i] == 1:
                    _, _, tvec = cv.solvePnP(obj_points, corners[i], camera_matrix, dist_coeffs)
                
                    distance = np.linalg.norm(tvec)
                    mark_x = int(np.mean(corners[i][0][:, 0]))
                    #mark_y = int(np.mean(corners[i][0][:, 1]))
                    
                    right, left = compute_signals(x=mark_x)
                    rob.set_motor(motor=rob.R, dir=rob.FWD, speed=right)
                    rob.set_motor(motor=rob.L, dir=rob.FWD, speed=left)

                    print(int(distance), 'cm ',  ids[i], left, right)


        else:
            rob.off()


if __name__ == '__main__':
    main()import cv2 as cv
import numpy as np
from robot import Robot


MARKER_SIZE = 5

dist_coeffs = np.zeros((5, 1), dtype=np.float32)
cam_x, cam_y = 320, 240


camera_matrix = np.array([
    [715.0,  0.0,      320.0],
    [0.0,    953.3333, 240.0],
    [0.0,    0.0,      1.0  ]
], dtype=np.float32)


obj_points = np.array([
        [-MARKER_SIZE/2,  MARKER_SIZE/2, 0],
        [ MARKER_SIZE/2,  MARKER_SIZE/2, 0],
        [ MARKER_SIZE/2, -MARKER_SIZE/2, 0],
        [-MARKER_SIZE/2, -MARKER_SIZE/2, 0]
    ], dtype=np.float32)


aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
parameters = cv.aruco.DetectorParameters()
detector = cv.aruco.ArucoDetector(aruco_dict, parameters)


def compute_signals(x: int) -> tuple:
    diff = x - cam_x
    sig  = int(255 - abs(diff * 0.7))
    if diff > 0:
        right = 255
        left  = sig

    else:
        right = sig
        left  = 255

    return right, left




def main():
    rob = Robot()

    cap = cv.VideoCapture(0)
    print('Capture started')

    while True:
        ok, img_raw = cap.read()
        if not ok:
            print("err")
            break
        
        corners, ids, _ = detector.detectMarkers(img_raw)

        if ids is not None:
            for i in range(len(ids)):
                if ids[i] == 1:
                    _, _, tvec = cv.solvePnP(obj_points, corners[i], camera_matrix, dist_coeffs)
                
                    distance = np.linalg.norm(tvec)
                    mark_x = int(np.mean(corners[i][0][:, 0]))
                    #mark_y = int(np.mean(corners[i][0][:, 1]))
                    
                    right, left = compute_signals(x=mark_x)
                    rob.set_motor(motor=rob.R, dir=rob.FWD, speed=right)
                    rob.set_motor(motor=rob.L, dir=rob.FWD, speed=left)

                    print(int(distance), 'cm ',  ids[i], right, left)


        else:
            rob.off()


if __name__ == '__main__':
    main()
