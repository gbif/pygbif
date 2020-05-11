import re


def occ_issues_lookup(issue=None, code=None):
    """
    Lookup occurrence issue definitions and short codes

    :param issue: Full name of issue, e.g, CONTINENT_COUNTRY_MISMATCH
    :param code: an issue short code, e.g. ccm

    Usage
    pygbif.occ_issues_lookup(issue = 'CONTINENT_COUNTRY_MISMATCH')
    pygbif.occ_issues_lookup(issue = 'MULTIMEDIA_DATE_INVALID')
    pygbif.occ_issues_lookup(issue = 'ZERO_COORDINATE')
    pygbif.occ_issues_lookup(code = 'cdiv')
    """
    if code is None:
        bb = [trymatch(issue, x) for x in gbifissues["issue"]]
        tmp = filter(None, bb)
    else:
        bb = [trymatch(code, x) for x in gbifissues["code"]]
        tmp = filter(None, bb)
    return tmp


def trymatch(pattern, string):
    temp = re.match(pattern, string)
    if temp is None:
        return None
    else:
        return temp.string


gbifissues = {
    "code": [
        "bri",
        "ccm",
        "cdc",
        "conti",
        "cdiv",
        "cdout",
        "cdrep",
        "cdrepf",
        "cdreps",
        "cdround",
        "cucdmis",
        "cudc",
        "cuiv",
        "cum",
        "depmms",
        "depnn",
        "depnmet",
        "depunl",
        "elmms",
        "elnn",
        "elnmet",
        "elunl",
        "gass84",
        "gdativ",
        "iddativ",
        "iddatunl",
        "mdativ",
        "mdatunl",
        "muldativ",
        "muluriiv",
        "preneglat",
        "preneglon",
        "preswcd",
        "rdativ",
        "rdatm",
        "rdatunl",
        "refuriiv",
        "txmatfuz",
        "txmathi",
        "txmatnon",
        "typstativ",
        "zerocd",
    ],
    "issue": [
        "BASIS_OF_RECORD_INVALID",
        "CONTINENT_COUNTRY_MISMATCH",
        "CONTINENT_DERIVED_FROM_COORDINATES",
        "CONTINENT_INVALID",
        "COORDINATE_INVALID",
        "COORDINATE_OUT_OF_RANGE",
        "COORDINATE_REPROJECTED",
        "COORDINATE_REPROJECTION_FAILED",
        "COORDINATE_REPROJECTION_SUSPICIOUS",
        "COORDINATE_ROUNDED",
        "COUNTRY_COORDINATE_MISMATCH",
        "COUNTRY_DERIVED_FROM_COORDINATES",
        "COUNTRY_INVALID",
        "COUNTRY_MISMATCH",
        "DEPTH_MIN_MAX_SWAPPED",
        "DEPTH_NON_NUMERIC",
        "DEPTH_NOT_METRIC",
        "DEPTH_UNLIKELY",
        "ELEVATION_MIN_MAX_SWAPPED",
        "ELEVATION_NON_NUMERIC",
        "ELEVATION_NOT_METRIC",
        "ELEVATION_UNLIKELY",
        "GEODETIC_DATUM_ASSUMED_WGS84",
        "GEODETIC_DATUM_INVALID",
        "IDENTIFIED_DATE_INVALID",
        "IDENTIFIED_DATE_UNLIKELY",
        "MODIFIED_DATE_INVALID",
        "MODIFIED_DATE_UNLIKELY",
        "MULTIMEDIA_DATE_INVALID",
        "MULTIMEDIA_URI_INVALID",
        "PRESUMED_NEGATED_LATITUDE",
        "PRESUMED_NEGATED_LONGITUDE",
        "PRESUMED_SWAPPED_COORDINATE",
        "RECORDED_DATE_INVALID",
        "RECORDED_DATE_MISMATCH",
        "RECORDED_DATE_UNLIKELY",
        "REFERENCES_URI_INVALID",
        "TAXON_MATCH_FUZZY",
        "TAXON_MATCH_HIGHERRANK",
        "TAXON_MATCH_NONE",
        "TYPE_STATUS_INVALID",
        "ZERO_COORDINATE",
    ],
    "description": [
        "The given basis of record is impossible to interpret or seriously different from the recommended vocabulary.",
        "The interpreted continent and country do not match up.",
        "The interpreted continent is based on the coordinates, not the verbatim string information.",
        "Uninterpretable continent values found.",
        "Coordinate value given in some form but GBIF is unable to interpret it.",
        "Coordinate has invalid lat/lon values out of their decimal max range.",
        "The original coordinate was successfully reprojected from a different geodetic datum to WGS84.",
        "The given decimal latitude and longitude could not be reprojected to WGS84 based on the provided datum.",
        "Indicates successful coordinate reprojection according to provided datum, but which results in a datum shift larger than 0.1 decimal degrees.",
        "Original coordinate modified by rounding to 5 decimals.",
        "The interpreted occurrence coordinates fall outside of the indicated country.",
        "The interpreted country is based on the coordinates, not the verbatim string information.",
        "Uninterpretable country values found.",
        "Interpreted country for dwc:country and dwc:countryCode contradict each other.",
        "Set if supplied min>max",
        "Set if depth is a non numeric value",
        "Set if supplied depth is not given in the metric system, for example using feet instead of meters",
        "Set if depth is larger than 11.000m or negative.",
        "Set if supplied min > max elevation",
        "Set if elevation is a non numeric value",
        "Set if supplied elevation is not given in the metric system, for example using feet instead of meters",
        "Set if elevation is above the troposphere (17km) or below 11km (Mariana Trench).",
        "Indicating that the interpreted coordinates assume they are based on WGS84 datum as the datum was either not indicated or interpretable.",
        "The geodetic datum given could not be interpreted.",
        "The date given for dwc:dateIdentified is invalid and cant be interpreted at all.",
        "The date given for dwc:dateIdentified is in the future or before Linnean times (1700).",
        "A (partial) invalid date is given for dc:modified, such as a non existing date, invalid zero month, etc.",
        "The date given for dc:modified is in the future or predates unix time (1970).",
        "An invalid date is given for dc:created of a multimedia object.",
        "An invalid uri is given for a multimedia object.",
        "Latitude appears to be negated, e.g. 32.3 instead of -32.3",
        "Longitude appears to be negated, e.g. 32.3 instead of -32.3",
        "Latitude and longitude appear to be swapped.",
        "A (partial) invalid date is given, such as a non existing date, invalid zero month, etc.",
        "The recording date specified as the eventDate string and the individual year, month, day are contradicting.",
        "The recording date is highly unlikely, falling either into the future or represents a very old date before 1600 that predates modern taxonomy.",
        "An invalid uri is given for dc:references.",
        "Matching to the taxonomic backbone can only be done using a fuzzy, non exact match.",
        "Matching to the taxonomic backbone can only be done on a higher rank and not the scientific name.",
        "Matching to the taxonomic backbone cannot be done cause there was no match at all or several matches with too little information to keep them apart (homonyms).",
        "The given type status is impossible to interpret or seriously different from the recommended vocabulary.",
        "Coordinate is the exact 0/0 coordinate, often indicating a bad null coordinate.",
    ],
}
