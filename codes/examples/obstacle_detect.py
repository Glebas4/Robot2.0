from robot import Robot

rob = Robot()

while True:
    dist_arr = rob.get_dist()
    while all(dist > 15 for dist in dist_arr):
        rob.move(rob.FWD, 255)

    while not all(dist > 15 for dist in dist_arr):
        rob.set_motor(rob.R, rob.BWD, 200)
        rob.set_motor(rob.L, rob.FWD, 200)
