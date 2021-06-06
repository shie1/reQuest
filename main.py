import os, webbrowser, sys, socketserver, socket, pytube, unicodedata, re, urllib, http.server, platform, pystray, getopt
from pytube.cli import on_progress
from threading import Thread
from time import sleep
from pyngrok.ngrok import connect as cn
from PIL import Image
from subprocess import Popen
from pynotifier import Notification

cwd = os.getcwd()

sys.tracebacklimit = 0

last = ""

iconfile = Image.open("icon.png")

opts, args = getopt.getopt(sys.argv[1:],"p:",["port="])

port = 4658

for opt, arg in opts:
    if opt in ('-p',"--port"):
        port = int(arg)

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

if(os.path.exists("downloads") == False):
    os.mkdir("downloads")

os.chdir('web')

if(platform.system() == "Windows"):
    def openPath(path):
        Popen('explorer.exe "' + path + '"', shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)
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
            url, res, type = params[0], params[1], params[2]
            convert(url,res, type)
            return super().do_GET()
        if(req.find("/open-path/") != -1):
            openPath(os.path.join(cwd, params[0]))
            return super().do_GET()
        return super().do_GET()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

def convert(url,resolution,type):
    global last
    def comp(a,b):
        global last
        if(b == last):
            return
        last = b
        if(type == "audio"):
            b = b.replace('.mp4', '.mp3')
        Notification(title="Video downloaded", description=b, duration=5, urgency='low', icon_path=os.path.join(cwd, "icon.png")).send()
    try:
        yt = pytube.YouTube(url)
    except:
        return
    fileName = slugify(yt.title)
    if(os.path.exists(os.path.join("downloads", fileName))):
        return "File already exists!"
    yt = pytube.YouTube(url,on_complete_callback=comp)
    stream = ""
    if(type == "video"):
        if(resolution != ""):
            stream = yt.streams.get_by_resolution(resolution) # example: 720p, 480p
        if(stream == None) or (resolution == ""):
            stream = yt.streams.get_highest_resolution()
    elif(type == "audio"):
        stream = yt.streams.filter(only_audio=True).all()[0]
    stream.download(os.path.join(cwd, "downloads"),filename=fileName)
    if(type == "audio"):
        os.rename(os.path.join(cwd, "downloads", fileName + '.mp4'), os.path.join(cwd, "downloads", fileName + '.mp3'))

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