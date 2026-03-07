''' Импорт необходимых модулей '''
import atexit
import serial
import os
import time
from colorama import Fore, Style, init

''' Класс робота '''
class Robot():
    def __init__(self):
        ''' Константы, небходимые для работы '''
        self.baudrate = 115200
        self.R = 1
        self.L = 0
        self.FWD = 1
        self.BWD = 0
        self.ex = atexit.register(self.shutdown)
        ''' Попытка подключиться к микроконтроллеру'''
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', self.baudrate, timeout=1)
        except:
            try:
                self.ser = serial.Serial('/dev/ttyUSB1', self.baudrate, timeout=1)
            except:
                ''' Если не удалось подключиться к микроконтроллеру то завершаем программу'''
                print("Can not connect to arduino, check USB connection")
                os._exit(0)
        ''' Инициализация USB порта, для этого нужно немного времени'''
        print(Fore.YELLOW + Style.BRIGHT + '[ROBOT] ' + Fore.LIGHTWHITE_EX + 'Initialization ...')
        time.sleep(5)
        print(Fore.YELLOW + Style.BRIGHT + '[ROBOT]' + Fore.LIGHTWHITE_EX + ' Ready') 

    ''' Функция,отправляющая контроллеру пакет из 3-ех байтов '''
    def send_pkg(self, key: int, cmd: int, val: int):
        bytes_array = [key, cmd, val]
        self.ser.write(bytes(bytes_array))

    ''' Задаем параметры работы мотора на базе функции send_pkg'''
    def set_motor(self, motor: bool, dir=0, speed=0):
        self.send_pkg(key=motor, cmd=dir, val=speed)

    ''' Включаем оба мотора'''
    def move(self, dir: bool, speed: int):
        self.set_motor(self.R, dir=dir, speed=speed)
        self.set_motor(self.L, dir=dir, speed=speed)

    ''' Остановка с блокировкой колес '''
    def stop(self):
        self.send_pkg(key=self.L, cmd=2, val=0)
        self.send_pkg(key=self.R, cmd=2, val=0)

    ''' Отключение моторов '''
    def off(self):
        self.send_pkg(key=self.L, cmd=3, val=0)
        self.send_pkg(key=self.R, cmd=3, val=0)


    ''' Замеряем расстояние с УЗ датчиков '''
    def get_dist(self) -> tuple:
        self.send_pkg(key=2, cmd=0, val=0)
        data = list(self.ser.read(3))

        data[2] = 50 #Правый дальномер помер,поэтому вставялем костыль

        return data

    ''' Когда программа завершена или произошла ошибка, то выключаем моторы робота для удобства'''
    def shutdown(self):
        self.off()
        print(Fore.YELLOW + Style.BRIGHT + '[ROBOT]' + Fore.LIGHTWHITE_EX + ' Shutdown')
