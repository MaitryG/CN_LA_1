import socket
import threading
import time

HEADER = 64  # how many bytes are we receiving
PORT = 1234  # define listening port
SERVER = socket.gethostbyname(
    socket.gethostname())  # gethostbyname: Translate a host name to IPv4 address format, gethostname: Return a
# string containing the hostname of the machine where the Python interpreter is currently executing
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET for IPv4 and SOCK_STREAM is for TCP connnections
s.bind((SERVER, PORT))  # binding the server socket object to a port and host


# This func is separate for each client
def handle_client(conn, addr):

    try:
        print(f"New connection, {addr} connected")
        connected = True
        while True:
            # msg_length = conn.recv(HEADER).decode(FORMAT)  # This is blocking line of code i.e. code that could potentially block the other
            # # processes that is why we have enabled threading
            # if msg_length:
            #     msg_length = int(msg_length)
            #     msg = conn.recv(msg_length).decode(FORMAT)
            #     if msg == DISCONNECT_MSG:
            #         connected = False
            #     print(f"[{addr}] {msg}")
            #     conn.send("Message received!".encode(FORMAT))
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
    finally:
        conn.close()



# This func is for all clients so threading is enabled inorder to handle each client in a different thread
def start():
    try:
        s.listen()
        while True:
            conn, addr = s.accept()  # This is blocking line of code
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    finally:
        s.close()



print("[STARTING] server is starting........")
print(socket.gethostbyname(socket.gethostname()))
start()
