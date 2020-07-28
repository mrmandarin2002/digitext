# import neccessary functions and classes
from datetime import datetime
import socket, sys

get_time = None
interact = None

# import database interaction functions
from interactions import *

# function to get the local ip address
def get_local_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return_var = s.getsockname()[0]
    s.close()
    return return_var

# initialize udp socket object and bind the socket to the localhost at port 7356
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('', 7356)
udp_socket.bind(server_address)
print(get_time()+"Server socket initialized")
print(get_time()+"Connect all clients to " + str(get_local_address()))

# list of client addresses
clients = []

# main server loop
print(get_time()+"Starting main server loop...")
while True:
    # receive incoming packages
    data, address = udp_socket.recvfrom(4096)
    # process any received data
    if data:
        print(get_time()+"Received data from: "+address[0]+":"+str(address[1]))
        # if the address of the received data does not exist in clients, add it before continuing
        if address not in clients:
            clients.append(address)
        # process the command request
        decoded_data = data.decode("utf-8")
        function_selection = decoded_data.split(';')[0]
        send_data = decoded_data.split(";")[1].split("|")
        received_data = str(interact[function_selection](send_data)).encode("utf-8")
        #print("Function: " + str(function_selection))
        #print("Data Sent: " + str(send_data))
        #print("Length of data: " + str(sys.getsizeof(received_data)))
        #print("Returned Data: " + str(received_data))
        udp_socket.sendto(received_data, address)
 