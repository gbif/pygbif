from ..gbifutils import *

def name_backbone(name, rank=None, kingdom=None, phylum=None, clazz=None,
  order=None, family=None, genus=None, strict=False, verbose=False,
  start=None, limit=100, **kwargs):
  '''
  Lookup names in the GBIF backbone taxonomy.

  :param name: (character) Full scientific name potentially with authorship (required)
  :param rank: (character) The rank given as our rank enum. (optional)
  :param kingdom: (character) If provided default matching will also try to match against this
     if no direct match is found for the name alone. (optional)
  :param phylum: (character) If provided default matching will also try to match against this
     if no direct match is found for the name alone. (optional)
  :param class: (character) If provided default matching will also try to match against this
     if no direct match is found for the name alone. (optional)
  :param order: (character) If provided default matching will also try to match against this
     if no direct match is found for the name alone. (optional)
  :param family: (character) If provided default matching will also try to match against this
     if no direct match is found for the name alone. (optional)
  :param genus: (character) If provided default matching will also try to match against this
     if no direct match is found for the name alone. (optional)
  :param strict: (logical) If True it (fuzzy) matches only the given name, but never a
     taxon in the upper classification (optional)
  :param verbose: (logical) If True show alternative matches considered which had been rejected.

  A list for a single taxon with many slots (with verbose=False - default), or a
  list of length two, first element for the suggested taxon match, and a data.frame
  with alternative name suggestions resulting from fuzzy matching (with verbose=True).

  If you don't get a match GBIF gives back a list of length 3 with slots synonym,
  confidence, and matchType='NONE'.

  reference: http://www.gbif.org/developer/species#searching

  Usage:
  >>> from pygbif import species
  >>> species.name_backbone(name='Helianthus annuus', kingdom='plants')
  >>> species.name_backbone(name='Helianthus', rank='genus', kingdom='plants')
  >>> species.name_backbone(name='Poa', rank='genus', family='Poaceae')
  >>>
  >>> # Verbose - gives back alternatives
  >>> species.name_backbone(name='Helianthus annuus', kingdom='plants', verbose=True)
  >>>
  >>> # Strictness
  >>> species.name_backbone(name='Poa', kingdom='plants', verbose=True, strict=False)
  >>> species.name_backbone(name='Helianthus annuus', kingdom='plants', verbose=True, strict=True)
  >>>
  >>> # Non-existent name
  >>> species.name_backbone(name='Aso')
  >>>
  >>> # Multiple equal matches
  >>> species.name_backbone(name='Oenante')
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

  :param q: (character, required) Simple search parameter. The value for this parameter can be a
     simple word or a phrase. Wildcards can be added to the simple word parameters only,
     e.g. q=*puma*
  :param datasetKey: (character) Filters by the checklist dataset key (a uuid, see examples)
  :param rank: (character) A taxonomic rank. One of class, cultivar, cultivar_group, domain, family,
     form, genus, informal, infrageneric_name, infraorder, infraspecific_name,
     infrasubspecific_name, kingdom, order, phylum, section, series, species, strain, subclass,
     subfamily, subform, subgenus, subkingdom, suborder, subphylum, subsection, subseries,
     subspecies, subtribe, subvariety, superclass, superfamily, superorder, superphylum,
     suprageneric_name, tribe, unranked, or variety.
  :param fields: (character) Fields to return in output data.frame (simply prunes columns off)

  Usage:
  >>> from pygbif import species
  >>> species.name_suggest(q='Puma concolor')
  >>> species.name_suggest(q='Puma')
  >>> species.name_suggest(q='Puma', rank="genus")
  >>> species.name_suggest(q='Puma', rank="subspecies")
  >>> species.name_suggest(q='Puma', rank="species")
  >>> species.name_suggest(q='Puma', rank="infraspecific_name")
  >>> species.name_suggest(q='Puma', limit=2)
  >>> species.name_suggest(q='Puma', fields=['key','canonicalName'])
  >>> species.name_suggest(q='Puma', fields=['key','canonicalName','higherClassificationMap'])
  '''
  url = gbif_baseurl + 'species/suggest'
  args = {'q':q, 'rank':rank, 'offset':start, 'limit':limit}
  tt = gbif_GET(url, args, **kwargs)

  if fields is None:
    toget = ["key","canonicalName","rank"]
  else:
    toget = fields

  buck = []
  for x in toget:
    buck.append(filter(lambda x: x is True, [x==toget[0] for x in suggestfields()]))

  if len(buck) == 0:
    raise NoResultException("some fields are not valid")

  if fields is not None:
    tmp1 = filter(None, [x=="higherClassificationMap" for x in fields])
  else:
    tmp1 = None

  if tmp1 is not None:
    hier = [ x['higherClassificationMap'] for x in tt ]
    [ x.pop('higherClassificationMap') for x in tt ]
    return {'data': tt, 'hierarchy': hier}
  else:
    out = []
    for x in tt:
      out.append(dict(zip(toget, [x[y] for y in toget])))
    return out

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
