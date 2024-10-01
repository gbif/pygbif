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



