"""Tests for species module - name_lookup methods"""
import vcr
from pygbif import species


@vcr.use_cassette("test/vcr_cassettes/test_name_lookup.yaml")
def test_name_lookup():
    "species.name_lookup - basic test"
    res = species.name_lookup(q="mammalia")
    assert dict == res.__class__
    assert 6 == len(res)
    assert 100 == len(res["results"])
    assert "Mammaliaformes" == res["results"][0]["canonicalName"]


@vcr.use_cassette("test/vcr_cassettes/test_name_lookup_paging.yaml")
def test_name_lookup_paging():
    "species.name_lookup - paging"
    res = species.name_lookup(q="mammalia", limit=1)
    assert dict == res.__class__
    assert 6 == len(res)
    assert 1 == len(res["results"])


@vcr.use_cassette("test/vcr_cassettes/test_name_lookup_rank.yaml")
def test_name_lookup_rank():
    "species.name_lookup - rank parameter"
    res = species.name_lookup("Helianthus annuus", rank="species", limit=10)
    assert dict == res.__class__
    assert 10 == len(res["results"])
    assert "SPECIES" == list(set([x["rank"] for x in res["results"]]))[0]


@vcr.use_cassette("test/vcr_cassettes/test_name_lookup_faceting.yaml")
def test_name_lookup_faceting():
    "species.name_lookup - faceting"
    res = species.name_lookup(facet="status", limit=0)
    assert dict == res.__class__
    assert 6 == len(res)
    assert 0 == len(res["results"])
    assert 1 == len(res["facets"])
    assert 2 == len(res["facets"][0])
