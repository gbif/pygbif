"""tests for collection search"""
import vcr
from pygbif import collection

keyz = ["count", "results", "endOfRecords", "limit", "offset"]

@vcr.use_cassette("test/vcr_cassettes/test_collection_search.yaml")
def test_search():
    "collection.search - basic test"
    res = collection.search(limit=10)
    assert "dict" == res.__class__.__name__
    assert 5 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    assert res["count"] >= 10000

@vcr.use_cassette("test/vcr_cassettes/test_collection_search_q.yaml")
def test_search_q():
    "collection.search - q"
    res = collection.search(q="Kansas", limit=10)
    assert "dict" == res.__class__.__name__
    assert 5 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    assert res["count"] >= 30
    assert res["count"] <= 10000

@vcr.use_cassette("test/vcr_cassettes/test_collection_search_country.yaml")
def test_search_country():
    "collection.search - country"
    res = collection.search(country=["US","GB"], limit=10)
    assert "dict" == res.__class__.__name__
    assert 5 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    assert res["count"] >= 3000
    assert res["count"] <= 10000

@vcr.use_cassette("test/vcr_cassettes/test_collection_search_active.yaml")
def test_search_active():
    "collection.search - active"
    res = collection.search(active=True, limit=10)
    assert "dict" == res.__class__.__name__
    assert 5 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    assert res["count"] >= 9000
    for r in res["results"]:
        assert r["active"] is True

@vcr.use_cassette("test/vcr_cassettes/test_collection_search_institutionKey.yaml")
def test_search_institutionKey():
    "collection.search - institutionKey"
    res = collection.search(institutionKey="6a6ac6c5-1b8a-48db-91a2-f8661274ff80", limit=10)
    assert "dict" == res.__class__.__name__
    assert 5 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    assert res["count"] >= 20
    for r in res["results"]:
        assert r["institutionKey"] == "6a6ac6c5-1b8a-48db-91a2-f8661274ff80"

