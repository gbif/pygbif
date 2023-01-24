import os
import csv
import json
import re
import datetime
import requests

from .. import package_metadata, occurrences
from ..gbifutils import (
    is_not_none,
    is_none,
    stop,
    gbif_GET,
    gbif_GET_write,
    gbif_DELETE,
)
import logging


def _parse_args(x):
    if re.match("geometry", x):
        geometry = re.search("(POLY|MULTIPOLY).+", x, re.IGNORECASE).group()
        return {"type": "within", "geometry": geometry}
    tmp = re.split("\s", x)
    pred_type = operator_lkup.get(tmp[1])
    key = key_lkup.get(tmp[0])
    return {"type": pred_type, "key": key, "value": tmp[2]}


def _check_environ(variable, value):
    """check if a variable is present in the environmental variables"""
    if is_not_none(value):
        return value
    else:
        value = os.environ.get(variable)
        if is_none(value):
            stop(
                "".join(
                    [
                        variable,
                        """ not supplied and no entry in environmental
                           variables""",
                    ]
                )
            )
        else:
            return value


def download(queries, user=None, pwd=None, email=None, pred_type="and"):
    """
    Spin up a download request for GBIF occurrence data.

    :param queries: One or more of query arguments to kick of a download job.
        See Details.
    :type queries: str or list
    :param pred_type: (character) One of ``equals`` (``=``), ``and`` (``&``),
        `or`` (``|``), ``lessThan`` (``<``), ``lessThanOrEquals`` (``<=``),
        ``greaterThan`` (``>``), ``greaterThanOrEquals`` (``>=``),
        ``in``, ``within``, ``not`` (``!``), ``like``
    :param user: (character) User name within GBIF's website.
        Required. Set in your env vars with the option ``GBIF_USER``
    :param pwd: (character) User password within GBIF's website. Required.
        Set in your env vars with the option ``GBIF_PWD``
    :param email: (character) Email address to recieve download notice done
        email. Required. Set in your env vars with the option ``GBIF_EMAIL``

    Argument passed have to be passed as character (e.g., ``country = US``),
    with a space between key (``country``), operator (``=``), and value (``US``).
    See the ``type`` parameter for possible options for the operator.
    This character string is parsed internally.

    Acceptable arguments to ``...`` (args) are:

     - taxonKey = ``TAXON_KEY``
     - scientificName = ``SCIENTIFIC_NAME``
     - country = ``COUNTRY``
     - publishingCountry = ``PUBLISHING_COUNTRY``
     - hasCoordinate = ``HAS_COORDINATE``
     - hasGeospatialIssue = ``HAS_GEOSPATIAL_ISSUE``
     - typeStatus = ``TYPE_STATUS``
     - recordNumber = ``RECORD_NUMBER``
     - lastInterpreted = ``LAST_INTERPRETED``
     - continent = ``CONTINENT``
     - geometry = ``GEOMETRY``
     - basisOfRecord = ``BASIS_OF_RECORD``
     - datasetKey = ``DATASET_KEY``
     - eventDate = ``EVENT_DATE``
     - catalogNumber = ``CATALOG_NUMBER``
     - year = ``YEAR``
     - month = ``MONTH``
     - decimalLatitude = ``DECIMAL_LATITUDE``
     - decimalLongitude = ``DECIMAL_LONGITUDE``
     - elevation = ``ELEVATION``
     - depth = ``DEPTH``
     - institutionCode = ``INSTITUTION_CODE``
     - collectionCode = ``COLLECTION_CODE``
     - issue = ``ISSUE``
     - mediatype = ``MEDIA_TYPE``
     - recordedBy = ``RECORDED_BY``
     - repatriated = ``REPATRIATED``

    See the API docs http://www.gbif.org/developer/occurrence#download
    for more info, and the predicates docs
    http://www.gbif.org/developer/occurrence#predicates

    GBIF has a limit of 100,000 predicates and 10,000 points (in within
    predicates) for download queries – so if your download request is
    particularly complex, you may need to split it into multiple
    requests by one factor or another.

    :return: A dictionary, of results

    Usage::

        from pygbif import occurrences as occ

        occ.download('basisOfRecord = PRESERVED_SPECIMEN')
        occ.download('taxonKey = 3119195')
        occ.download('decimalLatitude > 50')
        occ.download('elevation >= 9000')
        occ.download('decimalLatitude >= 65')
        occ.download('country = US')
        occ.download('institutionCode = TLMF')
        occ.download('catalogNumber = Bird.27847588')

        res = occ.download(['taxonKey = 7264332', 'hasCoordinate = TRUE'])

        # pass output to download_meta for more information
        occ.download_meta(occ.download('decimalLatitude > 75'))

        # Multiple queries
        gg = occ.download(['decimalLatitude >= 65',
                          'decimalLatitude <= -65'], type='or')
        gg = occ.download(['depth = 80', 'taxonKey = 2343454'],
                          type='or')

        # Repratriated data for Costa Rica
        occ.download(['country = CR', 'repatriated = true'])

        # turn off logging
        import logging
        logger = logging.getLogger()
        logger.disabled = True
        z = occ.download('elevation >= 95000')
        logger.disabled = False
        w = occ.download('elevation >= 10000')
    """

    user = _check_environ("GBIF_USER", user)
    pwd = _check_environ("GBIF_PWD", pwd)
    email = _check_environ("GBIF_EMAIL", email)

    if isinstance(queries, str):
        queries = [queries]

    keyval = [_parse_args(z) for z in queries]

    # USE GBIFDownload class to set up the predicates
    req = GbifDownload(user, email)
    req.main_pred_type = pred_type
    for predicate in keyval:
        if "geometry" in predicate.keys():
            req.add_geometry(predicate["geometry"])
        else:
            req.add_predicate(predicate["key"], predicate["value"], predicate["type"])

    out = req.post_download(user, pwd)
    return out, req.payload


