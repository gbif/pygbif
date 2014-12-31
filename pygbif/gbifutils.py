import requests
from simplejson import JSONDecodeError

class NoResultException(Exception):
    pass

def gbif_GET(url, args, **kwargs):
  out = requests.get(url, params=args, **kwargs)
  out.raise_for_status()
  stopifnot(out.headers['content-type'])
  return out.json()

def stopifnot(x):
	if x != 'application/json':
		raise NoResultException("content-type did not = application/json")

baseurl = "http://api.gbif.org/v1/"
