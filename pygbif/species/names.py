from ..gbifutils import *

def name_backbone(name, rank=None, kingdom=None, phylum=None, clazz=None,
  order=None, family=None, genus=None, strict=False, verbose=False,
  start=None, limit=100, **kwargs):
  '''
  Lookup names in the GBIF backbone taxonomy.

  :param name: [str] Full scientific name potentially with authorship (required)
  :param rank: [str] The rank given as our rank enum. (optional)
  :param kingdom: [str] If provided default matching will also try to match against this
     if no direct match is found for the name alone. (optional)
  :param phylum: [str] If provided default matching will also try to match against this
     if no direct match is found for the name alone. (optional)
  :param class: [str] If provided default matching will also try to match against this
     if no direct match is found for the name alone. (optional)
  :param order: [str] If provided default matching will also try to match against this
     if no direct match is found for the name alone. (optional)
  :param family: [str] If provided default matching will also try to match against this
     if no direct match is found for the name alone. (optional)
  :param genus: [str] If provided default matching will also try to match against this
     if no direct match is found for the name alone. (optional)
  :param strict: [bool] If True it (fuzzy) matches only the given name, but never a
     taxon in the upper classification (optional)
  :param verbose: [bool] If True show alternative matches considered which had been rejected.

  A list for a single taxon with many slots (with ``verbose=False`` - default), or a
  list of length two, first element for the suggested taxon match, and a data.frame
  with alternative name suggestions resulting from fuzzy matching (with ``verbose=True``).

  If you don't get a match GBIF gives back a list of length 3 with slots synonym,
  confidence, and ``matchType='NONE'``.

  reference: http://www.gbif.org/developer/species#searching

  Usage::

      from pygbif import species
      species.name_backbone(name='Helianthus annuus', kingdom='plants')
      species.name_backbone(name='Helianthus', rank='genus', kingdom='plants')
      species.name_backbone(name='Poa', rank='genus', family='Poaceae')

      # Verbose - gives back alternatives
      species.name_backbone(name='Helianthus annuus', kingdom='plants', verbose=True)

      # Strictness
      species.name_backbone(name='Poa', kingdom='plants', verbose=True, strict=False)
      species.name_backbone(name='Helianthus annuus', kingdom='plants', verbose=True, strict=True)

      # Non-existent name
      species.name_backbone(name='Aso')

      # Multiple equal matches
      species.name_backbone(name='Oenante')
  '''
  url = gbif_baseurl + 'species/match'
  args = {'name': name, 'rank': rank, 'kingdom': kingdom, 'phylum': phylum,
         'class': clazz, 'order': order, 'family': family, 'genus': genus,
         'strict': strict, 'verbose': verbose, 'offset': start, 'limit': limit}
  tt = gbif_GET(url, args, **kwargs)
  return tt

def name_suggest(q=None, datasetKey=None, rank=None, fields=None, start=None, limit=100, **kwargs):
  '''
  A quick and simple autocomplete service that returns up to 20 name usages by
  doing prefix matching against the scientific name. Results are ordered by relevance.

  References: http://www.gbif.org/developer/species#searching

  :param q: [str] Simple search parameter. The value for this parameter can be a
     simple word or a phrase. Wildcards can be added to the simple word parameters only,
     e.g. ``q=*puma*`` (Required)
  :param datasetKey: [str] Filters by the checklist dataset key (a uuid, see examples)
  :param rank: [str] A taxonomic rank. One of ``class``, ``cultivar``, ``cultivar_group``, ``domain``, ``family``,
     ``form``, ``genus``, ``informal``, ``infrageneric_name``, ``infraorder``, ``infraspecific_name``,
     ``infrasubspecific_name``, ``kingdom``, ``order``, ``phylum``, ``section``, ``series``, ``species``, ``strain``, ``subclass``,
     ``subfamily``, ``subform``, ``subgenus``, ``subkingdom``, ``suborder``, ``subphylum``, ``subsection``, ``subseries``,
     ``subspecies``, ``subtribe``, ``subvariety``, ``superclass``, ``superfamily``, ``superorder``, ``superphylum``,
     ``suprageneric_name``, ``tribe``, ``unranked``, or ``variety``.

  :return: A dictionary, of results

  Usage::

      from pygbif import species
      species.name_suggest(q='Puma concolor')
      x = species.name_suggest(q='Puma')
      x['data']
      x['hierarchy']
      species.name_suggest(q='Puma', rank="genus")
      species.name_suggest(q='Puma', rank="subspecies")
      species.name_suggest(q='Puma', rank="species")
      species.name_suggest(q='Puma', rank="infraspecific_name")
      species.name_suggest(q='Puma', limit=2)
  '''
  url = gbif_baseurl + 'species/suggest'
  args = {'q':q, 'rank':rank, 'offset':start, 'limit':limit}
  tt = gbif_GET(url, args, **kwargs)
  hier = [ x['higherClassificationMap'] for x in tt ]
  [ x.pop('higherClassificationMap') for x in tt ]
  return {'data': tt, 'hierarchy': hier}

