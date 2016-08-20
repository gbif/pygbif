"""Tests for occurrences module - get methods"""
import os
from pygbif import occurrences

def test_get():
    "occurrences.get - basic test"
    res = occurrences.get(key = 1248387548)
    assert 'dict' == res.__class__.__name__
    assert len(res) > 30
    assert 1248387548 == res['key']

def test_get_verbatim():
    "occurrences.get_verbatim - basic test"
    res = occurrences.get_verbatim(key = 1248387548)
    assert 'dict' == res.__class__.__name__
    assert len(res) > 20
    assert 1248387548 == res['key']

def test_get_fragment():
    "occurrences.get_fragment - basic test"
    res = occurrences.get_fragment(key = 1052909293)
    assert 'dict' == res.__class__.__name__
    assert 41 == len(res)
    assert 'HumanObservation' == res['basisOfRecord']
