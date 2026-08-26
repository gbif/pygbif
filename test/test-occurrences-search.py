"""Tests for occurrences module - search methods"""
import vcr
import warnings
from pygbif import occurrences

keyz = ["count", "facets", "results", "endOfRecords", "limit", "offset"]
x = "https://orcid.org/0000-0003-1691-239X"


@vcr.use_cassette("test/vcr_cassettes/test_search.yaml")
def test_search():
    "occurrences.search - basic test"
    res = occurrences.search(taxonKey="5TYZ9")  # Amanita muscaria (COL key)
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    assert sorted(keyz) == sorted(res.keys())


@vcr.use_cassette("test/vcr_cassettes/test_search_key1.yaml")
def test_search_key1():
    "occurrences.search - diff taxonKey"
    res = occurrences.search(taxonKey="KZQN")  # Batrachoseps luciae (COL key)
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    # COL key is in the classifications field when using COL checklist
    assert "KZQN" == res["results"][0]["classifications"]["7ddf754f-d193-4cc9-b351-99906754a03b"]["usage"]["key"]


@vcr.use_cassette("test/vcr_cassettes/test_search_key2.yaml")
def test_search_key2():
    "occurrences.search - diff taxonKey2"
    res = occurrences.search(taxonKey="32S2L")  # Cycas circinalis (COL key)
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    # COL key is in the classifications field when using COL checklist
    assert "32S2L" == res["results"][0]["classifications"]["7ddf754f-d193-4cc9-b351-99906754a03b"]["usage"]["key"]


@vcr.use_cassette("test/vcr_cassettes/test_search_recorded_by_id.yaml")
def test_search_recorded_by_id():
    "occurrences.search - recordedByID"
    res = occurrences.search(recordedByID=x, limit=3)
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    assert x == res["results"][0]["recordedByIDs"][0]["value"]


@vcr.use_cassette("test/vcr_cassettes/test_search_identified_by_id.yaml")
def test_search_identified_by_id():
    "occurrences.search - identifiedByID"
    res = occurrences.search(identifiedByID=x, limit=3)
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    assert x == res["results"][0]["identifiedByIDs"][0]["value"]

@vcr.use_cassette("test/vcr_cassettes/test_search_checklistKey.yaml")
def test_search_checklistKey():
    "occurrences.search - checklistKey"
    res = occurrences.search(checklistKey="7ddf754f-d193-4cc9-b351-99906754a03b", limit=3)
    assert "dict" == res.__class__.__name__
    assert 6 == len(res)
    res["results"][0]["classifications"]["7ddf754f-d193-4cc9-b351-99906754a03b"]["usage"]["key"]
    assert isinstance(res["results"][0]["classifications"]["7ddf754f-d193-4cc9-b351-99906754a03b"]["usage"]["key"], str)


@vcr.use_cassette("test/vcr_cassettes/test_search_numeric_key_warning.yaml")
def test_search_numeric_key_deprecation_warning():
    "occurrences.search - numeric key triggers deprecation warning"
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        res = occurrences.search(taxonKey=3329049, limit=1)
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "Numeric taxonomy keys detected" in str(w[-1].message)
        assert "gbif_to_col" in str(w[-1].message)
        assert "dict" == res.__class__.__name__


@vcr.use_cassette("test/vcr_cassettes/test_search_numeric_key_explicit_checklist.yaml")
def test_search_numeric_key_explicit_checklistKey_no_warning():
    "occurrences.search - explicit checklistKey with numeric key has no warning"
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        res = occurrences.search(taxonKey=3329049, checklistKey="7ddf754f-d193-4cc9-b351-99906754a03b", limit=1)
        # Filter out non-DeprecationWarnings from our code (like dateutil warnings)
        relevant_warnings = [warning for warning in w if "Numeric taxonomy keys" in str(warning.message)]
        assert len(relevant_warnings) == 0
        assert "dict" == res.__class__.__name__
