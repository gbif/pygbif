"""tests for literature search"""
import vcr
from pygbif import literature

keyz = ["count", "facets", "results", "endOfRecords", "limit", "offset"]

@vcr.use_cassette("test/vcr_cassettes/test_literature_search.yaml")
def test_search():
    "literature.search - basic test"
    res = literature.search()
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    print(res.keys())
    # assert sorted(keyz) == sorted(res.keys())
