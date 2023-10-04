import socket
from urllib.parse import urlparse
import argparse
class SimpleHTTPClient:
    def __init__(self, url):
        parsed_url = urlparse(url)
        self.host = parsed_url.hostname
        self.port = parsed_url.port or 80
        self.path = parsed_url.path or '/'
        self.query = parsed_url.query
        self.method = ""
        self.headers = {}
        self.body = ""

    def set_method(self, method):
        self.method = method

    def add_header(self, key, value):
        self.headers[key] = value

    def set_body(self, body):
        self.body = body

    def send_request(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))

        request = f"{self.method} {self.path}?{self.query} HTTP/1.1\r\n"
        request += f"Host: {self.host}\r\n"
        for key, value in self.headers.items():
            request += f"{key}: {value}\r\n"
        if self.body:
            request += f"Content-Length: {len(self.body)}\r\n"
        request += "\r\n"
        if self.body:
            request += self.body

        client_socket.sendall(request.encode())

        response = ""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data.decode()

        client_socket.close()
        return response

# Example usage:
parser = argparse.ArgumentParser()
parser.add_argument("get", help="get method")
# parser.add_argument("post", help="post method")
parser.add_argument("-v", help="verbose option")
parser.add_argument()
args = parser.parse_args()
print(args)
client = SimpleHTTPClient("http://httpbin.org/post")
client.set_method("POST")
client.add_header("User-Agent", "SimpleHTTPClient")
client.set_body('{"assignment" : 1}')
response = client.send_request()	
print("Response from server:")
print(response)


# # Usage: python echoclient.py --host host --port port
# parser = argparse.ArgumentParser()
# parser.add_argument("--host", help="server host", default="localhost")
# parser.add_argument("--port", help="server port", type=int, default=8007)
# args = parser.parse_args()
# run_client(args.host, args.port)
