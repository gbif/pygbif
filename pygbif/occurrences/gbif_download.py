"""
Name:   GBIF_download
Author: Jan K. Legind, Global Biodiversity Information Facility (GBIF), 2016-05-26
Enables users to launch user_downloads against the GBIF API http://www.gbif.org/developer/occurrence#download
Requires a user account on GBIF.org since credentials are needed.
Two patterns are supported: Searching by n taxonkeys, or searching by n taxonkeys and a polygon
The main function run_download() does not return any value since the download is handled entirely in the GBIF domain.
"""

import requests
import json
import csv
import datetime

url = 'http://api.gbif.org/v1/occurrence/download/request'
header = {'Content-Type': 'application/json'}
values = []
payload = {'creator': None, 'notification_address': [None], 'send_notification': 'true', 'created': None,
           'predicate': {
           'type': 'and',
           'predicates': []
            }
           }
geom = {'type': 'within', 'geometry': None}
species = {'type': 'or', 'predicates': None}
predicate_construct = {'type': 'equals', 'key': 'TAXON_KEY', 'value': None}
#These JSON variables can be overwritten to support other user download queries


def run_download(readfile, payload, creator, email, credentials, polygon=None, predicate=None):
    """Serves as exe function. Extracts the keys from the readfile to a list and prepares the species JSON.
    :param readfile: File containing the taxon keys to be searched.
    :param payload: Initial JSON template.
    :param creator: User name.
    :param email: -
    :param credentials: Username and passw0rd tuple.
    :param polygon: In this format 'POLYGON((x1 y1, x2 y2, x3 y3,... xn yn))'
    :param predicate: Default None. Can be used to override the preds_construct.
    """
    with open(readfile) as ff:
        reading = csv.reader(ff)
        for j in reading:
            values.append(j[0])
    if predicate is None:
        preds_construct = predicate_construct
    else:
        preds_construct = predicate
    print preds_construct
    p = make_predicate(preds_construct, values)
    print p
    pay = make_payload(payload, creator, email, p, polygon)
    print pay
    requests.post(url, auth=credentials, data=json.dumps(pay), headers=header)


def make_predicate(predicate, values, key='value'):
    """Creates all the individual predicates in JSON format.
    :param predicate: a dict
    :param values: List of all the values
    :param key: The key for the values
    :return: List of dicts
    """
    preds = []
    while values:
        predicate[key] = values.pop()
        preds.append(predicate.copy())
    return preds


def make_payload(payload, creator, email, predicate, polygon=None):
    """Creates the finished JSON payload going into the API call.
    :param payload: JSON template
    :return: Prepared JSON for the API call
    """
    payload["creator"] = creator
    payload["created"] = datetime.date.today().year
    payload["notification_address"][0] = email
    if polygon is None:
        print 'poly is NONE!'
        payload["predicate"]["type"] = 'or'
        for j in predicate:
            payload["predicate"]["predicates"].append(j)
    else:
        geom["geometry"] = polygon
        payload["predicate"]["predicates"].append(geom)
        species["predicates"] = predicate
        payload["predicate"]["predicates"].append(species)
    return payload
