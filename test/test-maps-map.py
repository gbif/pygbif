"""Tests for maps module - maps"""
import pytest
import unittest
import vcr
import requests
import matplotlib

matplotlib.use("Agg")
import pygbif


class TestMapsClass(unittest.TestCase):
    @vcr.use_cassette("test/vcr_cassettes/test_map.yaml")
    def test_map(self):
        "maps.map - basic test"
        res = pygbif.maps.map(taxonKey=2435098)
        self.assertIsInstance(res, pygbif.maps.GbifMap)
        self.assertIsInstance(res.response, requests.Response)
        self.assertIsInstance(res.path, str)
        self.assertIsInstance(res.img, matplotlib.image.AxesImage)

    def test_map_year_range(self):
        "maps.map - year range"
        res = pygbif.maps.map(taxonKey=2435098, year=range(2007, 2011 + 1))
        self.assertIsInstance(res, pygbif.maps.GbifMap)
        self.assertRegex(res.response.request.path_url, "2007%2C2011")
        # self.assertIsInstance(res.path, str)
        # self.assertIsInstance(res.img, matplotlib.image.AxesImage)

    def test_map_basisofrecord_str_class(self):
        "maps.map - basisofrecord"
        res = pygbif.maps.map(
            taxonKey=2480498, year=2010, basisOfRecord="HUMAN_OBSERVATION"
        )
        self.assertIsInstance(res, pygbif.maps.GbifMap)
        self.assertRegex(res.response.request.path_url, "basisOfRecord")
        self.assertRegex(res.response.request.path_url, "HUMAN_OBSERVATION")

    def test_map_basisofrecord_list_class(self):
        "maps.map - basisofrecord"
        res = pygbif.maps.map(
            taxonKey=2480498,
            year=2010,
            basisOfRecord=["HUMAN_OBSERVATION", "LIVING_SPECIMEN"],
        )
        self.assertIsInstance(res, pygbif.maps.GbifMap)
        self.assertRegex(res.response.request.path_url, "basisOfRecord")
        self.assertRegex(res.response.request.path_url, "HUMAN_OBSERVATION")
        self.assertRegex(res.response.request.path_url, "LIVING_SPECIMEN")

    def test_maps_fails_well(self):
        "maps.map - fails well"
        with pytest.raises(ValueError):
            pygbif.maps.map(year=2300)
            pygbif.maps.map(year="2010")
            pygbif.maps.map(basisOfRecord="foobar")
            pygbif.maps.map(format="foobar")
            pygbif.maps.map(source="foobar")
            pygbif.maps.map(srs="foobar")
            pygbif.maps.map(bin="foobar")
            pygbif.maps.map(style="foobar")
