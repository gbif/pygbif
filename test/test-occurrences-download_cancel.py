"""Tests for occurrences module - download_cancle methods"""
from pygbif import occurrences as occ
import vcr

@vcr.use_cassette(
    "test/vcr_cassettes/test_download_cancel.yaml", filter_headers=["authorization"]
)
def test_download_cancel():
    "occurrences.download_cancel - basic test"
    name_key = "156780401"  # for "Bear picornavirus 1"
    res = occ.download("taxonKey = " + name_key)
    download_key = res[0]
    out = occ.download_cancel(download_key)
    assert True == out
