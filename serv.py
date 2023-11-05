import http.server
import http.server
import socketserver
import os
import json
import threading
import argparse


# Define the request handler class
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    data_directory = os.getcwd() + ('/data/')  # Directory to store files

    def do_GET(self):
        try:
            if self.path == '/':
                # Handle GET request for listing files
                files = os.listdir(self.data_directory)
                response_data = json.dumps(files).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response_data)
            else:
                # Handle GET request for retrieving file content
                file_path = os.path.normpath(self.data_directory + self.path.lstrip('/'))
                if file_path.startswith(os.path.abspath(self.data_directory)):
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as file:
                            file_content = file.read()
                        self.send_response(200)
                        self.send_header('Content-type', 'application/octet-stream')
                        self.end_headers()
                        self.wfile.write(file_content)
                    else:
                        self.send_error(404, 'File not found')
                else:
                    self.send_error(403, 'Access denied')
        except Exception as e:
            self.send_error(500, f'Server error: {str(e)}')

    def do_POST(self):
        try:
            # Handle POST request to create or overwrite files
            content_length = int(self.headers['Content-Length'])
            uploaded_data = self.rfile.read(content_length)
            file_path = os.path.normpath(self.data_directory + self.path.lstrip('/'))
            if file_path.startswith(os.path.abspath(self.data_directory)):
                # Check if the file already exists and overwrite if necessary
                if os.path.exists(file_path):
                    os.remove(file_path)

                with open(file_path, 'wb') as f:
                    f.write(uploaded_data)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f'File {file_path} uploaded successfully.'.encode('utf-8'))
            else:
                self.send_error(403, 'Access denied')
        except Exception as e:
            self.send_error(500, f'Server error: {str(e)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="httpfs", description="httpfs is a simple file server.", epilog="Use \"httpfs [command] --help\"  for more information about a command.")
    parser.add_argument("--verbose", "-v", help="Prints debugging messages.")
    parser.add_argument("--port", "-p", default=8080, type=int, help="Specifies the port number that the server will listen and serve at. Default is 8080.")
    parser.add_argument("--data_dir", "-d", help="Specifies the directory that the server will use to read/write requested files. \
    Default is the current directory when launching the application.")
    args = parser.parse_args()

    # Define the server parameters
    port = args.port

    # Create a multithreaded HTTP server with the defined request handler
    httpd = socketserver.ThreadingTCPServer(('', port), MyHttpRequestHandler)
    if(args.data_dir):
        MyHttpRequestHandler.data_directory = args.data_dir

    # Print a message indicating that the server is running
    print(f'Serving on port {port}')

    # Start the server in a separate thread
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()

    # Wait for the server thread to finish
    server_thread.join()
