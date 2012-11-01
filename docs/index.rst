.. Shimehari-DebugToolbar documentation master file, created by
   sphinx-quickstart on Wed Feb 15 18:08:39 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Shimehari-DebugToolbar's documentation!
==============================================

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


Configuration
-------------

The toolbar support several configuration options:

====================================  =====================================   ==========================
Name                                  Description                             Default
====================================  =====================================   ==========================
``DEBUG_TB_ENABLED``                  Enable the toolbar?                     ``app.debug``
``DEBUG_TB_HOSTS``                    Whitelist of hosts to display toolbar   any host
``DEBUG_TB_INTERCEPT_REDIRECTS``      Should intercept redirects?             ``True``
``DEBUG_TB_PANELS``                   List of module/class names of panels    enable all built-in panels
``DEBUG_TB_PROFILER_ENABLED``         Enable the profiler on all requests     ``False``, user-enabled
``DEBUG_TB_TEMPLATE_EDITOR_ENABLED``  Enable the template editor              ``False``
====================================  =====================================   ==========================

To change one of the config options, set it in the Shimehari app's config like::

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


Contributing
------------

Fork us `on GitHub <https://github.com/matsumos/shimehari-debugtoolbar>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

