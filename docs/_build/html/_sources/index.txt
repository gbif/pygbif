Python GBIF Client
===========================

Low-level client for the GBIF API.

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


Example Usage
-------------

You can import the entire library

::

    import pygbif

Or each module individually as needed.

::

    ## Registry module
    from pygbif import registry
    registry.dataset_metrics(uuid='3f8a1297-3259-4700-91fc-acc4170b27ce')

    ## Species module
    from pygbif import species
    species.name_suggest(q='Puma concolor')

    ## Occurrences module
    from pygbif import occurrences
    occurrences.search(taxonKey = 3329049)
    occurrences.get(taxonKey = 252408386)
    occurrences.count(isGeoreferenced = True)


Contents
--------

.. toctree::
   :maxdepth: 2

   occurrences
   registry
   species

License
-------

MIT


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

