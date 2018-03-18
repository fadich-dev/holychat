import socket
import _thread
from settings import HOST, PORT, CHUNK


users = list()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print('\nThe server is running on <{}:{}>...\n'.format(HOST, PORT))


def on_new_client(connection, address):
    print('Connected by {}'.format(address))
    users.append(address)
    print('\n{}\n'.format(users))

    while True:
        try:
            message = connection.recv(CHUNK)

            for user in users:
                if user != address:
                    connection.sendto(message, address)

        except (BrokenPipeError, ConnectionResetError) as e:
            print('Disconnected by {}'.format(address))
            users.remove(address)
            exit()


try:
    while True:
        conn, address = server.accept()
        _thread.start_new_thread(on_new_client, (conn, address))
except KeyboardInterrupt as e:
    pass

server.close()
