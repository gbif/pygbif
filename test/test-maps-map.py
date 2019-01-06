"""Tests for maps module - map methods"""
from nose.tools import *
import unittest
import os
import vcr
import requests
import matplotlib
import pygbif
# from pygbif import maps

class TestMapsClass(unittest.TestCase):
    
    @vcr.use_cassette('test/vcr_cassettes/test_map.yaml')
    def test_map(self):
        "maps.map - basic test"
        res = pygbif.maps.map(taxonKey = 2435098)
        self.assertIsInstance(res, pygbif.maps.GbifMap)
        self.assertIsInstance(res.response, requests.Response)
        self.assertIsInstance(res.path, str)
        self.assertIsInstance(res.img, matplotlib.image.AxesImage)

    def test_map_year_range(self):
        "maps.map - year range"
        res = pygbif.maps.map(taxonKey = 2435098, year = range(2007, 2011+1))
        self.assertIsInstance(res, pygbif.maps.GbifMap)
        self.assertRegex(res.response.request.path_url, "2007%2C2011")
        # self.assertIsInstance(res.path, str)
        # self.assertIsInstance(res.img, matplotlib.image.AxesImage)

    @raises(ValueError)
    def test_maps_fails_well(self):
        "maps.map - fails well"
        pygbif.maps.map(year = 2300)

