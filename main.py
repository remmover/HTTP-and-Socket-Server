import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from datetime import datetime
import socket
import json
import socketserver
import threading


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {
            str(datetime.now()): {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}}
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

        send_to_socket_server(data_dict)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


class SocketServerHandler(socketserver.BaseRequestHandler):
    @staticmethod
    def save_to_json_file(data_dict):
        file_path = 'storage/data.json'
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
        data.update(data_dict)
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def handle(self):
        data = self.request[0].decode('UTF-8')
        try:
            data_dict = json.loads(data)
            self.save_to_json_file(data_dict)
        except json.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')

        print(f'Received data: {data}')


def run_http_server(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def run_socket_server(server_class=socketserver.UDPServer, handler_class=SocketServerHandler):
    server_address = ('', 5000)
    socket_server = server_class(server_address, handler_class)
    try:
        socket_server.serve_forever()
    except KeyboardInterrupt:
        socket_server.server_close()


def send_to_socket_server(data_dict):
    server_address = ('localhost', 5000)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        data = json.dumps(data_dict).encode('UTF-8')
        sock.sendto(data, server_address)


if __name__ == '__main__':
    http_thread = threading.Thread(target=run_http_server)
    socket_thread = threading.Thread(target=run_socket_server)

    http_thread.start()
    socket_thread.start()

    http_thread.join()
    socket_thread.join()
