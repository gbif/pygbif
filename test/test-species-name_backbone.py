"""Tests for species module - name_backbone methods"""
import vcr
from pygbif import species


@vcr.use_cassette("test/vcr_cassettes/test_name_backbone.yaml")
def test_name_backbone():
    "species.name_backbone - basic test"
    res = species.name_backbone(name="Helianthus annuus")
    assert dict == res.__class__
    assert 22 == len(res)
    assert "Helianthus annuus" == res["species"]


@vcr.use_cassette("test/vcr_cassettes/test_name_backbone_multiple_matches.yaml")
def test_name_backbone_multiple_matches():
    "species.name_backbone - multiple matches"
    res = species.name_backbone(name="Aso")
    assert dict == res.__class__
    assert 4 == len(res)
    assert "No match because of too little confidence" == res["note"]
