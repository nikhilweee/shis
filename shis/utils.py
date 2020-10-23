import os
import sys
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler, test

from tqdm import tqdm


def chunks(iterable, chunk_size):
    """Yield successive n-sized chunks from iterable."""
    for i in range(0, len(iterable), chunk_size):
        yield iterable[i:i + chunk_size]


def rreplace(string, find, replace):
    """Replace first occurence of `find` in `string` from the right with `replace`."""
    return replace.join(string.rsplit(find, 1))


def slugify(path):
    """Create a slug given a path."""
    if os.path.sep not in path:
        slug = 'index'
    else:
        slug = '-'.join(path.split(os.path.sep))
    return slug


def urlify(slug, page=1):
    """Create a URL given a slug and a page index."""
    if page > 1:
        url = f'html/{slug}-{page}.html'
    else:
        if slug == 'index':
            url = f'{slug}.html'
        else:
            url = f'html/{slug}.html'
    return url


class tqdm_class(tqdm):
    """Custom class for tqdm.contrib.concurrent.process_map."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.desc = "Generating Thumbnails "
        self.ncols = 80


class CustomHTTPHandler(SimpleHTTPRequestHandler):
    """This handler uses server.directory instead of always using os.getcwd()"""
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.directory, relpath)
        return fullpath


class CustomHTTPServer(HTTPServer):
    """The main server, you pass in directory which is the path you want to serve requests from"""
    def __init__(self, server_address, RequestHandlerClass=CustomHTTPHandler, directory=os.getcwd()):
        self.directory = directory
        HTTPServer.__init__(self, server_address, RequestHandlerClass)


def start_server(args):
    """Start a Simple HTTP Server. Supports Python 3.6."""
    assert sys.version_info.major == 3, "Only Python 3 is supported."
    if sys.version_info.minor == 6:
        handler_class = CustomHTTPHandler
        server_class = partial(CustomHTTPServer, directory=args.thumb_dir)
        test(handler_class, server_class, port=args.port)
    if sys.version_info.minor >= 7:
        handler_class = partial(SimpleHTTPRequestHandler, directory=args.thumb_dir)
        test(handler_class, port=args.port)
