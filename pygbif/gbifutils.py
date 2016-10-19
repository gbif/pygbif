import requests
import pygbif

class NoResultException(Exception):
    pass

def gbif_search_GET(url, args, **kwargs):
  # if args['geometry'] != None:
  #   if args['geometry'].__class__ == list:
  #     b = args['geometry']
  #     args['geometry'] = geometry.box(b[0], b[1], b[2], b[3]).wkt
  out = requests.get(url, params=args, **kwargs)
  out.raise_for_status()
  stopifnot(out.headers['content-type'])
  return out.json()

def gbif_GET(url, args, **kwargs):
  out = requests.get(url, params=args, headers=make_ua(), **kwargs)
  out.raise_for_status()
  stopifnot(out.headers['content-type'])
  return out.json()

def gbif_GET_write(url, path, **kwargs):
  out = requests.get(url, headers=make_ua(), stream=True, **kwargs)
  ctype = 'application/octet-stream; qs=0.5'
  if out.headers['content-type'] != ctype:
    raise NoResultException("content-type did not = '%s'" % ctype)
  if out.status_code == 200:
    with open(path, 'wb') as f:
      for chunk in out.iter_content(chunk_size = 1024):
        if chunk:
          f.write(chunk)
  return path

def gbif_POST(url, body, **kwargs):
  head = make_ua()
  out = requests.post(url, json=body, headers=head, **kwargs)
  out.raise_for_status()
  stopifnot(out.headers['content-type'])
  return out.json()

def stopifnot(x):
  if x != 'application/json':
    raise NoResultException("content-type did not = application/json")

def stop(x):
  raise ValueError(x)

def make_ua():
  return {'user-agent': 'python-requests/' + requests.__version__ + ',pygbif/' + pygbif.__version__}

def is_none(x):
  return x.__class__.__name__ == 'NoneType'

def is_not_none(x):
  return x.__class__.__name__ != 'NoneType'

gbif_baseurl = "http://api.gbif.org/v1/"

requests_argset = ['timeout', 'cookies', 'auth', 'allow_redirects',
                    'proxies', 'verify', 'stream', 'cert']

def bn(x):
  if x:
    return x
  else:
    return None

def parse_results(x, y):
  if y.__class__.__name__ != 'NoneType':
    if y.__class__ != dict:
      return x
    else:
      if 'endOfRecords' in x.keys():
        return x['results']
      else:
        return x
  else:
    return x['results']

def check_data(x,y):
  if len2(x) == 1:
    testdata = [x]
  else:
    testdata = x

  for z in testdata:
    if z not in y:
      raise TypeError(z + ' is not one of the choices')


def len2(x):
  if x.__class__ is str:
    return len([x])
  else:
    return len(x)

def get_meta(x):
  if has_meta(x):
    return { z: x[z] for z in ['offset','limit','endOfRecords'] }
  else:
    return None

def has_meta(x):
  if x.__class__ != dict:
    return False
  else:
    tmp = [y in x.keys() for y in ['offset','limit','endOfRecords']]
    return True in tmp
