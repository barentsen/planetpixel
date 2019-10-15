"""Defines the PlanetPixel class."""
import math
from datetime import datetime
from requests.auth import HTTPBasicAuth

import matplotlib.pyplot as pl
import numpy as np
import seaborn as sns
import matplotlib.dates as mdates

from planet import api
from gdal import Open

from . import orders, PL_API_KEY


PLANET_BANDS = {'blue': 1, 'green': 2, 'red': 3, 'nir': 4}


def get_median(data, band='blue'):
    """Returns the median of a band in a Planet GeoTIFF."""
    band_idx = PLANET_BANDS[band]
    dn = data.GetRasterBand(band_idx).ReadAsArray()
    return dn[int(dn.shape[1]/2), int(dn.shape[0]/2)]
    #return np.nanmedian(dn[dn > 0])


def get_geometry(lon, lat, size):
    """Returns a geo json geometry.
    
    Give lon, lat, and size in degrees.
    """
    geo_json_geometry = {
      "type": "Polygon",
      "coordinates": [
        [
          [lon-size/2, lat-size/2],
          [lon-size/2, lat+size/2],
          [lon+size/2, lat+size/2],
          [lon+size/2, lat-size/2],
          [lon-size/2, lat-size/2]
        ]
      ]
    }
    return geo_json_geometry


def get_item_ids(client, geo_json_geometry, start="2017-11-01T00:00:00.000Z",
                 stop="2017-11-15T00:00:00.000Z", limit=10):
    """Returns a list of planet item_id's given a geometry."""

    # filter for items the overlap with our chosen geometry
    geometry_filter = {
        "type": "GeometryFilter",
        "field_name": "geometry",
        "config": geo_json_geometry
    }

    # filter images acquired in a certain date range
    date_range_filter = {
       "type": "DateRangeFilter",
       "field_name": "acquired",
       "config": {
          "gte": start,
          "lte": stop
      }
    }

    # filter any images which are more than 50% clouds
    cloud_cover_filter = {
      "type": "RangeFilter",
      "field_name": "cloud_cover",
      "config": {
        "lte": 0.4
      }
    }

    # create a filter that combines our geo and date filters
    # could also use an "OrFilter"
    myfilter = {
      "type": "AndFilter",
      "config": [geometry_filter, date_range_filter, cloud_cover_filter]
    }
    
    item_types = ['PSScene4Band']
    request = api.filters.build_search_request(myfilter, item_types)
    results = client.quick_search(request, page_size=limit)
    items = [r['id'] for r in results.items_iter(limit)]
    return items


class PlanetPixel():
    """Download Planet data for a single position on Earth.

    Give longitude and latitude in degrees.
    """
    def __init__(self, lon, lat, start="2017-10-15T00:00:00.000Z",
                 stop="2018-02-01T00:00:00.000Z", size=10., limit=100,
                 download_dir="/tmp/data"):
        self.longitude = lon
        self.latitude = lat
        self.start = start
        self.stop = stop
        self.size = size  # must be in meter
        self.limit = limit
        self.download_dir = download_dir
        self._files = self._download()

    def _download(self):
        """Downloads the clipped images using the Planet Orders API."""
        client = api.ClientV1(api_key=PL_API_KEY)
        mysize = self.size / (111000.*math.cos(math.radians(self.latitude)))
        geom1 = get_geometry(self.longitude, self.latitude, mysize)
        
        item_ids = get_item_ids(client, geom1, start=self.start,
                                stop=self.stop, limit=self.limit)
        #print("Clipping from {} items.".format(len(item_ids)))

        geom2 = get_geometry(self.longitude, self.latitude, 20*mysize)
        self._clip_request_json = self._get_clip_request(item_ids, geom2)
       
        auth = HTTPBasicAuth(PL_API_KEY, '')
        clip_order_url = orders.place_order(self._clip_request_json, auth)
        orders.poll_for_success(clip_order_url, auth)
        downloaded_clip_files = orders.download_order(clip_order_url, auth,
                                                      destination=self.download_dir)
        return downloaded_clip_files

    def _get_clip_request(self, item_ids, geometry):
        clip = {
            "clip": {
                "aoi": geometry
            }
        }
        products = [{
            "item_ids": item_ids,
            "item_type": "PSScene4Band",
            "product_bundle": "analytic"
        }]
        clip_request = {
            "name": "just clip",
            "products": products,
            "tools": [clip]
        }
        return clip_request

    def get_timeseries(self):
        images = [str(pth) for pth in self._files.values()
                  if str(pth).endswith('AnalyticMS_clip.tif')]
        times, ratios = [], []
        for img in images:
            data = Open(img)
            ratio = get_median(data, "blue") / get_median(data, "red")
            ratios.append(ratio)
            time = datetime.strptime(data.GetMetadata_Dict()['TIFFTAG_DATETIME'], "%Y:%m:%d %H:%M:%S")
            times.append(time)
        return times, ratios

    def plot(self):
        time, ratio = self.get_timeseries()
        sns.set_style("whitegrid")
        sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
        pl.figure(figsize=(8, 4.5))
        ax = pl.scatter(time, ratio, s=15, marker='o', color='black')
        pl.ylabel("Blue / Red light ratio")
        pl.gca().xaxis.set_major_locator(mdates.MonthLocator())
        return ax
