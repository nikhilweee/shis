import argparse
import math
import os
import sys
import shutil
import random
import time
from itertools import repeat
from multiprocessing import cpu_count
from typing import Dict, Tuple

import imagesize
from tqdm import tqdm
from PIL import Image, ImageOps
from tqdm.contrib.concurrent import process_map
from jinja2 import Environment, FileSystemLoader, select_autoescape

from shis.utils import (chunks, filter_image, rreplace, slugify,
                        start_server, urlify, fixed_width_formatter)


def generate_thumbnail(paths: Tuple[str, str, str, str], args: argparse.Namespace):
    """Takes paths from :func:`process_paths` and generates thumbnail(s).

    By default, only one thumbnail of size :attr:`args.thumb_size` is 
    created, while previews are symlinked to the original image.
    If :attr:`args.previews` is set, previews of :attr:`args.preview_size` 
    will also be created. Download links are always symlinked to the 
    original image.

    :param paths: A tuple of paths to process.
    :param args: preprocessed command line arguments.
    """

    in_file, small_file, large_file, full_file = paths
    if os.path.exists(small_file):
        if os.path.getmtime(small_file) >= os.path.getmtime(in_file):
            return
    try:
        # Save Preview
        im = Image.open(in_file)
        if args.previews:
            im.thumbnail((args.preview_size, args.preview_size))
            im = ImageOps.exif_transpose(im)
            if 'exif' in im.info:
                exif = im.info['exif']
                im.save(large_file, exif=exif)
            else:
                im.save(large_file)
        # Save Thumbnail
        im.thumbnail((args.thumb_size, args.thumb_size))
        im = ImageOps.exif_transpose(im)
        if 'exif' in im.info:
            exif = im.info['exif']
            im.save(small_file, exif=exif)
        else:
            im.save(small_file)
        # Save Full
        full_dest = os.path.relpath(in_file, os.path.dirname(full_file))
        os.symlink(full_dest, full_file)
        # shutil.copy(in_file, full_file)
        return
    except Exception as e:
        return e


def process_paths(args: argparse.Namespace) -> Tuple[Tuple[str, str, str, str], int, bool]:
    """Generate paths to be processed by :func:`generate_thumbnail`

    If :attr:`args.clean` is set, all image files within :attr:`args.image_dir`
    will be included. Else, thumbnails which already exist and are newer than 
    the original image will be fileterd out.

    :param args: preprocessed command line arguments.
    :return: a tuple of (paths, num_pages, stale).

        - **paths** (*tuple*) - a 4-tuple containing (1) the absolute
          path of the original image, and the absolute path of the (2) small,
          (3) large and (4) full size thumbnails to be generated by
          :func:`generate_thumbnail`.
        - **num_pages** (*int*) - the number of webpages to generate.
        - **stale** (*bool*) - indicates whether a stale thumbnail was deleted.
    """
    paths = []
    num_pages = 0
    stale = False

    if not args.quiet:
        tqdm.write(f'Processing images from : {args.image_dir}')
        if args.clean and os.path.isdir(args.thumb_dir):
            existing_dir = os.path.relpath(args.thumb_dir, os.getcwd())
            tqdm.write(f'Clearing existing data : {args.thumb_dir}')
            shutil.rmtree(args.thumb_dir)
        tqdm.write(f'Creating thumbnails in : {args.thumb_dir}')

    for image_root, _, files in os.walk(args.image_dir):
        if args.thumb_dir in image_root:
            continue
        if image_root.count('/') > 100:
            raise ValueError(f'Too many subdirectories: {image_root}')
        small_root = rreplace(image_root, args.image_dir, f'{args.thumb_dir}/small')
        large_root = rreplace(image_root, args.image_dir, f'{args.thumb_dir}/large')
        full_root = rreplace(image_root, args.image_dir, f'{args.thumb_dir}/full')
        os.makedirs(small_root, exist_ok=True)
        os.makedirs(large_root, exist_ok=True)
        os.makedirs(full_root, exist_ok=True)
        num_pages += 1
        for idx, name in enumerate(filter(filter_image, files)):
            image_path = os.path.join(image_root, name)
            small_path = os.path.join(small_root, name)
            large_path = os.path.join(large_root, name)
            full_path = os.path.join(full_root, name)
            if idx != 0 and idx % args.pagination == 0:
                num_pages += 1
            if args.clean:
                paths.append((image_path, small_path, large_path, full_path))
            elif not os.path.exists(small_path):
                paths.append((image_path, small_path, large_path, full_path))
            elif os.path.getmtime(small_path) < os.path.getmtime(image_path):
                paths.append((image_path, small_path, large_path, full_path))
        # Make a list of thumbnails that have to be deleted
        thumb_files = filter(filter_image, os.listdir(small_root))
        stale_files = list(set(thumb_files) - set(files))
        stale = True if stale_files else stale
        for name in stale_files:
            for size_root in [small_root, large_root, full_root]:
                size_path = os.path.join(size_root, name)
                os.remove(size_path) if os.path.isfile(size_path) else None
    return paths, num_pages, stale


