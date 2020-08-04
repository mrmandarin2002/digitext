# import neccessary functions and classes
from datetime import datetime
import socket, sys, threading

get_time = None
interact = None

# import database interaction functions
from interactions import *

PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
HEADER = 16

# initialize udp socket object and bind the socket to the localhost at port 7356
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = socket.gethostbyname(socket.gethostname())
server_address = (ip_address, PORT)
server.bind(server_address)

print(get_time()+"Server socket initialized")
print(get_time()+"Connect all clients to " + ip_address)

def handle_client(conn, addr):
    print(get_time() + f"Client with address {addr} connected.")
    while True:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if(msg_length):
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    break
                print(get_time() + msg)
                function_selection = msg.split(';')[0]
                send_data = msg.split(";")[1].split("|")
                data_return = str(interact[function_selection](send_data)).encode("utf-8")
                conn.send(data_return)
        except Exception as e:
            print("An error occurred." + str(e))
            print(f"Connection with address {addr} closed.")
            conn.close()
            break

# main server loop
print(get_time()+"Starting main server loop...")
server.listen()
while True:
    # receive incoming packages
    conn, addr = server.accept()
    thread = threading.Thread(target = handle_client, args = (conn, addr))
    thread.start()
    print(get_time() + f" New client connected. There are currently {threading.activeCount() - 1} client(s) connected!")
        