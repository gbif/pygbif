Changelog
=========

0.2.0 (2016-10-18)
--------------------
- Download methods much improved (#16) (#27) thanks @jlegind @stijnvanhoey @peterdesmet !
- MULTIPOLYGON now supported in `geometry` parameter (#35)
- Fixed docs for `occurrences.get`, and `occurrences.get_verbatim`,
`occurrences.get_fragment` and demo that used occurrence keys that no longer
exist in GBIF (#39)
- xxx (#xx)
- xxx (#xx)
- xxx (#xx)
- xxx (#xx)

0.1.5.4 (2016-10-01)
--------------------
- Added many new `occurrence.search` parameters, including `repatriated`, `kingdomKey`, `phylumKey`, `classKey`, `orderKey`, `familyKey`, `genusKey`, `subgenusKey`, `establishmentMeans`, `facet`, `facetMincount`, `facetMultiselect`, and support for facet paging via	`**kwargs` (#30) (#34)
- Fixes to `**kwargs` in `occurrence.search` so that facet parameters can be parsed correctly and `requests` GET	request options are collected correctly (#36)
- Added `spellCheck` parameter to `occurrence.search` that goes along with the `q` parameter to optionally spell check full text searches (#31)

0.1.4 (2016-06-04)
--------------------
- Added variable types throughout docs
- Changed default `limit` value to 300 for `occurrences.search` method
- `tox` now included, via @xrotwang (#20)
- Added more registry methods (#11)
- Started occurrence download methods (#16)
- Added more names methods (#18)
- All requests now send user-agent headers with `requests` and `pygbif` versions (#13)
- Bug fix for `occurrences.download_get` (#23)
- Fixed bad example for `occurrences.get` (#22)
- Fixed wheel to be universal for 2 and 3 (#10)
- Improved documentation a lot, autodoc methods now

0.1.1 (2015-11-03)
--------------------
- Fixed distribution for pypi

0.1.0 (2015-11-02)
--------------------
- First release
