import socket
from urllib.parse import urlparse
import argparse
import re
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

    def validate_header(header):
        pattern = r"^(.+?):\s*(.+)$"
        if re.match(pattern, header):
            return header
        raise argparse.ArgumentTypeError("Invalid header format. Please use 'key:value'.")

    main_parser = argparse.ArgumentParser(prog="httpc", description="httpc is a curl-like application but supports HTTP protocol only.", epilog="Use \"httpc help [command]\" for more information about a command.")
    subparsers = main_parser.add_subparsers(dest="command")

    parser1_get = subparsers.add_parser("get", help="executes a HTTP GET request and prints the response.")
    parser1_get.add_argument("--verbose", "-v" , help="Prints the detail of the response such as protocol, status, and headers", action="store_true")
    parser1_get.add_argument("--headers", nargs='+', help="Additional headers in the format 'key:value'")

    parser2_post = subparsers.add_parser("post", help="Post executes a HTTP POST request for a given URL with inline data or from file.")
    parser2_post.add_argument("--verbose", "-v", help="Prints the detail of the response such as protocol, status, and headers", action="store_true")
    parser2_post.add_argument("--headers", metavar="header", type=validate_header, nargs="+", help="Headers in 'key:value' format")
    parser2_post.add_argument("-d", help="Associates an inline data to the body HTTP POST request.", action="store_true")
    parser2_post.add_argument("-f", help="Associates the content of a file to the body HTTP POST request.", action="store_true")

    main_parser.add_argument("url", help="URL determines the targeted HTTP server.")
    args = main_parser.parse_args()
    print(args)

    if(args.url[0] == '\''):
        client = ConcordiaHTTP(str(args.url).replace('\'', ''))
    else:
        client = ConcordiaHTTP(str(args.url))


    #Get method
    if(args.command=='get'):
        client.set_method("GET")
        client.add_header("User-Agent", "ConcordiaHTTP")
        response = client.send_request()
        print("Response from server:")
        print(response)
    elif args.command == 'post':
        client.set_method("POST")
        client.set_body('{"assignment": 1"')
        if args.headers:
            args_split_headers = str(args.header).split(":")
            client.add_header(args_split_headers[0], args_split_headers[1]) #'key:value'

        response = client.send_request()
        print("Response from server")
        print(response)
