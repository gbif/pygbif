from ..gbifutils import *
from .registry_utils import *

def organizations(data = 'all', uuid = None, query = None, identifier = None,
  identifierType = None, limit = 100, start = None, **kwargs):
  '''
  organizations metadata.

  :param data: [str] The type of data to get. Default is all data. If not ``all``, then one
     or more of ``contact``, ``endpoint``, ``identifier``, ``tag``, ``machineTag``,
     ``comment``, ``hostedDataset``, ``ownedDataset``, ``deleted``, ``pending``,
     ``nonPublishing``.
  :param uuid: [str] UUID of the data node provider. This must be specified if data
     is anything other than ``all``.
  :param query: [str] Query nodes. Only used when ``data='all'``. Ignored otherwise.

  References: http://www.gbif.org/developer/registry#organizations

  Usage::

      from pygbif import registry
      registry.organizations(limit=5)
      registry.organizations(query="france")
      registry.organizations(uuid="e2e717bf-551a-4917-bdc9-4fa0f342c530")
      registry.organizations(data='contact', uuid="e2e717bf-551a-4917-bdc9-4fa0f342c530")
      registry.organizations(data='endpoint', uuid="e2e717bf-551a-4917-bdc9-4fa0f342c530")
      registry.organizations(data='deleted')
      registry.organizations(data='deleted', limit=2)
      registry.organizations(data=['deleted','nonPublishing'], limit=2)
      registry.organizations(identifierType='DOI', limit=2)
  '''
  args = {'q': query, 'limit': limit, 'offset': start}
  data_choices = ['all', 'contact', 'endpoint',
    'identifier', 'tag', 'machineTag', 'comment', 'hostedDataset',
    'ownedDataset', 'deleted', 'pending', 'nonPublishing']
  check_data(data, data_choices)

  def getdata(x, uuid, args, **kwargs):
    nouuid = ['all', 'deleted', 'pending', 'nonPublishing']
    if x not in nouuid and uuid is None:
      stop('You must specify a uuid if data does not equal "all" and data does not equal one of ' + ', '.join(nouuid))

    if uuid is None:
      if x is 'all':
        url = gbif_baseurl + 'organization'
      else:
        url = gbif_baseurl + 'organization/' + x
    else:
      if x is 'all':
        url = gbif_baseurl + 'organization/' + uuid
      else:
        url = gbif_baseurl + 'organization/' + uuid + '/' + x

    res = gbif_GET(url, args, **kwargs)
    return {'meta': get_meta(res), 'data': parse_results(res, uuid)}

  if len2(data) == 1:
    return getdata(data, uuid, args, **kwargs)
  else:
    return [getdata(x, uuid, args, **kwargs) for x in data]
