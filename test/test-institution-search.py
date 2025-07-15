"""Tests for institution search"""
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

@vcr.use_cassette("test/vcr_cassettes/test_institution_search_country.yaml")
def test_search_country():
    "institution.search - country"
    res = institution.search(country=["US","GB"], limit=10)
    assert "dict" == res.__class__.__name__
    assert 5 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    assert res["count"] >= 2000

@vcr.use_cassette("test/vcr_cassettes/test_institution_search_typeSpecimenCount.yaml")
def test_search_typeSpecimenCount():
    "institution.search - typeSpecimenCount"
    res = institution.search(typeSpecimenCount="10,100", limit=10)
    assert "dict" == res.__class__.__name__
    assert 5 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    for result in res["results"]:
        assert 10 <= result["typeSpecimenCount"] <= 100

@vcr.use_cassette("test/vcr_cassettes/test_institution_search_numberSpecimens.yaml")
def test_search_numberSpecimens():
    "institution.search - numberSpecimens"
    res = institution.search(numberSpecimens="1000,*", limit=10)
    assert "dict" == res.__class__.__name__
    assert 5 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    for result in res["results"]:
        assert result["numberSpecimens"] >= 1000

