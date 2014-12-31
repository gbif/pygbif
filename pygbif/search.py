import sys
import requests
import json
from simplejson import JSONDecodeError

class NoResultException(Exception):
    pass

def occ_search(taxonKey=NULL, per_page=5, page=1, **kwargs):
  '''
  Search for occurrences

  :param x: xxx

  Usage:
  # Search by species name, using \code{\link{name_backbone}} first to get key
  (key = name_suggest(q='Helianthus annuus', rank='species')$key[1])
  occ_search(taxonKey=key, limit=2)

  # Return 20 results, this is the default by the way
  occ_search(taxonKey=key, limit=20)

  # Return just metadata for the search
  occ_search(taxonKey=key, limit=100, return='meta')
  '''
  url = baseurl + 'occurrence/search'
  out = requests.get(url, params = {'taxonKey': taxonKey, 'per_page': per_page, 'page': page})
  out.raise_for_status()
  return out.json()

# helper fxns
baseurl = "http://api.gbif.org/v1/"

def geometry_handler(x):
  if(!is.null(x)){
    if(!is.character(x)){
      gbif_bbox2wkt(bbox=x)
    } else { x }
  } else { x }

def pasteargs(b):
  arrrgs = attr(b, "args")
  arrrgs = rgbif_compact(arrrgs)
  tt = list(); for(i in seq_along(arrrgs)){ tt[[i]] = sprintf("%s=%s", names(arrrgs)[i],
          if(length(arrrgs[[i]]) > 1) paste0(arrrgs[[i]], collapse = ",") else arrrgs[[i]]) }
  paste0(tt, collapse = ", ")

def function(z, type='counts', n=10):
  xnames = names(z)
  xnames = sapply(xnames, function(x) if(nchar(x)>8) paste0(substr(x, 1, 6), "..", collapse = "") else x, USE.NAMES = FALSE)
  yep = switch(type,
         counts = vapply(z, function(y) y$meta$count, numeric(1), USE.NAMES = FALSE),
         returned = vapply(z, function(y) NROW(y$data), numeric(1), USE.NAMES = FALSE),
         hier = vapply(z, function(y) length(y$hierarchy), numeric(1), USE.NAMES = FALSE),
         media = vapply(z, function(y) length(y$media), numeric(1), USE.NAMES = FALSE)
  )
  tt = list(); for(i in seq_along(xnames)){ tt[[i]] = sprintf("%s (%s)", xnames[i], yep[[i]]) }
  paste0(tt, collapse = ", ")

def parse_issues(x):
  sapply(x, function(y) list(issue = y), USE.NAMES = FALSE)

def check_limit(x):
  if x > 1000000:
    raise IndexError("Maximum request size is 1 million. As a solution, either use the GBIF web interface, or in R, split up your request in a way that makes sense for your use case. E.g., you could split up your request into geographic chunks, by country or by bounding box. Or you could split up your request taxonomically, e.g., if you want data for all species in a large family of birds, split up by some higher taxonomic level, like tribe or genus.")
  else:
    return x

possparams = "taxonKey, scientificName, datasetKey, catalogNumber, collectorName, geometry, country, publishingCountry, recordNumber, search, institutionCode, collectionCode, decimalLatitude, decimalLongitude, depth, year, typeStatus, lastInterpreted, continent, or mediatype"

def check_vals(x, y):
  if(is.na(x) || is.null(x)) stop(sprintf("%s can not be NA or NULL", y), call. = FALSE)
  if(length(x) > 1) stop(sprintf("%s has to be length 1", y), call. = FALSE)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
