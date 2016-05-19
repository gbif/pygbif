"""Tests for registry module - nodes methods"""
import os
from pygbif import registry

def test_nodes():
    "Basic test of registry.nodes"
    res = registry.nodes()
    assert dict == res.__class__
    assert 2 == len(res)
    assert 100 == len(res['data'])
    assert ['data', 'meta'] == sorted(res.keys())

def test_nodes_limit():
    "limit param in registry.nodes"
    res = registry.nodes(limit=5)
    assert dict == res.__class__
    assert 5 == len(res['data'])

def test_nodes_return():
    "data param in registry.nodes"
    res = registry.nodes(data='identifier', uuid="03e816b3-8f58-49ae-bc12-4e18b358d6d9")
    assert dict == res.__class__
    assert 2 == len(res)
    assert 1 == len(res['data'])
    assert 5 == len(res['data'][0])
    assert 'identifier' in res['data'][0].keys()
