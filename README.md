# Simple HTTP Image Server
[![GitHub](https://img.shields.io/github/license/nikhilweee/shis)](https://github.com/nikhilweee/shis/blob/main/LICENSE.md)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/shis)](https://pypi.org/project/shis/)
[![PyPI](https://img.shields.io/pypi/v/shis)](https://pypi.org/project/shis/)
[![Documentation Status](https://readthedocs.org/projects/shis/badge/?version=stable)](https://shis.readthedocs.io)

A drop-in replacement for `python -m http.server`, albeit for images.


# Quickstart
Install SHIS.
```
pip install shis
```
Navigate to a `directory/containing/images`.
```
cd /directory/containing/images
```
Remember `python -m http.server`? Great. SHIS runs the same way.
```
python -m shis.server
```
There. You can now head over to http://0.0.0.0:7447/ (Or use your public IP instead). SHIS will generate thumbnails in the meanwhile.
```
# Serving HTTP on 0.0.0.0:7447. Press CTRL-C to quit.
# Processing images from : directory/containing/images
# Creating thumbnails in : directory/containing/images/shis
# Generating Website     : 100%|████████████████████|     4/    4 [00:00<00:00,  49.82it/s]
# Generating Thumbnails  : 100%|████████████████████|   300/  300 [00:00<00:00,  1.47kit/s]
```
**TIP**: You can install the latest development version directly from GitHub.
```
pip install git+https://github.com/nikhilweee/shis/
```


# Preview
<!--
    # shutil.copy(in_file, full_file) instead of os.symlink(full_dest, full_file)
    python -m shis.server -d sample-images --thumb-dir demo -s -n 100
    # find demo -type f -name "*.html" -exec sed -i "s/\"\//\"\/shis\//g" {} \;
    git subtree push --prefix demo/ origin gh-pages
-->
Here's an example of what you can expect to see. 

![Demo](https://raw.githubusercontent.com/nikhilweee/shis/main/static/demo.png)


# Features
* Drop-in replacement for `python -m http.server`, so it's easy on your brain.
* Serves website even before creating thumbnails, so you don't have to wait.
* Uses multiple processes to create thumbails, so it's fast.
* Minimal redundancy, we build on past progress.
* Creates both small and large size thumbnails, so it's easy on your eyes.
* Minimal dependencies - Pillow, Jinja2, tqdm, and imagesize.
* Server side pagination, so it's easy on your browser.
* Tries to preserve EXIF orientation, so you don't have to rotate manually.
* Displays the public IP (if exists), so you don't have to remember.
* Watches the filesystem continuously for changes, so you don't have to refresh.
* Added selection capabilities, so you can visually filter files.


# Usage
The following options are available. You can also access this help using `python -m shis.server -h`. Further documentation can be found at [shis.readthedocs.io](https://shis.readthedocs.io).
```
usage: python -m shis.server [-h] [-c] [-s] [-p PORT] [-d DIR] [-w [SEC]]
                             [-n ITEMS] [-g ITEMS] [-o ORDER] [--thumb-dir DIR]
                             [--previews] [--ncpus CPUS] [--thumb-size SIZE]
                             [--preview-size SIZE]

A drop in replacement for python -m http.server, albeit for images.

options:
  -h, --help            show this help message and exit
  -c, --clean           remove existing thumb dir (if any) before processing
  -s, --selection       enable selection mode on the website
  -p PORT, --port PORT  port to host the server on (default: 7447)
  -d DIR, --image-dir DIR
                        directory to scan for images (default: current dir)
  -w [SEC], --watch [SEC]
                        filesystem watch interval in seconds (default: False)
  -n ITEMS, --pagination ITEMS
                        number of items to display per page (default: 200)
  -g ITEMS, --group ITEMS
                        number of items to group together (default: None)
  -o ORDER, --order ORDER
                        image listing order: name (default), random, or original
  --thumb-dir DIR       directory to store generated website (default: shis)
  --previews            also generate fullscreen previews (takes more time)
  --ncpus CPUS          number of workers to spawn (default: all available CPUs)
  --thumb-size SIZE     size of generated thumbnails in pixels (default: 256)
  --preview-size SIZE   size of generated previews in pixels (default: 1024)
```


# Benchmarks
For comparison, I ran the following tools on the [FFHQ Dataset](https://github.com/NVlabs/ffhq-dataset). The dataset contains 70k images in 1024x1024 resolution for a total size of 90GB. The converted thumbnail size was set to 320x320 for all tools. The tests were done on a machine with an AMD EPYC 7401P CPU with 24 Cores, 32GB Memory and Python 3.6.10 running on Ubuntu 18.04. The config files used are provided below. All conversion times are in `hh:mm:ss` format.

| Library Version | Conversion Time |             Configuration             |
|:---------------:|:---------------:|:-------------------------------------:|
|    shis 0.0.5   |      22:50      |                default                |
|   sigal 2.1.1   |      33:39      | [sigal.conf.py](static/sigal.conf.py) |
| thumbsup 2.14.0 |       >1h       | [thumbsup.json](static/thumbsup.json) |


# Why SHIS?
There are a bunch of static image servers (thumbsup, sigal, etc) available in a bunch of different languages (javascript, python, etc). While some of them like fgallery and curator haven't been developed in a while, others like thumbsup and sigal take a lot of time converting images. SHIS is designed with just one use case in mind, and it plans to do it well. It aims to serve a large directory of images in the fastest and easiest way possible.


# Acknowledgements
The gallery template used to display images is a modified version of the cards theme from [thumbsup](https://github.com/thumbsup/theme-cards). SHIS also uses [lightgallery](https://github.com/sachinchoolur/lightGallery) for fullscreen previews and image slideshows.


# License
MIT License