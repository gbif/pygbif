"""Tests for occurrences module - search methods"""
import os
from pygbif import occurrences

def test_search():
    "occurrences.search - basic test"
    res = occurrences.search(taxonKey = 3329049)
    assert 'dict' == res.__class__.__name__
    assert 6 == len(res)
    assert [u'count', u'facets', u'results', u'endOfRecords', u'limit', u'offset'] == res.keys()

def test_search_():
    "occurrences.search - diff taxonKey"
    res = occurrences.search(taxonKey = 2431762)
    assert 'dict' == res.__class__.__name__
    assert 6 == len(res)
    assert 2431762 == res['results'][0]['taxonKey']

def test_search_():
    "occurrences.search - diff taxonKey2"
    res = occurrences.search(taxonKey = 2683264)
    assert 'dict' == res.__class__.__name__
    assert 6 == len(res)
    assert 2683264 == res['results'][0]['taxonKey']
