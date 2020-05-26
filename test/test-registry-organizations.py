"""Tests for registry module - organizations"""
import vcr
from pygbif import registry


@vcr.use_cassette("test/vcr_cassettes/test_organizations.yaml")
def test_organizations():
    "registry.organizations - basic test"
    res = registry.organizations()
    assert dict == res.__class__
    assert 2 == len(res)
    assert 100 == len(res["data"])
    assert ["data", "meta"] == sorted(res.keys())


@vcr.use_cassette("test/vcr_cassettes/test_organizations_limit.yaml")
def test_organizations_limit():
    "registry.organizations - limit param "
    res = registry.organizations(limit=5)
    assert dict == res.__class__
    assert 5 == len(res["data"])


@vcr.use_cassette("test/vcr_cassettes/test_organizations_uuid.yaml")
def test_organizations_uuid():
    "registry.organizations - with a uuid"
    res = registry.organizations(uuid="e2e717bf-551a-4917-bdc9-4fa0f342c530")
    assert dict == res.__class__
    assert 2 == len(res)
    assert list == res["data"]["contacts"].__class__
    assert dict == res["data"]["contacts"][0].__class__
    assert list == res["data"]["contacts"][0]["position"].__class__
    assert "numPublishedDatasets" in res["data"].keys()
