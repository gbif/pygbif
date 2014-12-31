import sys
import requests
import json
from simplejson import JSONDecodeError

class NoResultException(Exception):
    pass

def occ_search(taxonKey, per_page=5, page=1, **kwargs):
  '''
  Search for occurrences

  :param x: xxx

  Usage:
  # Search by species name, using \code{\link{name_backbone}} first to get key
  (key = name_suggest(q='Helianthus annuus', rank='species')$key[1])
  occ_search(taxonKey=key, limit=2)

  # Return 20 results, this is the default by the way
  occ_search(taxonKey=key, limit=20)

  # Return just metadata for the search
  occ_search(taxonKey=key, limit=100, return='meta')
  '''
  url = baseurl + 'occurrence/search'
  out = requests.get(url, params = {'taxonKey': taxonKey, 'per_page': per_page, 'page': page})
  out.raise_for_status()
  return out.json()

# helper fxns
baseurl = "http://api.gbif.org/v1/"

if __name__ == "__main__":
    import doctest
    doctest.testmod()
