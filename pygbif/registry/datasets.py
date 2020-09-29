import re

from pygbif.gbifutils import (
    gbif_baseurl,
    gbif_GET,
    len2,
    bool2str,
    check_data,
    requests_argset,
)


def dataset_metrics(uuid):
    """
    Get details on a GBIF dataset.

    :param uuid: [str] One or more dataset UUIDs. See examples.

    References: http://www.gbif.org/developer/registry#datasetMetrics

    Usage::

            from pygbif import registry
            registry.dataset_metrics(uuid='3f8a1297-3259-4700-91fc-acc4170b27ce')
            registry.dataset_metrics(uuid='66dd0960-2d7d-46ee-a491-87b9adcfe7b1')
            registry.dataset_metrics(uuid=['3f8a1297-3259-4700-91fc-acc4170b27ce', '66dd0960-2d7d-46ee-a491-87b9adcfe7b1'])
    """

    def getdata(x):
        url = gbif_baseurl + "dataset/" + x + "/metrics"
        return gbif_GET(url, {})

    if len2(uuid) == 1:
        return getdata(uuid)
    else:
        return [getdata(x) for x in uuid]


def datasets(
    data="all",
    type=None,
    uuid=None,
    query=None,
    id=None,
    limit=100,
    offset=None,
    **kwargs
):
    """
    Search for datasets and dataset metadata.

    :param data: [str] The type of data to get. Default: ``all``
    :param type: [str] Type of dataset, options include ``OCCURRENCE``, etc.
    :param uuid: [str] UUID of the data node provider. This must be specified if data
         is anything other than ``all``.
    :param query: [str] Query term(s). Only used when ``data = 'all'``
    :param id: [int] A metadata document id.

    References http://www.gbif.org/developer/registry#datasets

    Usage::

            from pygbif import registry
            registry.datasets(limit=5)
            registry.datasets(type="OCCURRENCE")
            registry.datasets(uuid="a6998220-7e3a-485d-9cd6-73076bd85657")
            registry.datasets(data='contact', uuid="a6998220-7e3a-485d-9cd6-73076bd85657")
            registry.datasets(data='metadata', uuid="a6998220-7e3a-485d-9cd6-73076bd85657")
            registry.datasets(data='metadata', uuid="a6998220-7e3a-485d-9cd6-73076bd85657", id=598)
            registry.datasets(data=['deleted','duplicate'])
            registry.datasets(data=['deleted','duplicate'], limit=1)
    """
    args = {"q": query, "type": type, "limit": limit, "offset": offset}
    data_choices = [
        "all",
        "organization",
        "contact",
        "endpoint",
        "identifier",
        "tag",
        "machinetag",
        "comment",
        "constituents",
        "document",
        "metadata",
        "deleted",
        "duplicate",
        "subDataset",
        "withNoEndpoint",
    ]
    check_data(data, data_choices)
    if len2(data) == 1:
        return datasets_fetch(data, uuid, args, **kwargs)
    else:
        return [datasets_fetch(x, uuid, args, **kwargs) for x in data]


def datasets_fetch(x, uuid, args, **kwargs):
    if (
        x not in ["all", "deleted", "duplicate", "subDataset", "withNoEndpoint"]
        and uuid is None
    ):
        raise TypeError(
            "You must specify a uuid if data does not equal all and data does not equal of deleted, duplicate, subDataset, or withNoEndpoint"
        )

    if uuid is None:
        if x == "all":
            url = gbif_baseurl + "dataset"
        else:
            if id is not None and x == "metadata":
                url = gbif_baseurl + "dataset/metadata/" + id + "/document"
            else:
                url = gbif_baseurl + "dataset/" + x
    else:
        if x == "all":
            url = gbif_baseurl + "dataset/" + uuid
        else:
            url = gbif_baseurl + "dataset/" + uuid + "/" + x

    res = gbif_GET(url, args, **kwargs)
    return res


