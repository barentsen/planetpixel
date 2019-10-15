PlanetPixel
===========

**A simple API for retrieving time series color data using the Planet API.**

*(Because API's don't have to be complicated!)*

Example
-------
*PlanetPixel* makes it fun and easy to plot the color of a single position on Earth as a function of time.  For example, you can use it to measure when Matthes lake in Yosemite froze in the winter of 2017:

|pic1| |pic2|

.. |pic1| image:: https://github.com/barentsen/planetpixel/blob/master/demo/lake1.png
   :width: 35%

.. |pic2| image:: https://github.com/barentsen/planetpixel/blob/master/demo/lake2.png
   :width: 35%

We can study this in a quantitative way as follows:

.. image:: https://github.com/barentsen/planetpixel/blob/master/demo/planetpixel-demo.png

*PlanetPixel* was created at the first public Planet Labs Hack Day on October 14th, 2019, in San Francisco, out of frustration with Planet's standard (complicated) API!


Installation
------------

.. code-block:: bash

  pip install planetpixel


Usage
-----

.. code-block:: python

  from planetpixel import PlanetPixel
  PlanetPixel(lon, lat).plot()


Caveat
------

Right now, the example above takes >10 minutes to run. 😬



Pre-requisites
--------------
You need to set your Planet Labs API key as the ``PL_API_KEY`` environment variable for this package to work.
