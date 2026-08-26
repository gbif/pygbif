import warnings
from pygbif.gbifutils import gbif_baseurl, bool2str, gbif_GET, check_param_lens

# Sentinel value to distinguish default checklistKey from explicit None
_DEFAULT_CHECKLIST = object()


def count(
    taxonKey=None,
    basisOfRecord=None,
    country=None,
    isGeoreferenced=None,
    datasetKey=None,
    publishingCountry=None,
    typeStatus=None,
    issue=None,
    year=None,
    checklistKey=_DEFAULT_CHECKLIST,
    **kwargs
):
    """
    Returns occurrence counts for a predefined set of dimensions

    For all parameters below, only one value allowed per function call.
    See :func:`~occurrences.search` for passing more than one value
    per parameter.

    :param taxonKey: [int/str] A taxon key from a checklist. Can be a GBIF Backbone
        integer key (deprecated, use COL instead) or a COL Extended Release alphanumeric key.
    :param basisOfRecord: [str] A GBIF occurrence identifier
    :param country: [str] A GBIF occurrence identifier
    :param isGeoreferenced: [bool] A GBIF occurrence identifier
    :param datasetKey: [str] A GBIF occurrence identifier
    :param publishingCountry: [str] A GBIF occurrence identifier
    :param typeStatus: [str] A GBIF occurrence identifier
    :param issue: [str] A GBIF occurrence identifier
    :param year: [int] A GBIF occurrence identifier
    :param checklistKey: [str] The UUID of the checklist to use for taxonomy. Defaults to
        COL Extended Release ("7ddf754f-d193-4cc9-b351-99906754a03b"). If you provide a
        numeric (integer) taxonKey without explicitly setting checklistKey, it will automatically
        switch to the GBIF Backbone taxonomy (checklistKey=None) for backward compatibility,
        but will issue a deprecation warning. Set to None explicitly to use GBIF Backbone taxonomy.

    :return: dict

    Usage::

        from pygbif import occurrences
        # With COL Extended Release (default)
        occurrences.count(taxonKey = "75F9")
        # With GBIF Backbone (deprecated)
        occurrences.count(taxonKey = 3329049, checklistKey = None)
        occurrences.count(country = 'CA')
        occurrences.count(isGeoreferenced = True)
        occurrences.count(basisOfRecord = 'OBSERVATION')
    """
    check_param_lens(
        taxonKey=taxonKey,
        basisOfRecord=basisOfRecord,
        country=country,
        isGeoreferenced=isGeoreferenced,
        datasetKey=datasetKey,
        publishingCountry=publishingCountry,
        typeStatus=typeStatus,
        issue=issue,
        year=year,
    )
    
    # Handle checklistKey default and detect if user explicitly provided it
    if checklistKey is _DEFAULT_CHECKLIST:
        user_provided_checklistkey = False
        checklistKey = "7ddf754f-d193-4cc9-b351-99906754a03b"  # Default to COL
    else:
        user_provided_checklistkey = True
    
    # Check if taxonKey is numeric (integer)
    # If so and user didn't explicitly provide checklistKey, switch to GBIF Backbone
    if taxonKey is not None and isinstance(taxonKey, int) and not user_provided_checklistkey:
        # Automatically switch to GBIF Backbone for numeric keys
        checklistKey = None
        warnings.warn(
            "Numeric taxonKey detected. Automatically switching to GBIF Backbone taxonomy. "
            "GBIF Backbone taxonomy is outdated. Please migrate to COL Extended Release with alphanumeric keys. "
            "Use pygbif.species.gbif_to_col() to convert your numeric GBIF keys to COL alphanumeric keys.",
            DeprecationWarning,
            stacklevel=2
        )
    
    url = gbif_baseurl + "occurrence/count"
    isGeoreferenced = bool2str(isGeoreferenced)
    out = gbif_GET(
        url,
        {
            "taxonKey": taxonKey,
            "basisOfRecord": basisOfRecord,
            "country": country,
            "isGeoreferenced": isGeoreferenced,
            "datasetKey": datasetKey,
            "publishingCountry": publishingCountry,
            "typeStatus": typeStatus,
            "issue": issue,
            "year": year,
            "checklistKey": checklistKey,
        },
        **kwargs
    )
    return out


