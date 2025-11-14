"""Tests for occurrences module - download_cancle methods"""
from pygbif import occurrences as occ
import vcr
import os
import pytest

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"
print(IN_GITHUB_ACTIONS)

@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Test doesn't work well in Github Actions.")
@vcr.use_cassette("test/vcr_cassettes/test_download_cancel.yaml", filter_headers=["authorization"])
def test_download_cancel():
    "occurrences.download_cancel - basic test"
    name_key = "789"  # Odonata
    res = occ.download("taxonKey = " + name_key)
    download_key = res[0]
    out = occ.download_cancel(download_key)
    assert True == out
