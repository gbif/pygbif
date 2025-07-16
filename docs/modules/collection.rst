.. _collection-modules:

=========================
collection module
=========================

collection module API:

* `search`

Example usage:

.. code-block:: python

    from pygbif import collection as coll
    coll.search(query="insect")
    coll.search(name="Insects;Entomology", limit=2)
    coll.search(numberSpecimens = "0,100", limit=1)
    coll.search(institutionKey = "6a6ac6c5-1b8a-48db-91a2-f8661274ff80")
    coll.search(query = "insect", country = ["US","GB"])

collection API
===============

.. py:module:: pygbif
   :noindex:

.. automethod:: collection.search
