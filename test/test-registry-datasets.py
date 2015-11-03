"""Tests for registry module - datasets methods"""
import os
from pygbif import registry

def test_datasets():
    "registry.datasets - basic test"
    res = registry.datasets()
    assert dict == res.__class__

def test_datasets_limit():
    "registry.datasets - limit param"
    res = registry.datasets(limit=1)
    assert dict == res.__class__
    assert 1 == len(res['data'])

    res = registry.datasets(limit=3)
    assert dict == res.__class__
    assert 3 == len(res['data'])

def test_datasets_type():
    "registry.datasets - type param"
    res = registry.datasets(type="OCCURRENCE")
    vv = [ x['type'] for x in res['data'] ]
    assert dict == res.__class__
    assert 100 == len(res['data'])
    assert 'OCCURRENCE' == list(set(vv))[0]

def test_dataset_metrics():
    "registry.dataset_metrics - basic test"
    res = registry.dataset_metrics(uuid='3f8a1297-3259-4700-91fc-acc4170b27ce')
    assert dict == res.__class__
    assert 19 == len(res)

def test_dataset_metrics_multiple_uuids():
    "registry.dataset_metrics - multiple uuids"
    uuids = ['3f8a1297-3259-4700-91fc-acc4170b27ce', '66dd0960-2d7d-46ee-a491-87b9adcfe7b1']
    res = registry.dataset_metrics(uuids)
    assert list == res.__class__
    assert 2 == len(res)
