pygbif
======

|pypi| |docs| |ghactions| |coverage| |black|

Python client for the `GBIF API <https://www.gbif.org/developer/summary>`_

`Source on GitHub at gbif/pygbif <https://github.com/gbif/pygbif>`_

Other GBIF clients:

* R: `rgbif`, `ropensci/rgbif <https://github.com/ropensci/rgbif>`_
* Ruby: `gbifrb`, `sckott/gbifrb <https://github.com/sckott/gbifrb>`_
* PHP: `php-gbif`, `restelae/php-gbif <https://gitlab.res-telae.cat/restelae/php-gbif>`_

Contributing: `CONTRIBUTING.md <https://github.com/gbif/pygbif/blob/master/.github/CONTRIBUTING.md>`_

Installation
============

Stable from pypi

.. code-block:: console

    pip install pygbif

Development version

.. code-block:: console

    [sudo] pip install git+git://github.com/gbif/pygbif.git#egg=pygbif


`pygbif` is split up into modules for each of the major groups of API methods.

* Registry - Datasets, Nodes, Installations, Networks, Organizations
* Species - Taxonomic names
* Occurrences - Occurrence data, including the download API
* Maps - Maps, get raster maps from GBIF as png or mvt

You can import the entire library, or each module individually as needed.

In addition there is a utils module, currently with one method: `wkt_rewind`, and
a `caching` method to manage whether HTTP requests are cached or not. See `?pygbif.caching`.

Registry module
===============

registry module API:

* `organizations`
* `nodes`
* `networks`
* `installations`
* `datasets`
* `dataset_metrics`
* `dataset_suggest`
* `dataset_search`

Example usage:

.. code-block:: python

    from pygbif import registry
    registry.dataset_metrics(uuid='3f8a1297-3259-4700-91fc-acc4170b27ce')

Species module
==============

species module API:

* `name_backbone`
* `name_suggest`
* `name_usage`
* `name_lookup`
* `name_parser`

Example usage:

.. code-block:: python

    from pygbif import species
    species.name_suggest(q='Puma concolor')

Occurrences module
==================

registry module API:

* `search`
* `get`
* `get_verbatim`
* `get_fragment`
* `count`
* `count_basisofrecord`
* `count_year`
* `count_datasets`
* `count_countries`
* `count_schema`
* `count_publishingcountries`
* `download`
* `download_meta`
* `download_list`
* `download_get`

Example usage:

.. code-block:: python

    from pygbif import occurrences as occ
    occ.search(taxonKey = 3329049)
    occ.get(key = 252408386)
    occ.count(isGeoreferenced = True)
    occ.download('basisOfRecord = PRESERVED_SPECIMEN')
    occ.download('taxonKey = 3119195')
    occ.download('decimalLatitude > 50')
    occ.download_list(user = "sckott", limit = 5)
    occ.download_meta(key = "0000099-140929101555934")
    occ.download_get("0000066-140928181241064")

Maps module
===========

maps module API:

* `map`

Example usage:

.. code-block:: python

    from pygbif import maps
    out = maps.map(taxonKey = 212, year = 1998, bin = "hex",
           hexPerTile = 30, style = "classic-noborder.poly")
    out.response
    out.path
    out.img
    out.plot()

.. image:: https://github.com/gbif/pygbif/raw/master/gbif_map.png
   :width: 25%
   :scale: 25%

utils module
============

utils module API:

* `wkt_rewind`

Example usage:

.. code-block:: python

    from pygbif import utils
    x = 'POLYGON((144.6 13.2, 144.6 13.6, 144.9 13.6, 144.9 13.2, 144.6 13.2))'
    utils.wkt_rewind(x)



Contributors
============

* `Scott Chamberlain <https://github.com/sckott>`_
* `Robert Forkel <https://github.com/xrotwang>`_
* `Jan Legind <https://github.com/jlegind>`_
* `Stijn Van Hoey <https://github.com/stijnvanhoey>`_
* `Peter Desmet <https://github.com/peterdesmet>`_
* `Nicolas Noé <https://github.com/niconoe>`_

Meta
====

* License: MIT, see `LICENSE file <LICENSE>`_
* Please note that this project is released with a `Contributor Code of Conduct <CONDUCT.md>`_. By participating in this project you agree to abide by its terms.

.. |pypi| image:: https://img.shields.io/pypi/v/pygbif.svg
   :target: https://pypi.python.org/pypi/pygbif

.. |docs| image:: https://readthedocs.org/projects/pygbif/badge/?version=latest
   :target: http://pygbif.rtfd.org/

.. |ghactions| image:: https://github.com/gbif/pygbif/workflows/Python/badge.svg
   :target: https://github.com/gbif/pygbif/actions?query=workflow%3APython

.. |coverage| image:: https://codecov.io/gh/gbif/pygbif/branch/master/graph/badge.svg?token=frXPREGk1D
   :target: https://codecov.io/gh/gbif/pygbif

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black


