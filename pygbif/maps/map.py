import os
import hashlib
import re
import warnings

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from appdirs import user_cache_dir

from pygbif.gbifutils import requests_argset, has, gbif_GET_map

# Sentinel value to detect if user explicitly provided checklistKey
_DEFAULT_CHECKLIST = object()


def map(
    source="density",
    z=0,
    x=0,
    y=0,
    format="@1x.png",
    srs="EPSG:4326",
    bin=None,
    hexPerTile=None,
    style="classic.point",
    taxonKey=None,
    country=None,
    publishingCountry=None,
    publisher=None,
    datasetKey=None,
    year=None,
    basisOfRecord=None,
    checklistKey=_DEFAULT_CHECKLIST,
    **kwargs
):
    """
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
      - ``@2x.png`` - 1024px raster tile
      - ``@3x.png`` - 2048px raster tile
      - ``@4x.png`` - 4096px raster tile

    :param srs: [str] Spatial reference system. One of:

      - ``EPSG:3857`` (Web Mercator)
      - ``EPSG:4326`` (WGS84 plate caree)
      - ``EPSG:3575`` (Arctic LAEA)
      - ``EPSG:3031`` (Antarctic stereographic)

    :param bin: [str] square or hex to aggregate occurrence counts into
        squares or hexagons. Points by default.
    :param hexPerTile: [str] sets the size of the hexagons (the number 
        horizontally across a tile)
    :param squareSize: [str] sets the size of the squares. Choose a factor 
        of 4096 so they tessalate correctly: probably from 8, 16, 32, 64, 
        128, 256, 512.
    :param style: [str] for raster tiles, choose from the available styles.
        Defaults to classic.point.
    :param taxonKey: [int/str] A taxon classification key (numeric for GBIF backbone, alphanumeric for COL)
    :param datasetKey: [str] The occurrence dataset key (a uuid)
    :param country: [str] The 2-letter country code (as per ISO-3166-1) of 
        the country in which the occurrence was recorded. See here
        http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
    :param basisOfRecord: [str] Basis of record, as defined in the BasisOfRecord enum 
        http://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/BasisOfRecord.html
        Acceptable values are

       - ``FOSSIL_SPECIMEN`` An occurrence record describing a fossilized specimen.
       - ``HUMAN_OBSERVATION`` An occurrence record describing an observation made by one or more people.
       - ``LIVING_SPECIMEN`` An occurrence record describing a living specimen.
       - ``MACHINE_OBSERVATION`` An occurrence record describing an observation made by a machine.
       - ``MATERIAL_CITATION`` An occurrence record based on a reference to a scholarly publication.
       - ``OBSERVATION`` An occurrence record describing an observation.
       - ``OCCURRENCE`` An existence of an organism at a particular place and time. No more specific basis.
       - ``PRESERVED_SPECIMEN`` An occurrence record describing a preserved specimen.

    :param year: [int] The 4 digit year. A year of 98 will be interpreted as 
        AD 98. Supports range queries, smaller,larger (e.g., ``1990,1991``, 
        whereas ``1991,1990`` wouldn't work)
    :param publishingCountry: [str] The 2-letter country code (as per 
        ISO-3166-1) of the country in which the occurrence was recorded.
    :param checklistKey: [str] The UUID of the checklist (taxonomy) to use. 
        Defaults to the Catalogue of Life (COL) Extended Release 
        (7ddf754f-d193-4cc9-b351-99906754a03b). Set to ``None`` to use the 
        GBIF backbone taxonomy.
        Note: If you provide a numeric (integer) taxonKey without explicitly setting 
        checklistKey, the function will automatically switch to GBIF backbone taxonomy 
        and issue a deprecation warning. Use pygbif.species.gbif_to_col() to migrate 
        your keys to COL alphanumeric format.

    :return: An object of class GbifMap

    For mvt format, see https://github.com/tilezen/mapbox-vector-tile to 
    decode, and example below

    Usage::

        from pygbif import maps
        out = maps.map(taxonKey = 2435098)
        out.response
        out.path
        out.img
        out.plot()

        out = maps.map(taxonKey = 2480498, year = range(2008, 2011+1))
        out.response
        out.path
        out.img
        out.plot()
        
        # srs
        maps.map(taxonKey = 2480498, year = 2010, srs = "EPSG:3857")
        # bin
        maps.map(taxonKey = 212, year = 1998, bin = "hex",
           hexPerTile = 30, style = "classic-noborder.poly")
        # style
        maps.map(taxonKey = 2480498, style = "purpleYellow.point").plot()
        # basisOfRecord
        maps.map(taxonKey = 2480498, year = 2010,
          basisOfRecord = "HUMAN_OBSERVATION", bin = "hex", 
          hexPerTile = 500).plot()
        maps.map(taxonKey = 2480498, year = 2010, 
          basisOfRecord = ["HUMAN_OBSERVATION", "LIVING_SPECIMEN"],
          hexPerTile = 500, bin = "hex").plot()

        # map vector tiles, gives back raw bytes
        from pygbif import maps
        x = maps.map(taxonKey = 2480498, year = 2010,
          format = ".mvt")
        x.response
        x.path
        x.img # None
        import mapbox_vector_tile
        mapbox_vector_tile.decode(x.response.content)
    """
    if format not in [".mvt", "@Hx.png", "@1x.png", "@2x.png", "@3x.png", "@4x.png"]:
        raise ValueError("'format' not in allowed set, see docs")
    if source not in ["density", "adhoc"]:
        raise ValueError("'source' not in allowed set, see docs")
    if srs not in ["EPSG:3857", "EPSG:4326", "EPSG:3575", "EPSG:3031"]:
        raise ValueError("'srs' not in allowed set, see docs")
    if bin is not None:
        if bin not in ["square", "hex"]:
            raise ValueError("'bin' not in allowed set, see docs")
    if style is not None:
        if style not in map_styles:
            raise ValueError("'style' not in allowed set, see docs")

    # Handle checklistKey default and detect if user explicitly provided it
    if checklistKey is _DEFAULT_CHECKLIST:
        user_provided_checklistkey = False
        checklistKey = "7ddf754f-d193-4cc9-b351-99906754a03b"  # Default to COL
    else:
        user_provided_checklistkey = True

    # Check if taxonKey is numeric (integer)
    # If so and user didn't explicitly provide checklistKey, switch to GBIF Backbone
    if taxonKey is not None and isinstance(taxonKey, int) and not user_provided_checklistkey:
        # Automatically switch to GBIF Backbone for numeric keys
        checklistKey = None
        warnings.warn(
            "Numeric taxonKey detected. Automatically switching to GBIF Backbone taxonomy. "
            "GBIF Backbone taxonomy is outdated. Please migrate to COL Extended Release with alphanumeric keys. "
            "Use pygbif.species.gbif_to_col() to convert your numeric GBIF keys to COL alphanumeric keys.",
            DeprecationWarning,
            stacklevel=2
        )

    maps_baseurl = "https://api.gbif.org"
    url = maps_baseurl + "/v2/map/occurrence/%s/%s/%s/%s%s"
    url = url % (source, z, x, y, format)
    year = __handle_year(year)
    basisOfRecord = __handle_bor(basisOfRecord)
    args = {
        "srs": srs,
        "bin": bin,
        "hexPerTile": hexPerTile,
        "style": style,
        "taxonKey": taxonKey,
        "country": country,
        "publishingCountry": publishingCountry,
        "publisher": publisher,
        "datasetKey": datasetKey,
        "year": year,
        "basisOfRecord": basisOfRecord,
        "checklistKey": checklistKey,
    }
    kw = {key: kwargs[key] for key in kwargs if key not in requests_argset}
    if kw is not None:
        xx = dict(zip([re.sub("_", ".", x) for x in kw.keys()], kw.values()))
        args.update(xx)
    kwargs = {key: kwargs[key] for key in kwargs if key in requests_argset}
    ctype = "image/png" if has(format, "png") else "application/x-protobuf"
    out = gbif_GET_map(url, args, ctype, **kwargs)
    # return out
    return GbifMap(out)


