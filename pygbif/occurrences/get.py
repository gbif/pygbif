from ..gbifutils import *

def get(taxonKey, **kwargs):
    '''
    Gets details for a single, interpreted occurrence

    :param key: [Fixnum] A GBIF occurrence key
    :return: Object response class, light wrapper around a dict

    Usage
    >>> from pygbif import occurrences
    >>> occurrences.get(taxonKey = 252408386)
    '''
    url = gbif_baseurl + 'occurrence/' + str(taxonKey)
    out = gbif_GET(url, {}, **kwargs)
    return out

def get_verbatim(taxonKey, **kwargs):
    '''
    Gets a verbatim occurrence record without any interpretation

    :param key: [Fixnum] A GBIF occurrence key
    :return: Object response class, light wrapper around a dict

    Usage
    >>> from pygbif import occurrences
    >>> occurrences.get_verbatim(taxonKey = 252408386)
    '''
    url = gbif_baseurl + 'occurrence/' + str(taxonKey) + '/verbatim'
    out = gbif_GET(url, {}, **kwargs)
    return out

def get_fragment(taxonKey, **kwargs):
    '''
    Get a single occurrence fragment in its raw form (xml or json)

    :param key: [Fixnum] A GBIF occurrence key
    :return: Object response class, light wrapper around a dict

    Usage
    >>> from pygbif import occurrences
    >>> occurrences.get_fragment(taxonKey = 1052909293)
    '''
    url = gbif_baseurl + 'occurrence/' + str(taxonKey) + '/fragment'
    out = gbif_GET(url, {}, **kwargs)
    return out
