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
    :param gbifDatasetKey: [str] GBIF dataset key
    :param gbifDownloadKey: [str] GBIF download key
    :param gbifHigherTaxonKey: [str] GBIF higher taxon key
    :param gbifNetworkKey: [str] GBIF network key
    :param gbifOccurrenceKey: [str] GBIF occurrence key
    :param gbifProjectIdentifier: [str] GBIF project identifier
    :param gbifProgrammeAcronym: [str] GBIF programme acronym
    :param gbifTaxonKey: [str] GBIF taxon key
    :param literatureType: [str] Type of literature
    :param openAccess: [bool] Open access
    :param peerReview: [bool] Peer review
    :param publisher: [str] Publisher
    :param publishingOrganizationKey: [str] Publishing organization key
    :param relevance: [str] Relevance
    :param source: [str] Source
    :param topics: [str] Topics
    :param websites: [str] Websites
    :param year: [str] Year
    :param language: [str] Language
    :param added: [str] Added
    :param published: [str] Published
    :param discovered: [str] Discovered
    :param modified: [str] Modified
    :param hl: [str] Highlight
    :param limit: [int] Limit
    :param offset: [int] Offset
    :param facet: [str] Facet
    :param facetMincount: [int] Facet mincount
    :param facetMultiselect: [bool] Facet multiselect
    :param facetOffset: [int] Facet offset

    :return: A dictionary

    Usage::

        from pygbif import literature
        literature.search(limit=10) # basic search for 10 records

        
    
    
    
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



