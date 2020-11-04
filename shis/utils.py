import os
import sys
import argparse
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
from typing import List
from tqdm import tqdm


def chunks(iterable: List[str], chunk_size: int):
    """Yield successive ``chunk_size`` sized chunks from ``iterable``.

    :param iterable: An iterable to split into chunks.
    :param chunk_size: Number of chunks to split ``iterable`` into.
    """
    for i in range(0, len(iterable), chunk_size):
        yield iterable[i:i + chunk_size]


def rreplace(string: str, find: str, replace: str):
    """Starting from the right, replace the first occurence of
    ``find`` in ``string`` with ``replace``.

    :param string: The string to search ``find`` in.
    :param find: The substring to find in ``string``.
    :param replace: The substring to replace ``find`` with.
    """
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


def filter_image(name):
    """Checks if a given file name is an image."""
    _, ext = os.path.splitext(name)
    if ext.lower() in ['.jpeg', '.jpg', '.png', '.tiff']:
        return True
    return False


class tqdm_class(tqdm):
    """Custom class for :class:`tqdm.contrib.concurrent.process_map`.

    This is a custom class to support a user defined progress bar text
    (currently ``Generating Thumbnails``) and column size (currently ``80``).
    """

    def __init__(self, *args, **kwargs):
        """Constructor Method."""
        super().__init__(*args, **kwargs)
        self.desc = "Generating Thumbnails "
        self.ncols = 120


class CustomHTTPHandler(SimpleHTTPRequestHandler):
    """A custom HTTP Handler to serve custom directories in Python 3.6.

    This handler uses :attr:`self.server.directory` instead of always 
    using ``os.getcwd()``
    """

    def translate_path(self, path: str) -> str:
        """Translates a :attr:`path` to the local filename syntax.

        The full path is calculated relative to :attr:`self.server.directory`

        :param path: the path to tranlsate
        :return: the translated path
        """
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.directory, relpath)
        return fullpath


class CustomHTTPServer(HTTPServer):
    """A custom HTTP Server to serve custom directories in Python 3.6.

    This server uses the :attr:`directory` argument as the path to serve requests from."""

    def __init__(self, server_address, 
                 RequestHandlerClass=CustomHTTPHandler,
                 directory=os.getcwd()):
        self.directory = directory
        HTTPServer.__init__(self, server_address, RequestHandlerClass)


def start_server(args: argparse.Namespace) -> None:
    """Start a Simple HTTP Server.

    This function calls :meth:`http.server.test` as is for Python 3.7 and 
    above. For Python 3.6, a custom server :class:`CustomHTTPServer` and
    handler :class:`CustomHTTPHandler` is used to support custom directories.
    
    :param args: preprocessed command line arguments.
    """
    assert sys.version_info.major == 3, "Only Python 3 is supported."
    if sys.version_info.minor == 6:
        handler_class = CustomHTTPHandler
        server_class = partial(CustomHTTPServer, directory=args.thumb_dir)
        test(handler_class, server_class, port=args.port)
    if sys.version_info.minor >= 7:
        handler_class = partial(SimpleHTTPRequestHandler, directory=args.thumb_dir)
        test(handler_class, port=args.port)
