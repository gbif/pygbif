"""Tests for occurrences module - count methods"""
import os
from pygbif import occurrences

brecord_res = [u'LITERATURE',
 u'OBSERVATION',
 u'LIVING_SPECIMEN',
 u'UNKNOWN',
 u'MATERIAL_SAMPLE',
 u'PRESERVED_SPECIMEN',
 u'MACHINE_OBSERVATION',
 u'HUMAN_OBSERVATION',
 u'FOSSIL_SPECIMEN']

year_res = [u'1991',
 u'1990',
 u'1993',
 u'1992',
 u'1995',
 u'1994',
 u'1997',
 u'1996',
 u'1999',
 u'1998',
 u'2000']

def test_count():
    "Basic test of occurrences.count"
    res = occurrences.count(taxonKey = 3329049)
    assert int == res.__class__

def test_count_basisofrecord():
    "Basic test of occurrences.count_basisofrecord"
    res = occurrences.count_basisofrecord()
    assert dict == res.__class__
    assert 9 == len(res)
    assert brecord_res == res.keys()

def test_count_year():
    "Basic test of occurrences.count_year"
    res = occurrences.count_year(year = '1990,2000')
    assert dict == res.__class__
    assert 11 == len(res)
    assert year_res == res.keys()

def test_count_datasets():
    "Basic test of occurrences.count_datasets"
    res = occurrences.count_datasets(country = "DE")
    assert dict == res.__class__
    assert unicode == res.keys()[0].__class__

def test_count_countries():
    "Basic test of occurrences.count_countries"
    res = occurrences.count_countries(publishingCountry = "DE")
    assert dict == res.__class__
    assert unicode == res.keys()[0].__class__
    assert int == res.values()[0].__class__

def test_count_schema():
    "Basic test of occurrences.count_schema"
    res = occurrences.count_schema()
    assert list == res.__class__
    assert dict == res[0].__class__
    assert "dimensions" == res[0].keys()[0]

def test_count_publishingcountries():
    "Basic test of occurrences.count_publishingcountries"
    res = occurrences.count_publishingcountries(country = "DE")
    assert dict == res.__class__
    assert unicode == res.keys()[0].__class__
    assert int == res.values()[0].__class__
