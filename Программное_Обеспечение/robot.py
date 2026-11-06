import serial
import sys
import time



class Robot():
    def __init__(self) -> None:
        print('[ROBOT] INIT ...') 
        self.baudrate = 115200

        self.R = 1
        self.L = 0
        
        self.FWD = 1
        self.BWD = 0

        self.__none = 0
        self.__stop = self.__sonar = 2
        self.__led = 3
        

        sys.excepthook = self.shutdown

        try:
            self.ser = serial.Serial('/dev/ttyUSB0', self.baudrate, timeout=1)
        except:
            self.ser = serial.Serial('/dev/ttyUSB1', self.baudrate, timeout=1)


        time.sleep(3)
        print('[ROBOT] READY') 



    def send_pkg(self, key: int, cmd: int, val: int) -> None:
        bytes_array = [key, cmd, val]
        self.ser.write(bytes(bytes_array))



    def set_motor(self, motor: bool, speed: int) -> None:
        dir = self.FWD
        if speed < 0:
            dir = self.BWD
            speed = -1*speed
        
        self.send_pkg(key=motor, cmd=dir, val=speed)



    def move(self, speed: int) -> None:
        self.set_motor(self.R, speed=speed)
        self.set_motor(self.L, speed=speed)



    def stop(self) -> None:
        self.send_pkg(key=self.L, cmd=self.__stop, val=self.__none)
        self.send_pkg(key=self.R, cmd=self.__stop, val=self.__none)



    def off(self) -> None:
        self.send_pkg(key=self.L, cmd=self.__none, val=self.__none)
        self.send_pkg(key=self.R, cmd=self.__none, val=self.__none)



    def get_dist(self) -> tuple:
        self.send_pkg(key=self.__sonar, cmd=self.__none, val=self.__none)
        data = list(self.ser.read(3))
        
        return data



    def led(self, state: bool) -> None:
        self.send_pkg(key=self.__led, cmd=state, val=self.__none)



    def shutdown(self, *args):
        self.off()
        self.led(False)
        self.ser.close()
        if len(args): print('[ROBOT]', ' ', args) 
        else: print('[ROBOT] SHUTDOWN OK')
