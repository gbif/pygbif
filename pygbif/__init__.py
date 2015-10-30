# -*- coding: utf-8 -*-

# pygbif

'''
pygbif library
~~~~~~~~~~~~~~~~~~~~~

pygbif is a Python client for GBIF. Example usage:

>>> # Import entire library
>>> import pygbif
>>> # or import modules as needed
>>> ## occurrences
>>> from pygbif import occurrences
>>> ## species
>>> from pygbif import species
>>> ## registry
>>> from pygbif import registry
'''

from .occurrences import search, get, count
from .species import names
from .registry import datasets, nodes
from .gbifissues import occ_issues_lookup
