Python GBIF Client
===========================

|pypi| |docs| |travis| |coverage|

Python client for the `GBIF API
<http://www.gbif.org/developer/summary>`__.

`Source on GitHub at sckott/pygbif <https://github.com/sckott/pygbif>`__

`pygbif` is split up into modules for each of the major groups of API methods.

* Registry - Datasets, Nodes, Installations, Networks, Organizations - `Registry API Docs`_
* Species - Taxonomic names - `Species API Docs`_
* Occurrences - Occurrence data, including the download API - `Occurrences API Docs`_

Note that GBIF maps API_ is not included in `pygbif`.

.. _API: http://www.gbif.org/developer/maps

Other GBIF clients:

* R: rgbif_

.. _rgbif: https://github.com/ropensci/rgbif
.. _Registry API Docs: http://www.gbif.org/developer/registry
.. _Species API Docs: http://www.gbif.org/developer/species
.. _Occurrences API Docs: http://www.gbif.org/developer/occurrences

Installation
-------------

::

    pip install pygbif


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

    from pygbif import occurrences as occ
    occ.search(taxonKey = 3329049)
    occ.get(key = 252408386)
    occ.count(isGeoreferenced = True)
    occ.download_list(user = "sckott", limit = 5)
    occ.download_meta(key = "0000099-140929101555934")
    occ.download_get("0000066-140928181241064")


Contributors
============

* `Scott Chamberlain <https://github.com/sckott>`__
* `Robert Forkel <https://github.com/xrotwang>`__
* `Jan Legind <https://github.com/jlegind>`__
* `Stijn Van Hoey <https://github.com/stijnvanhoey>`__
* `Peter Desmet <https://github.com/peterdesmet>`__


Meta
====

* License: MIT, see `LICENSE file <LICENSE>`__
* Please note that this project is released with a `Contributor Code of Conduct <CONDUCT.md>`__. By participating in this project you agree to abide by its terms.

.. |pypi| image:: https://img.shields.io/pypi/v/pygbif.svg
   :target: https://pypi.python.org/pypi/pygbif

.. |docs| image:: https://readthedocs.org/projects/pygbif/badge/?version=latest
   :target: http://pygbif.rtfd.org/

.. |travis| image:: https://travis-ci.org/sckott/pygbif.svg
   :target: https://travis-ci.org/sckott/pygbif

.. |coverage| image:: https://coveralls.io/repos/sckott/pygbif/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/sckott/pygbif?branch=master


Contents
--------

.. toctree::
   :maxdepth: 2

   occurrences
   registry
   species
   changelog_link

License
-------

MIT


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

