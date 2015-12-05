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

  A list for a single taxon with many slots (with verbose=False - default), or a
  list of length two, first element for the suggested taxon match, and a data.frame
  with alternative name suggestions resulting from fuzzy matching (with verbose=True).

  If you don't get a match GBIF gives back a list of length 3 with slots synonym,
  confidence, and matchType='NONE'.

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
     e.g. q=*puma* (Required)
  :param datasetKey: [str] Filters by the checklist dataset key (a uuid, see examples)
  :param rank: [str] A taxonomic rank. One of class, cultivar, cultivar_group, domain, family,
     form, genus, informal, infrageneric_name, infraorder, infraspecific_name,
     infrasubspecific_name, kingdom, order, phylum, section, series, species, strain, subclass,
     subfamily, subform, subgenus, subkingdom, suborder, subphylum, subsection, subseries,
     subspecies, subtribe, subvariety, superclass, superfamily, superorder, superphylum,
     suprageneric_name, tribe, unranked, or variety.

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

def suggestfields():
  '''
  Fields available in `gbif_suggest()` function
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
