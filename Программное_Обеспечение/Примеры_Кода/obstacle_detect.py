import time
from robot import Robot

rob = Robot()

def main():
    while True:
        dist_arr = rob.get_dist()
        left, fwd, right = dist_arr

        if all(dist > 15 for dist in dist_arr):
            rob.set_motor(rob.R, rob.FWD, 255)
            rob.set_motor(rob.L, rob.FWD, 255)

        elif left < right:
            rob.set_motor(rob.R, rob.BWD, 180)
            rob.set_motor(rob.L, rob.FWD, 180)

        else:
            rob.set_motor(rob.R, rob.FWD, 180)
            rob.set_motor(rob.L, rob.BWD, 180)

        time.sleep(0.05)


if __name__ == '__main__':
    main()
