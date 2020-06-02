from pygbif.gbifutils import gbif_baseurl, gbif_GET


def get(key, **kwargs):
    """
    Gets details for a single, interpreted occurrence

    :param key: [int] A GBIF occurrence key

    :return: A dictionary, of results

    Usage::

        from pygbif import occurrences
        occurrences.get(key = 1258202889)
        occurrences.get(key = 1227768771)
        occurrences.get(key = 1227769518)
    """
    url = gbif_baseurl + "occurrence/" + str(key)
    out = gbif_GET(url, {}, **kwargs)
    return out


def get_verbatim(key, **kwargs):
    """
    Gets a verbatim occurrence record without any interpretation

    :param key: [int] A GBIF occurrence key

    :return: A dictionary, of results

    Usage::

        from pygbif import occurrences
        occurrences.get_verbatim(key = 1258202889)
        occurrences.get_verbatim(key = 1227768771)
        occurrences.get_verbatim(key = 1227769518)
    """
    url = gbif_baseurl + "occurrence/" + str(key) + "/verbatim"
    out = gbif_GET(url, {}, **kwargs)
    return out


def get_fragment(key, **kwargs):
    """
    Get a single occurrence fragment in its raw form (xml or json)

    :param key: [int] A GBIF occurrence key

    :return: A dictionary, of results

    Usage::

        from pygbif import occurrences
        occurrences.get_fragment(key = 1052909293)
        occurrences.get_fragment(key = 1227768771)
        occurrences.get_fragment(key = 1227769518)
    """
    url = gbif_baseurl + "occurrence/" + str(key) + "/fragment"
    out = gbif_GET(url, {}, **kwargs)
    return out
