import socket
from urllib.parse import urlparse
import argparse
class ConcordiaHTTP:
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

if __name__ == "__main__":
    parser1_get = argparse.ArgumentParser(prog="httpc", description="httpc is a curl-like application but supports HTTP protocol only.", epilog="Use \"httpc help [command]\" for more information about a command.")
    parser1_get.add_argument("get", help="executes a HTTP GET request and prints the response.", default=str)
    parser1_get.add_argument("url", help="destination url", default=str)
    # parser.add_argument("post", help="executes a HTTP POST request and prints the response.")
    parser1_get.add_argument("--verbose", "-v" , help="verbose option", action="store_true")
    # parser1_get.add_argument("-h", "--headers", nargs='+', help="Additional headers in the format 'key:value'")
    args = parser1_get.parse_args()


    #if arg=='GET'
    #Get method
    client = ConcordiaHTTP('http://httpbin.org/get?course=networking&assignment=1')
    client.set_method("GET")
    client.add_header("User-Agent", "ConcordiaHTTP")
    # client = ConcordiaHTTP()
    # client.set_method(args.get)
    # client.add_header("User-Agent", "ConcordiaHTTP")

    #if arg=='POST'
    #Post method
    #client = ConcordiaHTTP("http://httpbin.org/post")
    #client.set_method("POST")
    # #client.add_header("User-Agent", "ConcordiaHTTP")
    # #client.set_body('{"assignment" : 1}')

    # u1 = urlparse((str(args.url))[1:-1])
    # print(u1)
    # print(u1.hostname)
    #
    # u2 = urlparse('http://httpbin.org/get?course=networking&assignment=1')
    # print(u2)
    # print(u2.hostname, u2.port)


    response = client.send_request()
    print("Response from server:")
    print(response)

            # Usage: python echoclient.py --host host --port port
            # parser = argparse.ArgumentParser()
            # parser.add_argument("--host", help="server host", default="localhost")
            # parser.add_argument("--port", help="server port", type=int, default=8007)
            # args = parser.parse_args()
            # run_client(args.host, args.port)httpbin.org/get
