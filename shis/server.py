import os
import argparse
import shutil

from itertools import repeat
from functools import partial
from multiprocessing import Pool, cpu_count
from http.server import test, SimpleHTTPRequestHandler

from tqdm import tqdm
from PIL import Image, ImageOps
from tqdm.contrib.concurrent import process_map
from jinja2 import Environment, FileSystemLoader, select_autoescape


class tqdm_class(tqdm):
    """Custom class for tqdm.contrib.concurrent.process_map."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.desc = "Generating Thumbnails"
        self.ncols = 80


def chunks(iterable, chunk_size):
    """Yield successive n-sized chunks from iterable."""
    for i in range(0, len(iterable), chunk_size):
        yield iterable[i:i + chunk_size]

def rreplace(string, find, replace):
    """Replace first occurence of `find` in `string` from the right with `replace`."""
    return replace.join(string.rsplit(find, 1))


def generate_thumbnail(paths, args):
    """Takes a four-tuple of paths and creates thumbnails.
    
    The paths are of the order:
        in_file: The path to the original image file
        small_file: The path to the small size thumbnail
            which will always be generated
        large_file: The path to the large size preview. 
            This will either be an image or a symlink to 
            in_file depending on args.large.
        full_file: The path to the full size image. 
            This will be a symlink to in_file.
    """
    in_file, small_file, large_file, full_file = paths
    if os.path.exists(small_file):
        if os.path.getmtime(small_file) >= os.path.getmtime(in_file):
            return
    try:
        # Save Preview
        im = Image.open(in_file)

        if args.large:
            im.thumbnail(args.preview_size)
            im = ImageOps.exif_transpose(im)
            if 'exif' in im.info:
                exif = im.info['exif']
                im.save(large_file, exif=exif)
            else:
                im.save(large_file)

        # Save Thumbnail
        im.thumbnail(args.thumb_size)
        im = ImageOps.exif_transpose(im)
        if 'exif' in im.info:
            exif = im.info['exif']
            im.save(small_file, exif=exif)
        else:
            im.save(small_file)

        # Save Full
        full_dest = os.path.relpath(in_file, os.path.dirname(full_file))
        os.symlink(full_dest, full_file)
        return
    except Exception as e:
        return e


def slugify(path):
    """Create a slug given a path."""
    if os.path.sep not in path:
        slug = 'index'
    else:
        slug = '-'.join(path.split(os.path.sep))
    return slug


def process_paths(args):
    paths = []
    num_files = 0
    for image_root, _, files in os.walk(args.image_dir):
        if args.thumb_dir in image_root:
            continue
        if image_root.count('/') > 100:
            raise ValueError(f'Too many subdirectories: {image_root}')
            return
        small_root = rreplace(image_root, args.image_dir, f'{args.thumb_dir}/small')
        large_root = rreplace(image_root, args.image_dir, f'{args.thumb_dir}/large')
        full_root = rreplace(image_root, args.image_dir, f'{args.thumb_dir}/full')
        os.makedirs(small_root, exist_ok=True)
        os.makedirs(large_root, exist_ok=True)
        os.makedirs(full_root, exist_ok=True)
        for name in files:
            image_path = os.path.join(image_root, name)
            small_path = os.path.join(small_root, name)
            large_path = os.path.join(large_root, name)
            full_path = os.path.join(full_root, name)
            num_files += 1
            if not os.path.exists(small_path):
                paths.append((image_path, small_path, large_path, full_path))
            elif os.path.getmtime(small_path) < os.path.getmtime(image_root):
                paths.append((image_path, small_path, large_path, full_path))
    return paths, num_files


def get_albums(args):
    small_base = os.path.join(args.thumb_dir, 'small')
    image_base = os.path.basename(args.image_dir)
    for small_root, folders, files in os.walk(small_base):
        index_root = rreplace(small_root, small_base, image_base)
        full_root = rreplace(small_root, 'small', 'full')
        large_root = rreplace(small_root, 'small', 'large')
        if not args.large:
            large_root = full_root

        slug = slugify(index_root)
        name = os.path.basename(index_root)
        album = {'name': name}

        # Breadcrumbs
        crumbs = []
        crumb_root = ''
        for name in index_root.split(os.path.sep):
            crumb_root = os.path.join(crumb_root, name)
            url = slugify(crumb_root) + '.html'
            crumb = {'name': name, 'url': url}
            crumbs.append(crumb)
        album['crumbs'] = crumbs

        # Albums
        albums = []
        for folder_name in folders:
            album_path = os.path.join(small_root, folder_name)
            album_size = len(os.listdir(album_path))
            image = ''
            if album_size > 0:
                for file_name in os.listdir(album_path):
                    _, ext = os.path.splitext(file_name)
                    if ext.lower() in ['.png', '.jpg', '.jpeg', '.tiff']:
                        image_path = os.path.join(album_path, file_name)
                        image = os.path.relpath(image_path, args.thumb_dir)
                        break
            slug_path = os.path.join(index_root, folder_name)
            url = slugify(slug_path) + '.html'
            folder = {'image': image, 'url': url, 'name': folder_name, 'size': album_size}
            albums.append(folder)
        album['albums'] = albums

        # Pagination
        num_pages = (len(files) // args.pagination) + 1
        pagination = []
        for x in range(1, num_pages + 1):
            if x > 1:
                url = f'{slug}-{x}.html'
            else:
                url = f'{slug}.html'
            page = {'number': x, 'url': url, 'current': ''}
            pagination.append(page)
        album['pagination'] = pagination

        # Images
        for page, chunk in enumerate(chunks(files, args.pagination)):
            thumbs = []
            for name in chunk:
                small_path = os.path.join(small_root, name)
                large_path = os.path.join(large_root, name)
                full_path = os.path.join(full_root, name)
                im = Image.open(small_path)
                width, height = im.size
                if width < height:
                    width = width * args.thumb_dim / height
                    height = args.thumb_dim
                if width == height:
                    width = args.thumb_dim * 0.8
                    height = args.thumb_dim * 0.8
                if width > height:
                    width = width * args.thumb_dim / height
                    height = args.thumb_dim
                small = os.path.relpath(small_path, args.thumb_dir)
                large = os.path.relpath(large_path, args.thumb_dir)
                full = os.path.relpath(full_path, args.thumb_dir)
                thumb = {'name': name, 'small': small, 'large': large, 'full': full, 'width': width, 'height': height}
                thumbs.append(thumb)
            album['thumbs'] = thumbs
            if page > 0:
                album['pagination'][page - 1]['current'] = None
            album['pagination'][page]['current'] = 'current'
            yield album, slug, page + 1
        
        if folders and not files:
            yield album, slug, 1


def create_templates(args, num_files):
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    public_src = os.path.join(template_dir, 'public')
    public_dest = os.path.join(args.thumb_dir, 'public')
    shutil.copytree(public_src, public_dest, dirs_exist_ok=True)
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    total = (num_files // args.pagination) + 1
    for album, slug, page in tqdm(get_albums(args), desc="Generating Website", total=total, ncols=80):
        template = env.get_template('index.html')
        if page > 1:
            html = f'{args.thumb_dir}/{slug}-{page}.html'
        else:
            html = f'{args.thumb_dir}/{slug}.html'
        template.stream(album=album).dump(html)


def start_server(args):
    """Start a Simple HTTP Server."""
    handler_class = partial(SimpleHTTPRequestHandler, directory=args.thumb_dir)
    test(handler_class, port=args.port)

def preprocess_args(args):
    args.image_dir = os.path.join(os.getcwd(), args.image_dir).rstrip(os.path.sep)
    args.thumb_dir = os.path.join(os.getcwd(), args.thumb_dir).rstrip(os.path.sep)
    args.thumb_size = tuple(args.thumb_size)
    args.preview_size = tuple(args.preview_size)
    print(f'Processing images from {args.image_dir}')
    print(f'Generating thumbnails in {args.thumb_dir}')
    return args

def main(args):
    args = preprocess_args(args)
    paths, num_files = process_paths(args)
    process_map(generate_thumbnail, paths, repeat(args),
                chunksize=1, tqdm_class=tqdm_class)
    create_templates(args, num_files)
    start_server(args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_dir', nargs='?', default='', help='directory to look for images (default: current directory)')
    parser.add_argument('-t', '--thumb-dir', default='shis', help='directory to store thumbnails and website (default: shis)')
    parser.add_argument('-l', '--large', action='store_true', help='also create large size previews')
    parser.add_argument('-s', '--thumb-dim', type=int, default=180, help='maximum dimension of thumbnail displayed on the webpage (default: 180)')
    parser.add_argument('-c', '--ncpus', type=int, default=cpu_count(), help='number of threads to spawn (default: multiprocessing.cpu_count())')
    parser.add_argument('-n', '--pagination', type=int, default=200, help='number of items to show per page (default: 200)')
    parser.add_argument('-p', '--port', type=int, default=8000, help='port to host the server on (default: 8000)')
    parser.add_argument('--thumb-size', nargs=2, metavar=('WIDTH', 'HEIGHT'), type=int, default=[320, 320], help='size of the generated thumbnails (default: 320x320)')
    parser.add_argument('--preview-size', nargs=2, metavar=('WIDTH', 'HEIGHT'), type=int, default=[1024, 1024], help='size of large size previews, if generated (default 1024x1024)')
    args = parser.parse_args()
    main(args)
