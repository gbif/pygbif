pygbif
=======

[![Build Status](https://travis-ci.org/sckott/pygbif.svg)](https://travis-ci.org/sckott/pygbif)
[![Coverage Status](https://coveralls.io/repos/sckott/pygbif/badge.svg?branch=master&service=github)](https://coveralls.io/github/sckott/pygbif?branch=master)
[![Docs](https://readthedocs.org/projects/pygbif/badge/?version=latest)](http://pygbif.rtfd.org/)

Python client for the [GBIF API](http://www.gbif.org/developer/summary)

Other GBIF clients:

* R: `rgbif`, [ropensci/rgbif](https://github.com/ropensci/rgbif)

## Installation

Stable from pypi

```
pip install pygbif
```

Development version

```
[sudo] pip install git+git://github.com/sckott/pygbif.git#egg=pygbif
```

`pygbif` is split up into modules for each of the major groups of API methods.

* Registry - Datasets, Nodes, Installations, Networks, Organizations
* Species - Taxonomic names
* Occurrences - Occurrence data, including the download API

You can import the entire library, or each module individually as needed.

Note that [GBIF maps API](http://www.gbif.org/developer/maps) is not included in `pygbif`.

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

## Meta

* License: MIT, see [LICENSE file](LICENSE)
* Please note that this project is released with a [Contributor Code of Conduct](CONDUCT.md). By participating in this project you agree to abide by its terms.
