pygbif
=======

This is a port of the R package `rgbif`, found at [ropensci/rgbif](https://github.com/ropensci/rgbif).

## Installation

```
[sudo] pip install git+git://github.com/sckott/pygbif.git#egg=pygbif
```

## Datasets info

```python
pygbif.dataset_metrics(uuid='3f8a1297-3259-4700-91fc-acc4170b27ce')
```

```python
{u'colCoveragePct': 71,
 u'colMatchingCount': 20045,
 u'countByIssue': {},
 u'countByKingdom': {u'ANIMALIA': 1, u'INCERTAE_SEDIS': 18, u'PLANTAE': 8871},
 u'countByOrigin': {u'DENORMED_CLASSIFICATION': 111,
  u'PROPARTE': 11,
  u'SOURCE': 27946},
 u'countByRank': {u'CLASS': 2,
  u'FAMILY': 172,
  u'GENUS': 1241,
  u'ORDER': 55,
  u'SECTION': 317,
  u'SERIES': 40,
  u'SPECIES': 5972,
  u'SUBCLASS': 6,
  u'SUBFAMILY': 148,
  u'SUBGENUS': 198,
  u'SUBSECTION': 56,
  u'SUBSPECIES': 748,
  u'SUBTRIBE': 57,
  u'SUPERORDER': 12,
  u'TRIBE': 323,
  u'VARIETY': 855},
 u'countExtRecordsByExtension': {u'DESCRIPTION': 10091,
  u'DISTRIBUTION': 28884,
  u'IDENTIFIER': 0,
  u'IMAGE': 0,
  u'REFERENCE': 0,
  u'SPECIES_PROFILE': 0,
  u'TYPES_AND_SPECIMEN': 0,
  u'VERNACULAR_NAME': 31045},
 u'countNamesByLanguage': {u'ENGLISH': 20474, u'FRENCH': 10571},
 u'created': u'2014-07-08T18:17:36.186+0000',
 u'datasetKey': u'3f8a1297-3259-4700-91fc-acc4170b27ce',
 u'distinctNamesCount': 28028,
 u'key': 4341,
 u'nubCoveragePct': 94,
 u'nubMatchingCount': 26618,
 u'otherCount': {},
 u'synonymsCount': 17866,
 u'usagesCount': 28068}
```

## Names

```python
pygbif.name_suggest(q='Puma concolor')
```

```python
[{'canonicalName': u'Puma', 'key': 2435098, 'rank': u'GENUS'},
 {'canonicalName': u'Puma concolor', 'key': 2435099, 'rank': u'SPECIES'},
 {'canonicalName': u'Puma yagouaroundi', 'key': 2435146, 'rank': u'SPECIES'},
 {'canonicalName': u'Puma lacustris', 'key': 4969803, 'rank': u'SPECIES'},
 {'canonicalName': u'Puma yagouaroundi yagouaroundi',
  'key': 7193926,
  'rank': u'SUBSPECIES'},
 {'canonicalName': u'Puma concolor concolor',
  'key': 7193927,
  'rank': u'SUBSPECIES'},
 {'canonicalName': u'Puma concolor anthonyi',
  'key': 6164589,
  'rank': u'SUBSPECIES'},
 {'canonicalName': u'Puma concolor couguar',
  'key': 6164590,
  'rank': u'SUBSPECIES'},

...cutoff
```

## Occurrence data

```python
key = pygbif.name_suggest(q='Helianthus annuus', rank='species')['key']
pygbif.search(taxonKey=key[0]['key'], limit=2)
```

```python
{u'count': 20314,
 u'endOfRecords': False,
 u'limit': 2,
 u'offset': 1,
 u'results': [{u'basisOfRecord': u'HUMAN_OBSERVATION',
   u'catalogNumber': u'569098',
   u'class': u'Magnoliopsida',
   u'classKey': 220,
   u'collectionCode': u'Observations',
   u'country': u'Singapore',
   u'countryCode': u'SG',
   u'datasetKey': u'50c9509d-22c7-4a22-a47d-8c48425ef4a7',
   u'datasetName': u'iNaturalist research-grade observations',
   u'dateIdentified': u'2014-03-15T05:22:53.000+0000',
   u'day': 30,
   u'decimalLatitude': 1.2789,
   u'decimalLongitude': 103.7993,
   u'eventDate': u'2014-01-30T08:36:00.000+0000',
   u'eventTime': u'00:36:00Z',
   u'extensions': {},
   u'facts': [],
   u'family': u'Asteraceae',
   u'familyKey': 3065,
   u'gbifID': u'899948224',
   u'genericName': u'Helianthus',
   u'genus': u'Helianthus',
   u'genusKey': 3119134,
   u'geodeticDatum': u'WGS84',
   u'identificationID': u'1000020',
   u'identifier': u'569098',
   u'identifiers': [],
   u'institutionCode': u'iNaturalist',
   u'issues': [u'COORDINATE_ROUNDED',
    u'GEODETIC_DATUM_ASSUMED_WGS84',
    u'COUNTRY_DERIVED_FROM_COORDINATES'],

...cutoff
```

## LICENSE

MIT
