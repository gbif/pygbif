import sys
import requests
import json
from simplejson import JSONDecodeError
from gbifutils import *

class NoResultException(Exception):
    pass

def search(taxonKey, limit=5, offset=1, **kwargs):
  '''
  Search for occurrences

  :param x: xxx

  Usage:
  # Search by species name, using `name_backbone()` to get key
  key = pygbif.name_suggest(q='Helianthus annuus', rank='species')['key']
  pygbif.search(taxonKey=key, limit=2)

  # Return 20 results, this is the default by the way
  pygbif.search(taxonKey=key, limit=20)

  # Return just metadata for the search
  pygbif.search(taxonKey=key, limit=100, return='meta')
  '''
  url = baseurl + 'occurrence/search'
  return gbif_GET(url, {'taxonKey': taxonKey, 'limit': limit, 'offset': offset}, **kwargs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
