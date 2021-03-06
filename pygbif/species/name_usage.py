from pygbif.gbifutils import check_data, len2, gbif_baseurl, gbif_GET


def name_usage(
    key=None,
    name=None,
    data="all",
    language=None,
    datasetKey=None,
    uuid=None,
    sourceId=None,
    rank=None,
    shortname=None,
    limit=100,
    offset=None,
    **kwargs
):
    """
    Lookup details for specific names in all taxonomies in GBIF.

    :param key: [fixnum] A GBIF key for a taxon
    :param name: [str] Filters by a case insensitive, canonical namestring,
         e.g. 'Puma concolor'
    :param data: [str] The type of data to get. Default: ``all``. Options: ``all``,
        ``verbatim``, ``name``, ``parents``, ``children``,
        ``related``, ``synonyms``, ``descriptions``, ``distributions``, ``media``,
        ``references``, ``speciesProfiles``, ``vernacularNames``, ``typeSpecimens``,
        ``root``
    :param language: [str] Language. Expects a ISO 639-1 language codes using 2 lower
        case letters. Languages returned are 3 letter codes. The language parameter
        only applies to the ``/species``, ``/species/{int}``,
        ``/species/{int}/parents``, ``/species/{int}/children``, ``/species/{int}/related``,
        ``/species/{int}/synonyms`` routes (here routes are determined by the ``data``
        parameter).
    :param datasetKey: [str] Filters by the dataset's key (a uuid)
    :param uuid: [str] A uuid for a dataset. Should give exact same results as datasetKey.
    :param sourceId: [fixnum] Filters by the source identifier.
    :param rank: [str] Taxonomic rank. Filters by taxonomic rank as one of:
            ``CLASS``, ``CULTIVAR``, ``CULTIVAR_GROUP``, ``DOMAIN``, ``FAMILY``, ``FORM``, ``GENUS``, ``INFORMAL``,
            ``INFRAGENERIC_NAME``, ``INFRAORDER``, ``INFRASPECIFIC_NAME``, ``INFRASUBSPECIFIC_NAME``,
            ``KINGDOM``, ``ORDER``, ``PHYLUM``, ``SECTION``, ``SERIES``, ``SPECIES``, ``STRAIN``, ``SUBCLASS``, ``SUBFAMILY``,
            ``SUBFORM``, ``SUBGENUS``, ``SUBKINGDOM``, ``SUBORDER``, ``SUBPHYLUM``, ``SUBSECTION``, ``SUBSERIES``,
            ``SUBSPECIES``, ``SUBTRIBE``, ``SUBVARIETY``, ``SUPERCLASS``, ``SUPERFAMILY``, ``SUPERORDER``,
            ``SUPERPHYLUM``, ``SUPRAGENERIC_NAME``, ``TRIBE``, ``UNRANKED``, ``VARIETY``
    :param shortname: [str] A short name..need more info on this?
    :param limit: [fixnum] Number of records to return. Default: ``100``. Maximum: ``1000``. (optional)
    :param offset: [fixnum] Record number to start at. (optional)

    References: See http://www.gbif.org/developer/species#nameUsages for details

    Usage::

            from pygbif import species

            species.name_usage(key=1)

            # Name usage for a taxonomic name
            species.name_usage(name='Puma', rank="GENUS")

            # All name usages
            species.name_usage()

            # References for a name usage
            species.name_usage(key=2435099, data='references')

            # Species profiles, descriptions
            species.name_usage(key=5231190, data='speciesProfiles')
            species.name_usage(key=5231190, data='descriptions')
            species.name_usage(key=2435099, data='children')

            # Vernacular names for a name usage
            species.name_usage(key=5231190, data='vernacularNames')

            # Limit number of results returned
            species.name_usage(key=5231190, data='vernacularNames', limit=3)

            # Search for names by dataset with datasetKey parameter
            species.name_usage(datasetKey="d7dddbf4-2cf0-4f39-9b2a-bb099caae36c")
    """
    args = {
        "language": language,
        "name": name,
        "datasetKey": datasetKey,
        "rank": rank,
        "sourceId": sourceId,
        "limit": limit,
        "offset": offset,
    }
    data_choices = [
        "all",
        "verbatim",
        "name",
        "parents",
        "children",
        "related",
        "synonyms",
        "descriptions",
        "distributions",
        "media",
        "references",
        "speciesProfiles",
        "vernacularNames",
        "typeSpecimens",
        "root",
    ]
    check_data(data, data_choices)
    if len2(data) == 1:
        return name_usage_fetch(data, key, shortname, uuid, args, **kwargs)
    else:
        return [name_usage_fetch(x, key, shortname, uuid, args, **kwargs) for x in data]


def name_usage_fetch(x, key, shortname, uuid, args, **kwargs):
    if x != "all" and key is None:
        raise TypeError("You must specify `key` if `data` does not equal `all`")

    if x == "all" and key is None:
        url = gbif_baseurl + "species"
    else:
        if x == "all" and key is not None:
            url = gbif_baseurl + "species/" + str(key)
        else:
            if x in [
                "verbatim",
                "name",
                "parents",
                "children",
                "related",
                "synonyms",
                "descriptions",
                "distributions",
                "media",
                "references",
                "speciesProfiles",
                "vernacularNames",
                "typeSpecimens",
            ]:
                url = gbif_baseurl + "species/%s/%s" % (str(key), x)
            else:
                if x == "root":
                    url = gbif_baseurl + "species/%s/%s" % (uuid, shortname)

    res = gbif_GET(url, args, **kwargs)
    return res
