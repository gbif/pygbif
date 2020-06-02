import re

from pygbif.gbifutils import bool2str, bn, requests_argset, gbif_GET, gbif_baseurl


def name_lookup(
    q=None,
    rank=None,
    higherTaxonKey=None,
    status=None,
    isExtinct=None,
    habitat=None,
    nameType=None,
    datasetKey=None,
    nomenclaturalStatus=None,
    limit=100,
    offset=None,
    facet=False,
    facetMincount=None,
    facetMultiselect=None,
    type=None,
    hl=False,
    verbose=False,
    **kwargs
):
    """
	Lookup names in all taxonomies in GBIF.

	This service uses fuzzy lookup so that you can put in partial names and
	you should get back those things that match. See examples below.

	:param q: [str] Query term(s) for full text search (optional)
	:param rank: [str] ``CLASS``, ``CULTIVAR``, ``CULTIVAR_GROUP``, ``DOMAIN``, ``FAMILY``,
		 ``FORM``, ``GENUS``, ``INFORMAL``, ``INFRAGENERIC_NAME``, ``INFRAORDER``, ``INFRASPECIFIC_NAME``,
		 ``INFRASUBSPECIFIC_NAME``, ``KINGDOM``, ``ORDER``, ``PHYLUM``, ``SECTION``, ``SERIES``, ``SPECIES``, ``STRAIN``, ``SUBCLASS``,
		 ``SUBFAMILY``, ``SUBFORM``, ``SUBGENUS``, ``SUBKINGDOM``, ``SUBORDER``, ``SUBPHYLUM``, ``SUBSECTION``, ``SUBSERIES``,
		 ``SUBSPECIES``, ``SUBTRIBE``, ``SUBVARIETY``, ``SUPERCLASS``, ``SUPERFAMILY``, ``SUPERORDER``, ``SUPERPHYLUM``,
		 ``SUPRAGENERIC_NAME``, ``TRIBE``, ``UNRANKED``, ``VARIETY`` (optional)
	:param verbose: [bool] If ``True`` show alternative matches considered which had been rejected.
	:param higherTaxonKey: [str] Filters by any of the higher Linnean rank keys. Note this
			is within the respective checklist and not searching nub keys across all checklists (optional)
	:param status: [str] (optional) Filters by the taxonomic status as one of:

		* ``ACCEPTED``
		* ``DETERMINATION_SYNONYM`` Used for unknown child taxa referred to via spec, ssp, ...
		* ``DOUBTFUL`` Treated as accepted, but doubtful whether this is correct.
		* ``HETEROTYPIC_SYNONYM`` More specific subclass of ``SYNONYM``.
		* ``HOMOTYPIC_SYNONYM`` More specific subclass of ``SYNONYM``.
		* ``INTERMEDIATE_RANK_SYNONYM`` Used in nub only.
		* ``MISAPPLIED`` More specific subclass of ``SYNONYM``.
		* ``PROPARTE_SYNONYM`` More specific subclass of ``SYNONYM``.
		* ``SYNONYM`` A general synonym, the exact type is unknown.

	:param isExtinct: [bool] Filters by extinction status (e.g. ``isExtinct=True``)
	:param habitat: [str] Filters by habitat. One of: ``marine``, ``freshwater``, or
			``terrestrial`` (optional)
	:param nameType: [str] (optional) Filters by the name type as one of:

		* ``BLACKLISTED`` surely not a scientific name.
		* ``CANDIDATUS`` Candidatus is a component of the taxonomic name for a bacterium that cannot be maintained in a Bacteriology Culture Collection.
		* ``CULTIVAR`` a cultivated plant name.
		* ``DOUBTFUL`` doubtful whether this is a scientific name at all.
		* ``HYBRID`` a hybrid formula (not a hybrid name).
		* ``INFORMAL`` a scientific name with some informal addition like "cf." or indetermined like Abies spec.
		* ``SCINAME`` a scientific name which is not well formed.
		* ``VIRUS`` a virus name.
		* ``WELLFORMED`` a well formed scientific name according to present nomenclatural rules.

	:param datasetKey: [str] Filters by the dataset's key (a uuid) (optional)
	:param nomenclaturalStatus: [str] Not yet implemented, but will eventually allow for
			filtering by a nomenclatural status enum
	:param limit: [fixnum] Number of records to return. Maximum: ``1000``. (optional)
	:param offset: [fixnum] Record number to start at. (optional)
	:param facet: [str] A list of facet names used to retrieve the 100 most frequent values
			for a field. Allowed facets are: ``datasetKey``, ``higherTaxonKey``, ``rank``, ``status``,
			``isExtinct``, ``habitat``, and ``nameType``. Additionally ``threat`` and ``nomenclaturalStatus``
			are legal values but not yet implemented, so data will not yet be returned for them. (optional)
	:param facetMincount: [str] Used in combination with the facet parameter. Set
			``facetMincount={#}`` to exclude facets with a count less than {#}, e.g.
			http://bit.ly/1bMdByP only shows the type value ``ACCEPTED`` because the other
			statuses have counts less than 7,000,000 (optional)
	:param facetMultiselect: [bool] Used in combination with the facet parameter. Set
			``facetMultiselect=True`` to still return counts for values that are not currently
			filtered, e.g. http://bit.ly/19YLXPO still shows all status values even though
			status is being filtered by ``status=ACCEPTED`` (optional)
	:param type: [str] Type of name. One of ``occurrence``, ``checklist``, or ``metadata``. (optional)
	:param hl: [bool] Set ``hl=True`` to highlight terms matching the query when in fulltext
			search fields. The highlight will be an emphasis tag of class ``gbifH1`` e.g.
			``q='plant', hl=True``. Fulltext search fields include: ``title``, ``keyword``, ``country``,
			``publishing country``, ``publishing organization title``, ``hosting organization title``, and
			``description``. One additional full text field is searched which includes information from
			metadata documents, but the text of this field is not returned in the response. (optional)

	:return: A dictionary

	:references: http://www.gbif.org/developer/species#searching

	Usage::

			from pygbif import species

			# Look up names like mammalia
			species.name_lookup(q='mammalia')

			# Paging
			species.name_lookup(q='mammalia', limit=1)
			species.name_lookup(q='mammalia', limit=1, offset=2)

			# large requests, use offset parameter
			first = species.name_lookup(q='mammalia', limit=1000)
			second = species.name_lookup(q='mammalia', limit=1000, offset=1000)

			# Get all data and parse it, removing descriptions which can be quite long
			species.name_lookup('Helianthus annuus', rank="species", verbose=True)

			# Get all data and parse it, removing descriptions field which can be quite long
			out = species.name_lookup('Helianthus annuus', rank="species")
			res = out['results']
			[ z.pop('descriptions', None) for z in res ]
			res

			# Fuzzy searching
			species.name_lookup(q='Heli', rank="genus")

			# Limit records to certain number
			species.name_lookup('Helianthus annuus', rank="species", limit=2)

			# Query by habitat
			species.name_lookup(habitat = "terrestrial", limit=2)
			species.name_lookup(habitat = "marine", limit=2)
			species.name_lookup(habitat = "freshwater", limit=2)

			# Using faceting
			species.name_lookup(facet='status', limit=0, facetMincount='70000')
			species.name_lookup(facet=['status', 'higherTaxonKey'], limit=0, facetMincount='700000')

			species.name_lookup(facet='nameType', limit=0)
			species.name_lookup(facet='habitat', limit=0)
			species.name_lookup(facet='datasetKey', limit=0)
			species.name_lookup(facet='rank', limit=0)
			species.name_lookup(facet='isExtinct', limit=0)

			# text highlighting
			species.name_lookup(q='plant', hl=True, limit=30)

			# Lookup by datasetKey
			species.name_lookup(datasetKey='3f8a1297-3259-4700-91fc-acc4170b27ce')
	"""
    args = {
        "q": q,
        "rank": rank,
        "higherTaxonKey": higherTaxonKey,
        "status": status,
        "isExtinct": bool2str(isExtinct),
        "habitat": habitat,
        "nameType": nameType,
        "datasetKey": datasetKey,
        "nomenclaturalStatus": nomenclaturalStatus,
        "limit": limit,
        "offset": offset,
        "facet": bn(facet),
        "facetMincount": facetMincount,
        "facetMultiselect": bool2str(facetMultiselect),
        "hl": bool2str(hl),
        "verbose": bool2str(verbose),
        "type": type,
    }
    gbif_kwargs = {key: kwargs[key] for key in kwargs if key not in requests_argset}
    if gbif_kwargs is not None:
        xx = dict(
            zip([re.sub("_", ".", x) for x in gbif_kwargs.keys()], gbif_kwargs.values())
        )
        args.update(xx)
    kwargs = {key: kwargs[key] for key in kwargs if key in requests_argset}
    return gbif_GET(gbif_baseurl + "species/search", args, **kwargs)
