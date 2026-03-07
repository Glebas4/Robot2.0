import time
from robot import Robot

rob = Robot()

while True:
    time.sleep(0.1)
    dist_arr = rob.get_dist()
    rob.set_motor(rob.R, rob.FWD, 220)
    rob.set_motor(rob.L, rob.FWD, 130)


    while not all(dist > 15 for dist in dist_arr):
        rob.set_motor(rob.R, rob.BWD, 200)
        rob.set_motor(rob.L, rob.FWD, 200)
        dist_arr = rob.get_dist()

