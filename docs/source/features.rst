Features
========

SHIS is built with speed in mind. Here are some features which help.

.. contents::
   :local:
   :depth: 2

Friendly syntax
---------------
SHIS is meant to be a drop in replacement for ``http.server``, so it's 
easier for your brain (and your hands) to remember it's usage. 
SHIS follows the same invocation as ``http.server``.

Instant serving
---------------
SHIS starts serving webpages even before the thumbnails can be created. This
means that you can start browsing the website for images while SHIS is busy
creating thumbnails. This is incredibly useful for large directories where
processing thumbnails can take a long time.

Multiprocessing support
-----------------------
SHIS uses multiprocessing to take advantage of all cores available on the
system. This means that multiple thumbnails can be generated paralelly,
which significantly speeds up the entire process.

Efficient resumes
-----------------
When SHIS is run for the first time, it creates thumbnails for every image
in the directory. However, when the next time SHIS is run, it only creates 
thumbnails for files which have changed. In case SHIS was interrupted in 
between, it will only create thumbnails for images which haven't been
processed. This means subsequent runs will be significantly faster.

Create thumbnails and previews
------------------------------
SHIS can create both, small size thumbnails and large size previews. This
means one can quickly skim through large size previews instead of waiting
for the original full size image to load in the browser. To enable large 
size previews, run SHIS with the ``--previews`` flag. SHIS also lets you
customize the size of the generated thumbnails and previews using the 
``--thumb-size`` and ``--preview-size`` flags.

Minimal dependencies
--------------------
SHIS does not depend on a lot of third party modules. It uses ``Pillow``
(PIL) to create thumbnails, ``Jinja2`` as the templating language to create 
HTML pages, and ``tqdm`` to display clean progress bars. It uses the built 
in HTTP Server included with python to serve webpages.

Pagination support
------------------
SHIS was designed keeping in mind hundreds (or even thousands) of images
per directory. With such quantity, it becomes necessary to split images 
across multiple pages. SHIS automatically does that for you. By default,
SHIS only displays up to 200 items per page. You can customize This
using the ``--pagination`` flag.

Preserve EXIF orientation
-------------------------
More often than not, the correct orientation of an image is stored in its
EXIF data. SHIS will honor the EXIF orientation (if present) in an image and
rotate it accordingly. This means you no longer have to worry about rotating
images anymore.

Determines public IP
--------------------
In a scenario where you're running SHIS on a remove VM such as EC2, it's
helpful to know the public IP of the server. SHIS tries to determine the
public IP of your machine, and displays that address whenever possible.
This means you no longer have to remember the public IP of your server.

Selection support
-----------------
SHIS makes it easier to visually filter images by adding a *Selection Mode*,
which can be enabled using the ``-s`` or ``--selection`` flags. After you
enable selection mode, you can select images on the website the same way
you'd do in a file explorer. Once you have selected images, click *Copy* on
the top right of the page, and all file names will be copied to a clipboard.
You can then paste these file names in a text file or a terminal, and use
the filtered file names to move or delete files. As an example, if you paste
all file names to ``files.txt`` and you want to copy those files to another
folder, you can simply use ``cat files.txt | xargs -i cp src/{} dest/`` on
a unix based system.

Watch filesystem for changes
----------------------------
SHIS can continously scan the filesystem for any changes and automatically
update the contents of the website. To enable this functionality, simply
use the ``-w`` or the ``--watch`` flags. By default, SHIS will scan the
filesystem for changes every 30 seconds. You can specify the scanning
interval (in seconds) right after the watch flag. For example, ``-w 15``
sets the watch interval as 15 seconds.
