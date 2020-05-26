"""Tests for registry module - datasets method"""
import vcr
from pygbif import registry


@vcr.use_cassette("test/vcr_cassettes/test_datasets.yaml")
def test_datasets():
    "registry.datasets - basic test"
    res = registry.datasets()
    assert dict == res.__class__


@vcr.use_cassette("test/vcr_cassettes/test_datasets_limit.yaml")
def test_datasets_limit():
    "registry.datasets - limit param"
    res = registry.datasets(limit=1)
    assert dict == res.__class__
    assert 1 == len(res["results"])

    res = registry.datasets(limit=3)
    assert dict == res.__class__
    assert 3 == len(res["results"])


@vcr.use_cassette("test/vcr_cassettes/test_datasets_type.yaml")
def test_datasets_type():
    "registry.datasets - type param"
    res = registry.datasets(type="OCCURRENCE")
    vv = [x["type"] for x in res["results"]]
    assert dict == res.__class__
    assert 100 == len(res["results"])
    assert "OCCURRENCE" == list(set(vv))[0]
