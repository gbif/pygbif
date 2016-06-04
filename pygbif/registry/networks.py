from ..gbifutils import *
from .registry_utils import *

def networks(data = 'all', uuid = None, query = None, identifier = None,
  identifierType = None, limit = 100, start = None, **kwargs):
  '''
  Networks metadata.

  :param data: [str] The type of data to get. Default: 'all'
  :param uuid: [str] UUID of the data network provider. This must be specified if data
     is anything other than 'all'.
  :param query: [str] Query networks. Only used when `data = 'all'`. Ignored otherwise.

  References: http://www.gbif.org/developer/registry#networks

  :return: A dict

  Usage::

      from pygbif import registry
      registry.networks(limit=5)
      registry.networks(uuid='16ab5405-6c94-4189-ac71-16ca3b753df7')
      registry.networks(data='endpoint', uuid='16ab5405-6c94-4189-ac71-16ca3b753df7')
  '''
  args = {'q': query, 'limit': limit, 'offset': start}
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

