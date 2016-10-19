pygbif
======

|pypi| |docs| |travis| |coverage|

Python client for the `GBIF API
<http://www.gbif.org/developer/summary>`_

`Source on GitHub at sckott/pygbif <https://github.com/sckott/pygbif>`_

Other GBIF clients:

* R: `rgbif`, `ropensci/rgbif <https://github.com/ropensci/rgbif>`_

Installation
============

Stable from pypi

.. code-block:: console

    pip install pygbif

Development version

.. code-block:: console

    [sudo] pip install git+git://github.com/sckott/pygbif.git#egg=pygbif

`pygbif` is split up into modules for each of the major groups of API methods.

* Registry - Datasets, Nodes, Installations, Networks, Organizations
* Species - Taxonomic names
* Occurrences - Occurrence data, including the download API

You can import the entire library, or each module individually as needed.

Note that `GBIF maps API <http://www.gbif.org/developer/maps>`_ is not included in `pygbif`.

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
    occ.download('basisOfRecord = LITERATURE')
    occ.download('taxonKey = 3119195')
    occ.download('decimalLatitude > 50')
    occ.download_list(user = "sckott", limit = 5)
    occ.download_meta(key = "0000099-140929101555934")
    occ.download_get("0000066-140928181241064")


Contributors
============

* `Scott Chamberlain <https://github.com/sckott>`_
* `Robert Forkel <https://github.com/xrotwang>`_
* `Jan Legind <https://github.com/jlegind>`_
* `Stijn Van Hoey <https://github.com/stijnvanhoey>`_
* `Peter Desmet <https://github.com/peterdesmet>`_

Meta
====

* License: MIT, see `LICENSE file <LICENSE>`_
* Please note that this project is released with a `Contributor Code of Conduct <CONDUCT.md>`_. By participating in this project you agree to abide by its terms.

.. |pypi| image:: https://img.shields.io/pypi/v/pygbif.svg
   :target: https://pypi.python.org/pypi/pygbif

.. |docs| image:: https://readthedocs.org/projects/pygbif/badge/?version=latest
   :target: http://pygbif.rtfd.org/

.. |travis| image:: https://travis-ci.org/sckott/pygbif.svg
   :target: https://travis-ci.org/sckott/pygbif

.. |coverage| image:: https://coveralls.io/repos/sckott/pygbif/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/sckott/pygbif?branch=master
