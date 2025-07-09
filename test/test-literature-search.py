"""tests for literature search"""
import vcr
from pygbif import literature

keyz = ["count", "facets", "results", "endOfRecords", "limit", "offset"]

@vcr.use_cassette("test/vcr_cassettes/test_literature_search.yaml")
def test_search():
    "literature.search - basic test"
    res = literature.search(limit=10)
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    assert res["count"] >= 48132 # unlikely to go down 

@vcr.use_cassette("test/vcr_cassettes/test_literature_search_key.yaml")
def test_search_key():
    "literature.search - key"
    res = literature.search(gbifDownloadKey="0235283-220831081235567")
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 1 == len(res["results"])
    assert 2024 == res["results"][0]["year"]
    assert ["0235283-220831081235567","0026791-240906103802322"] == res["results"][0]["gbifDownloadKey"]

@vcr.use_cassette("test/vcr_cassettes/test_literature_search_year.yaml")
def test_search_year():
    "literature.search - year"
    res = literature.search(year="2010,2024", limit=10)
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    for result in res["results"]:
        assert 2010 <= result["year"] <= 2024

@vcr.use_cassette("test/vcr_cassettes/test_literature_search_facet.yaml")
def test_search_facet():
    "literature.search - facet"
    res = literature.search(facet="year", limit=10)
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    assert sorted(keyz) == sorted(res.keys())
    assert 10 == len(res["results"])
    assert "list" == res["facets"].__class__.__name__
    assert 2 == len(res["facets"][0]["counts"][0])
    assert set(['name', 'count']) == set(res["facets"][0]["counts"][0].keys())

