import socket

HEADER = 64  # how many bytes are we receiving
PORT = 1234  # define listening port
SERVER = socket.gethostbyname(
    socket.gethostname())  # gethostbyname: Translate a host name to IPv4 address format, gethostname: Return a
# string containing the hostname of the machine where the Python interpreter is currently executing
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send('Hello World')
send("eooo")
send("Hello!!!!1")
send(DISCONNECT_MSG)