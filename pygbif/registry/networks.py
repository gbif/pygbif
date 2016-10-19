from ..gbifutils import *

def networks(data = 'all', uuid = None, q = None, identifier = None,
  identifierType = None, limit = 100, offset = None, **kwargs):
  '''
  Networks metadata.

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
      registry.networks(limit=5)
      registry.networks(uuid='16ab5405-6c94-4189-ac71-16ca3b753df7')
      registry.networks(data='endpoint', uuid='16ab5405-6c94-4189-ac71-16ca3b753df7')
  '''
  args = {'q': q, 'limit': limit, 'offset': offset, 'identifier': identifier,
    'identifierType': identifierType}
  data_choices = ['all', 'contact', 'endpoint', 'identifier',
    'tag', 'machineTag', 'comment', 'constituents']
  check_data(data, data_choices)

  def getdata(x, uuid, args, **kwargs):
    if x is not 'all' and uuid is None:
      stop('You must specify a uuid if data does not equal "all"')

    if uuid is None:
      url = gbif_baseurl + 'network'
    else:
      if x is 'all':
        url = gbif_baseurl + 'network/' + uuid
      else:
        url = gbif_baseurl + 'network/' + uuid + '/' + x

    res = gbif_GET(url, args, **kwargs)
    return {'meta': get_meta(res), 'data': parse_results(res, uuid)}

  if len2(data) == 1:
    return getdata(data, uuid, args, **kwargs)
  else:
    return [getdata(x, uuid, args, **kwargs) for x in data]

