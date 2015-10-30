"""Tests for occurrences module - get methods"""
import os
from pygbif import occurrences

def test_get():
    "Basic test of occurrences.get"
    res = occurrences.get(taxonKey = 252408386)
    assert 'dict' == res.__class__.__name__
    assert 30 == len(res)
    assert 252408386 == res['key']

def test_get_verbatim():
    "Basic test of occurrences.get_verbatim"
    res = occurrences.get_verbatim(taxonKey = 252408386)
    assert 'dict' == res.__class__.__name__
    assert 24 == len(res)
    assert 252408386 == res['key']

def test_get_fragment():
    "Basic test of occurrences.get_fragment"
    res = occurrences.get_fragment(taxonKey = 1052909293)
    assert 'dict' == res.__class__.__name__
    assert 41 == len(res)
    assert 'HumanObservation' == res['basisOfRecord']
