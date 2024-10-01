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
    q=None
):
    """
    Search for literature indexed by GBIF
    :param citationType: [str] The manner in which GBIF is cited in a paper.
    :param countriesOfCoverage: str, Countries of coverage
    :param countriesOfResearcher: [str] Country or area of institution with which author is affiliated. 
    
    
    
    
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
    # kwargs = {key: kwargs[key] for key in kwargs if key in requests_argset}
    # out = gbif_GET(url, args, **kwargs)
    # return out



