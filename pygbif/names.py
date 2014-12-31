import sys
import json
from simplejson import JSONDecodeError
from gbifutils import *

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
  pygbif.name_backbone(name='Helianthus annuus', kingdom='plants')
  pygbif.name_backbone(name='Helianthus', rank='genus', kingdom='plants')
  pygbif.name_backbone(name='Poa', rank='genus', family='Poaceae')

  # Verbose - gives back alternatives
  pygbif.name_backbone(name='Helianthus annuus', kingdom='plants', verbose=True)

  # Strictness
  pygbif.name_backbone(name='Poa', kingdom='plants', verbose=True, strict=False)
  pygbif.name_backbone(name='Helianthus annuus', kingdom='plants', verbose=True, strict=True)

  # Non-existent name - returns list of lenght 3 stating no match
  pygbif.name_backbone(name='Aso')
  pygbif.name_backbone(name='Oenante')
  '''
  url = baseurl + 'species/match'
  args = {'name': name, 'rank': rank, 'kingdom': kingdom, 'phylum': phylum,
         'class': clazz, 'order': order, 'family': family, 'genus': genus,
         'strict': strict, 'verbose': verbose, 'offset': start, 'limit': limit}
  tt = gbif_GET(url, args, **kwargs)
  return tt
  # if verbose:
  #   alt = do.call(rbind.fill, lapply(tt$alternatives, backbone_parser))
  #   dat = data.frame(tt[!names(tt) %in% c("alternatives","note")], stringsAsFactors=False)
  #   structure(list(data=dat, alternatives=alt), note=tt$note)
  # else:
  #   structure(tt[!names(tt) %in% c("alternatives","note")], note=tt$note)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
