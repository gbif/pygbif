from pygbif.gbifutils import gbif_baseurl, bool2str, gbif_GET, check_param_lens


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
    **kwargs
):
    """
    Returns occurrence counts for a predefined set of dimensions

    For all parameters below, only one value allowed per function call.
    See :func:`~occurrences.search` for passing more than one value
    per parameter.

    :param taxonKey: [int] A GBIF occurrence identifier
    :param basisOfRecord: [str] A GBIF occurrence identifier
    :param country: [str] A GBIF occurrence identifier
    :param isGeoreferenced: [bool] A GBIF occurrence identifier
    :param datasetKey: [str] A GBIF occurrence identifier
    :param publishingCountry: [str] A GBIF occurrence identifier
    :param typeStatus: [str] A GBIF occurrence identifier
    :param issue: [str] A GBIF occurrence identifier
    :param year: [int] A GBIF occurrence identifier

    :return: dict

    Usage::

        from pygbif import occurrences
        occurrences.count(taxonKey = 3329049)
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


def count_datasets(taxonKey=None, country=None, **kwargs):
    """
    Lists occurrence counts for datasets that cover a given taxon or country

    :param taxonKey: [int] Taxon key
    :param country: [str] A country, two letter code

    :return: dict

    Usage::

            from pygbif import occurrences
            occurrences.count_datasets(country = "DE")
    """
    url = gbif_baseurl + "occurrence/counts/datasets"
    out = gbif_GET(url, {"taxonKey": taxonKey, "country": country}, **kwargs)
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
