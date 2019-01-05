.. _usecases:

Usecases
========

Use case 1: Get occurrence data for a set of taxonomic names
------------------------------------------------------------

Load library

.. code-block:: python

    from pygbif import species as species
    from pygbif import occurrences as occ

First, get GBIF backbone taxonomic keys

.. code-block:: python

    splist = ['Cyanocitta stelleri', 'Junco hyemalis', 'Aix sponsa',
      'Ursus americanus', 'Pinus conorta', 'Poa annuus']
    keys = [ species.name_backbone(x)['usageKey'] for x in splist ]

Then, get a count of occurrence records for each taxon, and pull out
number of records found for each taxon

.. code-block:: python

    out = [ occ.search(taxonKey = x, limit=0)['count'] for x in keys ]

Make a dict of species names and number of records, sorting in
descending order

.. code-block:: python

		x = dict(zip(splist, out))
		sorted(x.items(), key=lambda z:z[1], reverse=True)

