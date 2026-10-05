"""Tests for species module - name_suggest methods"""
import vcr
import re
import requests
from urllib.parse import parse_qs, urlsplit
from pygbif import species


@vcr.use_cassette("test/vcr_cassettes/test_name_suggest.yaml")
def test_name_suggest():
    "species.name_suggest - basic test"
    res = species.name_suggest(q="Puma concolor")
    assert list == res.__class__
    assert True == all(
        [bool(re.search("Puma concolor", z["canonicalName"])) for z in res]
    )


@vcr.use_cassette("test/vcr_cassettes/test_name_suggest_paging.yaml")
def test_name_suggest_paging():
    "species.name_suggest - paging"
    res = species.name_suggest(q="Aso", limit=3)
    assert list == res.__class__
    assert 3 == len(res)


def sent_query(monkeypatch, **kwargs):
    "Call name_suggest offline and return the query string it sent"
    sent = []

    def send(session, request, **send_kwargs):
        sent.append(request)
        res = requests.Response()
        res.status_code = 200
        res.headers["content-type"] = "application/json"
        res._content = b"[]"
        return res

    monkeypatch.setattr(requests.Session, "send", send)
    species.name_suggest(q="Puma", **kwargs)
    return parse_qs(urlsplit(sent[0].url).query)


def test_name_suggest_datasetKey(monkeypatch):
    "species.name_suggest - datasetKey is sent"
    key = "7ddf754f-d193-4cc9-b351-99906754a03b"
    query = sent_query(monkeypatch, datasetKey=key)
    assert query == {"q": ["Puma"], "datasetKey": [key], "limit": ["100"]}


def test_name_suggest_no_datasetKey(monkeypatch):
    "species.name_suggest - request unchanged without datasetKey"
    assert sent_query(monkeypatch) == {"q": ["Puma"], "limit": ["100"]}