# def name_lookup(query=None, rank=None, higherTaxonKey=None, status=None, isExtinct=None,
#   habitat=None, nameType=None, datasetKey=None, nomenclaturalStatus=None,
#   limit=100, start=None, facet=None, facetMincount=None, facetMultiselect=None, type=None, hl=None,
#   verbose=FALSE, return="all", ...):
#   '''
#   Lookup names in all taxonomies in GBIF.

#   This service uses fuzzy lookup so that you can put in partial names and
#   you should get back those things that match. See examples below.

#   Faceting: If ``facet=FALSE`` or left to the default (``NULL``), no faceting is done. And therefore,
#   all parameters with facet in their name are ignored (``facetOnly``, ``facetMincount``, ``facetMultiselect``).

#   :param query: [str] Query term(s) for full text search (optional)
#   :param rank: [str] ``CLASS``, ``CULTIVAR``, ``CULTIVAR_GROUP``, ``DOMAIN``, ``FAMILY``,
#      ``FORM``, ``GENUS``, ``INFORMAL``, ``INFRAGENERIC_NAME``, ``INFRAORDER``, ``INFRASPECIFIC_NAME``,
#      ``INFRASUBSPECIFIC_NAME``, ``KINGDOM``, ``ORDER``, ``PHYLUM``, ``SECTION``, ``SERIES``, ``SPECIES``, ``STRAIN``, ``SUBCLASS``,
#      ``SUBFAMILY``, ``SUBFORM``, ``SUBGENUS``, ``SUBKINGDOM``, ``SUBORDER``, ``SUBPHYLUM``, ``SUBSECTION``, ``SUBSERIES``,
#      ``SUBSPECIES``, ``SUBTRIBE``, ``SUBVARIETY``, ``SUPERCLASS``, ``SUPERFAMILY``, ``SUPERORDER``, ``SUPERPHYLUM``,
#      ``SUPRAGENERIC_NAME``, ``TRIBE``, ``UNRANKED``, ``VARIETY`` (optional)
#   :param verbose: [bool] If True show alternative matches considered which had been rejected.
#   :param higherTaxonKey: [str] Filters by any of the higher Linnean rank keys. Note this
#       is within the respective checklist and not searching nub keys across all checklists (optional)
#   :param status: [str] (optional) Filters by the taxonomic status as one of:
#     - ``ACCEPTED``
#     - ``DETERMINATION_SYNONYM`` Used for unknown child taxa referred to via spec, ssp, ...
#     - ``DOUBTFUL`` Treated as accepted, but doubtful whether this is correct.
#     - ``HETEROTYPIC_SYNONYM`` More specific subclass of ``SYNONYM``.
#     - ``HOMOTYPIC_SYNONYM`` More specific subclass of ``SYNONYM``.
#     - ``INTERMEDIATE_RANK_SYNONYM`` Used in nub only.
#     - ``MISAPPLIED`` More specific subclass of ``SYNONYM``.
#     - ``PROPARTE_SYNONYM`` More specific subclass of ``SYNONYM``.
#     - ``SYNONYM`` A general synonym, the exact type is unknown.
#   :param isExtinct: [bool] Filters by extinction status (e.g. ``isExtinct=TRUE``)
#   :param habitat: [str] Filters by habitat. One of: ``marine``, ``freshwater``, or
#       ``terrestrial`` (optional)
#   :param nameType: [str] (optional) Filters by the name type as one of:
#     - ``BLACKLISTED`` surely not a scientific name.
#     - ``CANDIDATUS`` Candidatus is a component of the taxonomic name for a bacterium
#     that cannot be maintained in a Bacteriology Culture Collection.
#     - ``CULTIVAR`` a cultivated plant name.
#     - ``DOUBTFUL`` doubtful whether this is a scientific name at all.
#     - ``HYBRID`` a hybrid formula (not a hybrid name).
#     - ``INFORMAL`` a scientific name with some informal addition like "cf." or
#     indetermined like Abies spec.
#     - ``SCINAME`` a scientific name which is not well formed.
#     - ``VIRUS`` a virus name.
#     - ``WELLFORMED`` a well formed scientific name according to present nomenclatural rules.
#   :param datasetKey: [str] Filters by the dataset's key (a uuid) (optional)
#   :param nomenclaturalStatus: [str] Not yet implemented, but will eventually allow for
#       filtering by a nomenclatural status enum
#   :param limit: [fixnum] Number of records to return. Maximum: ``1000``. (optional)
#   :param start: [fixnum] Record number to start at. (optional)
#   :param facet: [str] A list of facet names used to retrieve the 100 most frequent values
#       for a field. Allowed facets are: ``datasetKey``, ``higherTaxonKey``, ``rank``, ``status``,
#       ``isExtinct``, ``habitat``, and ``nameType``. Additionally ``threat`` and ``nomenclaturalStatus``
#       are legal values but not yet implemented, so data will not yet be returned for them. (optional)
#   :param facetMincount: [str] Used in combination with the facet parameter. Set
#       ``facetMincount={#}`` to exclude facets with a count less than {#}, e.g.
#       http://bit.ly/1bMdByP only shows the type value ``ACCEPTED`` because the other
#       statuses have counts less than 7,000,000 (optional)
#   :param facetMultiselect: [bool] Used in combination with the facet parameter. Set
#       ``facetMultiselect=TRUE`` to still return counts for values that are not currently
#       filtered, e.g. http://bit.ly/19YLXPO still shows all status values even though
#       status is being filtered by ``status=ACCEPTED`` (optional)
#   :param type: [str] Type of name. One of ``occurrence``, ``checklist``, or ``metadata``. (optional)
#   :param hl: [bool] Set ``hl=TRUE`` to highlight terms matching the query when in fulltext
#       search fields. The highlight will be an emphasis tag of class ``gbifH1`` e.g.
#       ``query='plant', hl=TRUE``. Fulltext search fields include: ``title``, ``keyword``, ``country``,
#       ``publishing country``, ``publishing organization title``, ``hosting organization title``, and
#       ``description``. One additional full text field is searched which includes information from
#       metadata documents, but the text of this field is not returned in the response. (optional)

