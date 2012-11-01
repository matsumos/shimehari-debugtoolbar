Shimehari Debug-toolbar
===================

This is a port of the excellent `django-debug-toolbar <https://github.com/django-debug-toolbar/django-debug-toolbar>`_
for Shimehari applications.


Installation
------------

Installing is simple with pip::

    $ pip install shimehari-debugtoolbar


Usage
-----

Setting up the debug toolbar is simple::

    from shimehari import Shimehari
    from shimehari_debugtoolbar import DebugToolbarExtension

    app = Shimehari(__name__)

    toolbar = DebugToolbarExtension(app)


The toolbar will automatically be injected into Jinja templates when debug mode is on.

See the `documentation`_ for more information.

.. _documentation: http://shimehari-debugtoolbar.readthedocs.org
