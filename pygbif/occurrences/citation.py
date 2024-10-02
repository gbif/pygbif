from pygbif.gbifutils import gbif_baseurl, gbif_GET_raw
import re

def citation(key):
    """
    Get citation from a download key

    :param key: [int] A GBIF download key

    :return: A dictionary, of results

    Usage::

        from pygbif import occurrences
        occurrences.citation("0235283-220831081235567")

    """
    url = gbif_baseurl + "occurrence/download/" + str(key) + "/citation"
    if re.fullmatch(r'^\d+-\d+$', key):
        out = gbif_GET_raw(url).decode('utf-8')
        return(out)
    else:
        raise ValueError("key must be a GBIF download key")

