Changelog
=========
0.6.4 (2024-03-12)
------------------
- fixed a bug in building the documentation with readthedocs :issue:`138`, :issue:`129`
- tests now run against live GBIF APIs :issue:`101`, :issue:`128`  
- updated caching.py since the ``remove_expired_responses`` method is deprecated. :issue:`126`

0.6.3 (2023-05-25)
------------------
- added support for predicates: ``isNull``, ``isNotNull``, ``in`` and ``not`` :issue:`92`, :issue:`102` and :issue:`103` 
- added support for nested queries/dictionaries :issue:`104`
- deprecated the ``add_predicate`` function and added ``add_pred_dict`` to accomodate for newly supported predicates to ensure that the arguments that are sent are added in the payload function :issue:`108`
- added support for multiple download formats :issue:`105`
- updated operators and look-up tables :issue:`107`
- included documentation on newly supported predicates and dictionaries :issue:`106`

0.6.2 (2023-01-24)
------------------
- update to fix requesting GBIF downloads
- minor documentation updates :issue:`95` and :issue:`99`

0.6.1 (2022-06-23)
------------------
- update to fix broken dependencies :issue:`93`
- minor documentation updates

0.6.0 (2021-07-08)
------------------
- Fix for `occurrences.download` when giving `geometry` as a string rather than using `add_geometry`; predicates were being split on whitespace, which doesn't work for WKT :issue:`81` :issue:`84`
- Moved to using the `logging` module instead of `print()` for giving information on occurrence download methods :issue:`78`
- Clarify that `occurrences.count` for length 1 inputs only; see `occurrences.search` for > 1 value :issue:`75` :issue:`77`
- Improved documentation for `species.name_usage` method, mostly for the `language` parameter :issue:`68`
- Gains download method `download_cancel` for cancelling/deleting a download request :issue:`59`

0.5.0 (2020-09-29)
------------------
- `occurrences.search` now supports `recordedByID` and `identifiedByID` search parameters :issue:`62`
- clean up the Contributing file, thanks @niconoe :issue:`64`
- clean up internal imports in the library, thanks @niconoe :issue:`65`
- fix usage of `is` and `==`, was using them inappropriately sometimes (via https://realpython.com/python-is-identity-vs-equality/), :issue:`69`
- remove redundant parameter in a doc string, thanks @faroit :issue:`71`
- make a test for internal fxn `gbif_GET_write` more general to avoid errors if GBIF changes content type response header slightly :issue:`72`

0.4.0 (2019-11-20)
------------------
- changed base url to https for all requests; was already https for maps and downloads in previous versions
- occurrences, species, and registry modules gain docstrings with brief summary of each method
- pygbif gains ability to cache http requests. caching is off by default. See `?pygbif.caching` for all the details :issue:`52` :issue:`56` via @nleguillarme
- made note in docs that if you are trying to get the same behavior as the GBIF website for name searching, `species.name_backbone` is likely what you want :issue:`55` thanks @qgroom
- for parameters that expect a `bool`, convert them to lowercase strings internally before doing HTTP requests

0.3.0 (2019-01-25)
------------------
- pygbif is Python 3 only now :issue:`19`
- Gains maps module with maps.map method for working with the GBIF maps API :issue:`41` :issue:`49`
- Gains new module utils with one method `wkt_rewind`  :issue:`46` thanks @aubreymoore for the inspiration
- Fixed bug in registry.installations: typo in one of the parameters `identifierTyp` instead of `identifierType` :issue:`48` thanks @data-biodiversity-aq
- Link to GitHub issues from Changelog 🎉
- Fix a occurrence download test :issue:`47`
- Much more thorough docs :issue:`25`

0.2.0 (2016-10-18)
------------------
- Download methods much improved :issue:`16` :issue:`27` thanks @jlegind @stijnvanhoey @peterdesmet !
- MULTIPOLYGON now supported in `geometry` parameter :issue:`35`
- Fixed docs for `occurrences.get`, and `occurrences.get_verbatim`, `occurrences.get_fragment` and demo that used occurrence keys that no longer exist in GBIF :issue:`39`
- Added `organizations` method to `registry` module :issue:`12`
- Added remainder of datasets methods: `registry.dataset_search` (including faceting support :issue:`37`) and `registry.dataset_suggest`, for the `/dataset/search` and `/dataset/suggest` routes, respectively :issue:`40`
- Added remainder of species methods: `species.name_lookup` (including faceting support :issue:`38`) and `species.name_usage`, for the `/species/search` and `/species` routes, respectively :issue:`18`
- Added more tests to cover new methods
- Changed `species.name_suggest` to give back data stucture as received from GBIF. We used to parse out the classification data, but for simplicity and speed, that is left up to the user now.
- `start` parameter in `species.name_suggest`, `occurrences.download_list`, `registry.organizations`, `registry.nodes`, `registry.networks`, and `registry.installations`, changed to `offset` to match GBIF API and match usage throughout remainder of `pygbif`

0.1.5.4 (2016-10-01)
--------------------
- Added many new `occurrence.search` parameters, including `repatriated`, `kingdomKey`, `phylumKey`, `classKey`, `orderKey`, `familyKey`, `genusKey`, `subgenusKey`, `establishmentMeans`, `facet`, `facetMincount`, `facetMultiselect`, and support for facet paging via	`**kwargs` :issue:`30` :issue:`34`
- Fixes to `**kwargs` in `occurrence.search` so that facet parameters can be parsed correctly and `requests` GET	request options are collected correctly :issue:`36`
- Added `spellCheck` parameter to `occurrence.search` that goes along with the `q` parameter to optionally spell check full text searches :issue:`31`

0.1.4 (2016-06-04)
------------------
- Added variable types throughout docs
- Changed default `limit` value to 300 for `occurrences.search` method
- `tox` now included, via @xrotwang :issue:`20`
- Added more registry methods :issue:`11`
- Started occurrence download methods :issue:`16`
- Added more names methods :issue:`18`
- All requests now send user-agent headers with `requests` and `pygbif` versions :issue:`13`
- Bug fix for `occurrences.download_get` :issue:`23`
- Fixed bad example for `occurrences.get` :issue:`22`
- Fixed wheel to be universal for 2 and 3 :issue:`10`
- Improved documentation a lot, autodoc methods now

0.1.1 (2015-11-03)
------------------
- Fixed distribution for pypi

0.1.0 (2015-11-02)
------------------
- First release
