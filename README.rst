PlanetPixel
===========

**A simple API for retrieving time series color data using the Planet API.**

*(Because API's don't have to be complicated!)*

Purpose
-------
*PlanetPixel* makes it fun and easy to plot the color of a single position on Earth as a function of time.  For example, you can use it to measure when a lake in Yosemite froze in the winter of 2017:

.. code-block:: python

  from planetpixel import PlanetPixel
  PlanetPixel(lon, lat).plot()

*PlanetPixel* was created at the first public Planet Labs Hack Day on October 14th, 2019, in San Francisco, out of frustration with Planet's standard (complicated) API!

Pre-requisites
--------------

You need to set your Planet Labs API key as the ``PL_API_KEY`` environment variable for this package to work.
