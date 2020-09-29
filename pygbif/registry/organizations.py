from pygbif.gbifutils import (
    check_data,
    stop,
    gbif_baseurl,
    gbif_GET,
    get_meta,
    parse_results,
    len2,
)


def organizations(
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
  Organizations metadata.

  :param data: [str] The type of data to get. Default is all data. If not ``all``, then one
     or more of ``contact``, ``endpoint``, ``identifier``, ``tag``, ``machineTag``,
     ``comment``, ``hostedDataset``, ``ownedDataset``, ``deleted``, ``pending``,
     ``nonPublishing``.
  :param uuid: [str] UUID of the data node provider. This must be specified if data
     is anything other than ``all``.
  :param q: [str] Query nodes. Only used when ``data='all'``. Ignored otherwise.
  :param identifier: [fixnum] The value for this parameter can be a simple string or integer,
      e.g. identifier=120
  :param identifierType: [str] Used in combination with the identifier parameter to filter
      identifiers by identifier type: ``DOI``, ``FTP``, ``GBIF_NODE``, ``GBIF_PARTICIPANT``,
      ``GBIF_PORTAL``, ``HANDLER``, ``LSID``, ``UNKNOWN``, ``URI``, ``URL``, ``UUID``
  :param limit: [int] Number of results to return. Default: ``100``
  :param offset: [int] Record to start at. Default: ``0``

  :return: A dictionary

  References: http://www.gbif.org/developer/registry#organizations

  Usage::

      from pygbif import registry
      registry.organizations(limit=5)
      registry.organizations(q="france")
      registry.organizations(identifier=120)
      registry.organizations(uuid="e2e717bf-551a-4917-bdc9-4fa0f342c530")
      registry.organizations(data='contact', uuid="e2e717bf-551a-4917-bdc9-4fa0f342c530")
      registry.organizations(data='deleted')
      registry.organizations(data='deleted', limit=2)
      registry.organizations(data=['deleted','nonPublishing'], limit=2)
      registry.organizations(identifierType='DOI', limit=2)
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
        "hostedDataset",
        "ownedDataset",
        "deleted",
        "pending",
        "nonPublishing",
    ]
    check_data(data, data_choices)

    def getdata(x, uuid, args, **kwargs):
        nouuid = ["all", "deleted", "pending", "nonPublishing"]
        if x not in nouuid and uuid is None:
            stop(
                'You must specify a uuid if data does not equal "all" and data does not equal one of '
                + ", ".join(nouuid)
            )

        if uuid is None:
            if x == "all":
                url = gbif_baseurl + "organization"
            else:
                url = gbif_baseurl + "organization/" + x
        else:
            if x == "all":
                url = gbif_baseurl + "organization/" + uuid
            else:
                url = gbif_baseurl + "organization/" + uuid + "/" + x

        res = gbif_GET(url, args, **kwargs)
        return {"meta": get_meta(res), "data": parse_results(res, uuid)}

    if len2(data) == 1:
        return getdata(data, uuid, args, **kwargs)
    else:
        return [getdata(x, uuid, args, **kwargs) for x in data]
