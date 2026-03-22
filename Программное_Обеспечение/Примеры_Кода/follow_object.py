import cv2 as cv
import numpy as np
from robot import Robot



hsv_down = (50, 78, 97)
hsv_up   = (91, 255, 180)
cam_x_center = 640  
speed = 255



def find_obj(img):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    bin = cv.inRange(hsv, hsv_down, hsv_up)
    if cv.countNonZero(hsv) > 20:
        M = cv.moments(bin)
        if M['m00']:
            x = int(M['m10'] / M['m00'])

        return x
    
    else:
        return None
    


def calculate_sig(x_obj):
    error   = (x_obj - cam_x_center) / cam_x_center
    if error > 0:
        right = speed - abs(speed * error)
        left  = speed

    else:
        right = speed
        left  = speed - abs(speed * error)

    return right, left



def main():
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    rob = Robot()

    while True:
        ok, img_raw = cap.read()
        if not ok:
            print('error')
            break

        x = find_obj(img=img_raw)

        if x is not None:
            r, l = calculate_sig(x_obj=x)
            rob.set_motor(rob.R, rob.FWD, r)
            rob.set_motor(rob.L, rob.BWD, l)

        else:
            rob.off()


if __name__ == '__main__':
    main()
