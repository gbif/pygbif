.. _occurrence-modules:

=================
occurrence module
=================

occurrence module API:

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
    occ.get(key = 1986559641)
    occ.count(isGeoreferenced = True)
    occ.download('basisOfRecord = LITERATURE')
    occ.download('taxonKey = 3119195')
    occ.download('decimalLatitude > 50')
    occ.download_list(user = "sckott", limit = 5)
    occ.download_meta(key = "0000099-140929101555934")
    occ.download_get("0000066-140928181241064")


occurrences API
===============


.. py:module:: pygbif

.. automethod:: occurrences.search
.. automethod:: occurrences.get
.. automethod:: occurrences.get_verbatim
.. automethod:: occurrences.get_fragment
.. automethod:: occurrences.count
.. automethod:: occurrences.count_basisofrecord
.. automethod:: occurrences.count_year
.. automethod:: occurrences.count_datasets
.. automethod:: occurrences.count_countries
.. automethod:: occurrences.count_schema
.. automethod:: occurrences.count_publishingcountries
.. automethod:: occurrences.download
.. automethod:: occurrences.download_meta
.. automethod:: occurrences.download_list
.. automethod:: occurrences.download_get
