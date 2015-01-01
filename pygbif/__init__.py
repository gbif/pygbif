# -*- coding: utf-8 -*-

# pygbif

'''
pygbif library
~~~~~~~~~~~~~~~~~~~~~

pygbif is a Python client for GBIF. Example usage:

   >>> import pygbif
   >>> pygbif.xxxx
'''

from .search import search
from .names import name_backbone, name_suggest
from .gbifissues import occ_issues_lookup
from .datasets import dataset_metrics, datasets
