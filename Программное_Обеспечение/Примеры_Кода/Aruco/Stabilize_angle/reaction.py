import socket
from robot import Robot

rob = Robot()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(('', 12345)) 
    server.listen(1)
    
    print('Wait for client ...')

    client, address = server.accept()
    print(f'Client ip: {address}')

    server.settimeout(0.1)

    rob.led(rob.ON)

    while True:
        try:
            direction = int(client.recv(1))

            if direction == 2:
                rob.off()

            elif direction == 1:
                rob.set_motor(rob.R, rob.BWD, 70)
                rob.set_motor(rob.L, rob.FWD, 70)

            else:
                rob.set_motor(rob.R, rob.FWD, 70)
                rob.set_motor(rob.L, rob.BWD, 70)

            
        except TimeoutError:
            rob.off()


if __name__ == '__main__':
    main()