#   :return: A dictionary, of results

#   :references: http://www.gbif.org/developer/species#searching

#   Usage::

#       # Look up names like mammalia
#       species.name_lookup(query='mammalia')

#       # Paging
#       species.name_lookup(query='mammalia', limit=1)
#       species.name_lookup(query='mammalia', limit=1, start=2)

#       # large requests, use start parameter
#       first = species.name_lookup(query='mammalia', limit=1000)
#       second = species.name_lookup(query='mammalia', limit=1000, start=1000)
#       tail(first$data)
#       head(second$data)
#       first$meta
#       second$meta

#       # Get all data and parse it, removing descriptions which can be quite long
#       out = species.name_lookup('Helianthus annuus', rank="species", verbose=TRUE)
#       lapply(out$data, function(x) x[!names(x) %in% c("descriptions","descriptionsSerialized")])

#       # Search for a genus, returning just data
#       species.name_lookup(query='Cnaemidophorus', rank="genus", return="data")

#       # Just metadata
#       species.name_lookup(query='Cnaemidophorus', rank="genus", return="meta")

#       # Just hierarchies
#       species.name_lookup(query='Cnaemidophorus', rank="genus", return="hierarchy")

#       # Just vernacular (common) names
#       species.name_lookup(query='Cnaemidophorus', rank="genus", return="names")

#       # Fuzzy searching
#       species.name_lookup(query='Cnaemidophor', rank="genus")

#       # Limit records to certain number
#       species.name_lookup('Helianthus annuus', rank="species", limit=2)

#       # Query by habitat
#       species.name_lookup(habitat = "terrestrial", limit=2)
#       species.name_lookup(habitat = "marine", limit=2)
#       species.name_lookup(habitat = "freshwater", limit=2)