class GbifDownload(object):
    def __init__(self, creator, email, polygon=None):
        """class to setup a JSON doc with the query and POST a request

        All predicates (default key-value or iterative based on a list of
        values) are combined with an AND statement. Iterative predicates are
        creating a subset equal statements combined with OR

        :param creator: User name.
        :param email: user email
        :param polygon: Polygon of points to extract data from
        """
        self.predicates = []
        self._main_pred_type = "and"

        self.url = "http://api.gbif.org/v1/occurrence/download/request"
        self.header = {
            "accept": "application/json",
            "content-type": "application/json",
            "user-agent": "".join(
                [
                    "python-requests/",
                    requests.__version__,
                    ",pygbif/",
                    package_metadata.__version__,
                ]
            ),
        }

        self.payload = {
            "creator": creator,
            "notification_address": [email],
            "sendNotification": True,
            "predicate": {"type": self._main_pred_type, "predicates": self.predicates},
        }
        self.request_id = None

        # prepare the geometry polygon constructions
        if polygon:
            self.add_geometry(polygon)

    @property
    def main_pred_type(self):
        """get main predicate combination type"""
        return self._main_pred_type

    @main_pred_type.setter
    def main_pred_type(self, value):
        """set main predicate combination type

        :param value: (character) One of ``equals`` (``=``), ``and`` (``&``), ``or`` (``|``),
        ``lessThan`` (``<``), ``lessThanOrEquals`` (``<=``), ``greaterThan`` (``>``),
        ``greaterThanOrEquals`` (``>=``), ``in``, ``within``, ``not`` (``!``), ``like``
        """
        if value not in operators:
            value = operator_lkup.get(value)
        if value:
            self._main_pred_type = value
            self.payload["predicate"]["type"] = self._main_pred_type
        else:
            raise Exception("main predicate combiner not a valid operator")

    def add_predicate(self, key, value, predicate_type="equals"):
        """
        add key, value, type combination of a predicate

        :param key: query KEY parameter
        :param value: the value used in the predicate
        :param predicate_type: the type of predicate (e.g. ``equals``)
        """
        if predicate_type not in operators:
            predicate_type = operator_lkup.get(predicate_type)
        if predicate_type:
            self.predicates.append({"type": predicate_type, "key": key, "value": value})
        else:
            raise Exception("predicate type not a valid operator")

    @staticmethod
    def _extract_values(values_list):
        """extract values from either file or list

        :param values_list: list or file name (str) with list of values
        """
        values = []
        # check if file or list of values to iterate
        if isinstance(values_list, str):
            with open(values_list) as ff:
                reading = csv.reader(ff)
                for j in reading:
                    values.append(j[0])
        elif isinstance(values_list, list):
            values = values_list
        else:
            raise Exception("input datatype not supported.")
        return values

    def add_iterative_predicate(self, key, values_list):
        """add an iterative predicate with a key and set of values
        which it can be equal to in and or function.
        The individual predicates are specified with the type ``equals`` and
        combined with a type ``or``.

        The main reason for this addition is the inability of using ``in`` as
        predicate type wfor multiple taxon_key values
        (cfr. http://dev.gbif.org/issues/browse/POR-2753)

        :param key: API key to use for the query.
        :param values_list: Filename or list containing the taxon keys to be s
            searched.

        """
        values = self._extract_values(values_list)

        predicate = {"type": "equals", "key": key, "value": None}
        predicates = []
        while values:
            predicate["value"] = values.pop()
            predicates.append(predicate.copy())
        self.predicates.append({"type": "or", "predicates": predicates})

    def add_geometry(self, polygon, geom_type="within"):
        """add a geometry type of predicate

        :param polygon: In this format ``POLYGON((x1 y1, x2 y2,... xn yn))``
        :param geom_type: type of predicate, e.g. ``within``
        :return:
        """
        self.predicates.append({"type": geom_type, "geometry": polygon})

    def post_download(self, user=None, pwd=None):
        """

        :param user: Username
        :param pwd: Password
        :return:
        """
        user = _check_environ("GBIF_USER", user)
        pwd = _check_environ("GBIF_PWD", pwd)

        # pprint.pprint(self.payload)
        r = requests.post(
            self.url,
            auth=requests.auth.HTTPBasicAuth(user, pwd),
            data=json.dumps(self.payload),
            headers=self.header,
        )
        if r.status_code > 203:
            raise Exception(
                "error: "
                + r.text
                + ", with error status code "
                + str(r.status_code)
                + "check your number of active downloads."
            )
        else:
            self.request_id = r.text
            logging.info("Your download key is " + self.request_id)
        return self.request_id

    def get_status(self):
        """get the current download status"""
        return get_download_status(self.request_id)


