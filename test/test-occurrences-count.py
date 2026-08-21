"""Tests for occurrences module - count methods"""
import pytest
import warnings
import vcr
from pygbif import occurrences

brecord_res = [
    "HUMAN_OBSERVATION",
    "PRESERVED_SPECIMEN", 
    "MATERIAL_SAMPLE", 
    "OBSERVATION", 
    "MACHINE_OBSERVATION", 
    "OCCURRENCE", 
    "FOSSIL_SPECIMEN", 
    "MATERIAL_CITATION", 
    "LIVING_SPECIMEN"
]

year_res = [
    "1991",
    "1990",
    "1993",
    "1992",
    "1995",
    "1994",
    "1997",
    "1996",
    "1999",
    "1998",
    "2000",
]


@vcr.use_cassette("test/vcr_cassettes/test_count.yaml")
def test_count():
    "occurrences.count - basic test"
    res = occurrences.count(taxonKey="5TYZ9")
    assert int == res.__class__


def test_count_param_length():
    "occurrences.count_param_length"
    with pytest.raises(TypeError):
        occurrences.count(datasetKey=["foo", "bar"])


@vcr.use_cassette("test/vcr_cassettes/test_count_basisofrecord.yaml")
def test_count_basisofrecord():
    "occurrences.count_basisofrecord - basic test"
    res = occurrences.count_basisofrecord()
    assert dict == res.__class__
    assert 9 == len(res)
    assert sorted(brecord_res) == sorted(res.keys())


@vcr.use_cassette("test/vcr_cassettes/test_count_year.yaml")
def test_count_year():
    "occurrences.count_year - basic test"
    res = occurrences.count_year(year="1990,2000")
    assert dict == res.__class__
    assert 11 == len(res)
    assert sorted(year_res) == sorted(res.keys())


@vcr.use_cassette("test/vcr_cassettes/test_count_datasets.yaml")
def test_count_datasets():
    "occurrences.count_datasets - basic test"
    res = occurrences.count_datasets(country="DE")
    assert dict == res.__class__
    assert str == str(list(res.keys())[0]).__class__


@vcr.use_cassette("test/vcr_cassettes/test_count_countries.yaml")
def test_count_countries():
    "occurrences.count_countries - basic test"
    res = occurrences.count_countries(publishingCountry="DE")
    assert dict == res.__class__
    assert str == str(list(res.keys())[0]).__class__
    assert int == list(res.values())[0].__class__


@vcr.use_cassette("test/vcr_cassettes/test_count_schema.yaml")
def test_count_schema():
    "occurrences.count_schema - basic test"
    res = occurrences.count_schema()
    assert list == res.__class__
    assert dict == res[0].__class__
    assert "dimensions" == list(res[0].keys())[0]


@vcr.use_cassette("test/vcr_cassettes/test_count_publishingcountries.yaml")
def test_count_publishingcountries():
    "occurrences.count_publishingcountries - basic test"
    res = occurrences.count_publishingcountries(country="DE")
    assert dict == res.__class__
    assert str == str(list(res.keys())[0]).__class__
    assert int == list(res.values())[0].__class__


def test_count_numeric_key_deprecation_warning():
    "occurrences.count - numeric taxonKey triggers deprecation warning"
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        res = occurrences.count(taxonKey=3329049)
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "Numeric taxonKey detected" in str(w[-1].message)
        assert "gbif_to_col" in str(w[-1].message)
        assert int == res.__class__


def test_count_numeric_key_explicit_checklistkey_no_warning():
    "occurrences.count - numeric taxonKey with explicit checklistKey doesn't warn"
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        res = occurrences.count(taxonKey=3329049, checklistKey=None)
        # Filter out non-DeprecationWarning warnings
        deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
        assert len(deprecation_warnings) == 0
        assert int == res.__class__


def test_count_datasets_numeric_key_deprecation_warning():
    "occurrences.count_datasets - numeric taxonKey triggers deprecation warning"
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        res = occurrences.count_datasets(taxonKey=3329049)
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "Numeric taxonKey detected" in str(w[-1].message)
        assert dict == res.__class__
