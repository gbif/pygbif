pygbif
=======

|pypi| |docs| |travis| |coverage|

Python client for the `GBIF API
<http://www.gbif.org/developer/summary>`__.

`Source on GitHub at sckott/pygbif <https://github.com/sckott/pygbif>`__

Other GBIF clients:

* R: `rgbif`, `ropensci/rgbif <https://github.com/ropensci/rgbif>`__

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

Note that `GBIF maps API <http://www.gbif.org/developer/maps>`__ is not included in `pygbif`.

Registry module
===============

.. code-block:: python

		from pygbif import registry
		registry.dataset_metrics(uuid='3f8a1297-3259-4700-91fc-acc4170b27ce')

Species module
===============

.. code-block:: python

		from pygbif import species
		species.name_suggest(q='Puma concolor')

Occurrences module
==================

.. code-block:: python

		from pygbif import occurrences
		occurrences.search(taxonKey = 3329049)
		occurrences.get(taxonKey = 252408386)
		occurrences.count(isGeoreferenced = True)

Meta
====

* License: MIT, see `LICENSE file <LICENSE>`__
* Please note that this project is released with a `Contributor Code of Conduct <CONDUCT.md>`__. By participating in this project you agree to abide by its terms.

.. |pypi| image:: https://img.shields.io/pypi/v/habanero.svg
   :target: https://pypi.python.org/pypi/habanero

.. |docs| image:: https://readthedocs.org/projects/pygbif/badge/?version=latest
   :target: http://pygbif.rtfd.org/

.. |travis| image:: https://travis-ci.org/sckott/pygbif.svg
   :target: https://travis-ci.org/sckott/pygbif

.. |coverage| image:: https://coveralls.io/repos/sckott/pygbif/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/sckott/pygbif?branch=master
