import socket
from robot import Robot
import struct as st


rob = Robot()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(('', 12345)) 
    server.listen(1)
    
    print(server.getsockname())

    client, address = server.accept()
    print(f'Connect: {address}')

    server.settimeout(1)

    rob.led(True)

    while True:
        try:
            data_pkg = client.recv(4)
            L_val, R_val = st.unpack('>hh', data_pkg)

            if not L_val and not R_val:
                rob.stop()
                continue

            rob.set_motor(rob.R, R_val)
            rob.set_motor(rob.L, L_val)

            
        except BaseException:
            rob.stop()
            rob.off()
            server.close()
            break

    print('Disconnected')

if __name__ == '__main__':
    main()
