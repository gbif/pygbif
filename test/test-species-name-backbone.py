"""Tests for species module - name_usage methods"""
import vcr
from pygbif import species


@vcr.use_cassette("test/vcr_cassettes/test_name_backbone.yaml")
def test_name_backbone():
    "species.name_backbone - basic test (COL Extended Release default)"
    res = species.name_backbone(scientificName="Calopteryx splendens")
    assert dict == res.__class__
    assert 5 == len(res)
    assert "Calopteryx splendens (Harris, 1780)" == res["usage"]["name"]
    assert res["usage"]["key"] == "Q2M4"  # COL key
    assert list(res.keys()) == ['usage', 'classification', 'diagnostics', 'additionalStatus', 'synonym']

@vcr.use_cassette("test/vcr_cassettes/test_name_backbone_verbose.yaml")
def test_name_backbone_verbose():
    "species.name_backbone - verbose test"
    res = species.name_backbone(scientificName="Calopteryx", verbose=True)
    assert dict == res.__class__
    assert list(res.keys()) == ['diagnostics', 'synonym']
    assert list(res["diagnostics"]) == ['matchType', 'issues', 'confidence', 'note', 'timeTaken', 'alternatives', 'timings']
    assert len(res["diagnostics"]["alternatives"]) > 5

@vcr.use_cassette("test/vcr_cassettes/test_name_backbone_class.yaml")
def test_name_backbone_class():
    "species.name_backbone - class test (COL Extended Release default)"
    res = species.name_backbone(class_="Insecta")
    assert dict == res.__class__
    assert 4 == len(res)
    assert "Insecta" == res["usage"]["name"]
    assert res["usage"]["key"] == "H6"  # COL key
    assert list(res.keys()) == ['usage', 'classification', 'diagnostics', 'synonym']

@vcr.use_cassette("test/vcr_cassettes/test_name_backbone_gbif.yaml")
def test_name_backbone_gbif_backbone():
    "species.name_backbone - explicit GBIF Backbone (checklistKey=None)"
    res = species.name_backbone(scientificName="Calopteryx splendens", checklistKey=None)
    assert dict == res.__class__
    assert "Calopteryx splendens (Harris, 1780)" == res["usage"]["name"]
    assert isinstance(res["usage"]["key"], str)
    assert res["usage"]["key"].isdigit()  # GBIF Backbone uses numeric keys

@vcr.use_cassette("test/vcr_cassettes/test_name_backbone_gbif_uuid.yaml")
def test_name_backbone_gbif_backbone_uuid():
    "species.name_backbone - explicit GBIF Backbone UUID"
    res = species.name_backbone(scientificName="Calopteryx splendens", checklistKey="d7dddbf4-2cf0-4f39-9b2a-bb099caae36c")
    assert dict == res.__class__
    assert "Calopteryx splendens (Harris, 1780)" == res["usage"]["name"]
    assert res["usage"]["key"] == "1427067"  # GBIF Backbone numeric key
    assert isinstance(res["usage"]["key"], str)
    assert res["usage"]["key"].isdigit()

@vcr.use_cassette("test/vcr_cassettes/test_name_backbone_checklistKey.yaml")
def test_name_backbone_checklistKey():
    "species.name_backbone - checklistKey test"
    res = species.name_backbone(scientificName="Calopteryx splendens", checklistKey="7ddf754f-d193-4cc9-b351-99906754a03b")
    assert dict == res.__class__
    assert res["usage"]["key"] == "Q2M4"
    # Check for essential fields (API response structure may vary between taxonomies)
    assert "usage" in res
    assert "classification" in res
    assert "diagnostics" in res
    assert "Calopteryx splendens" == res["usage"]["canonicalName"]

