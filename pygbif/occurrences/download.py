from ..gbifutils import *
import os
from requests import auth

def occ_download(*arg,
   type = "and", user = ENV("GBIF_USER"), pwd = ENV("GBIF_PWD"),
   email, **kwargs):
   '''
   Spin up a download request for GBIF occurrence data.

   :param ...: One or more of query arguments to kick of a download job. See Details.
   :param type: (charcter) One of equals (=), and (&), or (|), lessThan (<), lessThanOrEquals (<=),
    greaterThan (>), greaterThanOrEquals (>=), in, within, not (!), like
   :param user: (character) User name within GBIF's website. Required. Set in your env
    vars with the option `GBIF_USER`
   :param pwd: (character) User password within GBIF's website. Required. Set in your env
    vars with the option `GBIF_PWD`
   :param email: (character) Email address to recieve download notice done email. Required.
    Set in your env vars with the option `GBIF_EMAIL`
   :param **kwargs: Further named arguments passed on to `requests.post`

    Argument passed have to be passed as character (e.g., 'country = US'), with a space
    between key ('country'), operator ('='), and value ('US'). See the `type` parameter for
    possible options for the operator.  This character string is parsed internally.

    Acceptable arguments to `...` are:

     - taxonKey = 'TAXON_KEY'
     - scientificName = 'SCIENTIFIC_NAME'
     - country = 'COUNTRY'
     - publishingCountry = 'PUBLISHING_COUNTRY'
     - hasCoordinate = 'HAS_COORDINATE'
     - hasGeospatialIssue = 'HAS_GEOSPATIAL_ISSUE'
     - typeStatus = 'TYPE_STATUS'
     - recordNumber = 'RECORD_NUMBER'
     - lastInterpreted = 'LAST_INTERPRETED'
     - continent = 'CONTINENT'
     - geometry = 'GEOMETRY'
     - basisOfRecord = 'BASIS_OF_RECORD'
     - datasetKey = 'DATASET_KEY'
     - eventDate = 'EVENT_DATE'
     - catalogNumber = 'CATALOG_NUMBER'
     - year = 'YEAR'
     - month = 'MONTH'
     - decimalLatitude = 'DECIMAL_LATITUDE'
     - decimalLongitude = 'DECIMAL_LONGITUDE'
     - elevation = 'ELEVATION'
     - depth = 'DEPTH'
     - institutionCode = 'INSTITUTION_CODE'
     - collectionCode = 'COLLECTION_CODE'
     - issue = 'ISSUE'
     - mediatype = 'MEDIA_TYPE'
     - recordedBy = 'RECORDED_BY'

    See the API docs http://www.gbif.org/developer/occurrence#download for
    more info, and the predicates docs http://www.gbif.org/developer/occurrence#predicates

    :return: A dictionary, of results

    Usage::

        occ_download(args = ["basisOfRecord = LITERATURE", 'decimalLatitude > 50'])
        occ_download(args = ['decimalLatitude > 50'])

        occ_download("basisOfRecord = LITERATURE")
        occ_download('taxonKey = 3119195')
        occ_download('decimalLatitude > 50')
        occ_download('elevation >= 9000')
        occ_download('decimalLatitude >= 65')
        occ_download("country = US")
        occ_download("institutionCode = TLMF")
        occ_download("catalogNumber = Bird.27847588")

        res = occ_download('taxonKey = 7264332', 'hasCoordinate = TRUE')

        # pass output to occ_download_meta for more information
        occ_download_meta(occ_download('decimalLatitude > 75'))

        # Multiple queries
        gg = occ_download('decimalLatitude >= 65', 'decimalLatitude <= -65', type="or")
        gg = occ_download('depth = 80', 'taxonKey = 2343454', type="or")
    '''
    url = gbif_baseurl + 'occurrence/download/request'

    user = os.environ["GBIF_USER"]
    pwd = os.environ["GBIF_PWD"]
    email = os.environ["GBIF_EMAIL"]

    keyval = [ parse_args(z) for z in args ]

    if len(keyval) > 1:
      req = {'creator': user,
           'notification_address': email,
           'predicate': {'type': type, 'predicates': keyval}}
    else:
      if type == "within" or "within" in [ s['type'] for s in keyval ]:
        req = {'creator': user,
             'notification_address': email,
             'predicate': {
               'type': keyval[0]['type'],
               'value': keyval[0]['value']
             }}
        req['predicate'][keyval[0]['key'].lower()] = req['predicate'].pop('value')
      else:
        req = {'creator': user,
           'notification_address': email,
           'predicate': {
              'type': keyval[0]['type'],
              'key': keyval[0]['key'],
              'value': keyval[0]['value']}}

    out = rg_POST(url, req, user, pwd, **kwargs)
    return [out, user, email]

def rg_POST(url, req, user, pwd, **kwargs):
  heads = {'accept': 'application/json',
    'content-type': 'application/json',
    'user-agent': 'python-requests/' + requests.__version__ + ',pygbif/' + pygbif.__version__
  }
  r = requests.post(url, data = json.dumps(req), headers = heads, auth = auth.HTTPBasicAuth(user, pwd))
  if r.status_code > 203:
    raise 'error: ' + r.content
  if r.headers()['Content-Type'] == 'application/json':
    raise 'not of type json'

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

# print.occ_download = function(x, ...) {
#   stopifnot(is(x, 'occ_download'))
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