def count_basisofrecord(**kwargs):
    """
    Lists occurrence counts by basis of record.

    :return: dict

    Usage::

            from pygbif import occurrences
            occurrences.count_basisofrecord()
    """
    url = gbif_baseurl + "occurrence/counts/basisOfRecord"
    out = gbif_GET(url, {}, **kwargs)
    return out


def count_year(year, **kwargs):
    """
    Lists occurrence counts by year

    :param year: [int] year range, e.g., ``1990,2000``. Does not support ranges like ``asterisk,2010``

    :return: dict

    Usage::

            from pygbif import occurrences
            occurrences.count_year(year = '1990,2000')
    """
    url = gbif_baseurl + "occurrence/counts/year"
    out = gbif_GET(url, {"year": year}, **kwargs)
    return out


def count_datasets(taxonKey=None, country=None, checklistKey=_DEFAULT_CHECKLIST, **kwargs):
    """
    Lists occurrence counts for datasets that cover a given taxon or country

    :param taxonKey: [int/str] A taxon key from a checklist. Can be a GBIF Backbone
        integer key (deprecated, use COL instead) or a COL Extended Release alphanumeric key.
    :param country: [str] A country, two letter code
    :param checklistKey: [str] The UUID of the checklist to use for taxonomy. Defaults to
        COL Extended Release ("7ddf754f-d193-4cc9-b351-99906754a03b"). If you provide a
        numeric (integer) taxonKey without explicitly setting checklistKey, it will automatically
        switch to the GBIF Backbone taxonomy (checklistKey=None) for backward compatibility,
        but will issue a deprecation warning. Set to None explicitly to use GBIF Backbone taxonomy.

    :return: dict

    Usage::

            from pygbif import occurrences
            occurrences.count_datasets(country = "DE")
            # With COL Extended Release (default)
            occurrences.count_datasets(taxonKey = "75F9")
            # With GBIF Backbone (deprecated)
            occurrences.count_datasets(taxonKey = 3329049, checklistKey = None)
    """
    # Handle checklistKey default and detect if user explicitly provided it
    if checklistKey is _DEFAULT_CHECKLIST:
        user_provided_checklistkey = False
        checklistKey = "7ddf754f-d193-4cc9-b351-99906754a03b"  # Default to COL
    else:
        user_provided_checklistkey = True
    
    # Check if taxonKey is numeric (integer)
    # If so and user didn't explicitly provide checklistKey, switch to GBIF Backbone
    if taxonKey is not None and isinstance(taxonKey, int) and not user_provided_checklistkey:
        # Automatically switch to GBIF Backbone for numeric keys
        checklistKey = None
        warnings.warn(
            "Numeric taxonKey detected. Automatically switching to GBIF Backbone taxonomy. "
            "GBIF Backbone taxonomy is outdated. Please migrate to COL Extended Release with alphanumeric keys. "
            "Use pygbif.species.gbif_to_col() to convert your numeric GBIF keys to COL alphanumeric keys.",
            DeprecationWarning,
            stacklevel=2
        )
    
    url = gbif_baseurl + "occurrence/counts/datasets"
    out = gbif_GET(url, {"taxonKey": taxonKey, "country": country, "checklistKey": checklistKey}, **kwargs)
    return out


def count_countries(publishingCountry, **kwargs):
    """
    Lists occurrence counts for all countries covered by the data published by the given country

    :param publishingCountry: [str] A two letter country code

    :return: dict

    Usage::

            from pygbif import occurrences
            occurrences.count_countries(publishingCountry = "DE")
    """
    url = gbif_baseurl + "occurrence/counts/countries"
    out = gbif_GET(url, {"publishingCountry": publishingCountry}, **kwargs)
    return out


def count_publishingcountries(country, **kwargs):
    """
    Lists occurrence counts for all countries that publish data about the given country

    :param country: [str] A country, two letter code

    :return: dict

    Usage::

            from pygbif import occurrences
            occurrences.count_publishingcountries(country = "DE")
    """
    url = gbif_baseurl + "occurrence/counts/publishingCountries"
    out = gbif_GET(url, {"country": country}, **kwargs)
    return out


def count_schema(**kwargs):
    """
    List the supported metrics by the service

    :return: dict

    Usage::

            from pygbif import occurrences
            occurrences.count_schema()
    """
    url = gbif_baseurl + "occurrence/count/schema"
    out = gbif_GET(url, {}, **kwargs)
    return out
