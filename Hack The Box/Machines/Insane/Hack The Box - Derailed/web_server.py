#!/usr/bin/python3
import socketserver
from http.server import SimpleHTTPRequestHandler

class Server(socketserver.TCPServer):
    allow_reuse_address = True

class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)
        
def serve_http(ip, port):
    handler = CORSRequestHandler
    with Server((ip, port), handler) as httpd:
        httpd.serve_forever()

if __name__ == '__main__':
    serve_http('10.10.14.4',9000)
