import os, webbrowser, sys, socketserver, socket, pytube, unicodedata, re, urllib, http.server, platform, slugi, pystray, getopt
from pytube.cli import on_progress
from threading import Thread
from time import sleep
from pyngrok.ngrok import connect as cn
from PIL import Image
from subprocess import Popen
from pynotifier import Notification

last = ""

iconfile = Image.open("icon.png")

opts, args = getopt.getopt(sys.argv[1:],"p:",["port=","no-init"])

no_init = False
port = 4658

for opt, arg in opts:
    if opt in ('-p',"--port"):
        port = int(arg)
    elif opt in ("--no-init"):
        no_init = True

if no_init == False:
    slugi.init(cn(port))

os.chdir('web')

if(platform.system() == "Windows"):
    def openPath(path):
        Popen("explorer.exe " + path, shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)
    def clear():
        os.system("cls")
elif(platform.system() == "Linux"):
    def openPath(path):
        Popen("xdg-open " + path, shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)
    def clear():
        os.system("clear")
elif(platform.system() == "Darwin"):
    def openPath(path):
        Popen("open " + path, shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)
    def clear():
        os.system("clear")

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        req = self.requestline.split(" ")[1]
        try:
            nparams = req.split('?')[1].split('&')
        except:
            try:
                nparams = [req.split('?')[1]]
            except:
                nparams = []
        params = []
        for item in nparams:
            params.append(urllib.parse.unquote(item))
        if(req.find("/convert/get") != -1):
            url, res = params[0], params[1]
            convert(url,res)
            return super().do_GET()
        if(req.find("/eval/") != -1):
            eval(params[0])
            return super().do_GET()
        if(req.find("/open-path/") != -1):
            openPath(params[0])
            return super().do_GET()
        return super().do_GET()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

def convert(url,resolution):
    global last
    def comp(a,b):
        global last
        print(b, last)
        if(b == last):
            return
        last = b
        Notification(title="Video downloaded", description=b, duration=5, urgency='low', icon_path=None).send()
    yt = pytube.YouTube(url)
    fileName = slugi.slugify(yt.title)
    if(os.path.exists("downloads/" + fileName)):
        return "File already exists!"
    yt = pytube.YouTube(url,on_complete_callback=comp)
    stream = yt.streams.get_by_resolution(resolution) # example: 720p, 480p
    if(stream == None):
        stream = yt.streams.get_highest_resolution()
    stream.download("downloads",filename=fileName)

if __name__ == '__main__':
    try:
        server = ThreadedHTTPServer(('localhost', port), Handler)
        print('Starting server, use <Ctrl-C> to stop')
        print('http://localhost:' + str(port))
        server.serve_forever()
    except OSError:
        print('Server already running!')
        print('http://localhost:' + str(port))
        sys.exit()
    except KeyboardInterrupt:
        clear()
        while True:
            sys.exit()