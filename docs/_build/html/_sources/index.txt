Python GBIF Client
===========================

Low-level client for the GBIF API.

`pygbif` is split up into modules for each of the major groups of API methods.

* Registry - Datasets, Nodes, Installations, Networks, Organizations
* Species - Taxonomic names
* Occurrences - Occurrence data, including the download API

You can import the entire library, or each module individually as needed.

Note that GBIF maps API_ is not included in `pygbif`.

.. _API: http://www.gbif.org/developer/maps

Installation
-------------

::

    pip install pygbif


Example Usage
-------------

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

