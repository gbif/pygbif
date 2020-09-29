from pygbif.gbifutils import (
    check_data,
    stop,
    gbif_baseurl,
    gbif_GET,
    get_meta,
    parse_results,
    len2,
)


def nodes(
    data="all",
    uuid=None,
    q=None,
    identifier=None,
    identifierType=None,
    limit=100,
    offset=None,
    isocode=None,
    **kwargs
):
    """
  Nodes metadata.

  :param data: [str] The type of data to get. Default: ``all``
  :param uuid: [str] UUID of the data node provider. This must be specified if data
     is anything other than ``all``.
  :param q: [str] Query nodes. Only used when ``data = 'all'``
  :param identifier: [fixnum] The value for this parameter can be a simple string or integer,
      e.g. identifier=120
  :param identifierType: [str] Used in combination with the identifier parameter to filter
      identifiers by identifier type: ``DOI``, ``FTP``, ``GBIF_NODE``, ``GBIF_PARTICIPANT``,
      ``GBIF_PORTAL``, ``HANDLER``, ``LSID``, ``UNKNOWN``, ``URI``, ``URL``, ``UUID``
  :param limit: [int] Number of results to return. Default: ``100``
  :param offset: [int] Record to start at. Default: ``0``
  :param isocode: [str] A 2 letter country code. Only used if ``data = 'country'``.

  :return: A dictionary

  References http://www.gbif.org/developer/registry#nodes

  Usage::

      from pygbif import registry
      registry.nodes(limit=5)
      registry.nodes(identifier=120)
      registry.nodes(uuid="1193638d-32d1-43f0-a855-8727c94299d8")
      registry.nodes(data='identifier', uuid="03e816b3-8f58-49ae-bc12-4e18b358d6d9")
      registry.nodes(data=['identifier','organization','comment'], uuid="03e816b3-8f58-49ae-bc12-4e18b358d6d9")

      uuids = ["8cb55387-7802-40e8-86d6-d357a583c596","02c40d2a-1cba-4633-90b7-e36e5e97aba8",
      "7a17efec-0a6a-424c-b743-f715852c3c1f","b797ce0f-47e6-4231-b048-6b62ca3b0f55",
      "1193638d-32d1-43f0-a855-8727c94299d8","d3499f89-5bc0-4454-8cdb-60bead228a6d",
      "cdc9736d-5ff7-4ece-9959-3c744360cdb3","a8b16421-d80b-4ef3-8f22-098b01a89255",
      "8df8d012-8e64-4c8a-886e-521a3bdfa623","b35cf8f1-748d-467a-adca-4f9170f20a4e",
      "03e816b3-8f58-49ae-bc12-4e18b358d6d9","073d1223-70b1-4433-bb21-dd70afe3053b",
      "07dfe2f9-5116-4922-9a8a-3e0912276a72","086f5148-c0a8-469b-84cc-cce5342f9242",
      "0909d601-bda2-42df-9e63-a6d51847ebce","0e0181bf-9c78-4676-bdc3-54765e661bb8",
      "109aea14-c252-4a85-96e2-f5f4d5d088f4","169eb292-376b-4cc6-8e31-9c2c432de0ad",
      "1e789bc9-79fc-4e60-a49e-89dfc45a7188","1f94b3ca-9345-4d65-afe2-4bace93aa0fe"]

      [ registry.nodes(data='identifier', uuid=x) for x in uuids ]
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
        "organization",
        "endpoint",
        "identifier",
        "tag",
        "machineTag",
        "comment",
        "pendingEndorsement",
        "country",
        "dataset",
        "installation",
    ]
    check_data(data, data_choices)

    def getdata(x, uuid, args, **kwargs):
        if x != "all" and uuid is None:
            stop('You must specify a uuid if data does not equal "all"')

        if uuid is None:
            if x == "all":
                url = gbif_baseurl + "node"
            else:
                if isocode is not None and x == "country":
                    url = gbif_baseurl + "node/country/" + isocode
                else:
                    url = gbif_baseurl + "node/" + x
        else:
            if x == "all":
                url = gbif_baseurl + "node/" + uuid
            else:
                url = gbif_baseurl + "node/" + uuid + "/" + x

        res = gbif_GET(url, args, **kwargs)
        return {"meta": get_meta(res), "data": parse_results(res, uuid)}

    # Get data
    if len2(data) == 1:
        return getdata(data, uuid, args, **kwargs)
    else:
        return [getdata(x, uuid, args, **kwargs) for x in data]
