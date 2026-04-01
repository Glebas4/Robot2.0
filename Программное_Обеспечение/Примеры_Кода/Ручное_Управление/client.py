import keyboard
import socket
import time


class ManualControl:
    def __init__(self, ip: str, port: str) -> None:
        self.ip   = ip
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.robot_addr = (ip, port)


        try:
            self.socket.connect(self.robot_addr)
            print('Connected')

        except Exception as e:
            print(f'Can not connect to robot: {e}')


    
    def buttons_pressed(self) -> tuple:
        buttons = [0, 0, 0, 0] # [w, a, s, d]

        for b in keyboard._pressed_events:
            if b == 17:
                buttons[0] = 1

            elif b == 30:
                buttons[1] = 1

            elif b == 31:
                buttons[2] = 1

            elif b == 32:
                buttons[3] = 1

        return buttons #[1, 1, 0, 0]



    def send_pkg(self, pkg: tuple) -> None:
        self.socket.sendall(bytes(pkg))




def main():
    ip = input('ip: ')
    port = int(input('port: '))

    controller = ManualControl(ip=ip, port=port)

    keyboard.hook(lambda e: None)  #Без этого не обновляется _pressed_events

    while True:
        buttons = controller.buttons_pressed()
        controller.send_pkg(buttons)
        time.sleep(0.05)



if __name__ == '__main__':
    main()
