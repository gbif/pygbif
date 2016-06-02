"""Tests for occurrences module - download_get methods"""
import os
from pygbif import occurrences

def test_download_get():
    "occurrences.download_get - basic test"
    key = "0000066-140928181241064"
    res = occurrences.download_get(key)
    assert 'dict' == res.__class__.__name__
    assert len(res) == 3
    assert key == res['key']
