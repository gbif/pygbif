"""Tests for registry module - dataset_metrics method"""
import vcr
from pygbif import registry


@vcr.use_cassette("test/vcr_cassettes/test_dataset_metrics.yaml")
def test_dataset_metrics():
    "registry.dataset_metrics - basic test"
    res = registry.dataset_metrics(uuid="3f8a1297-3259-4700-91fc-acc4170b27ce")
    assert dict == res.__class__
    assert 18 == len(res)


@vcr.use_cassette("test/vcr_cassettes/test_dataset_metrics_multiple_uuids.yaml")
def test_dataset_metrics_multiple_uuids():
    "registry.dataset_metrics - multiple uuids"
    uuids = [
        "3f8a1297-3259-4700-91fc-acc4170b27ce",
        "66dd0960-2d7d-46ee-a491-87b9adcfe7b1",
    ]
    res = registry.dataset_metrics(uuids)
    assert list == res.__class__
    assert 2 == len(res)
