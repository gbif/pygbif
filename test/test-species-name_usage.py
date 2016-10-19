"""Tests for species module - name_usage methods"""
import os
from pygbif import species

def test_name_usage():
    "species.name_usage - basic test"
    res = species.name_usage(key=1)
    assert dict == res.__class__
    assert 22 == len(res)
    assert 1 == res['key']

def test_name_usage_paging():
    "species.name_usage - paging"
    res = species.name_usage(limit = 10)
    assert dict == res.__class__
    assert 4 == len(res)
    assert 10 == len(res['results'])

def test_name_usage_datasetkey():
    "species.name_usage - datasetkey works"
    res = species.name_usage(datasetKey="d7dddbf4-2cf0-4f39-9b2a-bb099caae36c")
    assert dict == res.__class__
    assert 4 == len(res)
    assert 'd7dddbf4-2cf0-4f39-9b2a-bb099caae36c' == list(set([ x['datasetKey'] for x in res['results'] ]))[0]
