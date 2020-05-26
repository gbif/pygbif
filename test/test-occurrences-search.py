"""Tests for occurrences module - search methods"""
import vcr
from pygbif import occurrences

keyz = ["count", "facets", "results", "endOfRecords", "limit", "offset"]


@vcr.use_cassette("test/vcr_cassettes/test_search.yaml")
def test_search():
    "occurrences.search - basic test"
    res = occurrences.search(taxonKey=3329049)
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    assert sorted(keyz) == sorted(res.keys())


@vcr.use_cassette("test/vcr_cassettes/test_search_key1.yaml")
def test_search_key1():
    "occurrences.search - diff taxonKey"
    res = occurrences.search(taxonKey=2431762)
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    assert 2431762 == res["results"][0]["taxonKey"]


@vcr.use_cassette("test/vcr_cassettes/test_search_key2.yaml")
def test_search_key2():
    "occurrences.search - diff taxonKey2"
    res = occurrences.search(taxonKey=2683264)
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    assert 2683264 == res["results"][0]["taxonKey"]
