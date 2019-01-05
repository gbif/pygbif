.. _species-modules:

==============
species module
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


species API
===========

.. py:module:: pygbif

.. automethod:: species.name_backbone
.. automethod:: species.name_suggest
.. automethod:: species.name_lookup
.. automethod:: species.name_usage
.. automethod:: species.name_parser
