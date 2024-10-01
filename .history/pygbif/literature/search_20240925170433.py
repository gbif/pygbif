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
    :param citationType: str, Citation type
    :param countriesOfCoverage: str, Countries of coverage

    
    
    
    
    """
