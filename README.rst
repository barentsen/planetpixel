PlanetPixel
===========

**A simple API for retrieving time series color data using the Planet API.**

*(Because API's don't have to be complicated! 😬)*

Summary
-------
*PlanetPixel* makes it fun and easy to plot the color of a single position on Earth as a function of time.  For example, you can use it to measure when Matthes lake in Yosemite froze in the winter of 2017:

.. image:: https://github.com/barentsen/planetpixel/blob/master/demo/planetpixel-demo.png

*PlanetPixel* was created at the first public Planet Labs Hack Day on October 14th, 2019, in San Francisco, out of frustration with Planet's standard (complicated) API!

Installation
------------

.. code-block:: bash

  python setup.py install


Usage
-----

.. code-block:: python

  from planetpixel import PlanetPixel
  PlanetPixel(lon, lat).plot()


Pre-requisites
--------------

You need to set your Planet Labs API key as the ``PL_API_KEY`` environment variable for this package to work.
