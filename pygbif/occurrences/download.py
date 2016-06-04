from ..gbifutils import *
import os
from requests import auth

# def download(*arg, type="and", user = ENV("GBIF_USER"), pwd = ENV("GBIF_PWD"),
#    email, **kwargs):
#    '''
#    Spin up a download request for GBIF occurrence data.

#    :param ...: One or more of query arguments to kick of a download job. See Details.
#    :param type: (charcter) One of equals (=), and (&), or (|), lessThan (<), lessThanOrEquals (<=),
#     greaterThan (>), greaterThanOrEquals (>=), in, within, not (!), like
#    :param user: (character) User name within GBIF's website. Required. Set in your env
#     vars with the option `GBIF_USER`
#    :param pwd: (character) User password within GBIF's website. Required. Set in your env
#     vars with the option `GBIF_PWD`
#    :param email: (character) Email address to recieve download notice done email. Required.
#     Set in your env vars with the option `GBIF_EMAIL`
#    :param **kwargs: Further named arguments passed on to `requests.post`

#     Argument passed have to be passed as character (e.g., 'country = US'), with a space
#     between key ('country'), operator ('='), and value ('US'). See the `type` parameter for
#     possible options for the operator.  This character string is parsed internally.

#     Acceptable arguments to `...` are:

#      - taxonKey = 'TAXON_KEY'
#      - scientificName = 'SCIENTIFIC_NAME'
#      - country = 'COUNTRY'
#      - publishingCountry = 'PUBLISHING_COUNTRY'
#      - hasCoordinate = 'HAS_COORDINATE'
#      - hasGeospatialIssue = 'HAS_GEOSPATIAL_ISSUE'
#      - typeStatus = 'TYPE_STATUS'
#      - recordNumber = 'RECORD_NUMBER'
#      - lastInterpreted = 'LAST_INTERPRETED'
#      - continent = 'CONTINENT'
#      - geometry = 'GEOMETRY'
#      - basisOfRecord = 'BASIS_OF_RECORD'
#      - datasetKey = 'DATASET_KEY'
#      - eventDate = 'EVENT_DATE'
#      - catalogNumber = 'CATALOG_NUMBER'
#      - year = 'YEAR'
#      - month = 'MONTH'
#      - decimalLatitude = 'DECIMAL_LATITUDE'
#      - decimalLongitude = 'DECIMAL_LONGITUDE'
#      - elevation = 'ELEVATION'
#      - depth = 'DEPTH'
#      - institutionCode = 'INSTITUTION_CODE'
#      - collectionCode = 'COLLECTION_CODE'
#      - issue = 'ISSUE'
#      - mediatype = 'MEDIA_TYPE'
#      - recordedBy = 'RECORDED_BY'

#     See the API docs http://www.gbif.org/developer/occurrence#download for
#     more info, and the predicates docs http://www.gbif.org/developer/occurrence#predicates

#     :return: A dictionary, of results

#     Usage::

#         from pygbif import occurrences as occ
#         occ.download(args = ["basisOfRecord = LITERATURE", 'decimalLatitude > 50'])
#         occ.download(args = ['decimalLatitude > 50'])

#         occ.download("basisOfRecord = LITERATURE")
#         occ.download('taxonKey = 3119195')
#         occ.download('decimalLatitude > 50')
#         occ.download('elevation >= 9000')
#         occ.download('decimalLatitude >= 65')
#         occ.download("country = US")
#         occ.download("institutionCode = TLMF")
#         occ.download("catalogNumber = Bird.27847588")

#         res = occ.download('taxonKey = 7264332', 'hasCoordinate = TRUE')

#         # pass output to download_meta for more information
#         occ.download_meta(occ.download('decimalLatitude > 75'))

#         # Multiple queries
#         gg = occ.download('decimalLatitude >= 65', 'decimalLatitude <= -65', type="or")
#         gg = occ.download('depth = 80', 'taxonKey = 2343454', type="or")
#     '''
#     url = gbif_baseurl + 'occurrence/download/request'

#     user = os.environ["GBIF_USER"]
#     pwd = os.environ["GBIF_PWD"]
#     email = os.environ["GBIF_EMAIL"]

#     keyval = [ parse_args(z) for z in args ]

#     if len(keyval) > 1:
#       req = {'creator': user,
#            'notification_address': email,
#            'predicate': {'type': type, 'predicates': keyval}}
#     else:
#       if type == "within" or "within" in [ s['type'] for s in keyval ]:
#         req = {'creator': user,
#              'notification_address': email,
#              'predicate': {
#                'type': keyval[0]['type'],
#                'value': keyval[0]['value']
#              }}
#         req['predicate'][keyval[0]['key'].lower()] = req['predicate'].pop('value')
#       else:
#         req = {'creator': user,
#            'notification_address': email,
#            'predicate': {
#               'type': keyval[0]['type'],
#               'key': keyval[0]['key'],
#               'value': keyval[0]['value']}}

#     out = rg_POST(url, req, user, pwd, **kwargs)
#     return [out, user, email]

def download_meta(key, **kwargs):
  '''
  Retrieves the occurrence download metadata by its unique key.

  :param key: [str] A key generated from a request, like that from `download`
  :param **kwargs: Further named arguments passed on to `requests.get`

  Usage::

      from pygbif import occurrences as occ
      occ.download_meta(key = "0003970-140910143529206")
      occ.download_meta(key = "0000099-140929101555934")
  '''
  url = 'http://api.gbif.org/v1/occurrence/download/' + key
  return gbif_GET(url, {}, **kwargs)

