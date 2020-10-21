# Simple HTTP Image Server
A drop-in replacement for `python -m http.server`, albeit for images.

# Quickstart
```shell
# Install using the plain old way.
$ pip install shis

# Navigate to a directory containing images.
$ cd directory/containing/images

# Remember python -m http.server? Good.
$ python -m shis.server
# Processing images from directory/containing/images
# Generating thumbnails in directory/containing/images/shis
# Generating Thumbnails: 100%|█████████████████| 120/120 [00:00<00:00, 145.10it/s]
# Generating Website: 2it [00:00, 40.82it/s]                                      
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
* Preserve EXIF orientation, so you don't have to rotate manually.

# Why this project?
There are a bunch of static image servers (thumbsup, sigal, etc) available in a bunch of different languages (javascript, python, etc). This repo is designed with just one use case in mind, and it plans to do it well. It aims to serve a large directory of images in the fastest way possible.

# License
MIT License