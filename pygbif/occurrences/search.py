from ..gbifutils import *

def search(taxonKey, limit=5, offset=1, **kwargs):
    '''
    Search GBIF occurrences

    :param taxonKey: [Fixnum] A GBIF occurrence identifier
    :param limit: [Fixnum] Number of results to return.
    :param offset: [Fixnum] Start at record X

    :return: Object response class, light wrapper around a dict

    Usage
    >>> from pygbif import occurrences
    >>> occurrences.search(taxonKey = 3329049)
    '''
    url = gbif_baseurl + 'occurrence/search'
    out = gbif_GET(url, {'taxonKey': taxonKey, 'limit': limit, 'offset': offset}, **kwargs)
    return out