def download_list(user=None, pwd=None, limit = 20, start = 0, **kwargs):
  '''
  Lists the downloads created by a user.

  :param user: [str] A user name, look at env var "GBIF_USER" first
  :param pwd: [str] Your password, look at env var "GBIF_PWD" first
  :param limit: [int] Number of records to return. Default: 20
  :param start: [int] Record number to start at. Default: 0
  :param **kwargs: Further named arguments passed on to `requests.get`

  Usage::

      from pygbif import occurrences as occ
      occ.download_list(user = "sckott")
      occ.download_list(user = "sckott", limit = 5)
      occ.download_list(user = "sckott", start = 21)
  '''
  if is_none(user):
    user = os.environ.get('GBIF_USER')
    if is_none(user):
      stop('user not supplied and no entry for GBIF_USER')

  if is_none(pwd):
    pwd = os.environ.get('GBIF_PWD')
    if is_none(pwd):
      stop('pwd not supplied and no entry for GBIF_PWD')

  url = 'http://api.gbif.org/v1/occurrence/download/user/' + user
  args = {'limit': limit, 'offset': start}
  res = gbif_GET(url, args, auth=(user, pwd))
  return {'meta': {'offset': res['offset'], 'limit': res['limit'],
    'endofrecords': res['endOfRecords'], 'count': res['count']},
   'results': res['results']}

def download_get(key, path=".", overwrite=False, **kwargs):
  '''
  Get a download from GBIF.

  :param key: [str] A key generated from a request, like that from `download`
  :param path: [str] Path to write zip file to. Default: `"."`, with a `.zip`
    appended to the end.
  :param **kwargs: Further named arguments passed on to `requests.get`

  Downloads the zip file to a directory you specify on your machine.
  We stream the zip data to a file. This function only downloads the file.
  See `download_import` to open a downloaded file in Python. The speed of this
  function is of course proportional to the size of the file to download, and affected
  by your internet connection speed. For example, a 58 MB file on my machine took
  about 26 seconds.

  Usage::

    from pygbif import occurrences as occ
    occ.download_get("0000066-140928181241064")
    occ.download_get("0003983-140910143529206")
  '''
  meta = pygbif.occurrences.download_meta(key)
  if meta['status'] != 'SUCCEEDED':
    raise Exception('download "%s" not of status SUCCEEDED' % key)
  else:
    print('Download file size: %s bytes' % meta['size'])
    url = 'http://api.gbif.org/v1/occurrence/download/request/' + key
    path = "%s/%s.zip" % (path, key)
    res = gbif_GET_write(url, path, **kwargs)
    # options(gbifdownloadpath = path)
    print( "On disk at " + path )
    return {'path': path, 'size': meta['size'], 'key': key}


# helper functions
def rg_POST(url, req, user, pwd, **kwargs):
  heads = {'accept': 'application/json',
    'content-type': 'application/json',
    'user-agent': 'python-requests/' + requests.__version__ + ',pygbif/' + pygbif.__version__
  }
  r = requests.post(url, data = json.dumps(req), headers = heads, auth = auth.HTTPBasicAuth(user, pwd))
  if r.status_code > 203:
    raise Exception('error: ' + r.content)
  if r.headers()['Content-Type'] == 'application/json':
    raise Exception('not of type json')

  return r.json()

# def rg_POST(url, req, user, pwd, callopts):
#   tmp = requests.post(url, config = c(
#     content_type_json(),
#     accept_json(),
#     authenticate(user = user, password = pwd),
#     callopts), body = jsonlite::toJSON(req),
#     make_rgbif_ua())
#   if (tmp$status_code > 203) stop(content(tmp, as = "text"), call. = FALSE)
#   stopifnot(tmp$header$`content-type` == 'application/json')
#   content(tmp, as = "text")

# print.download = function(x, ...) {
#   stopifnot(is(x, 'download'))
#   cat("<<gbif download>>", "\n", sep = "")
#   cat("  Username: ", attr(x, "user"), "\n", sep = "")
#   cat("  E-mail: ", attr(x, "email"), "\n", sep = "")
#   cat("  Download key: ", x, "\n", sep = "")
# }

def parse_args(x):
  tmp = re.split('\s', x)
  type = operator_lkup.get(tmp[1])
  key = key_lkup.get(tmp[0])
  return {'type': type, 'key': key, 'value': tmp[2]}

operator_lkup = {'=': 'equals', '&': 'and', '|': 'or',
    '<': 'lessThan', '<=': 'lessThanOrEquals', '>': 'greaterThan',
    '>=': 'greaterThanOrEquals', '!': 'not',
    'in': 'in', 'within': 'within', 'like': 'like'}

key_lkup = {'taxonKey': 'TAXON_KEY', 'scientificName': 'SCIENTIFIC_NAME', 'country': 'COUNTRY',
     'publishingCountry': 'PUBLISHING_COUNTRY', 'hasCoordinate': 'HAS_COORDINATE',
     'hasGeospatialIssue': 'HAS_GEOSPATIAL_ISSUE', 'typeStatus': 'TYPE_STATUS',
     'recordNumber': 'RECORD_NUMBER', 'lastInterpreted': 'LAST_INTERPRETED', 'continent': 'CONTINENT',
     'geometry': 'GEOMETRY', 'basisOfRecord': 'BASIS_OF_RECORD', 'datasetKey': 'DATASET_KEY',
     'eventDate': 'EVENT_DATE', 'catalogNumber': 'CATALOG_NUMBER', 'year': 'YEAR', 'month': 'MONTH',
     'decimalLatitude': 'DECIMAL_LATITUDE', 'decimalLongitude': 'DECIMAL_LONGITUDE', 'elevation': 'ELEVATION',
     'depth': 'DEPTH', 'institutionCode': 'INSTITUTION_CODE', 'collectionCode': 'COLLECTION_CODE',
     'issue': 'ISSUE', 'mediatype': 'MEDIA_TYPE', 'recordedBy': 'RECORDED_BY'}
