import socket
from robot import Robot


rob = Robot()

def control(buttons: tuple) -> None:
    w, a, s, d = buttons

    if w:
        rob.set_motor(rob.R, rob.FWD, 255)
        rob.set_motor(rob.L, rob.FWD, 255)

    elif s:
        rob.set_motor(rob.R, rob.BWD, 255)
        rob.set_motor(rob.L, rob.BWD, 255)

    elif a:
        rob.set_motor(rob.R, rob.FWD, 180)
        rob.set_motor(rob.L, rob.BWD, 180)

    elif d:
        rob.set_motor(rob.R, rob.BWD, 180)
        rob.set_motor(rob.L, rob.FWD, 180)

    else:
        rob.off()



def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(('', 12345)) 
    server.listen(1)
    
    print('Wait for client ...')

    client, address = server.accept()
    print(f'Client ip: {address}')

    while True:
        data = list(client.recv(4))
        control(data)


if __name__ == '__main__':
    main()
