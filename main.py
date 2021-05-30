import os, webbrowser, sys, socketserver, socket
import http.server

if(len(sys.argv) > 1):
    try:
        port = int(sys.argv[1])
    except:
        port = 8080
else:
    port = 8080

os.chdir('web')

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if(self.client_address[0] != socket.gethostbyname("localhost")):
            return
        return super().do_GET()

myHandler = Handler
sock = socketserver.TCPServer(("", port), myHandler)
sock.serve_forever()