def generate_albums(args: argparse.Namespace) -> Tuple[Dict, int]:
    """Generate data required to populate Jinja2 templates.

    This function generates the correct names and URLs for all 
    thumbnails, albums, breadcrumbs and previews required for
    populating each HTML page of the website.

    :param args: preprocessed command line arguments.
    :return: a generator which yields data required to populate each page.
    """
    small_base = os.path.join(args.thumb_dir, 'small')
    image_base = os.path.dirname(args.image_dir)

    for index_root, folders, files in os.walk(args.image_dir):
        if args.thumb_dir in index_root:
            continue
        small_root = rreplace(index_root, args.image_dir, small_base)
        full_root = rreplace(small_root, 'small', 'full')
        large_root = rreplace(small_root, 'small', 'large')
        slug_path = os.path.relpath(index_root, image_base)
        if not args.previews:
            large_root = full_root

        slug = slugify(slug_path)
        name = os.path.basename(slug_path)
        album = {'name': name}
        files = list(filter(filter_image, files))

        # Breadcrumbs
        crumbs = []
        crumb_root = ''
        for name in slug_path.split(os.path.sep):
            crumb_root = os.path.join(crumb_root, name)
            url = urlify(slugify(crumb_root))
            crumb = {'name': name, 'url': url}
            crumbs.append(crumb)
        album['crumbs'] = crumbs

        # Sort
        if args.order == 'name':
            files = sorted(files)
            folders = sorted(folders)
        if args.order == 'random':
            random.shuffle(files)
            random.shuffle(folders)

        # Albums
        albums = []
        for folder_name in folders:
            album_path = os.path.join(index_root, folder_name)
            if args.thumb_dir in album_path:
                continue
            image_root = os.path.join(small_root, folder_name)
            album_size = len(os.listdir(album_path))
            image = ''
            if album_size > 0:
                for file_name in os.listdir(album_path):
                    if filter_image(file_name):
                        image_path = os.path.join(image_root, file_name)
                        image = os.path.relpath(image_path, args.thumb_dir)
                        break
            album_slug_path = os.path.join(slug_path, folder_name)
            url = urlify(slugify(album_slug_path))
            folder = {'image': image, 'url': url,
                      'name': folder_name, 'size': album_size}
            albums.append(folder)
        album['albums'] = albums

        # Pagination
        num_pages = max(1, math.ceil(len(files) / args.pagination))
        pagination = []
        for page in range(1, num_pages + 1):
            url = urlify(slug, page)
            page = {'page': page, 'url': url, 'current': ''}
            pagination.append(page)
        album['pagination'] = pagination

        # Images
        for page, chunk in enumerate(chunks(files, args.pagination)):
            thumbs = []
            for name in chunk:
                small_path = os.path.join(small_root, name)
                large_path = os.path.join(large_root, name)
                full_path = os.path.join(full_root, name)
                real_path = os.path.join(index_root, name)
                try:
                    width, height = imagesize.get(real_path)
                except ValueError:
                    continue
                if width < height:
                    width = width * args.thumb_size / height
                    height = args.thumb_size
                if width == height:
                    width = args.thumb_size
                    height = args.thumb_size
                if width > height:
                    width = width * args.thumb_size / height
                    height = args.thumb_size
                small = os.path.relpath(small_path, args.thumb_dir)
                large = os.path.relpath(large_path, args.thumb_dir)
                full = os.path.relpath(full_path, args.thumb_dir)
                thumb = {'name': name, 'small': small, 'large': large,
                         'full': full, 'width': width, 'height': height}
                thumbs.append(thumb)
            album['thumbs'] = thumbs
            if page > 0:
                album['pagination'][page - 1]['current'] = None
            album['pagination'][page]['current'] = 'current'
            yield album, page

        # Ensure that empty folders are not skipped
        if not files:
            yield album, 0


