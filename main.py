import socket
import sys
from urllib.parse import urlparse
import argparse
import re
import json
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

        if(self.query):
            request = f"{self.method} {self.path}?{self.query} HTTP/1.1\r\n"
        else:
            request = f"{self.method} {self.path} HTTP/1.1\r\n"
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
            data = client_socket.recv(3000)
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

    main_parser = argparse.ArgumentParser(prog="httpc", description="httpc is a curl-like application but supports HTTP protocol only.", epilog="Use \"httpc [command] --help\"  for more information about a command.")
    subparsers = main_parser.add_subparsers(dest="command")

    parser1_get = subparsers.add_parser("get", help="executes a HTTP GET request and prints the response.")
    parser1_get.add_argument("--verbose", "-v" , help="Prints the detail of the response such as protocol, status, and headers", action="store_true")
    parser1_get.add_argument("--headers", nargs='+', help="Additional headers in the format 'key:value'")
    parser1_get.add_argument("--output", "-o", help="Writes the body of the response to a file instead of console")

    parser2_post = subparsers.add_parser("post", help="Post executes a HTTP POST request for a given URL with inline data or from file.")
    parser2_post.add_argument("--verbose", "-v", help="Prints the detail of the response such as protocol, status, and headers", action="store_true")
    parser2_post.add_argument("--headers", metavar="header", type=validate_header, nargs="+", help="Headers in 'key:value' format")
    parser2_post.add_argument("--data", "-d", help="Associates an inline data to the body HTTP POST request.", nargs="+")
    parser2_post.add_argument("--file", "-f", help="Associates the content of a file to the body HTTP POST request.")

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
        if args.headers:
            for x in args.headers:
                args_remove_brackets = str(x).replace('\'', '')
                args_remove_brackets = str(args_remove_brackets).replace('[','')
                args_remove_brackets = str(args_remove_brackets).replace(']', '')
                args_split_headers = str(args_remove_brackets).split(":")
                client.add_header(args_split_headers[0], args_split_headers[1]) #'key:value'

        client.add_header("User-Agent", "ConcordiaHTTP")
        response = client.send_request()
        if args.output:
            with open(args.output, 'w') as file:
                # Write content to the file
                file.write(response)
            sys.exit()

        print("Response from server:")
        print(response)
    elif args.command == 'post':
        client.set_method("POST")

        if args.headers:
            for x in args.headers:
                args_remove_brackets = str(x).replace('\'', '')
                args_remove_brackets = str(args_remove_brackets).replace('[','')
                args_remove_brackets = str(args_remove_brackets).replace(']', '')
                args_split_headers = str(args_remove_brackets).split(":")
                client.add_header(args_split_headers[0], args_split_headers[1]) #'key:value'
        if args.data:
            client.set_body(json.dumps(args.data))   #str(args.data).replace('\'', ''))
        elif args.file:
            with open(args.file, 'r') as file:
                data = file.read()
                client.set_body(data)
        else:
            print("Error: Either -d or -f should be specified. Not both.")

        client.add_header("User-Agent", "ConcordiaHTTP")


        response = client.send_request()
        print("Response from server")
        print(response)
