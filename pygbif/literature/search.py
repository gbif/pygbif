from pygbif.gbifutils import gbif_baseurl, bool2str, requests_argset, gbif_GET

def search(
    citationType=None,
    countriesOfCoverage=None,
    countriesOfResearcher=None,
    doi=None,
    gbifDatasetKey=None,
    gbifDownloadKey=None,
    gbifHigherTaxonKey=None,
    gbifNetworkKey=None,
    gbifOccurrenceKey=None,
    gbifProjectIdentifier=None,
    gbifProgrammeAcronym=None,
    gbifTaxonKey=None,
    literatureType=None,
    openAccess=None,
    peerReview=None,
    publisher=None,
    publishingOrganizationKey=None,
    relevance=None,
    source=None,
    topics=None,
    websites=None,
    year=None,
    language=None,
    added=None,
    published=None,
    discovered=None,
    modified=None,
    hl=None,
    limit=100,
    offset=0,
    facet=None,
    facetMincount=None,
    facetMultiselect=None,
    facetLimit=None,
    facetOffset=None,
    q=None,
    **kwargs
):
    """
    Search for literature indexed by GBIF
    
    :param citationType: [str] The manner in which GBIF is cited in a paper.
    :param countriesOfCoverage: [str], Countries of coverage
    :param countriesOfResearcher: [str] Country or area of institution with which author is affiliated. 
    :param doi: [str] Digital Object Identifier (DOI) of the literature item.
    :param gbifDatasetKey: [str] GBIF dataset key uuid referenced in publication.
    :param gbifDownloadKey: [str] GBIF download referenced in publication.
    :param gbifHigherTaxonKey: [str] All parent keys of any taxon that is the focus of the paper.
    :param gbifNetworkKey: [str] GBIF network referenced in publication.
    :param gbifOccurrenceKey: [str] Any GBIF occurrence keys directly mentioned in a paper.
    :param gbifProjectIdentifier: [str] GBIF dataset referenced in publication.
    :param gbifProgrammeAcronym: [str] GBIF dataset referenced in publication.
    :param gbifTaxonKey: [str] Key(s) from the GBIF backbone of taxa that are the focus of a paper.
    :param literatureType: [str] Type of literature, e.g. journal article.
    :param openAccess: [bool] Is the publication Open Access?
    :param peerReview: [bool] Has the publication undergone peer review?
    :param publisher: [str] Publisher of journal.
    :param publishingOrganizationKey: [str] Publisher whose dataset is referenced in publication.
    :param relevance: [str] Relevance to GBIF community.
    :param source: [str] Journal of publication.
    :param topics: [str] Topic of publication.
    :param websites: [str] Website of publication.
    :param year: [str] Year of publication. This can be a single range such as "2019,2021".
    :param language: [str] 3 letter language code of publication. e.g. "eng"
    :param added: [str] Date or date range when the publication was added. Format is ISO 8601, e.g., '2024-07-14' or '2024-07-14,2024-08-14'.
    :param published: [str] Date or date range when the publication was published. Format is ISO 8601, e.g., '2024-02-22' or '2024-02-22,2024-03-22'.
    :param discovered: [str] Date or date range when the publication was discovered. Format is ISO 8601, e.g., '2024-02-26' or '2024-02-26,2024-03-26'.
    :param modified: [str] Date or date range when the publication was discovered. Format is ISO 8601, e.g., '2024-07-26' or '2024-07-26,2024-10-26'.
    :param hl: [str] Set hl=true to highlight terms matching the query when in fulltext search fields. 
    :param limit: [int] Controls the number of results in the page.
    :param offset: [int] Determines the offset for the search results.
    :param facet: [str] A facet name used to retrieve the most frequent values for a field.
    :param facetMincount: [int] Used in combination with the facet parameter. Set facetMincount={#} to exclude facets with a count less than {#}.
    :param facetMultiselect: [bool] Used in combination with the facet parameter. Set facetMultiselect=true to still return counts for values that are not currently filtered.
    :param facetLimit: [int] Limit the number of facet values returned.
    :param facetOffset: [int] Facet parameters allow paging requests using the parameters facetOffset and facetLimit.
    :param q: [str] Full text query. 
    
    :return: A dictionary

    Usage::

        from pygbif import literature as lit
        lit.search(limit=10) # basic search for 10 records

        # search for a specific download key
        lit.search(gbifDownloadKey="0235283-220831081235567") 

        # search for a year range
        lit.search(year="2010,2024", limit=10)

        # search for count only 
        lit.search(year="2010,2024", limit=0)["count"]    
    """
    url = gbif_baseurl + "literature/search"
    args = {
        "citationType": citationType,
        "countriesOfCoverage": countriesOfCoverage,
        "countriesOfResearcher": countriesOfResearcher,
        "doi": doi,
        "gbifDatasetKey": gbifDatasetKey,
        "gbifDownloadKey": gbifDownloadKey,
        "gbifHigherTaxonKey": gbifHigherTaxonKey,
        "gbifNetworkKey": gbifNetworkKey,
        "gbifOccurrenceKey": gbifOccurrenceKey,
        "gbifProjectIdentifier": gbifProjectIdentifier,
        "gbifProgrammeAcronym": gbifProgrammeAcronym,
        "gbifTaxonKey": gbifTaxonKey,
        "literatureType": literatureType,
        "openAccess": openAccess,
        "peerReview": peerReview,
        "publisher": publisher,
        "publishingOrganizationKey": publishingOrganizationKey,
        "relevance": relevance,
        "source": source,
        "topics": topics,
        "websites": websites,
        "year": year,
        "language": language,
        "added": added,
        "published": published,
        "discovered": discovered,
        "modified": modified,
        "hl": hl,
        "limit": limit,
        "offset": offset,
        "facet": facet,
        "facetMincount": facetMincount,
        "facetMultiselect": facetMultiselect,
        "facetLimit": facetLimit,
        "facetOffset": facetOffset,
        "q": q,
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



