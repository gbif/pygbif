from pygbif.gbifutils import gbif_baseurl, bool2str, requests_argset, gbif_GET
import re

def search(
    q=None,
    type=None,
    institutionalGovernance=None,
    disciplines=None,
    name=None,
    fuzzyName=None,
    numberSpecimens=None,
    occurrenceCount=None,
    typeSpecimenCount=None,
    sourceId=None,
    source=None,
    code=None,
    alternativeCode=None,
    contact=None,
    institutionKey=None,
    country=None,
    city=None,
    gbifRegion=None,
    machineTagNamespace=None,
    machineTagName=None,
    machineTagValue=None,
    identifier=None,
    identifierType=None,
    active=None,
    displayOnNHCPortal=None,
    masterSourceType=None,
    replacedBy=None,
    sortBy=None,
    sortOrder=None,
    offset=None,
    limit=None,
    **kwargs
    ): 
    """
    Search for institutions in GRSciColl.

    :param q: [str] Simple full text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported
    :param type: [str] Type of a GrSciColl institution. Available values: BIOMEDICAL_RESEARCH_INSTITUTE, BOTANICAL_GARDEN, HERBARIUM, LIVING_ORGANISM_COLLECTION, MEDICAL_RESEARCH_INSTITUTE, MUSEUM, MUSEUM_HERBARIUM_PRIVATE_NON_PROFIT, OTHER_INSTITUTIONAL_TYPE, OTHER_TYPE_RESEARCH_INSTITUTION_BIOREPOSITORY, UNIVERSITY_COLLEGE, ZOO_AQUARIUM
    :param institutionalGovernance: [str] Institutional governance of a GrSciColl institution. Available values: ACADEMIC_FEDERAL, ACADEMIC_FOR_PROFIT, ACADEMIC_LOCAL, ACADEMIC_NON_PROFIT, ACADEMIC_STATE, FEDERAL, FOR_PROFIT, LOCAL, NON_PROFIT, OTHER, STATE
    :param disciplines: [str] Discipline of a GrSciColl institution. Check available values: https://techdocs.gbif.org/en/openapi/v1/registry#/Institutions/listInstitutions
    :param name: [str] Name of a GrSciColl institution or collection
    :param fuzzyName: [str] It searches by name fuzzily so the parameter doesn't have to be the exact name
    :param numberSpecimens: [str] Number of specimens. It supports ranges and a '*' can be used as a wildcard
    :param occurrenceCount: [str] Count of occurrences linked. It supports ranges and a '*' can be used as a wildcard
    :param typeSpecimenCount: [str] Count of type specimens linked. It supports ranges and a '*' can be used as a wildcard
    :param sourceId: [str] sourceId of MasterSourceMetadata
    :param source: [str] Source attribute of MasterSourceMetadata. Available values: DATASET, ORGANIZATION, IH_IRN
    :param code: [str] Code of a GrSciColl institution or collection
    :param alternativeCode: [str] Alternative code of a GrSciColl institution
    :param contact: [str] Filters collections and institutions whose contacts contain the person key specified
    :param institutionKey: [str] Keys of institutions to filter by
    :param country: [str] Filters by country given as a ISO 639-1 (2 letter) country code
    :param city: [str] Filters by the city of the address. It searches in both the physical and the mailing address
    :param gbifRegion: [str] Filters by a gbif region. Available values: AFRICA, ASIA, EUROPE, NORTH_AMERICA, OCEANIA, LATIN_AMERICA, ANTARCTICA
    :param machineTagNamespace: [str] Filters for entities with a machine tag in the specified namespace
    :param machineTagName: [str] Filters for entities with a machine tag with the specified name (use in combination with the machineTagNamespace parameter)
    :param machineTagValue: [str] Filters for entities with a machine tag with the specified value (use in combination with the machineTagNamespace and machineTagName parameters)
    :param identifier: [str] An identifier of the type given by the identifierType parameter, for example a DOI or UUID
    :param identifierType: [str] An identifier type for the identifier parameter. Available values: URL, LSID, HANDLER, DOI, UUID, FTP, URI, UNKNOWN, GBIF_PORTAL, GBIF_NODE, GBIF_PARTICIPANT, GRSCICOLL_ID, GRSCICOLL_URI, IH_IRN, ROR, GRID, CITES, SYMBIOTA_UUID, WIKIDATA, NCBI_BIOCOLLECTION, ISIL, CLB_DATASET_KEY
    :param active: [bool] Active status of a GrSciColl institution or collection
    :param displayOnNHCPortal: [bool] Flag to show this record in the NHC portal
    :param masterSourceType: [str] The master source type of a GRSciColl institution or collection. Available values: GRSCICOLL, GBIF_REGISTRY, IH
    :param replacedBy: [str] Key of the entity that replaced another entity
    :param sortBy: [str] Field to sort the results by. It only supports the fields contained in the enum. Available values: NUMBER_SPECIMENS
    :param sortOrder: [str] Sort order to use with the sortBy parameter. Available values: ASC, DESC
    :param offset: [int] Determines the offset for the search results
    :param limit: [int] Controls the number of results in the page. Default 20
    :param kwargs: Further named arguments passed on to requests.get

    :return: A dictionary

    Usage::
        from pygbif import institution as inst

        inst.search(q="Kansas",limit=1)
        inst.search(numberSpecimens = "1000,*",limit=2)
        inst.search(source = "IH_IRN") 
        inst.search(country = ["US","GB"])
        inst.search(typeSpecimenCount = "10,100")
    """
    url = gbif_baseurl + "grscicoll/institution"
    args = {
        "q": q,
        "type": type,
        "institutionalGovernance": institutionalGovernance,
        "disciplines": disciplines,
        "name": name,
        "fuzzyName": fuzzyName,
        "numberSpecimens": numberSpecimens,
        "occurrenceCount": occurrenceCount,
        "typeSpecimenCount": typeSpecimenCount,
        "sourceId": sourceId,
        "source": source,
        "code": code,
        "alternativeCode": alternativeCode,
        "contact": contact,
        "institutionKey": institutionKey,
        "country": country,
        "city": city,
        "gbifRegion": gbifRegion,
        "machineTagNamespace": machineTagNamespace,
        "machineTagName": machineTagName,
        "machineTagValue": machineTagValue,
        "identifier": identifier,
        "identifierType": identifierType,
        "active": active,
        "displayOnNHCPortal": displayOnNHCPortal,
        "masterSourceType": masterSourceType,
        "replacedBy": replacedBy,
        "sortBy": sortBy,
        "sortOrder": sortOrder,
        "offset": offset,
        "limit": limit, 
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