#       # Using faceting
#       species.name_lookup(facet='status', limit=0, facetMincount='70000')
#       species.name_lookup(facet=c('status','higherTaxonKey'), limit=0, facetMincount='700000')

#       species.name_lookup(facet='nameType', limit=0)
#       species.name_lookup(facet='habitat', limit=0)
#       species.name_lookup(facet='datasetKey', limit=0)
#       species.name_lookup(facet='rank', limit=0)
#       species.name_lookup(facet='isExtinct', limit=0)

#       species.name_lookup(isExtinct=TRUE, limit=0)

#       # text highlighting
#       ## turn on highlighting
#       res = species.name_lookup(query='canada', hl=TRUE, limit=5)
#       res$data
#       species.name_lookup(query='canada', hl=TRUE, limit=45, return='data')
#       ## and you can pass the output to gbif_names() function
#       res = species.name_lookup(query='canada', hl=TRUE, limit=5)
#       gbif_names(res)

#       # Lookup by datasetKey
#       species.name_lookup(datasetKey='3f8a1297-3259-4700-91fc-acc4170b27ce')
#   '''
#   if is_not_none(facetMincount) and facetMincount.__class__ != str:
#     raise "Make sure facetMincount is character"

#   if is_not_none(facet):
#     facetbyname = facet
#     names(facetbyname) = rep('facet', len(facet))
#   else:
#     facetbyname = None

#   url = gbif_baseurl + '/species/search'
#   args = {'q': query, 'rank': rank, 'higherTaxonKey': higherTaxonKey,
#     'status': status, 'isExtinct': isExtinct, 'habitat': habitat,
#     'nameType': nameType, 'datasetKey': datasetKey,
#     'nomenclaturalStatus': nomenclaturalStatus, 'limit': limit, 'offset': start,
#     'facetMincount': facetMincount, 'facetMultiselect': facetMultiselect,
#     'hl': hl, 'type': type}
#   args = c(args, facetbyname)
#   tt = gbif_GET(url, args, **kwargs)

#   # metadata
#   meta = tt[c('offset', 'limit', 'endOfRecords', 'count')]

#   # facets
#   facets = tt$facets
#   if (!length(facets) == 0) {
#     facetsdat = lapply(facets, function(x) do.call(rbind, lapply(x$counts, data.frame, stringsAsFactors = FALSE)))
#     names(facetsdat) = tolower(sapply(facets, "[[", "field"))
#   } else {
#     facetsdat = NULL
#   }

#   # actual data
#   if (!verbose) {
#     data = as.data.frame(
#       data.table::rbindlist(
#         lapply(tt$results, namelkupcleaner),
#         use.names = TRUE, fill = TRUE))
#     if (limit > 0) data = movecols(data, c('key', 'scientificName'))
#   } else {
#     data = tt$results
#   }

#   # hierarchies
#   hierdat = lapply(tt$results, function(x){
#     tmp = x[ names(x) %in% "higherClassificationMap" ]
#     tmpdf = data.frame(rankkey = names(rgbif_compact(tmp[[1]])),
#                         name = unlist(unname(rgbif_compact(tmp[[1]]))),
#                         stringsAsFactors = FALSE)
#     if (NROW(tmpdf) == 0) NULL else tmpdf
#   })
#   names(hierdat) = vapply(tt$results, "[[", numeric(1), "key")

#   # vernacular names
#   vernames = lapply(tt$results, function(x){
#     rbind_fill(lapply(x$vernacularNames, data.frame))
#   })
#   names(vernames) = vapply(tt$results, "[[", numeric(1), "key")

#   return {meta = meta, data = data, facets = facetsdat,
#     hierarchies = compact_null(hierdat), names = compact_null(vernames))}

def suggestfields():
  '''
  Fields available in ``gbif_suggest()`` function
  '''
  return ["key","datasetTitle","datasetKey","nubKey","parentKey","parent",
    "kingdom","phylum","class","order","family","genus","species",
    "kingdomKey","phylumKey","classKey","orderKey","familyKey","genusKey",
    "speciesKey","species","canonicalName","authorship",
    "accordingTo","nameType","taxonomicStatus","rank","numDescendants",
    "numOccurrences","sourceId","nomenclaturalStatus","threatStatuses",
    "synonym","higherClassificationMap"]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
