.. shis documentation master file, created by
   sphinx-quickstart on Wed Oct 21 23:14:10 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SHIS
====

**S**\imple **H**\TTP **I**\mage **S**\erver (or SHIS for short) is a drop in
replacement for ``python -m http.server``, albeit for images. It lets you
quickly and conveniently browse through image directories directly in your
browser.

.. toctree::
   :hidden:
   :maxdepth: 1

   self
   features
   usage
   api


Quickstart
**********

First, make sure you have ``shis`` installed. ::

   $ pip install shis

Next, navigate to a directory containing images. ::

   $ cd directory/containing/images

Finally, run ``shis.server`` the same way you'd run ``http.server`` ::

   $ python -m shis.server
   # Serving HTTP on 0.0.0.0:7447. Press CTRL-C to quit.
   # Processing images from : directory/containing/images
   # Creating thumbnails in : directory/containing/images/shis
   # Generating Website     : 100%|████████████████████|     4/    4 [00:00<00:00,  49.82it/s]
   # Generating Thumbnails  : 100%|████████████████████|   300/  300 [00:00<00:00,  1.47kit/s]

There. You should now be able to view images at ``http://0.0.0.0:7447/``.
For more information on advanced usage, please see :doc:`usage`. For a list of 
features, head over to :doc:`features`. A live preview is also available at
`nikhilweee.github.io/shis <https://nikhilweee.github.io/shis/>`_.
