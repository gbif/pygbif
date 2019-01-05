"""Tests for utils module - wkt_rewind"""
from nose.tools import *
import re
from pygbif import utils

x = 'POLYGON((144.6 13.2, 144.6 13.6, 144.9 13.6, 144.9 13.2, 144.6 13.2))'

def test_wkt_rewind():
    "utils.wkt_rewind - basic test"
    res = utils.wkt_rewind(x)
    assert str == res.__class__

def test_wkt_rewind_digits():
    "utils.wkt_rewind - digits works as expected"
    res = utils.wkt_rewind(x, digits = 3)
    pat = re.compile('\\.[0-9]{3}\\s')
    out = pat.search(res)
    assert re.Match == out.__class__

@raises(TypeError)
def test_wkt_rewind_fails_well():
    "utils.wkt_rewind - fails well"
    utils.wkt_rewind(x, digits = "foo")
