import atexit
import serial
import os
import time
from colorama import Fore, Style, init


class Robot():
    def __init__(self):
        self.baudrate = 115200
        self.R = 1
        self.L = 0
        self.FWD = 1
        self.BWD = 0
        self.ex = atexit.register(self.shutdown)

        try:
            self.ser = serial.Serial('/dev/ttyUSB0', self.baudrate, timeout=1)
        except:
            try:
                self.ser = serial.Serial('/dev/ttyUSB1', self.baudrate, timeout=1)
            except:
                print("Can not connect to arduino, check USB connection")
                os._exit(0)
       
        print(Fore.YELLOW + Style.BRIGHT + '[ROBOT] ' + Fore.LIGHTWHITE_EX + 'Initialization ...')
        time.sleep(5)
        print(Fore.YELLOW + Style.BRIGHT + '[ROBOT]' + Fore.LIGHTWHITE_EX + ' Ready') 


    def send_pkg(self, key: int, cmd: int, val: int):
        bytes_array = [key, cmd, val]
        self.ser.write(bytes(bytes_array))


    def set_motor(self, motor: bool, dir=0, speed=0):
        self.send_pkg(key=motor, cmd=dir, val=speed)


    def move(self, dir: bool, speed: int):
        self.set_motor(self.R, dir=dir, speed=speed)
        self.set_motor(self.L, dir=dir, speed=speed)


    def stop(self):
        self.send_pkg(key=self.L, cmd=2, val=0)
        self.send_pkg(key=self.R, cmd=2, val=0)


    def off(self):
        self.send_pkg(key=self.L, cmd=3, val=0)
        self.send_pkg(key=self.R, cmd=3, val=0)



    def get_dist(self) -> tuple:
        self.send_pkg(key=2, cmd=0, val=0)
        data = list(self.ser.read(3))

        data[2] = 50 #Правый дальномер помер,поэтому вставялем костыль

        return data


    def shutdown(self):
        self.off()
        print(Fore.YELLOW + Style.BRIGHT + '[ROBOT]' + Fore.LIGHTWHITE_EX + ' Shutdown')

