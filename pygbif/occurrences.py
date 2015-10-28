import sys
import requests
import json
from simplejson import JSONDecodeError
from gbifutils import *

base_url = "http://api.gbif.org/v1/"

def search(taxonKey, limit=5, offset=1, **kwargs):
    '''
    Search GBIF occurrences

    :param taxonKey: [Fixnum] A GBIF occurrence identifier
    :param limit: [Fixnum] Number of results to return.
    :param offset: [Fixnum] Start at record X

    :return: Object response class, light wrapper around a dict

    Usage
    >>> from pygbif import occurrences
    >>> occurrences.search(taxonKey = 3329049)
    '''
    url = base_url + 'occurrence/search'
    out = gbif_GET(url, {'taxonKey': taxonKey, 'limit': limit, 'offset': offset}, **kwargs)
    return out

def get(taxonKey, fragment = False, verbatim = False, **kwargs):
    '''
    Search GBIF occurrences

    :param key: [Fixnum] A GBIF occurrence key
    :param fragment: [Fixnum] get fragment
    :param verbatim: [Fixnum] get verbatim

    :return: Object response class, light wrapper around a dict

    Usage
    >>> from pygbif import occurrences
    >>> occurrences.get(taxonKey = 252408386)
    '''
    url = base_url + 'occurrence/' + str(taxonKey)
    out = gbif_GET(url, {}, **kwargs)
    return out

# class Occ(object):
#     '''
#     Occ: occurrences search class
#     '''
#     def __init__(self, base_url = "http://api.gbif.org/v1/", taxonKey = None, limit = 5, offset = 1, **kwargs):
#         self.base_url = base_url
#         self.taxonKey = taxonKey
#         self.limit = limit
#         self.offset = offset

#     def search(self, taxonKey = None, limit=5, offset=1, **kwargs):
#         '''
#         Search GBIF occurrences

#         :param taxonKey: [Fixnum] A GBIF occurrence identifier
#         :param limit: [Fixnum] Number of results to return.
#         :param offset: [Fixnum] Start at record X

#         :return: Object response class, light wrapper around a dict

#         Usage
#         >>> from pygbif import Occ
#         >>> oc = Occ()
#         >>> oc.search(taxonKey = 412651381)
#         '''
#         url = self.base_url + 'occurrence/search'
#         out = gbif_GET(url, {'taxonKey': taxonKey, 'limit': limit, 'offset': offset}, **kwargs)
#         return out
