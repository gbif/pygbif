"""tests for institution search"""
import vcr
from pygbif import institution

keyz = ["count", "results", "endOfRecords", "limit", "offset"]

@vcr.use_cassette("test/vcr_cassettes/test_institution_search.yaml")
def test_search():
    "institution.search - basic test"
    res = institution.search(limit=10)
    assert "dict" == res.__class__.__name__
    assert 5 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    assert res["count"] >= 8000

@vcr.use_cassette("test/vcr_cassettes/test_institution_search_q.yaml")
def test_search_q():
    "institution.search - q"
    res = institution.search(q="Kansas", limit=10)
    assert "dict" == res.__class__.__name__
    assert 5 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    assert res["count"] >= 10
    assert res["count"] <= 8000

@vcr.use_cassette("test/vcr_cassettes/test_institution_search_country.yaml")
def test_search_country():
    "institution.search - country"
    res = institution.search(country=["US", "GB"], limit=10)
    assert "dict" == res.__class__.__name__
    assert 5 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    assert res["count"] >= 1000
    assert res["count"] <= 8000

@vcr.use_cassette("test/vcr_cassettes/test_institution_search_active.yaml")
def test_search_active():
    "institution.search - active"
    res = institution.search(active=True, limit=10)
    assert "dict" == res.__class__.__name__
    assert 5 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    for r in res["results"]:
        assert r["active"] is True

@vcr.use_cassette("test/vcr_cassettes/test_institution_typeSpecimenCount.yaml")
def test_search_typeSpecimenCount():
    "institution.search - typeSpecimenCount"
    res = institution.search(typeSpecimenCount="10,100", limit=10)
    assert "dict" == res.__class__.__name__
    assert 5 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    for r in res["results"]:
        assert r["typeSpecimenCount"] >= 10
        assert r["typeSpecimenCount"] <= 100

