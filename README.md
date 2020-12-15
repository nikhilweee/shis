# Simple HTTP Image Server
[![GitHub](https://img.shields.io/github/license/nikhilweee/shis)](https://github.com/nikhilweee/shis/blob/main/LICENSE.md)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/shis)](https://pypi.org/project/shis/)
[![PyPI](https://img.shields.io/pypi/v/shis)](https://pypi.org/project/shis/)
[![Documentation Status](https://readthedocs.org/projects/shis/badge/?version=stable)](https://shis.readthedocs.io)

A drop-in replacement for `python -m http.server`, albeit for images.

# Quickstart
Install `shis`.
```
$ pip install shis
```
Navigate to a `directory/containing/images`.
```
$ cd /directory/containing/images
```
Remember `python -m http.server`? Great.
```
$ python -m shis.server
# Serving HTTP on 0.0.0.0:7447. Press CTRL-C to quit.
# Processing images from : directory/containing/images
# Creating thumbnails in : directory/containing/images/shis
# Generating Website     : 100%|████████████████████| 2/2 [00:00<00:00, 35.09it/s]
# Generating Thumbnails  : 100%|███████████████| 120/120 [00:00<00:00, 132.48it/s]
```
There. You can now head over to http://0.0.0.0:7447/ (Or use your public IP instead).

# Preview
Here's an example of what you can expect to see.

![Demo](https://raw.githubusercontent.com/nikhilweee/shis/main/static/demo.png)

# Features
* Drop-in replacement for `python -m http.server`, so it's easy on your brain.
* Serves website even before creating thumbnails, so you don't have to wait.
* Uses multiple processes to create thumbails, so it's fast.
* Efficient resumes, so we build on past progress.
* Creates both small and large size thumbnails, so it's easy on your eyes.
* Minimal dependencies - just Pillow, Jinja2 and tqdm.
* Server side pagination, so it's easy on your browser.
* Tries to preserve EXIF orientation, so you don't have to rotate manually.
* Displays the public IP (if exists), so you don't have to remember.

# Usage
The following options are available. You can also access this via `python -m shis.server -h`
```
usage: python -m shis.server [-h] [--image-dir DIR] [--thumb-dir DIR] [--previews] [--clean] [--ncpus CPUS]
                             [--pagination ITEMS] [--port PORT] [--order ORDER] [--thumb-size SIZE]
                             [--preview-size SIZE]

A drop in replacement for python -m http.server, albeit for images.

optional arguments:
  -h, --help            show this help message and exit
  --image-dir DIR, -d DIR
                        directory to scan for images (default: current directory)
  --thumb-dir DIR, -s DIR
                        directory to store generated thumbnails and website (default: shis)
  --previews, -f        also generate fullscreen previews (takes more time)
  --clean, -c           remove existing thumbnail directory (if any) before processing
  --ncpus CPUS, -j CPUS
                        number of workers to spawn (default: number of available CPUs)
  --pagination ITEMS, -n ITEMS
                        number of items to show per page (default: 200)
  --port PORT, -p PORT  port to host the server on (default: 7447)
  --order ORDER, -o ORDER
                        file listing order (choices: random, name, original; default: name)
  --thumb-size SIZE     size of generated thumbnails in pixels (default: 256)
  --preview-size SIZE   size of fullscreen previews (if generated) in pixels (default 1024)
```
Further documentation can be found at [shis.readthedocs.io](https://shis.readthedocs.io).

# Benchmarks

For comparison, I ran the following tools on the [FFHQ Dataset](https://github.com/NVlabs/ffhq-dataset). The dataset contains 70k images in 1024x1024 resolution for a total size of 90GB. The converted thumbnail size was set to 320x320 for all tools. The tests were done on a machine with an AMD EPYC 7401P CPU with 24 Cores, 32GB Memory and Python 3.6.10 running on Ubuntu 18.04. The config files used are provided below. All conversion times are in `hh:mm:ss` format.

| Library Version | Conversion Time |             Configuration             |
|:---------------:|:---------------:|:-------------------------------------:|
|    shis 0.0.5   |      22:50      |                default                |
|   sigal 2.1.1   |      33:39      | [sigal.conf.py](static/sigal.conf.py) |
| thumbsup 2.14.0 |       >1h       | [thumbsup.json](static/thumbsup.json) |

# Why SHIS?
There are a bunch of static image servers (thumbsup, sigal, etc) available in a bunch of different languages (javascript, python, etc). While some of them like fgallery and curator haven't been developed in a while, others like thumbsup and sigal take a lot of time converting images. SHIS is designed with just one use case in mind, and it plans to do it well. It aims to serve a large directory of images in the fastest and easiest way possible.

# License
MIT License