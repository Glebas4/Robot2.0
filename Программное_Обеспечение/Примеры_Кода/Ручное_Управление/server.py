import socket
from robot import Robot


rob = Robot()

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
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(('', 12345)) 
    server.listen(1)
    
    print('Wait for client ...')

    client, address = server.accept()
    print(f'Client ip: {address}')

    while True:
        data = list(client.recv(4))
        #print(data)
        control(data)


if __name__ == '__main__':
    main()