def dataset_suggest(
    q=None,
    type=None,
    keyword=None,
    owningOrg=None,
    publishingOrg=None,
    hostingOrg=None,
    publishingCountry=None,
    decade=None,
    limit=100,
    offset=None,
    **kwargs
):
    """
    Search that returns up to 20 matching datasets. Results are ordered by relevance.


    :param q: [str] Query term(s) for full text search.  The value for this parameter can be a simple word or a phrase. Wildcards can be added to the simple word parameters only, e.g. ``q=*puma*``
    :param type: [str] Type of dataset, options include OCCURRENCE, etc.
    :param keyword: [str] Keyword to search by. Datasets can be tagged by keywords, which you can search on. The search is done on the merged collection of tags, the dataset keywordCollections and temporalCoverages. SEEMS TO NOT BE WORKING ANYMORE AS OF 2016-09-02.
    :param owningOrg: [str] Owning organization. A uuid string. See :func:`~pygbif.registry.organizations`
    :param publishingOrg: [str] Publishing organization. A uuid string. See :func:`~pygbif.registry.organizations`
    :param hostingOrg: [str] Hosting organization. A uuid string. See :func:`~pygbif.registry.organizations`
    :param publishingCountry: [str] Publishing country.
    :param decade: [str] Decade, e.g., 1980. Filters datasets by their temporal coverage broken down to decades. Decades are given as a full year, e.g. 1880, 1960, 2000, etc, and will return datasets wholly contained in the decade as well as those that cover the entire decade or more. Facet by decade to get the break down, e.g. ``/search?facet=DECADE&facet_only=true`` (see example below)
    :param limit: [int] Number of results to return. Default: ``300``
    :param offset: [int] Record to start at. Default: ``0``

    :return: A dictionary

    References: http://www.gbif.org/developer/registry#datasetSearch

    Usage::

            from pygbif import registry
            registry.dataset_suggest(q="Amazon", type="OCCURRENCE")

            # Suggest datasets tagged with keyword "france".
            registry.dataset_suggest(keyword="france")

            # Suggest datasets owned by the organization with key
            # "07f617d0-c688-11d8-bf62-b8a03c50a862" (UK NBN).
            registry.dataset_suggest(owningOrg="07f617d0-c688-11d8-bf62-b8a03c50a862")

            # Fulltext search for all datasets having the word "amsterdam" somewhere in
            # its metadata (title, description, etc).
            registry.dataset_suggest(q="amsterdam")

            # Limited search
            registry.dataset_suggest(type="OCCURRENCE", limit=2)
            registry.dataset_suggest(type="OCCURRENCE", limit=2, offset=10)

            # Return just descriptions
            registry.dataset_suggest(type="OCCURRENCE", limit = 5, description=True)

            # Search by decade
            registry.dataset_suggest(decade=1980, limit = 30)
    """
    url = gbif_baseurl + "dataset/suggest"
    args = {
        "q": q,
        "type": type,
        "keyword": keyword,
        "publishingOrg": publishingOrg,
        "hostingOrg": hostingOrg,
        "owningOrg": owningOrg,
        "decade": decade,
        "publishingCountry": publishingCountry,
        "limit": limit,
        "offset": offset,
    }
    out = gbif_GET(url, args, **kwargs)
    return out


