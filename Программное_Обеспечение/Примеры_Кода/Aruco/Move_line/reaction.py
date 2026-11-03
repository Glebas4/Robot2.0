import socket
from robot import Robot
import struct as st

rob = Robot()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(('', 12345)) 
    server.listen(1)
    
    print(server.getsockname())

    client, address = server.accept()
    print(f'Connect: {address}')

    server.settimeout(0.1)

    rob.led(rob.ON)

    while True:
        try:
            L_dir = R_dir = rob.FWD

            data_pkg = client.recv(4)
            L, R = st.unpack('>hh', data_pkg)

            if L < 0:
                L_dir = rob.BWD

            if R < 0:
                R_dir = rob.BWD

            rob.set_motor(rob.R, R_dir, abs(R))
            rob.set_motor(rob.L, L_dir, abs(L))

            
        except TimeoutError:
            rob.off()


if __name__ == '__main__':
    main()
