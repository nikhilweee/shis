import os
import sys
import argparse
import urllib.request
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from typing import Generator, List, Tuple

from tqdm import tqdm


#-------------------------------------------------------------------------------
# General Utils
#-------------------------------------------------------------------------------


def chunks(iterable: List[str], chunk_size: int) -> Generator[List[str], None, None] :
    """Yield successive :attr:`chunk_size` sized chunks from :attr:`iterable`.

    :param iterable: an iterable to split into chunks.
    :param chunk_size: number of chunks to split :attr:`iterable` into.
    :return: a generator comtaining chunks of :attr:`iterable`.
    """
    for i in range(0, len(iterable), chunk_size):
        yield iterable[i:i + chunk_size]


def rreplace(string: str, find: str, replace: str) -> str:
    """Starting from the right, replace the first occurence of
    :attr:`find` in :attr:`string` with :attr:`replace`.

    :param string: the string to search :attr:`find` in.
    :param find: the substring to find in :attr:`string`.
    :param replace: the substring to replace :attr:`find` with.
    :return: the replaced string.
    """
    return replace.join(string.rsplit(find, 1))


def slugify(path: str) -> str:
    """Create a slug given a :attr:`path`.

    Essentially, this replaces slashes with dashes.

    :param path: the path to slugify.
    :return: the slugified path.
    """
    if os.path.sep not in path:
        return 'index'
    else:
        return '-'.join(path.split(os.path.sep))


def urlify(slug: str, page=1) -> str:
    """Create a URL given a :attr:`slug` and a :attr:`page` index.

    :param slug: a slug from :func:`slugify`.
    :param page: an optional page number to include in the url.
    :return: the path of the HTML page described by :attr:`slug`.
    """
    if page > 1:
        url = f'html/{slug}-{page}.html'
    else:
        if slug == 'index':
            url = f'{slug}.html'
        else:
            url = f'html/{slug}.html'
    return url


def filter_image(name: str) -> bool:
    """Checks if a given file name is an image.

    :param name: the file name to check.
    :return: ``True`` if the file name is an image, ``False`` otherwise.
    """
    _, ext = os.path.splitext(name)
    if ext.lower() in ['.jpeg', '.jpg', '.png', '.tiff']:
        return True
    return False


#-------------------------------------------------------------------------------
# Argparse Utils
#-------------------------------------------------------------------------------


def fixed_width_formatter(width: int=80) -> argparse.HelpFormatter:
    """Patch :class:`argparse.HelpFormatter` to use a fixed width.

    :param width: the maximum width of the help and usage text generated.
    :return: a patched instance of the formatter class.
    """

    class HelpFormatter(argparse.HelpFormatter):

        def __init__(self, *args, **kwargs):
            super().__init__(width=width, *args, **kwargs)

    return HelpFormatter


#-------------------------------------------------------------------------------
# Server Utils
#-------------------------------------------------------------------------------


class CustomHTTPHandler(SimpleHTTPRequestHandler):
    """An HTTP Handler to serve arbitrary directories compatible with Python 3.6.

    This handler uses :attr:`self.server.directory` instead of always using
    ``os.getcwd()``

    :meta private:
    """

    protocol_version = "HTTP/1.1"

    def translate_path(self, path: str) -> str:
        """Translates a path to the local filename syntax."""
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        if hasattr(self.server, 'directory'):
            relpath = os.path.relpath(path, os.getcwd())
            path = os.path.join(self.server.directory, relpath)
        return path
    
    def log_message(self, format: str, *args: str) -> None:
        """A dummy function overridden to disable logging."""
        pass
    
    def handle(self) -> None:
        """Handle multiple requests if necessary."""
        self.close_connection = True
        try:
            self.handle_one_request()
            while not self.close_connection:
                self.handle_one_request()
        except (ConnectionResetError, BrokenPipeError):
            pass


def start_server(args: argparse.Namespace) -> HTTPServer:
    """Start a Simple HTTP Server as a separate thread.
    
    :param args: preprocessed command line arguments.
    """
    if sys.version_info.minor == 6:
        return start_server_36(args)
    if sys.version_info.minor >= 7:
        return start_server_37(args)


def get_public_ip(host: str, port: int) -> Tuple[str, int]:
    """Try to determine the public IP of the server.

    :param host: the fallback host to return in case of an error
    :param port: the port to check for public availability
    """
    try:
        with urllib.request.urlopen('https://api.ipify.org', timeout=5) as r:
            public_host = r.read().decode('utf-8')
            shis_server_url = f'http://{public_host}:{port}/'
        with urllib.request.urlopen(shis_server_url, timeout=5) as r:
            status = r.getcode()
        if status == 200:
            host = public_host
    except urllib.error.URLError as error:
        pass
    return host, port


def start_httpd(server: HTTPServer, address: Tuple[str, int], 
    handler: SimpleHTTPRequestHandler, args: argparse.Namespace) -> HTTPServer:
    """Try to start an HTTPServer, choosing the next available port.

    :param server: the server class to execute
    :param address: the address to start the server on
    :param handler: the request handler to use with the server
    :param args: preprocessed command line arguments
    """
    try:
        return server(address, handler)
    except OSError as error:
        if str(error) == '[Errno 98] Address already in use':
            if args.port is not None or address[1] > 7500:
                print(f'OSError: {error}. Try a different port using the -p flag.')
                sys.exit()
            else:
                address = (address[0], address[1]+1)
                return start_httpd(server, address, handler, args)
        else:
            raise error


def start_server_36(args):
    """Start an HTTP Server on Python 3.6.
    
    :meta private:
    """
    import socketserver

    class CustomHTTPServer(HTTPServer):
        def __init__(self, server_address: str, 
                     RequestHandlerClass: HTTPServer=CustomHTTPHandler,
                     directory: str=os.getcwd()):
            self.directory = directory
            HTTPServer.__init__(self, server_address, RequestHandlerClass)

    class ThreadingHTTPServer(socketserver.ThreadingMixIn, CustomHTTPServer):
        daemon_threads = False
    
    handler_class = CustomHTTPHandler
    server_class = partial(ThreadingHTTPServer, directory=args.thumb_dir)
    server_address = ("", args.port or 7447)
    httpd = start_httpd(server_class, server_address, handler_class, args)

    Thread(target=httpd.serve_forever).start()

    host, port = httpd.socket.getsockname()
    host, port = get_public_ip(host, port)
    serve_message = "Serving HTTP on {host}:{port}. "
    serve_message += "Press CTRL-C to quit."
    tqdm.write(serve_message.format(host=host, port=port))

    return httpd


def start_server_37(args):
    """Start an HTTP Server on Python 3.7 and above.
    
    :meta private:
    """    
    import contextlib
    from http.server import ThreadingHTTPServer, _get_best_family

    class DualStackServer(ThreadingHTTPServer):
        def server_bind(self):
            # suppress exception when protocol is IPv4
            with contextlib.suppress(Exception):
                self.socket.setsockopt(
                    socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

    handler_class = partial(CustomHTTPHandler, directory=args.thumb_dir)
    server_class = DualStackServer
    server_class.address_family, server_address = \
        _get_best_family(None, args.port or 7447)
    httpd = start_httpd(server_class, server_address, handler_class, args)
    
    Thread(target=httpd.serve_forever).start()

    host, port = httpd.socket.getsockname()[:2]
    host, port = get_public_ip(host, port)
    tqdm.write(f"Serving HTTP on {host}:{port}. "
               f"Press CTRL-C to quit.")

    return httpd