def get_download_status(request_key):
    """get the current download status"""
    return download_meta(request_key).get("status")


def download_meta(key, **kwargs):
    """
    Retrieves the occurrence download metadata by its unique key. Further
    named arguments passed on to ``requests.get`` can be included as additional
    arguments

    :param key: [str] A key generated from a request, like that from ``download``

    Usage::

      from pygbif import occurrences as occ
      occ.download_meta(key = "0003970-140910143529206")
      occ.download_meta(key = "0000099-140929101555934")
    """
    url = "http://api.gbif.org/v1/occurrence/download/" + key
    return gbif_GET(url, {}, **kwargs)


def download_cancel(key, user=None, pwd=None, **kwargs):
    """
    Delete a download request by its unique key. Further
    named arguments passed on to ``requests.get`` can be included as additional
    arguments

    :param key: [str] A key generated from a request, like that from ``download``
    :param user: [str] A user name, look at env var ``GBIF_USER`` first
    :param pwd: [str] Your password, look at env var ``GBIF_PWD`` first

    :return: a bool, `True` if cancel request successful, otherwise `False`

    Usage::

      from pygbif import occurrences as occ
      # first, make a download request
      x = occ.download('taxonKey = 156780401')
      occ.download_meta(x[0])
      # then cancel it - do so before the download is ready, or it will have no effect
      occ.download_cancel(key = x[0])
    """
    user = _check_environ("GBIF_USER", user)
    pwd = _check_environ("GBIF_PWD", pwd)

    url = "http://api.gbif.org/v1/occurrence/download/request/" + key
    return gbif_DELETE(url, {}, auth=(user, pwd), **kwargs)


