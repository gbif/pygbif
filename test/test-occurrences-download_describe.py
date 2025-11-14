"""Tests for occurrences module - download_describe"""
from pygbif import occurrences as occ
import vcr

@vcr.use_cassette("test/vcr_cassettes/test_download_describe.yaml")
def test_download_describe():
    "occurrences.download_describe - basic usage"
    res=occ.download_describe("simpleCsv") 
    assert dict == res.__class__ 
    assert len(res["fields"]) >= 50 # unlikely to get smaller
    assert "gbifID" == res["fields"][0]["name"]

def test_download_describe_fails_well():
    "occurrences.download_describe - fail test"
    try:
        res=occ.download_describe("dog")
    except Exception as e:
        assert str(e) == "format not in list of acceptable formats"
