import socket
import threading

BYTES = 1024
PORT = 5050
SERVER = '192.168.1.2'
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

name = input("Enter your name: ")

def receive():
    while True:
        try:
            msg = client.recv(BYTES).decode(FORMAT)
            if msg == '!NEWX_USERX':
                client.send(name.encode(FORMAT))
            else:
                print(msg)
        except:
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        msg = '{}: {}'.format(name, input(''))
        client.send(msg.encode(FORMAT))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
