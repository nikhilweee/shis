.. shis documentation master file, created by
   sphinx-quickstart on Wed Oct 21 23:14:10 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Simple HTTP Image Server
========================

SHIS is a drop in replacement for ``python -m http.server``, albeit for 
images. It lets you quickly and conveniently browse through image directories
directly in your browser.

.. toctree::
   :hidden:
   :maxdepth: 1

   usage
   features
   api


Quickstart
**********

First, make sure you have ``shis`` installed. ::

   $ pip install shis

Next, navigate to a directory containing images. ::

   $ cd directory/containing/images

Finally, run ``shis.server`` the same way you'd run ``http.server`` ::

   $ python -m shis.server
   # Serving HTTP on 0.0.0.0 port 7447. Press CTRL-\ (SIGQUIT) to quit.
   # Processing images from : directory/containing/images
   # Creating thumbnails in : directory/containing/images/shis
   # Generating Website     : 100%|████████████████████| 2/2 [00:00<00:00, 35.09it/s]
   # Generating Thumbnails  : 100%|███████████████| 120/120 [00:00<00:00, 132.48it/s]

There. You should now be able to view the images at ``http://0.0.0.0:7447/``
For more information on advanced usage, please see :doc:`usage`. For a list of 
features, please see :doc:`features`.