def create_templates(args: argparse.Namespace, num_pages: int) -> None:
    """Generate HTML files and corresponding directories for the website.

    This function creates ``static`` and ``html`` directories inside
    :attr:`args.thumb_dir`. If the directories already exist, they will be 
    cleared before continuing. All static content (JS/CSS) is stored 
    in :attr:`args.thumb_dir` ``/static`` and all HTML files (except 
    ``index.html``) are stored in :attr:`args.thumb_dir` ``/html``. 
    The data required to populate Jinja2 templates is obtained 
    from :func:`generate_albums`.

    :param args: preprocessed command line arguments.
    :param num_pages: number of HTML files (pages) to create.
    """
    # Copy JS/CSS
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    static_src = os.path.join(template_dir, 'static')
    static_dest = os.path.join(args.thumb_dir, 'static')
    html_dir = os.path.join(args.thumb_dir, 'html')
    # Remove existing directories
    if os.path.exists(static_dest):
        shutil.rmtree(static_dest)
    if os.path.exists(html_dir):
        shutil.rmtree(html_dir)
    shutil.copytree(static_src, static_dest)
    os.makedirs(html_dir)
    # Generate fresh HTML
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )

    image_root = os.path.basename(args.image_dir)
    redir_html = os.path.join(args.thumb_dir, 'index.html')
    with open(redir_html, 'w') as f:
        f.write(f'<html><head><meta http-equiv="Refresh" '
                f'content="0; URL=/html/{image_root}"></head></html>')


    with tqdm(generate_albums(args),
        desc="Generating Website     ", total=num_pages, ncols=100,
        bar_format=("{l_bar}{bar:20}| {n_fmt:>5}/{total_fmt:>5} "
        "[{elapsed}<{remaining}, {rate_fmt:>10}{postfix}]")) as pbar:
        for album, page in generate_albums(args):
            template = env.get_template('index.html')
            url = album['pagination'][page]['url']
            html = f'{args.thumb_dir}/{url}/index.html'
            html_dir = os.path.dirname(html)
            if not os.path.isdir(html_dir):
                os.makedirs(html_dir, exist_ok=True)
            template.stream(album=album).dump(html)
            # Handle tqdm when files are still being added
            pbar.update(1)
            if pbar.n > pbar.total:
                pbar.total = pbar.n


def preprocess_args(args: argparse.Namespace) -> argparse.Namespace:
    """Preprocess arguments parsed by argparse.

    Specifically, this function disambiguates the relative
    paths supplied for :attr:`args.image_dir` and :attr:`args.thumb_dir`
    and converts them into absolute paths.

    :param args: command line arguments parsed by argparse.
    :return: preprocessed command line arguments.
    """
    args.image_dir = os.path.abspath(os.path.join(
        os.getcwd(), args.image_dir)).rstrip(os.path.sep)
    args.thumb_dir = os.path.abspath(os.path.join(
        os.getcwd(), args.thumb_dir)).rstrip(os.path.sep)
    return args


def main(args: argparse.Namespace) -> None:
    """The main script for coordinating shis.

    :param args: command line arguments parsed by argparse.
    """
    args = preprocess_args(args)
    # Start the server process
    try:
        server = start_server(args)
        stale_paths = []
        while True:
            # Generate HTML pages
            paths, num_pages, stale = process_paths(args)
            new_paths = list(set(paths) - set(stale_paths))
            if new_paths or stale:
                create_templates(args, num_pages)
            # Generate thumbnails
            if paths:
                process_map(generate_thumbnail, paths, repeat(args),
                    chunksize=1, max_workers=args.ncpus, unit_scale=True,
                    desc='Generating Thumbnails  ', ncols=100,
                    bar_format=("{l_bar}{bar:20}| {n_fmt:>5}/{total_fmt:>5} "
                    "[{elapsed}<{remaining}, {rate_fmt:>10}{postfix}]"))
            stale_paths = paths
            args.clean = False
            args.quiet = True
            if not args.watch:
                break
            else:
                time.sleep(args.watch)
        while True:
            # Loop until a KeyboardInterrupt is received
            time.sleep(1)
    except KeyboardInterrupt:
        print('\nKeyboard interrupt received, exiting.')
        server.shutdown()
        sys.exit()


def make_parser() -> argparse.ArgumentParser:
    """Creates a parser with the specified options.

    :return: a parser with the specified options.
    """

    parser = argparse.ArgumentParser(
        prog='python -m shis.server', 
        description='A drop in replacement for python -m http.server, albeit for images.',
        formatter_class=fixed_width_formatter(width=80))
    parser.add_argument('--image-dir', '-d', default='', metavar='DIR',
        help='directory to scan for images (default: current dir)')
    parser.add_argument('--thumb-dir', '-s', default='shis', metavar='DIR',
        help='directory to store generated content (default: %(default)s)')
    parser.add_argument('--port', '-p', type=int, default=None,
        help='port to host the server on (default: 7447)')
    parser.add_argument('--pagination', '-n', type=int, default=200, metavar='ITEMS',
        help='number of items to display per page (default: %(default)s)')
    parser.add_argument('--order', '-o', default='name', metavar='ORDER',
        choices = ['original', 'random', 'name'],
        help='image listing order: name (default), random, or original')
    parser.add_argument('--ncpus', '-j', type=int, default=cpu_count(), metavar='CPUS',
        help='number of workers to spawn (default: available CPUs)')
    parser.add_argument('--watch', '-w', type=int, default=False, const=30, nargs='?',
        metavar='SEC', help='filesystem watch interval in seconds (default: False)')
    parser.add_argument('--clean', '-c', action='store_true',
        help='remove existing --thumb-dir (if any) before processing')
    parser.add_argument('--previews', '-f', action='store_true',
        help='also generate fullscreen previews (takes more time)')
    parser.add_argument('--thumb-size', type=int, default=256, metavar='SIZE',
        help='size of generated thumbnails in pixels (default: %(default)s)')
    parser.add_argument('--preview-size', type=int, default=1024, metavar='SIZE',
        help='size of generated previews in pixels (default: %(default)s)')
    return parser


if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()
    args.quiet = False
    main(args)