class GbifMap(object):
    """
    GbifMap response class

    contains:
    
    - response: the response from the requests library
    - path: the path to the image
    - img: the image data, of class matplotlib AxesImage
    - plot(): a method to plot the image with matplotlib
    """

    def __init__(self, x):
        super(GbifMap, self).__init__()
        self.response = x
        self.path = self.__make_path()
        self.__write_file()
        if has(self.response.headers["Content-Type"], "png"):
            self.img = self.__prep_plot()
        else:
            self.img = None

    def __write_file(self):
        fh = open(self.path, "wb")
        fh.write(self.response.content)
        fh.close()

    def __prep_plot(self):
        img = mpimg.imread(self.path)
        return plt.imshow(img)

    def __make_path(self):
        uu = hashlib.sha256(self.response.content).hexdigest()
        base_path = user_cache_dir("python/pygbif")
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        file_ext = (
            ".png" if has(self.response.headers["Content-Type"], "png") else ".mvt"
        )
        path = base_path + "/" + uu + file_ext
        return path

    def plot(self):
        plt.show()


def __handle_year(year):
    if year is not None:
        if isinstance(year, int):
            year = [year]
        if isinstance(year, range):
            year = list(year)
        bools = [w in range(0, 2200) for w in year]
        if not all(bools):
            raise ValueError("one or more 'year' values not in acceptable set")
        if len(year) > 1:
            year = ",".join([str(min(year)), str(max(year))])
        else:
            year = str(year[0])
        return year


def __handle_bor(basisOfRecord):
    if basisOfRecord is not None:
        if isinstance(basisOfRecord, str):
            basisOfRecord = [basisOfRecord]
        bools = [w in basis_of_record_values for w in basisOfRecord]
        if not all(bools):
            raise ValueError("one or more 'basisOfRecord' values not in acceptable set")
        return basisOfRecord


map_styles = [
    "purpleHeat.point",
    "blueHeat.point",
    "orangeHeat.point",
    "greenHeat.point",
    "classic.point",
    "purpleYellow.point",
    "fire.point",
    "glacier.point",
    "classic.poly",
    "classic-noborder.poly",
    "purpleYellow.poly",
    "purpleYellow-noborder.poly",
    "green.poly",
    "green2.poly",
    "iNaturalist.poly",
    "purpleWhite.poly",
    "red.poly",
    "blue.marker",
    "orange.marker",
    "outline.poly",
]

basis_of_record_values = [
    "OBSERVATION",
    "HUMAN_OBSERVATION",
    "MACHINE_OBSERVATION",
    "MATERIAL_SAMPLE",
    "PRESERVED_SPECIMEN",
    "FOSSIL_SPECIMEN",
    "LIVING_SPECIMEN",
    "LITERATURE",
    "UNKNOWN",
]
