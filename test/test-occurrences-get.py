"""Tests for occurrences module - get methods"""
import os
from pygbif import occurrences

def test_get():
    "occurrences.get - basic test"
    res = occurrences.get(taxonKey = 252408386)
    assert 'dict' == res.__class__.__name__
    assert 30 == len(res)
    assert 252408386 == res['key']

def test_get_verbatim():
    "occurrences.get_verbatim - basic test"
    res = occurrences.get_verbatim(taxonKey = 252408386)
    assert 'dict' == res.__class__.__name__
    assert 24 == len(res)
    assert 252408386 == res['key']

def test_get_fragment():
    "occurrences.get_fragment - basic test"
    res = occurrences.get_fragment(taxonKey = 1052909293)
    assert 'dict' == res.__class__.__name__
    assert 41 == len(res)
    assert 'HumanObservation' == res['basisOfRecord']
