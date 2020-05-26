"""Tests for species module - name_suggest methods"""
import vcr
import re
from pygbif import species


@vcr.use_cassette("test/vcr_cassettes/test_name_suggest.yaml")
def test_name_suggest():
    "species.name_suggest - basic test"
    res = species.name_suggest(q="Puma concolor")
    assert list == res.__class__
    assert True == all(
        [bool(re.search("Puma concolor", z["canonicalName"])) for z in res]
    )


@vcr.use_cassette("test/vcr_cassettes/test_name_suggest_paging.yaml")
def test_name_suggest_paging():
    "species.name_suggest - paging"
    res = species.name_suggest(q="Aso", limit=3)
    assert list == res.__class__
    assert 3 == len(res)
