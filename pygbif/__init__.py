# -*- coding: utf-8 -*-

# pygbif

'''
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
		import httplib as http_client
		http_client.HTTPConnection.debuglevel = 1
		logging.basicConfig()
		logging.getLogger().setLevel(logging.DEBUG)
		requests_log = logging.getLogger("requests.packages.urllib3")
		requests_log.setLevel(logging.DEBUG)
		requests_log.propagate = True
		### then make request
		from pygbif import occurrences
		occurrences.search(geometry='POLYGON((30.1 10.1, 10 20, 20 40, 40 40, 30.1 10.1))', limit=20)
'''

__version__ = '0.2.0'
__title__ = 'pygbif'
__author__ = 'Scott Chamberlain'
__license__ = 'MIT'

from .occurrences import search, get, count, download
from .species import name_parser, name_suggest, name_backbone, name_lookup, name_usage
from .registry import datasets, nodes, networks, organizations, installations
from .gbifissues import occ_issues_lookup
