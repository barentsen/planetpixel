"""Rough Python client to access the Planet Orders API.

Most of the code in this module is borrowed from `planetlabs/notebooks/orders`.
"""
import json
import os
import pathlib
import time
import logging
import requests


orders_url = 'https://api.planet.com/compute/ops/orders/v2'


def place_order(request, auth, headers={'content-type': 'application/json'}):
    response = requests.post(orders_url, data=json.dumps(request), auth=auth, headers=headers)
    logging.debug(response)
    
    if not response.ok:
        raise Exception(response.content)

    order_id = response.json()['id']
    logging.debug(order_id)
    order_url = orders_url + '/' + order_id
    return order_url


def poll_for_success(order_url, auth, num_loops=50000):
    count = 0
    while(count < num_loops):
        count += 1
        r = requests.get(order_url, auth=auth)
        response = r.json()
        state = response['state']
        logging.debug(state)
        success_states = ['success', 'partial']
        if state == 'failed':
            raise Exception(response)
        elif state in success_states:
            break

        time.sleep(100)


def download_order(order_url, auth, destination="/tmp/data/", overwrite=False):
    r = requests.get(order_url, auth=auth)
    logging.debug(r)

    response = r.json()
    results = response['_links']['results']
    results_urls = [r['location'] for r in results]
    results_names = [r['name'] for r in results]
    results_paths = [pathlib.Path(os.path.join(destination, n)) for n in results_names]
    logging.debug('{} items to download'.format(len(results_urls)))

    for url, name, path in zip(results_urls, results_names, results_paths):
        if overwrite or not path.exists():
            logging.debug('downloading {} to {}'.format(name, path))
            r = requests.get(url, allow_redirects=True)
            path.parent.mkdir(parents=True, exist_ok=True)
            open(path, 'wb').write(r.content)
        else:
            logging.debug('{} already exists, skipping {}'.format(path, name))
 
    return dict(zip(results_names, results_paths))
