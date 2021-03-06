"""Tests for occurrences module - download_get methods"""
from pygbif import occurrences as occ


def test_download_get():
    "occurrences.download_get - basic test"
    key = "0089857-160910150852091"
    res = occ.download_get(key)
    assert "dict" == res.__class__.__name__
    assert len(res) == 3
    assert key == res["key"]
