import sys
import requests
import json
from simplejson import JSONDecodeError
from gbifutils import *

class Occ(object):
    '''
    Occ: occurrences search class
    '''
    def __init__(self, base_url = "http://api.gbif.org/v1/", taxonKey, limit=5, offset=1, **kwargs):
        self.base_url = base_url
        self.taxonKey = taxonKey
        self.limit = limit
        self.offset = offset

    def search2(self, taxonKey, limit=5, offset=1, **kwargs):
        '''
        Search GBIF occurrences

        :param taxonKey: [Fixnum] A GBIF occurrence identifier
        :param limit: [Fixnum] Number of results to return.
        :param offset: [Fixnum] Start at record X

        :return: Object response class, light wrapper around a dict

        Usage
        >>> from pygbif import Occ
        >>> Occ.search()
        >>> Occ.search(ids = '10.1371/journal.pone.0033693')
        >>> x = Occ.search(query = "ecology")
        >>> x.status()
        '''
        url = self.base_url + 'occurrence/search'
        out = gbif_GET(url, {'taxonKey': taxonKey, 'limit': limit, 'offset': offset}, **kwargs)
        return out
