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

@vcr.use_cassette("test/vcr_cassettes/test_literature_search_key.yaml")
def test_search_key():
    "literature.search - key"
    res = literature.search(gbifDownloadKey="0235283-220831081235567")
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    assert sorted(keyz) == sorted(res.keys())

    # assert 1 == len(res["results"])
    # assert "10.3897/zookeys.50.504" == res["results"][0]["doi"]