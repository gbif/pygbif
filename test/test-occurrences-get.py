"""Tests for occurrences module - get methods"""
import vcr
from pygbif import occurrences


@vcr.use_cassette("test/vcr_cassettes/test_get.yaml")
def test_get():
    "occurrences.get - basic test"
    res = occurrences.get(key=1986620884)
    assert "dict" == res.__class__.__name__
    assert len(res) > 30
    assert 1986620884 == res["key"]


@vcr.use_cassette("test/vcr_cassettes/test_get_verbatim.yaml")
def test_get_verbatim():
    "occurrences.get_verbatim - basic test"
    res = occurrences.get_verbatim(key=1986620884)
    assert "dict" == res.__class__.__name__
    assert len(res) > 20
    assert 1986620884 == res["key"]


@vcr.use_cassette("test/vcr_cassettes/test_get_fragment.yaml")
def test_get_fragment():
    "occurrences.get_fragment - basic test"
    res = occurrences.get_fragment(key=1986620884)
    assert "dict" == res.__class__.__name__
    assert "HumanObservation" == res["basisOfRecord"]
