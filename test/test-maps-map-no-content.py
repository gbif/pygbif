"""Map responses with no content must not be decoded as PNG images."""

import importlib
from io import BytesIO
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import pytest
import requests

from pygbif import maps
from pygbif.gbifutils import NoResultException


@pytest.fixture
def map_response(monkeypatch, tmp_path):
    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "image/png"
    response._content = b""
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: response)
    map_module = importlib.import_module("pygbif.maps.map")
    monkeypatch.setattr(map_module, "user_cache_dir", lambda app: str(tmp_path))
    figures = set(plt.get_fignums())
    yield response
    for figure in set(plt.get_fignums()) - figures:
        plt.close(figure)


def test_map_no_content(map_response):
    map_response.status_code = 204
    figures = plt.get_fignums()

    result = maps.map(z=10, x=10, y=10)

    assert isinstance(result, maps.GbifMap)
    assert result.response is map_response
    assert "Content-Length" not in result.response.headers
    assert Path(result.path).suffix == ".png"
    assert Path(result.path).read_bytes() == b""
    assert result.img is None
    assert result.plot() is None
    assert plt.get_fignums() == figures


def test_map_png_content(map_response):
    image = BytesIO()
    Image.new("RGB", (1, 1), "red").save(image, format="PNG")
    map_response._content = image.getvalue()

    result = maps.map()

    assert result.response is map_response
    assert Path(result.path).read_bytes() == map_response.content
    assert isinstance(result.img, matplotlib.image.AxesImage)
    assert result.img.get_array().shape == (1, 1, 3)


@pytest.mark.parametrize("content", [b"", b"not a PNG"])
def test_map_invalid_png_still_raises(map_response, content):
    map_response._content = content

    with pytest.raises(SyntaxError, match="not a PNG file"):
        maps.map()


def test_map_vector_content(map_response):
    map_response.headers["Content-Type"] = "application/x-protobuf"
    map_response._content = b"vector tile"
    figures = plt.get_fignums()

    result = maps.map(format=".mvt")

    assert result.response is map_response
    assert Path(result.path).suffix == ".mvt"
    assert Path(result.path).read_bytes() == map_response.content
    assert result.img is None
    assert result.plot() is None
    assert plt.get_fignums() == figures


@pytest.mark.parametrize("status", [404, 500])
def test_map_http_error_still_raises(map_response, tmp_path, status):
    map_response.status_code = status

    with pytest.raises(requests.HTTPError):
        maps.map()

    assert list(tmp_path.iterdir()) == []


def test_map_unexpected_content_type_still_raises(map_response, tmp_path):
    map_response.headers["Content-Type"] = "text/html"

    with pytest.raises(NoResultException):
        maps.map()

    assert list(tmp_path.iterdir()) == []
