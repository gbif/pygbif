"""Tests for occurrences module - download_cancel methods"""
from pygbif import occurrences as occ
import vcr
import os
import pytest

# Skip if credentials not available (they are provided in CI via secrets)
SKIP_TEST = not all([
    os.getenv("GBIF_USER"),
    os.getenv("GBIF_PWD"), 
    os.getenv("GBIF_EMAIL")
])

@pytest.mark.skipif(SKIP_TEST, reason="Test requires GBIF credentials")
@vcr.use_cassette("test/vcr_cassettes/test_download_cancel.yaml", filter_headers=["authorization"])
def test_download_cancel():
    "occurrences.download_cancel - basic test"
    name_key = "5WZLF"  # COL Extended Release alphanumeric key
    res = occ.download("taxonKey = " + name_key)
    download_key = res[0]
    out = occ.download_cancel(download_key)
    assert True == out
