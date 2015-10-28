pygbif
=======

Python client for the [GBIF API](http://www.gbif.org/developer/summary)

Other GBIF clients:

* R: `rgbif`, [ropensci/rgbif](https://github.com/ropensci/rgbif)

## Installation

```
[sudo] pip install git+git://github.com/sckott/pygbif.git#egg=pygbif
```

## Datasets

```python
pygbif.dataset_metrics(uuid='3f8a1297-3259-4700-91fc-acc4170b27ce')
```

## Taxonomic Names

```python
pygbif.name_suggest(q='Puma concolor')
```

## Occurrence data

```python
from pygbif import occurrences
occurrences.search(taxonKey = 3329049)
occurrences.get(taxonKey = 252408386)
occurrences.count(isGeoreferenced = True)
```

## LICENSE

MIT, see [LICENSE file](LICENSE)
