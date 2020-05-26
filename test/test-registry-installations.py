"""Tests for registry module - installations methods"""
import vcr

from pygbif import registry


@vcr.use_cassette("test/vcr_cassettes/test_installations.yaml")
def test_installations():
    "registry.installations - basic test"
    res = registry.installations()
    assert dict == res.__class__
    assert 2 == len(res)
    assert 100 == len(res["data"])
    assert ["data", "meta"] == sorted(res.keys())


@vcr.use_cassette("test/vcr_cassettes/test_installations_limit.yaml")
def test_installations_limit():
    "registry.installations - limit param "
    res = registry.installations(limit=5)
    assert dict == res.__class__
    assert 5 == len(res["data"])


@vcr.use_cassette("test/vcr_cassettes/test_installations_uuid.yaml")
def test_installations_uuid():
    "registry.installations - with a uuid"
    res = registry.installations(uuid="b77901f9-d9b0-47fa-94e0-dd96450aa2b4")
    assert dict == res.__class__
    assert 2 == len(res)
    assert 16 == len(res["data"])
    assert dict == res["data"]["endpoints"][0].__class__
    assert "identifiers" in res["data"].keys()
