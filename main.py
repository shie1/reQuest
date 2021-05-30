import os, webbrowser, sys
from http.server import HTTPServer, CGIHTTPRequestHandler

if(len(sys.argv) > 1):
    try:
        port = int(sys.argv[1])
    except:
        port = 8080
else:
    port = 8080

os.chdir('web')

server_object = HTTPServer(server_address=('', port), RequestHandlerClass=CGIHTTPRequestHandler)

server_object.serve_forever()