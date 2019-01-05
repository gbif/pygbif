.. _registry-modules:

===============
registry module
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


registry API
============

.. py:module:: pygbif

.. automethod:: registry.datasets
.. automethod:: registry.dataset_metrics
.. automethod:: registry.dataset_suggest
.. automethod:: registry.dataset_search
.. automethod:: registry.installations
.. automethod:: registry.networks
.. automethod:: registry.nodes
.. automethod:: registry.organizations
