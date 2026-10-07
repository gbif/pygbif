"""Tests for species module - name_usage methods"""
import warnings
import vcr
from pygbif import species


@vcr.use_cassette("test/vcr_cassettes/test_name_usage.yaml")
def test_name_usage():
    "species.name_usage - basic test"
    res = species.name_usage(key=1)
    assert dict == res.__class__
    assert 23 == len(res)
    assert 1 == res["key"]


@vcr.use_cassette("test/vcr_cassettes/test_name_usage_paging.yaml")
def test_name_usage_paging():
    "species.name_usage - paging"
    res = species.name_usage(limit=10)
    assert dict == res.__class__
    assert 4 == len(res)
    assert 10 == len(res["results"])


@vcr.use_cassette("test/vcr_cassettes/test_name_usage_datasetkey.yaml")
def test_name_usage_datasetkey():
    "species.name_usage - datasetkey works"
    res = species.name_usage(datasetKey="d7dddbf4-2cf0-4f39-9b2a-bb099caae36c")
    assert dict == res.__class__
    assert 4 == len(res)
    assert (
        "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"
        == list(set([x["datasetKey"] for x in res["results"]]))[0]
    )


@vcr.use_cassette("test/vcr_cassettes/test_name_usage_key_datasetkey_warning.yaml")
def test_name_usage_key_datasetkey_warning():
    "species.name_usage - warns when both key and datasetKey are provided"
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        res = species.name_usage(key=1, datasetKey="d7dddbf4-2cf0-4f39-9b2a-bb099caae36c")
        
        # Should have both deprecation warning and UserWarning
        assert len(w) >= 2
        
        # Check for the specific UserWarning about key+datasetKey
        user_warnings = [warning for warning in w if issubclass(warning.category, UserWarning)]
        assert len(user_warnings) == 1
        assert "datasetKey is ignored" in str(user_warnings[0].message)
        
        # Result should use GBIF Backbone (key lookup), not the datasetKey
        assert dict == res.__class__
        assert res["key"] == 1

