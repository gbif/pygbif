"""Tests for registry module - networks"""
import vcr
from pygbif import registry


@vcr.use_cassette("test/vcr_cassettes/test_networks.yaml")
def test_networks():
    "registry.networks - basic test"
    res = registry.networks()
    assert dict == res.__class__
    assert 2 == len(res)
    assert 12 == len(res["data"])
    assert ["data", "meta"] == sorted(res.keys())


@vcr.use_cassette("test/vcr_cassettes/test_networks_limit.yaml")
def test_networks_limit():
    "registry.networks - limit param "
    res = registry.networks(limit=5)
    assert dict == res.__class__
    assert 5 == len(res["data"])


@vcr.use_cassette("test/vcr_cassettes/test_networks_uuid.yaml")
def test_networks_uuid():
    "registry.networks - with a uuid"
    res = registry.networks(uuid="2b7c7b4f-4d4f-40d3-94de-c28b6fa054a6")
    assert dict == res.__class__
    assert 2 == len(res)
    assert str == res["data"]["title"].__class__
    assert "modifiedBy" in res["data"].keys()
