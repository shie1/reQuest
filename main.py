import os, webbrowser, sys, socketserver, socket, pytube, unicodedata, re, urllib, http.server
from threading import Thread
from time import sleep

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
        return super().do_GET()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

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

def convert(url,resolution):
    yt = pytube.YouTube(url)
    stream = yt.streams.get_by_resolution(resolution) # example: 720p, 480p
    if(stream == None):
        stream = yt.streams.get_highest_resolution()
    fileName = slugify(yt.title)
    if(os.path.exists("downloads/" + fileName)):
        return "File already exists!"
    stream.download("downloads",filename=fileName)
    return "File downloaded!"

if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', port), Handler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()