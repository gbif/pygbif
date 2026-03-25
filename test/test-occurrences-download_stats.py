"""Tests for occurrences module - download_stats methods"""
import pytest
import vcr
from pygbif import occurrences as occ


@vcr.use_cassette("test/vcr_cassettes/test_download_stats.yaml")
def test_download_stats():
    "occurrences.download_stats - basic test"
    res = occ.download_stats()
    assert dict == res.__class__
    assert "results" in res
    assert "count" in res
    assert len(res["results"]) >= 10


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_with_filters.yaml")
def test_download_stats_with_filters():
    "occurrences.download_stats - with date and country filters"
    res = occ.download_stats(
        fromDate="2023-01-01",
        toDate="2023-12-31",
        publishingCountry="US",
        limit=10
    )
    assert dict == res.__class__
    assert "results" in res
    assert len(res["results"]) == 10
    assert "count" in res
    assert res["count"] > 0
    # Verify date filter - all results should be from 2023
    for result in res["results"]:
        if "year" in result:
            assert result["year"] == 2023
        if "month" in result:
            assert 1 <= result["month"] <= 12


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_with_dataset.yaml")
def test_download_stats_with_dataset():
    "occurrences.download_stats - with dataset filter"
    dataset_key = "50c9509d-22c7-4a22-a47d-8c48425ef4a7"
    res = occ.download_stats(
        datasetKey=dataset_key,
        limit=5
    )
    assert dict == res.__class__
    assert "results" in res
    assert len(res["results"]) == 5
    assert "count" in res
    # Should have results since iNaturalist is a major dataset
    assert res["count"] > 0
    # Verify all results have the expected structure and filtered datasetKey
    for result in res["results"]:
        assert "datasetKey" in result
        assert result["datasetKey"] == dataset_key
        assert "numberDownloads" in result or "year" in result


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_with_org.yaml")
def test_download_stats_with_org():
    "occurrences.download_stats - with publishing org filter"
    res = occ.download_stats(
        publishingOrgKey="e2e717bf-551a-4917-bdc9-4fa0f342c530",
        limit=5
    )
    assert dict == res.__class__
    assert "results" in res
    assert "count" in res
    # Results should be limited to this specific org's data
    assert len(res["results"]) <= 5
    assert res["count"] >= 0  # May be 0 if org has no download stats


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_user_country.yaml")
def test_download_stats_user_country():
    "occurrences.download_stats_user_country - basic test"
    res = occ.download_stats_user_country()
    assert dict == res.__class__
    # Response is organized by year, not in a results wrapper
    assert len(res) > 0


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_user_country_with_dates.yaml")
def test_download_stats_user_country_with_dates():
    "occurrences.download_stats_user_country - with date range"
    res = occ.download_stats_user_country(
        fromDate="2023-01",
        toDate="2023-12"
    )
    assert dict == res.__class__
    assert "2023" in res
    assert len(res) > 0
    # Verify date filter - should ONLY have 2023 data
    for year in res.keys():
        assert year == "2023", f"Expected only 2023, but found {year}"


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_user_country_specific.yaml")
def test_download_stats_user_country_specific():
    "occurrences.download_stats_user_country - specific country"
    res = occ.download_stats_user_country(userCountry="US")
    assert dict == res.__class__
    assert len(res) > 0
    # Verify response structure - should have year keys
    for year_key in res.keys():
        # Year keys should be strings representing years
        assert isinstance(year_key, str)


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_records_by_dataset.yaml")
def test_download_stats_records_by_dataset():
    "occurrences.download_stats_records_by_dataset - basic test"
    res = occ.download_stats_records_by_dataset()
    assert dict == res.__class__
    # Response is organized by year, not in a results wrapper
    assert len(res) > 0


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_records_by_dataset_filtered.yaml")
def test_download_stats_records_by_dataset_filtered():
    "occurrences.download_stats_records_by_dataset - with filters"
    res = occ.download_stats_records_by_dataset(
        fromDate="2023-01-01",
        toDate="2023-12-31",
        publishingCountry="DK"
    )
    assert dict == res.__class__
    assert "2023" in res
    assert len(res["2023"]) > 0
    # Verify date filter - should ONLY have 2023 data
    for year in res.keys():
        assert year == "2023", f"Expected only 2023, but found {year}"


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_records_by_dataset_with_datasetkey.yaml")
def test_download_stats_records_by_dataset_with_datasetkey():
    "occurrences.download_stats_records_by_dataset - with dataset filter"
    res = occ.download_stats_records_by_dataset(
        datasetKey="50c9509d-22c7-4a22-a47d-8c48425ef4a7"
    )
    assert dict == res.__class__
    assert len(res) > 0
    # Verify response has year-based structure
    for year, data in res.items():
        assert year.isdigit(), f"Expected year key, got {year}"
        assert isinstance(data, dict)


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_records_by_dataset_with_org.yaml")
def test_download_stats_records_by_dataset_with_org():
    "occurrences.download_stats_records_by_dataset - with org filter"
    res = occ.download_stats_records_by_dataset(
        publishingOrgKey="e2e717bf-551a-4917-bdc9-4fa0f342c530"
    )
    assert dict == res.__class__
    # May return empty dict if org has no download records
    assert len(res) >= 0
    # If there's data, verify structure
    if len(res) > 0:
        for year, data in res.items():
            assert year.isdigit(), f"Expected year key, got {year}"


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_by_dataset.yaml")
def test_download_stats_by_dataset():
    "occurrences.download_stats_by_dataset - basic test"
    res = occ.download_stats_by_dataset()
    assert dict == res.__class__
    # Response is organized by year, not in a results wrapper
    assert len(res) > 0


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_by_dataset_with_dates.yaml")
def test_download_stats_by_dataset_with_dates():
    "occurrences.download_stats_by_dataset - with date range"
    res = occ.download_stats_by_dataset(
        fromDate="2023-06-01",
        toDate="2023-06-30"
    )
    assert dict == res.__class__
    assert "2023" in res
    assert len(res["2023"]) > 0
    # Verify date filter - should ONLY have 2023 data
    for year in res.keys():
        assert year == "2023", f"Expected only 2023, but found {year}"


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_by_dataset_country.yaml")
def test_download_stats_by_dataset_country():
    "occurrences.download_stats_by_dataset - with country filter"
    res = occ.download_stats_by_dataset(
        publishingCountry="GB"
    )
    assert dict == res.__class__
    assert len(res) > 0


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_by_dataset_with_datasetkey.yaml")
def test_download_stats_by_dataset_with_datasetkey():
    "occurrences.download_stats_by_dataset - with dataset filter (iNaturalist)"
    res = occ.download_stats_by_dataset(
        datasetKey="50c9509d-22c7-4a22-a47d-8c48425ef4a7"
    )
    assert dict == res.__class__
    assert len(res) > 0
    # Verify response has year-based structure
    for year, data in res.items():
        assert year.isdigit(), f"Expected year key, got {year}"
        assert isinstance(data, dict)


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_by_dataset_with_org.yaml")
def test_download_stats_by_dataset_with_org():
    "occurrences.download_stats_by_dataset - with org filter"
    res = occ.download_stats_by_dataset(
        publishingOrgKey="e2e717bf-551a-4917-bdc9-4fa0f342c530"
    )
    assert dict == res.__class__
    assert len(res) >= 0
    # If there's data, verify structure
    if len(res) > 0:
        for year, data in res.items():
            assert year.isdigit(), f"Expected year key, got {year}"


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_by_source.yaml")
def test_download_stats_by_source():
    "occurrences.download_stats_by_source - basic test"
    res = occ.download_stats_by_source()
    assert dict == res.__class__
    # Response is organized by year, not in a results wrapper
    assert len(res) > 0


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_by_source_filtered.yaml")
def test_download_stats_by_source_filtered():
    "occurrences.download_stats_by_source - with filters"
    res = occ.download_stats_by_source(
        fromDate="2023-01",
        toDate="2023-12"
    )
    assert dict == res.__class__
    assert "2023" in res
    assert len(res["2023"]) > 0
    # Verify date filter - should ONLY have 2023 data
    for year in res.keys():
        assert year == "2023", f"Expected only 2023, but found {year}"


@vcr.use_cassette("test/vcr_cassettes/test_download_stats_by_source_pygbif.yaml")
def test_download_stats_by_source_pygbif():
    "occurrences.download_stats_by_source - with source filter (pygbif)"
    res = occ.download_stats_by_source(source="pygbif")
    assert dict == res.__class__
    assert len(res) > 0
    # Verify response has year-based structure
    for year, data in res.items():
        assert year.isdigit(), f"Expected year key, got {year}"
        assert isinstance(data, dict)
