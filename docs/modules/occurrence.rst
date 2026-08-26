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
* `download_sql`
* `download_describe`
* `download_citation`

Example usage:

.. code-block:: python

    from pygbif import occurrences as occ
    occ.search(taxonKey = 3329049)
    occ.get(key = 1986559641)
    occ.count(isGeoreferenced = True)
    occ.download('basisOfRecord = PRESERVED_SPECIMEN')
    occ.download('taxonKey = 3119195')
    occ.download('decimalLatitude > 50')
    
    # Using custom taxonomy checklist
    # By default, Catalogue of Life (COL) Extended Release is used
    # Use alphanumeric COL keys directly
    occ.download('taxonKey = 5WZLF')  # COL key (default)
    # Or explicitly set checklistKey=None to use GBIF Backbone (deprecated)
    occ.download('taxonKey = 3119195', checklistKey=None)
    
    occ.download_list(user = "sckott", limit = 5)
    occ.download_meta(key = "0000099-140929101555934")
    occ.download_get("0000066-140928181241064")
    occ.download_sql("SELECT datasetKey, countryCode, COUNT(*) FROM occurrence WHERE continent = 'EUROPE' GROUP BY datasetKey, countryCode")
    occ.download_describe("simpleCsv")
    occ.download_citation("0002526-241107131044228")

.. note::
    Download endpoints require GBIF credentials.
    Set them as environment variables:

    .. code-block:: bash

        export GBIF_USER="your_gbif_username"
        export GBIF_PWD="your_gbif_password"

    You can also pass credentials directly via ``user=`` and ``pwd=`` arguments.

.. note::
    **Custom Taxonomy Checklists (checklistKey)**
    
    Users can specify the taxonomy to be included in occurrence downloads by 
    adding the ``checklistKey`` parameter. By default, the Catalogue of Life (COL) 
    Extended Release (7ddf754f-d193-4cc9-b351-99906754a03b) will be used if no 
    ``checklistKey`` is supplied. Set ``checklistKey=None`` to use the deprecated 
    GBIF Backbone Taxonomy instead.
    
    The ``checklistKey`` parameter accepts a UUID of a checklist from ChecklistBank
    and can be used in two ways:
    
    1. **Root-level (Global)**: Added as a parameter to the download function, it 
       applies globally to all predicates in the download request.
       
    2. **Predicate-level (Search Filtering)**: Included within individual predicates 
       to specify the taxonomy to be used for filtering occurrence records for that 
       specific predicate.
    
    Examples:
    
    .. code-block:: python
    
        # Root-level: applies to entire download
        occ.download('taxonKey = 5WZLF', 
                     checklistKey='7ddf754f-d193-4cc9-b351-99906754a03b')
        
        # Predicate-level: for filtering specific predicates
        query = {
            "type": "equals",
            "key": "TAXON_KEY",
            "value": "5WZLF",
            "checklistKey": "7ddf754f-d193-4cc9-b351-99906754a03b"
        }
        occ.download(query)


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
.. automethod:: occurrences.download_sql
.. automethod:: occurrences.download_describe
.. automethod:: occurrences.download_citation
    
