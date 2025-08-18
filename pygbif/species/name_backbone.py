from pygbif.gbifutils import gbif_baseurl, bool2str, gbif_GET

def name_backbone(
   scientificName=None,
   taxonRank=None,
   usageKey=None,
   kingdom=None,
   phylum=None,
   class_=None,
   order=None,
   superfamily=None,
   family=None,
   subfamily=None,
   tribe=None,
   subtribe=None,
   genus=None,
   subgenus=None,
   species=None,
   taxonID=None,
   taxonConceptID=None,
   scientificNameID=None,
   scientificNameAuthorship=None,
   genericName=None,
   specificEpithet=None,
   infraspecificEpithet=None,
   verbatimTaxonRank= None,
   exclude=None,
   strict=None,
   verbose=None,
   checklistKey=None,    
   **kwargs
):
   """
   Match names to the GBIF backbone taxonomy.

   :param scientificName: [str]
      Full scientific name potentially with authorship. (Required)
   :param taxonRank: [str], optional
      Filter by taxonomic rank. See API reference for available values.
   :param usageKey: [str], optional
      The usage key to look up. When provided, all other fields are ignored.
   :param kingdom: [str], optional
      Kingdom to match.
   :param phylum: [str], optional
      Phylum to match.
   :param class_: [str], optional
      Class to match.
   :param order: [str], optional
      Order to match.
   :param superfamily: [str], optional
      Superfamily to match.
   :param family: [str], optional
      Family to match.
   :param subfamily: [str], optional
      Subfamily to match.
   :param tribe: [str], optional
      Tribe to match.
   :param subtribe: [str], optional
      Subtribe to match.
   :param genus: [str], optional
      Genus to match.
   :param subgenus: [str], optional
      Subgenus to match.
   :param species: [str], optional
      Species to match.
   :param taxonID: [str], optional
      The taxon ID to look up. Matches to a taxonID will take precedence over
      scientificName values supplied. A comparison of the matched scientific and
      taxonID is performed to check for inconsistencies.
   :param taxonConceptID: [str], optional
      The taxonConceptID to match. Matches to a taxonConceptID will take precedence
      over scientificName values supplied. A comparison of the matched scientific and
      taxonConceptID is performed to check for inconsistencies.
   :param scientificNameID: [str], optional
      Matches to a scientificNameID will take precedence over scientificName values
      supplied. A comparison of the matched scientific and scientificNameID is performed
      to check for inconsistencies.
   :param scientificNameAuthorship: [str], optional
      The scientific name authorship to match against.
   :param genericName: [str], optional
      Generic part of the name to match when given as atomised parts instead of the full name.
   :param specificEpithet: [str], optional
      Specific epithet to match.
   :param infraspecificEpithet: [str], optional
      Infraspecific epithet to match.
   :param verbatimTaxonRank: [str], optional
      Filters by free text taxon rank.
   :param exclude: [str], optional
      An array of usage keys to exclude from the match.
   :param strict: [bool], optional
      If set to True, fuzzy matches only the given name, but never a taxon in the upper classification.
   :param verbose: [bool], optional
      If set to True, shows alternative matches which were considered but then rejected.
   :param checklistKey: [str], optional
      The key of a checklist to use. Default is the GBIF Backbone taxonomy.

   ``name_backbone()`` return a dictionary with the following keys: 
   ``['usage', 'classification', 'diagnostics', 'synonym']`` 

   - ``usage``: Returns the matched name and some details such usage key.
   - ``classification``: Returns the upper classification of the matched name.
   - ``diagnostics``: Returns information about the match, such as match type, issues, and confidence.
   - ``synonym``: Indicates if the matched name is a synonym.

   The default is to return the best match for the given name. If there are "multiple equal matches", ``name_backbone()``, 
   will return a note in the diagnostics section:
   ``res["diagnostics"]["note"] = "Multiple equal matches for name"``.

   This note usually happens when a binomial name is provided without authorship. Proving authorship will almost always fix the 
   "multiple equal matches" issue. If ``verbose=True``, the function will return other alternative matches. These are accessible 
   via ``res['diagnostics']['alternatives']``.     

   If your name does not get a match, the GBIF API will return ``[matchType] ='NONE'``. If the species-level
   name is not found, the API will sometimes return ``[matchType] = 'HIGHERRANK'``. With higher rank matches,
   the name is matched to a higher taxonomic rank, such as genus or family. Often supplying authorship will 
   improve matching results.  

   If ``strict=True``, then higher taxon ranks will not be returned when there is a "fuzzy match". 
   Higher rank matches will still be returned if the match is exact.

   To match names against a specific checklist, you can use the `checklistKey` parameter.
   This allows you to specify a checklist from which the name should be matched. If no checklistKey is provided,
   the GBIF Backbone Taxonomy is used by default.

   For more information, see the GBIF API documentation:
   https://techdocs.gbif.org/en/openapi/v1/species#/Searching%20names/matchNames

   Usage::

       from pygbif import species
       species.name_backbone(scientificName="Helianthus annuus", kingdom="Plantae")
       species.name_backbone(scientificName="Poa", taxonRank="GENUS", family="Poaceae")

       # Verbose - gives back alternatives
       species.name_backbone(scientificName="Helianthus annuus", kingdom="Plantae", verbose=True)

       # Strictness
       # If strict=True, then higher taxon ranks will not be returned  when there is a "fuzzy match".
       # Higher rank matches will still be returned if the match is exact.
       species.name_backbone(scientificName="Poa", kingdom="Plantae", verbose=True, strict=False)
       species.name_backbone(scientificName="Helianthus annuus", kingdom="Plantae", verbose=True, strict=True)

       # Multiple equal matches
       species.name_backbone(scientificName="Oenante")
       species.name_backbone(scientificName="Oenante", verbose=True)
       species.name_backbone(scientificName="Calopteryx")
       species.name_backbone(scientificName="Calopteryx", verbose=True)

       # Including authorship in scientificName fixes "Multiple equal matches" note
       species.name_backbone(scientificName="Calopteryx splendens (Harris, 1780)")
       species.name_backbone(scientificName="Oenanthe L.")

       # Match using an alternative checklist 
       species.name_backbone(scientificName="Calopteryx splendens", checklistKey="7ddf754f-d193-4cc9-b351-99906754a03b")
   """
   url = "https://api.gbif.org/v2/" + "species/match"
   args = {
       "scientificName": scientificName,
       "taxonRank": taxonRank,
       "usageKey": usageKey,
       "kingdom": kingdom,
       "phylum": phylum,
       "class": class_,
       "order": order,
       "superfamily": superfamily,
       "family": family,
       "subfamily": subfamily,
       "tribe": tribe,
       "subtribe": subtribe,
       "genus": genus,
       "subgenus": subgenus,
       "species": species,
       "taxonID": taxonID,
       "taxonConceptID": taxonConceptID,
       "scientificNameID": scientificNameID,
       "scientificNameAuthorship": scientificNameAuthorship,
       "genericName": genericName,
       "specificEpithet": specificEpithet,
       "infraspecificEpithet": infraspecificEpithet,
       "verbatimTaxonRank": verbatimTaxonRank,
       "exclude": exclude,
       "strict": bool2str(strict),
       "verbose": bool2str(verbose),
       "checklistKey": checklistKey
   }
   tt = gbif_GET(url, args, **kwargs)
   return tt