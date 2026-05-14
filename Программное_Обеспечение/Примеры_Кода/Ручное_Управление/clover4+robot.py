import rospy
from mavros_msgs.msg import RCIn
from robot import Robot


def callback(data) -> None:
    if data.channels[5] > 1500:
        left  = int((data.channels[2] - 1500) * 0.5)
        right = int((data.channels[1] - 1500) * 0.5)

        print(left, right)

        if abs(left) > 100:
            if left > 0:
                l_dir = rob.FWD
            else:
                l_dir = rob.BWD
            
            rob.set_motor(rob.L, l_dir, abs(left))

        else:
            rob.set_motor(rob.L, rob.FWD, 0)

        if abs(right) > 100:
            if right > 0:
                r_dir = rob.FWD
            else:
                r_dir = rob.BWD
            
            rob.set_motor(rob.R, r_dir, abs(right))
        else:
            rob.set_motor(rob.R, rob.FWD, 0)

    else:
        rob.off()

        


def main() -> None:
    rospy.init_node('Manual')
    rospy.Subscriber("/mavros/rc/in", RCIn, callback)
    rospy.spin()



if __name__ == '__main__':
    rob = Robot()
    main()
