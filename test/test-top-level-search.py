"""Tests for the top-level namespace - search name (issue #213)"""
import pygbif


def test_search_is_occurrence_search():
    "top-level search - resolves to occurrences.search"
    assert pygbif.search is pygbif.occurrences.search


def test_other_searches_stay_in_their_namespace():
    "top-level namespace - literature/collection/institution search not clobbered"
    assert pygbif.literature.search is not pygbif.search
    assert pygbif.collection.search is not pygbif.search
    assert pygbif.institution.search is not pygbif.search
