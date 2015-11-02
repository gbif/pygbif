# """Tests for registry module - nodes methods"""
# import os
# from pygbif import registry

# def test_nodes():
#     "Basic test of registry.nodes"
#     res = registry.nodes()
#     assert 'dict' == res.__class__.__name__
#     assert 5 == len(res)
#     assert [u'count', u'endOfRecords', u'limit', u'results', u'offset'] == res.keys()

# def test_nodes_limit():
#     "limit param in registry.nodes"
#     res = registry.nodes(limit=5)
#     assert 'dict' == res.__class__.__name__
#     assert 24 == len(res)
#     assert 252408386 == res['key']

# def test_nodes_return():
#     "data param in registry.nodes"
#     res = registry.nodes(taxonKey = 1052909293)
#     assert 'dict' == res.__class__.__name__
#     assert 5 == len(res)
