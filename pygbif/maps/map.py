from ..gbifutils import *

def map(source, z, x, y, format, srs=None, bin=None, hexPerTile=None,
    style=None, taxonKey=None, country=None,
    publishingCountry=None, publisher=None,
    datasetKey=None, year=None, basisOfRecord=None, **kwargs):
    '''
    GBIF maps API

    :param source: [str] Either ``density`` for fast, precalculated tiles,
        or ``adhoc`` for any search
    :param z: [str] zoom level
    :param x: [str] longitude
    :param y: [str] latitude
    :param format: [str] format of returned data. One of:

    - ``.mvt`` - vector tile
    - ``@Hx.png`` - 256px raster tile (for legacy clients)
    - ``@1x.png`` - 512px raster tile, @2x.png for a 1024px raster tile
    - ``@3x.png`` - 2048px raster tile, @4x.png for a 4096px raster tile

    :param srs: [str] Spatial reference system. One of:

    - ``EPSG:3857`` (Web Mercator)
    - ``EPSG:4326`` (WGS84 plate careé)
    - ``EPSG:3575`` (Arctic LAEA)
    - ``EPSG:3031`` (Antarctic stereographic)

    :param bin: [str] square or hex to aggregate occurrence counts into
        squares or hexagons. Points by default.
    :param hexPerTile: [str] sets the size of the hexagons (the number horizontally
        across a tile)
    :param squareSize: [str] sets the size of the squares. Choose a factor of 4096
        so they tessalate correctly: probably from 8, 16, 32, 64, 128, 256, 512.
    :param style: [str] for raster tiles, choose from the available styles.
        Defaults to classic.point.
    :param taxonKey: [int] A GBIF occurrence identifier
    :param datasetKey: [str] The occurrence dataset key (a uuid)
    :param country: [str] The 2-letter country code (as per ISO-3166-1) of the country
        in which the occurrence was recorded. See here
        http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
    :param basisOfRecord: [str] Basis of record, as defined in our BasisOfRecord
        enum here http://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/BasisOfRecord.html
        Acceptable values are:

     - ``FOSSIL_SPECIMEN`` An occurrence record describing a fossilized specimen.
     - ``HUMAN_OBSERVATION`` An occurrence record describing an observation made by
     one or more people.
     - ``LITERATURE`` An occurrence record based on literature alone.
     - ``LIVING_SPECIMEN`` An occurrence record describing a living specimen, e.g.
     - ``MACHINE_OBSERVATION`` An occurrence record describing an observation made
     by a machine.
     - ``OBSERVATION`` An occurrence record describing an observation.
     - ``PRESERVED_SPECIMEN`` An occurrence record describing a preserved specimen.
     - ``UNKNOWN`` Unknown basis for the record.

    :param year: [int] The 4 digit year. A year of 98 will be interpreted as AD 98.
        Supports range queries, smaller,larger (e.g., ``1990,1991``, whereas
        ``1991,1990`` wouldn't work)
    :param publishingCountry: [str] The 2-letter country code (as per ISO-3166-1) of the
       country in which the occurrence was recorded.

    :return: A dictionary

    Usage::

        from pygbif import maps
        maps.map(taxonKey = 2435098)
    '''
    url = maps_baseurl + 'maps/occurrence/%s/%s/%s/%s.%s'
    url = url % ( source, z, x, y, format )
    args = {'srs': srs, 'bin': bin, 'hexPerTile': hexPerTile, 'style': style,
        'taxonKey': taxonKey, 'country': country,
        'publishingCountry': publishingCountry, 'publisher': publisher,
        'datasetKey': datasetKey, 'year': year,
        'basisOfRecord': basisOfRecord}
    gbif_kwargs = {key: kwargs[key] for key in kwargs if key not in requests_argset}
    if gbif_kwargs is not None:
        xx = dict(zip( [ re.sub('_', '.', x) for x in gbif_kwargs.keys() ], gbif_kwargs.values() ))
        args.update(xx)
    kwargs = {key: kwargs[key] for key in kwargs if key in requests_argset}
    out = gbif_GET(url, args, **kwargs)
    return out
