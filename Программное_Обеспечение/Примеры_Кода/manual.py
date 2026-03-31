from robot import Robot
import keyboard
import time


rob = Robot()

keyboard.hook(lambda e: None)  #Без этого не обновляется _pressed_events



def get_currently_pressed() -> tuple:
    buttons = [0, 0, 0, 0]

    for b in keyboard._pressed_events:
        if b == 17:
            buttons[0] = 'w'

        elif b == 30:
            buttons[1] = 'a'

        elif b == 31:
            buttons[2] = 's'

        elif b == 32:
            buttons[3] = 'd'

    return buttons




def control(buttons: tuple) -> None:
    w, a, s, d = buttons
    
    if w and a:
        rob.set_motor(rob.R, rob.FWD, 255)
        rob.set_motor(rob.L, rob.FWD, 130)

    elif w and d:
        rob.set_motor(rob.R, rob.FWD, 220)
        rob.set_motor(rob.L, rob.FWD, 160)


    elif s and a:
        rob.set_motor(rob.R, rob.BWD, 255)
        rob.set_motor(rob.L, rob.BWD, 130)

    elif s and d:
        rob.set_motor(rob.R, rob.FWD, 220)
        rob.set_motor(rob.L, rob.FWD, 160)



    elif w:
        rob.set_motor(rob.R, rob.FWD, 220)
        rob.set_motor(rob.L, rob.FWD, 130)

    elif s:
        rob.set_motor(rob.R, rob.BWD, 220)
        rob.set_motor(rob.L, rob.BWD, 130)

    elif a:
        rob.set_motor(rob.R, rob.FWD, 220)
        rob.set_motor(rob.L, rob.BWD, 130)

    elif d:
        rob.set_motor(rob.R, rob.BWD, 220)
        rob.set_motor(rob.L, rob.FWD, 130)

    else:
        rob.off()




def main():
    while True:
        buttons = get_currently_pressed()
        control(buttons)
        time.sleep(0.05)



if __name__ == '__main__':
    main()