def dataset_search(
    q=None,
    type=None,
    keyword=None,
    owningOrg=None,
    publishingOrg=None,
    hostingOrg=None,
    decade=None,
    publishingCountry=None,
    facet=None,
    facetMincount=None,
    facetMultiselect=None,
    hl=False,
    limit=100,
    offset=None,
    **kwargs
):
    """
    Full text search across all datasets. Results are ordered by relevance.

    :param q: [str] Query term(s) for full text search.  The value for this parameter
         can be a simple word or a phrase. Wildcards can be added to the simple word
         parameters only, e.g. ``q=*puma*``
    :param type: [str] Type of dataset, options include OCCURRENCE, etc.
    :param keyword: [str] Keyword to search by. Datasets can be tagged by keywords, which
         you can search on. The search is done on the merged collection of tags, the
         dataset keywordCollections and temporalCoverages. SEEMS TO NOT BE WORKING
         ANYMORE AS OF 2016-09-02.
    :param owningOrg: [str] Owning organization. A uuid string. See :func:`~pygbif.registry.organizations`
    :param publishingOrg: [str] Publishing organization. A uuid string. See :func:`~pygbif.registry.organizations`
    :param hostingOrg: [str] Hosting organization. A uuid string. See :func:`~pygbif.registry.organizations`
    :param publishingCountry: [str] Publishing country.
    :param decade: [str] Decade, e.g., 1980. Filters datasets by their temporal coverage
         broken down to decades. Decades are given as a full year, e.g. 1880, 1960, 2000,
         etc, and will return datasets wholly contained in the decade as well as those
         that cover the entire decade or more. Facet by decade to get the break down,
         e.g. ``/search?facet=DECADE&facet_only=true`` (see example below)
    :param facet: [str] A list of facet names used to retrieve the 100 most frequent values
            for a field. Allowed facets are: type, keyword, publishingOrg, hostingOrg, decade,
            and publishingCountry. Additionally subtype and country are legal values but not
            yet implemented, so data will not yet be returned for them.
    :param facetMincount: [str] Used in combination with the facet parameter. Set
            facetMincount={#} to exclude facets with a count less than {#}, e.g.
            http://api.gbif.org/v1/dataset/search?facet=type&limit=0&facetMincount=10000
            only shows the type value 'OCCURRENCE' because 'CHECKLIST' and 'METADATA' have
            counts less than 10000.
    :param facetMultiselect: [bool] Used in combination with the facet parameter. Set
            ``facetMultiselect=True`` to still return counts for values that are not currently
            filtered, e.g.
            http://api.gbif.org/v1/dataset/search?facet=type&limit=0&type=CHECKLIST&facetMultiselect=true
            still shows type values 'OCCURRENCE' and 'METADATA' even though type is being
            filtered by ``type=CHECKLIST``
    :param hl: [bool] Set ``hl=True`` to highlight terms matching the query when in fulltext
            search fields. The highlight will be an emphasis tag of class 'gbifH1' e.g.
            http://api.gbif.org/v1/dataset/search?q=plant&hl=true
            Fulltext search fields include: title, keyword, country, publishing country,
            publishing organization title, hosting organization title, and description. One
            additional full text field is searched which includes information from metadata
            documents, but the text of this field is not returned in the response.
    :param limit: [int] Number of results to return. Default: ``300``
    :param offset: [int] Record to start at. Default: ``0``

    :note: Note that you can pass in additional faceting parameters on a per field basis.
            For example, if you want to limit the numbef of facets returned from a field ``foo`` to
            3 results, pass in ``foo_facetLimit = 3``. GBIF does not allow all per field parameters,
            but does allow some. See also examples.

    :return: A dictionary

    References: http://www.gbif.org/developer/registry#datasetSearch

    Usage::

            from pygbif import registry
            # Gets all datasets of type "OCCURRENCE".
            registry.dataset_search(type="OCCURRENCE", limit = 10)

            # Fulltext search for all datasets having the word "amsterdam" somewhere in
            # its metadata (title, description, etc).
            registry.dataset_search(q="amsterdam", limit = 10)

            # Limited search
            registry.dataset_search(type="OCCURRENCE", limit=2)
            registry.dataset_search(type="OCCURRENCE", limit=2, offset=10)

            # Search by decade
            registry.dataset_search(decade=1980, limit = 10)

            # Faceting
            ## just facets
            registry.dataset_search(facet="decade", facetMincount=10, limit=0)

            ## data and facets
            registry.dataset_search(facet="decade", facetMincount=10, limit=2)

            ## many facet variables
            registry.dataset_search(facet=["decade", "type"], facetMincount=10, limit=0)

            ## facet vars
            ### per variable paging
            x = registry.dataset_search(
                facet = ["decade", "type"],
                decade_facetLimit = 3,
                type_facetLimit = 3,
                limit = 0
            )

            ## highlight
            x = registry.dataset_search(q="plant", hl=True, limit = 10)
            [ z['description'] for z in x['results'] ]
    """
    url = gbif_baseurl + "dataset/search"
    args = {
        "q": q,
        "type": type,
        "keyword": keyword,
        "owningOrg": owningOrg,
        "publishingOrg": publishingOrg,
        "hostingOrg": hostingOrg,
        "decade": decade,
        "publishingCountry": publishingCountry,
        "facet": facet,
        "facetMincount": facetMincount,
        "facetMultiselect": bool2str(facetMultiselect),
        "hl": bool2str(hl),
        "limit": limit,
        "offset": offset,
    }
    gbif_kwargs = {key: kwargs[key] for key in kwargs if key not in requests_argset}
    if gbif_kwargs is not None:
        xx = dict(
            zip([re.sub("_", ".", x) for x in gbif_kwargs.keys()], gbif_kwargs.values())
        )
        args.update(xx)
    kwargs = {key: kwargs[key] for key in kwargs if key in requests_argset}
    out = gbif_GET(url, args, **kwargs)
    return out
