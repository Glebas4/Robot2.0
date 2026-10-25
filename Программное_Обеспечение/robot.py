import serial
import sys
import time


class Robot():
    def __init__(self) -> None:
        self.baudrate = 115200

        self.R = 1
        self.L = 0
        
        self.FWD = 1
        self.BWD = 0

        self.ON = 1
        self.OFF = 0
        

        self.__none = 0
        self.__stop = self.__sonar = 2
        self.__off = self.__led = 3
        

        sys.excepthook = self.shutdown

        try:
            self.ser = serial.Serial('/dev/ttyUSB0', self.baudrate, timeout=1)
        except:
            self.ser = serial.Serial('/dev/ttyUSB1', self.baudrate, timeout=1)


        print('Initialization ...')
        time.sleep(5)
        print('Ready') 


    def send_pkg(self, key: int, cmd: int, val: int) -> None:
        bytes_array = [key, cmd, val]
        self.ser.write(bytes(bytes_array))


    def set_motor(self, motor: bool, dir=0, speed=0) -> None:
        self.send_pkg(key=motor, cmd=dir, val=speed)


    def move(self, dir: bool, speed: int) -> None:
        self.set_motor(self.R, dir=dir, speed=speed)
        self.set_motor(self.L, dir=dir, speed=speed)


    def stop(self) -> None:
        self.send_pkg(key=self.L, cmd=self.__stop, val=self.__none)
        self.send_pkg(key=self.R, cmd=self.__stop, val=self.__none)

    
    def off(self) -> None:
        self.send_pkg(key=self.L, cmd=self.__off, val=self.__none)
        self.send_pkg(key=self.R, cmd=self.__off, val=self.__none)

    
    def get_dist(self) -> tuple:
        self.send_pkg(key=self.__sonar, cmd=self.__none, val=self.__none)
        data = list(self.ser.read(3))
        
        return data

    
    def led(self, state: bool) -> None:
        self.send_pkg(key=self.__led, cmd=state, val=self.__none)

    
    def shutdown(self, _, value, __):
        self.off()
        print(value)
