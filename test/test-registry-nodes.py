"""Tests for registry module - nodes methods"""
import vcr

from pygbif import registry


@vcr.use_cassette("test/vcr_cassettes/test_nodes.yaml")
def test_nodes():
    "registry.nodes - basic test"
    res = registry.nodes()
    assert dict == res.__class__
    assert 2 == len(res)
    assert 100 == len(res["data"])
    assert ["data", "meta"] == sorted(res.keys())


@vcr.use_cassette("test/vcr_cassettes/test_nodes_limit.yaml")
def test_nodes_limit():
    "registry.nodes - limit param"
    res = registry.nodes(limit=5)
    assert dict == res.__class__
    assert 5 == len(res["data"])


@vcr.use_cassette("test/vcr_cassettes/test_nodes_return.yaml")
def test_nodes_return():
    "registry.nodes - data param"
    res = registry.nodes(data="identifier", uuid="03e816b3-8f58-49ae-bc12-4e18b358d6d9")
    assert dict == res.__class__
    assert 2 == len(res)
    assert 1 == len(res["data"])
    assert 5 == len(res["data"][0])
    assert "identifier" in res["data"][0].keys()
