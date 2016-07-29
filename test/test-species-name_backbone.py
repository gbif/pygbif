"""Tests for species module - name_backbone methods"""
import os
from pygbif import species

def test_name_backbone():
    "species.name_backbone - basic test"
    res = species.name_backbone(name='Helianthus annuus')
    assert dict == res.__class__
    assert 22 == len(res)
    assert 'Helianthus annuus' == res['species']

def test_name_backbone_multiple_matches():
    "species.name_backbone - multiple matches"
    res = species.name_backbone(name='Aso')
    assert dict == res.__class__
    assert 4 == len(res)
    assert 'Multiple equal matches for Aso' == res['note']