def download_list(user=None, pwd=None, limit=20, offset=0):
    """
    Lists the downloads created by a user.

    :param user: [str] A user name, look at env var ``GBIF_USER`` first
    :param pwd: [str] Your password, look at env var ``GBIF_PWD`` first
    :param limit: [int] Number of records to return. Default: ``20``
    :param offset: [int] Record number to start at. Default: ``0``

    Usage::

      from pygbif import occurrences as occ
      occ.download_list(user = "sckott")
      occ.download_list(user = "sckott", limit = 5)
      occ.download_list(user = "sckott", offset = 21)
    """

    user = _check_environ("GBIF_USER", user)
    pwd = _check_environ("GBIF_PWD", pwd)

    url = "http://api.gbif.org/v1/occurrence/download/user/" + user
    args = {"limit": limit, "offset": offset}
    res = gbif_GET(url, args, auth=(user, pwd))
    return {
        "meta": {
            "offset": res["offset"],
            "limit": res["limit"],
            "endofrecords": res["endOfRecords"],
            "count": res["count"],
        },
        "results": res["results"],
    }


def download_get(key, path=".", **kwargs):
    """
    Get a download from GBIF.

    :param key: [str] A key generated from a request, like that from ``download``
    :param path: [str] Path to write zip file to. Default: ``"."``, with a ``.zip`` appended to the end.
    :param **kwargs**: Further named arguments passed on to ``requests.get``

    Downloads the zip file to a directory you specify on your machine.
    The speed of this function is of course proportional to the size of the
    file to download, and affected by your internet connection speed.

    This function only downloads the file. To open and read it, see
    https://github.com/BelgianBiodiversityPlatform/python-dwca-reader

    Usage::

      from pygbif import occurrences as occ
      x=occ.download_get("0000066-140928181241064")
      occ.download_get("0003983-140910143529206")
      
      # turn off logging
      import logging
      logger = logging.getLogger()
      logger.disabled = True
      x = occ.download_get("0000066-140928181241064")
      
      # turn back on
      logger.disabled = False
      x = occ.download_get("0000066-140928181241064")
    """
    meta = occurrences.download_meta(key)
    if meta["status"] != "SUCCEEDED":
        raise Exception('download "%s" not of status SUCCEEDED' % key)
    else:
        logging.info("Download file size: %s bytes" % meta["size"])
        url = "http://api.gbif.org/v1/occurrence/download/request/" + key
        path = "%s/%s.zip" % (path, key)
        gbif_GET_write(url, path, **kwargs)
        logging.info("On disk at " + path)
        return {"path": path, "size": meta["size"], "key": key}


operators = [
    "equals",
    "and",
    "or",
    "lessThan",
    "lessThanOrEquals",
    "greaterThan",
    "greaterThanOrEquals",
    "in",
    "within",
    "not",
    "like",
]

operator_lkup = {
    "=": "equals",
    "&": "and",
    "|": "or",
    "<": "lessThan",
    "<=": "lessThanOrEquals",
    ">": "greaterThan",
    ">=": "greaterThanOrEquals",
    "!": "not",
    "in": "in",
    "within": "within",
    "like": "like",
}

key_lkup = {
    "taxonKey": "TAXON_KEY",
    "scientificName": "SCIENTIFIC_NAME",
    "country": "COUNTRY",
    "publishingCountry": "PUBLISHING_COUNTRY",
    "hasCoordinate": "HAS_COORDINATE",
    "hasGeospatialIssue": "HAS_GEOSPATIAL_ISSUE",
    "typeStatus": "TYPE_STATUS",
    "recordNumber": "RECORD_NUMBER",
    "lastInterpreted": "LAST_INTERPRETED",
    "continent": "CONTINENT",
    "geometry": "GEOMETRY",
    "basisOfRecord": "BASIS_OF_RECORD",
    "datasetKey": "DATASET_KEY",
    "eventDate": "EVENT_DATE",
    "catalogNumber": "CATALOG_NUMBER",
    "year": "YEAR",
    "month": "MONTH",
    "decimalLatitude": "DECIMAL_LATITUDE",
    "decimalLongitude": "DECIMAL_LONGITUDE",
    "elevation": "ELEVATION",
    "depth": "DEPTH",
    "institutionCode": "INSTITUTION_CODE",
    "collectionCode": "COLLECTION_CODE",
    "issue": "ISSUE",
    "mediatype": "MEDIA_TYPE",
    "recordedBy": "RECORDED_BY",
    "repatriated": "REPATRIATED",
}
