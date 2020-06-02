from pygbif.gbifutils import gbif_baseurl, gbif_GET


def name_suggest(q=None, datasetKey=None, rank=None, limit=100, offset=None, **kwargs):
    """
  A quick and simple autocomplete service that returns up to 20 name usages by
  doing prefix matching against the scientific name. Results are ordered by relevance.

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
  :param limit: [fixnum] Number of records to return. Maximum: ``1000``. (optional)
  :param offset: [fixnum] Record number to start at. (optional)

  :return: A dictionary

  References: http://www.gbif.org/developer/species#searching

  Usage::

      from pygbif import species

      species.name_suggest(q='Puma concolor')
      x = species.name_suggest(q='Puma')
      species.name_suggest(q='Puma', rank="genus")
      species.name_suggest(q='Puma', rank="subspecies")
      species.name_suggest(q='Puma', rank="species")
      species.name_suggest(q='Puma', rank="infraspecific_name")
      species.name_suggest(q='Puma', limit=2)
  """
    url = gbif_baseurl + "species/suggest"
    args = {"q": q, "rank": rank, "offset": offset, "limit": limit}
    return gbif_GET(url, args, **kwargs)


def suggestfields():
    """
  Fields available in ``gbif_suggest()`` function
  """
    return [
        "key",
        "datasetTitle",
        "datasetKey",
        "nubKey",
        "parentKey",
        "parent",
        "kingdom",
        "phylum",
        "class",
        "order",
        "family",
        "genus",
        "species",
        "kingdomKey",
        "phylumKey",
        "classKey",
        "orderKey",
        "familyKey",
        "genusKey",
        "speciesKey",
        "species",
        "canonicalName",
        "authorship",
        "accordingTo",
        "nameType",
        "taxonomicStatus",
        "rank",
        "numDescendants",
        "numOccurrences",
        "sourceId",
        "nomenclaturalStatus",
        "threatStatuses",
        "synonym",
        "higherClassificationMap",
    ]
