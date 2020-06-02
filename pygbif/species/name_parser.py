from pygbif.gbifutils import gbif_baseurl, gbif_POST


def name_parser(name, **kwargs):
    """
  Parse taxon names using the GBIF name parser

  :param name: [str] A character vector of scientific names. (required)

  reference: http://www.gbif.org/developer/species#parser

  Usage::

      from pygbif import species
      species.name_parser('x Agropogon littoralis')
      species.name_parser(['Arrhenatherum elatius var. elatius',
        'Secale cereale subsp. cereale', 'Secale cereale ssp. cereale',
        'Vanessa atalanta (Linnaeus, 1758)'])
  """
    url = gbif_baseurl + "parser/name"
    if name.__class__ == str:
        name = [name]
    return gbif_POST(url, name, **kwargs)
