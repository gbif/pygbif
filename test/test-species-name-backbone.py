"""Tests for species module - name_usage methods"""
import vcr
from pygbif import species


@vcr.use_cassette("test/vcr_cassettes/test_name_backbone.yaml")
def test_name_backbone():
    "species.name_backbone - basic test"
    res = species.name_backbone(scientificName="Calopteryx splendens")
    assert dict == res.__class__
    assert 5 == len(res)
    assert "Calopteryx splendens (Harris, 1780)" == res["usage"]["name"]
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
    "species.name_backbone - class test"
    res = species.name_backbone(class_="Insecta")
    assert dict == res.__class__
    assert 4 == len(res)
    assert "Insecta" == res["usage"]["name"]
    assert list(res.keys()) == ['usage', 'classification', 'diagnostics', 'synonym']

@vcr.use_cassette("test/vcr_cassettes/test_name_backbone_checklistKey.yaml")
def test_name_backbone_checklistKey():
    "species.name_backbone - checklistKey test"
    res = species.name_backbone(scientificName="Calopteryx splendens", checklistKey="7ddf754f-d193-4cc9-b351-99906754a03b")
    assert dict == res.__class__
    assert res["usage"]["key"] == "Q2M4"
    assert 5 == len(res)
    assert "Calopteryx splendens" == res["usage"]["canonicalName"]
    assert list(res.keys()) == ['usage', 'classification', 'diagnostics', 'additionalStatus', 'synonym']

