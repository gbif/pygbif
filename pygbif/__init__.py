# pygbif

"""
pygbif library
~~~~~~~~~~~~~~~~~~~~~

pygbif is a Python client for the Global Biodiversity Information Facility (GBIF) API.

Usage::

        # Import entire library
        import pygbif
        # or import modules as needed
        ## occurrences
        from pygbif import occurrences
        ## species
        from pygbif import species
        ## registry
        from pygbif import registry

        ## use advanced logging
        ### setup first
        import requests
        import logging
        import http.client
        http.client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
        ### then make request
        from pygbif import occurrences
        occurrences.search(geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)
"""

from .package_metadata import __author__, __license__, __version__, __title__
from .occurrences import search, get, count, download
from .species import name_parser, name_suggest, name_backbone, name_lookup, name_usage
from .registry import datasets, nodes, networks, organizations, installations
from .maps import map, GbifMap
from .gbifissues import occ_issues_lookup
from .utils import *
from .caching import caching

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
