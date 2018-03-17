import socket
import _thread
from settings import HOST, PORT, CHUNK


def on_new_client(connection, address):
    print('Connected by {}'.format(address))
    users.append(address)
    print()
    print(users)
    print()
    while True:
        try:
            connection.sendall(connection.recv(CHUNK))
        except (BrokenPipeError, ConnectionResetError) as e:
            print('Disconnected by {}'.format(address))
            users.remove(address)
            exit()


users = list()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

try:
    while True:
        conn, address = server.accept()
        _thread.start_new_thread(on_new_client, (conn, address))
except KeyboardInterrupt as e:
    pass

server.close()
