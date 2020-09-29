from pygbif.gbifutils import (
    check_data,
    stop,
    gbif_baseurl,
    gbif_GET,
    get_meta,
    parse_results,
    len2,
)


def networks(
    data="all",
    uuid=None,
    q=None,
    identifier=None,
    identifierType=None,
    limit=100,
    offset=None,
    **kwargs
):
    """
  Networks metadata.

  Note: there's only 1 network now, so there's not a lot you can do with this method.

  :param data: [str] The type of data to get. Default: ``all``
  :param uuid: [str] UUID of the data network provider. This must be specified if data
     is anything other than ``all``.
  :param q: [str] Query networks. Only used when ``data = 'all'``. Ignored otherwise.
  :param identifier: [fixnum] The value for this parameter can be a simple string or integer,
      e.g. identifier=120
  :param identifierType: [str] Used in combination with the identifier parameter to filter
      identifiers by identifier type: ``DOI``, ``FTP``, ``GBIF_NODE``, ``GBIF_PARTICIPANT``,
      ``GBIF_PORTAL``, ``HANDLER``, ``LSID``, ``UNKNOWN``, ``URI``, ``URL``, ``UUID``
  :param limit: [int] Number of results to return. Default: ``100``
  :param offset: [int] Record to start at. Default: ``0``

  :return: A dictionary

  References: http://www.gbif.org/developer/registry#networks

  Usage::

      from pygbif import registry
      registry.networks(limit=1)
      registry.networks(uuid='2b7c7b4f-4d4f-40d3-94de-c28b6fa054a6')
  """
    args = {
        "q": q,
        "limit": limit,
        "offset": offset,
        "identifier": identifier,
        "identifierType": identifierType,
    }
    data_choices = [
        "all",
        "contact",
        "endpoint",
        "identifier",
        "tag",
        "machineTag",
        "comment",
        "constituents",
    ]
    check_data(data, data_choices)

    def getdata(x, uuid, args, **kwargs):
        if x != "all" and uuid is None:
            stop('You must specify a uuid if data does not equal "all"')

        if uuid is None:
            url = gbif_baseurl + "network"
        else:
            if x == "all":
                url = gbif_baseurl + "network/" + uuid
            else:
                url = gbif_baseurl + "network/" + uuid + "/" + x

        res = gbif_GET(url, args, **kwargs)
        return {"meta": get_meta(res), "data": parse_results(res, uuid)}

    if len2(data) == 1:
        return getdata(data, uuid, args, **kwargs)
    else:
        return [getdata(x, uuid, args, **kwargs) for x in data]
