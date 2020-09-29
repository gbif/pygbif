.. _utils-modules:

============
utils module
============

utils module API:

* `wkt_rewind`

Example usage:

.. code-block:: python

    from pygbif import utils
    x = 'POLYGON((144.6 13.2, 144.6 13.6, 144.9 13.6, 144.9 13.2, 144.6 13.2))'
    utils.wkt_rewind(x)


utils API
=========

.. py:module:: pygbif
  :noindex:

.. automethod:: utils.wkt_rewind
