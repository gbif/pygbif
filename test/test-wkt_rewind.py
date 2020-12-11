"""Tests for utils module - wkt_rewind"""
import pytest
import unittest
import re
from pygbif import utils

x = "POLYGON((144.6 13.2, 144.6 13.6, 144.9 13.6, 144.9 13.2, 144.6 13.2))"


def test_wkt_rewind():
    "utils.wkt_rewind - basic test"
    res = utils.wkt_rewind(x)
    assert str == res.__class__


class TestWKTClass(unittest.TestCase):
    def test_wkt_rewind_digits(self):
        "utils.wkt_rewind - digits works as expected"
        res = utils.wkt_rewind(x, digits=3)
        pat = re.compile("\\.[0-9]{3}\\s")
        out = pat.search(res)
        self.assertIsInstance(out.string, str)


def test_wkt_rewind_fails_well():
    "utils.wkt_rewind - fails well"
    with pytest.raises(TypeError):
        utils.wkt_rewind(x, digits="foo")
