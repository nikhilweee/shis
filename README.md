# Simple HTTP Image Server
A drop-in replacement for `python -m http.server`, albeit for images.

# Quickstart
```shell
# Install (using test pypi for now)
$ pip install -i https://test.pypi.org/simple/ shis

# Navigate to a directory containing images.
$ cd /directory/containing/images

# Remember python -m http.server? Good.
$ python -m shis.server
# Processing images from    /directory/containing/images
# Generating data in   	    /directory/containing/images/shis
# Generating Thumbnails : 100%|████████████████| 120/120 [00:00<00:00, 146.27it/s]
# Generating Website    : 100%|█████████████████████| 2/2 [00:00<00:00, 38.03it/s]
# Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...

# There. You can now head over to http://localhost:8000/
# (Or use your public IP instead)
```

# Features
* Drop-in replacement for `python -m http.server`, so it's easy on your brain.
* Recursively process image directory trees, so you can see them all.
* Parallelly create both small and large size thumbnails, so you don't have to wait.
* Minimal dependencies - just Pillow and Jinja2.
* Server side pagination, so it's easy on your browser.
* Tries to preserve EXIF orientation, so you don't have to rotate manually.

# Usage
The following options are available. You can also access this from `python -m shis.server -h`
```
usage: python -m shis.server [-h] [-t THUMB_DIR] [-l] [-s THUMB_DIM] [-j NCPUS] [-n PAGINATION] [-p PORT]
                             [--thumb-size WIDTH HEIGHT] [--preview-size WIDTH HEIGHT]
                             [image_dir]

A drop in replacement for python -m http.server, albeit for images.

positional arguments:
  image_dir             directory to look for images (default: current directory)

optional arguments:
  -h, --help            show this help message and exit
  -t THUMB_DIR, --thumb-dir THUMB_DIR
                        directory to store thumbnails and website (default: shis)
  -l, --large           also create large size previews (takes more time)
  -s THUMB_DIM, --thumb-dim THUMB_DIM
                        maximum dimension of thumbnail displayed on the webpage (default: 180)
  -j NCPUS, --ncpus NCPUS
                        number of threads to spawn (default: multiprocessing.cpu_count())
  -n PAGINATION, --pagination PAGINATION
                        number of items to show per page (default: 200)
  -p PORT, --port PORT  port to host the server on (default: 8000)
  --thumb-size WIDTH HEIGHT
                        size of the generated thumbnails (default: 320x320)
  --preview-size WIDTH HEIGHT
                        size of large previews, if generated (default 1024x1024)
```

# Benchmarks

| Library Version | Dataset | Dataset Size | Image Dimensions | Number of Images | Thumbnail Dimensions | Thumbnail Size | Conversion Time |                            Machine Specs                           |
|:---------------:|:-------:|:------------:|:----------------:|:----------------:|:--------------------:|:--------------:|:---------------:|:------------------------------------------------------------------:|
|      0.0.5      |   FFHQ  |     90GB     |    1024 x 1024   |        70k       |       320 x 320      |      11GB      |      22:50      | AMD EPYC 7401P, 24 Cores, 32GB Memory, Ubuntu 18.04, Python 3.6.10 |



# Why this project?
There are a bunch of static image servers (thumbsup, sigal, etc) available in a bunch of different languages (javascript, python, etc). This repo is designed with just one use case in mind, and it plans to do it well. It aims to serve a large directory of images in the fastest way possible.

# License
MIT License