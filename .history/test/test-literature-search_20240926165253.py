"""tests for literature search"""
import vcr
from pygbif import literature


@vcr.use_cassette("test/vcr_cassettes/test_literature_search.yaml")
def test_search():
    "literature.search - basic test"
    res = literature.search(q="mammals")
    assert "dict" == res.__class__.__name__
    # assert 6 == len(res)
    # assert sorted(keyz) == sorted(res.keys())
