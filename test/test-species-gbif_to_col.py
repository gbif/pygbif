"""Tests for species module - gbif_to_col method"""
import vcr
from pygbif import species


@vcr.use_cassette("test/vcr_cassettes/test_gbif_to_col_single.yaml")
def test_gbif_to_col_single():
    "species.gbif_to_col - single key conversion"
    res = species.gbif_to_col(5231190)  # Passer domesticus (house sparrow)
    assert "dict" == res.__class__.__name__
    assert "5231190" == res["gbif_key"]
    assert res["usage"] is not None
    assert isinstance(res["usage"]["key"], str)
    assert res["usage"]["name"] is not None
    assert res["classification"] is not None
    assert res["diagnostics"] is not None


@vcr.use_cassette("test/vcr_cassettes/test_gbif_to_col_multiple.yaml")
def test_gbif_to_col_multiple():
    "species.gbif_to_col - multiple keys conversion"
    res = species.gbif_to_col([5231190, 2435099, 2877951])  # Passer domesticus, Helianthus annuus, Balaenoptera musculus
    assert "list" == res.__class__.__name__
    assert 3 == len(res)
    assert all("gbif_key" in r for r in res)
    assert all("usage" in r for r in res)


@vcr.use_cassette("test/vcr_cassettes/test_gbif_to_col_string_key.yaml")
def test_gbif_to_col_string_key():
    "species.gbif_to_col - string key conversion"
    res = species.gbif_to_col("5231190")  # Passer domesticus (house sparrow)
    assert "dict" == res.__class__.__name__
    assert "5231190" == res["gbif_key"]
    assert res["usage"] is not None
