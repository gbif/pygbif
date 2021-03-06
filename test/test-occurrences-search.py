"""Tests for occurrences module - search methods"""
import vcr
from pygbif import occurrences

keyz = ["count", "facets", "results", "endOfRecords", "limit", "offset"]
x = "https://orcid.org/0000-0003-1691-239X"


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


@vcr.use_cassette("test/vcr_cassettes/test_search_recorded_by_id.yaml")
def test_search_recorded_by_id():
    "occurrences.search - recordedByID"
    res = occurrences.search(recordedByID=x, limit=3)
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    assert x == res["results"][0]["recordedByIDs"][0]["value"]


@vcr.use_cassette("test/vcr_cassettes/test_search_identified_by_id.yaml")
def test_search_identified_by_id():
    "occurrences.search - identifiedByID"
    res = occurrences.search(identifiedByID=x, limit=3)
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    assert x == res["results"][0]["identifiedByIDs"][0]["value"]
