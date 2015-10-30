pygbif
=======

[![Build Status](https://travis-ci.org/sckott/pygbif.svg)](https://travis-ci.org/sckott/pygbif)
[![Coverage Status](https://coveralls.io/repos/sckott/pygbif/badge.svg?branch=master&service=github)](https://coveralls.io/github/sckott/pygbif?branch=master)

Python client for the [GBIF API](http://www.gbif.org/developer/summary)

Other GBIF clients:

* R: `rgbif`, [ropensci/rgbif](https://github.com/ropensci/rgbif)

## Installation

```
[sudo] pip install git+git://github.com/sckott/pygbif.git#egg=pygbif
```

## Registry module

```python
from pygbif import registry
registry.dataset_metrics(uuid='3f8a1297-3259-4700-91fc-acc4170b27ce')
```

## Species module

```python
from pygbif import species
species.name_suggest(q='Puma concolor')
```

## Occurrences module

```python
from pygbif import occurrences
occurrences.search(taxonKey = 3329049)
occurrences.get(taxonKey = 252408386)
occurrences.count(isGeoreferenced = True)
```

## LICENSE

MIT, see [LICENSE file](LICENSE)
