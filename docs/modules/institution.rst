.. _institution-modules:

=========================
institution module
=========================

institution module API:

* `search`

Example usage:
.. code-block:: python
    
    from pygbif import institution as inst
    inst.search(q="Kansas")
    inst.search(numberSpecimens = "1000,*")
    inst.search(source = "IH_IRN") 
    inst.search(country = ["US","GB"])
    inst.search(typeSpecimenCount = "10,100")

institution API
===============
.. py:module:: pygbif
   :noindex:

.. automethod:: institution.search
