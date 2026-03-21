import cv2 as cv
import numpy as np
from flask import Flask, render_template, Response, request


app = Flask(__name__)

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

MARKER_SIZE = 5

dist_coeffs = np.zeros((5, 1), dtype=np.float32)
cam_x, cam_y = 640, 360


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




def getFramesGenerator():
    while True:
        ok, img = cap.read()
        if not ok:
            print("err")
            break
        
        corners, ids, _ = detector.detectMarkers(img)

        if ids is not None:
            for i in range(len(ids)):
                if ids[i] == 1:
                    _, _, tvec = cv.solvePnP(obj_points, corners[i], camera_matrix, dist_coeffs)
                
                    distance = np.linalg.norm(tvec)
                    #mark_x = int(np.mean(corners[i][0][:, 0]))
                    #mark_y = int(np.mean(corners[i][0][:, 1]))
                    img_raw = cv.aruco.drawDetectedMarkers(img_raw, [corners[i]], ids[i])

                    print(int(distance), 'cm ',  ids[i])



        _, buffer = cv.imencode('.jpg', img)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        


@app.route('/video_feed')
def video_feed():
    """ Генерируем и отправляем изображения с камеры"""
    return Response(getFramesGenerator(), mimetype='multipart/x-mixed-replace; boundary=frame')

        



def main():
    app.run(host='0.0.0.0', port=5000, debug=True)
   
