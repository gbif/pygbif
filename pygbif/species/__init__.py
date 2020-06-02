"""
GBIF taxonomic names APIs methods

* `name_backbone`: Lookup names in the GBIF backbone taxonomy
* `name_suggest`: Quick and simple autocomplete lookup service
* `name_usage`: Lookup details for specific names in all taxonomies in GBIF
* `name_lookup`: Lookup names in all taxonomies in GBIF
* `name_parser`: Parse taxon names using the GBIF name parser

If you are looking for behavior similar to the GBIF website when you search
for a name, `name_backbone` may be what you want. For example, a search for
*Lantanophaga pusillidactyla* on the GBIF website and with `name_backbone`
will give back as a first result the correct name
*Lantanophaga pusillidactylus*.
"""

from .name_suggest import name_suggest
from .name_backbone import name_backbone
from .name_lookup import name_lookup
from .name_usage import name_usage
from .name_parser import name_parser
