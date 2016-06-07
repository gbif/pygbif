from ..gbifutils import *
from .registry_utils import *

def installations(data = 'all', uuid = None, query = None, identifier = None,
  identifierType = None, limit = 100, start = None, **kwargs):
  '''
  Installations metadata.

  :param data: [str] The type of data to get. Default is all data. If not ``all``, then one
     or more of ``contact``, ``endpoint``, ``dataset``, ``comment``, ``deleted``, ``nonPublishing``.
  :param uuid: [str] UUID of the data node provider. This must be specified if data
     is anything other than ``all``.
  :param query: [str] Query nodes. Only used when ``data='all'``. Ignored otherwise.

  References: http://www.gbif.org/developer/registry#installations

  Usage::

      from pygbif import registry
      registry.installations(limit=5)
      registry.installations(query="france")
      registry.installations(uuid="b77901f9-d9b0-47fa-94e0-dd96450aa2b4")
      registry.installations(data='contact', uuid="b77901f9-d9b0-47fa-94e0-dd96450aa2b4")
      registry.installations(data='contact', uuid="2e029a0c-87af-42e6-87d7-f38a50b78201")
      registry.installations(data='endpoint', uuid="b77901f9-d9b0-47fa-94e0-dd96450aa2b4")
      registry.installations(data='dataset', uuid="b77901f9-d9b0-47fa-94e0-dd96450aa2b4")
      registry.installations(data='deleted')
      registry.installations(data='deleted', limit=2)
      registry.installations(data=['deleted','nonPublishing'], limit=2)
      registry.installations(identifierType='DOI', limit=2)
  '''
  args = {'q': query, 'limit': limit, 'offset': start}
  data_choices = ['all', 'contact', 'endpoint', 'dataset',
   'identifier', 'tag', 'machineTag', 'comment',
   'deleted', 'nonPublishing']
  check_data(data, data_choices)

  def getdata(x, uuid, args, **kwargs):
    if x not in ['all','deleted', 'nonPublishing'] and uuid is None:
      stop('You must specify a uuid if data does not equal all and data does not equal one of deleted or nonPublishing')

    if uuid is None:
      if x is 'all':
        url = gbif_baseurl + 'installation'
      else:
        url = gbif_baseurl + 'installation/' + x
    else:
      if x is 'all':
        url = gbif_baseurl + 'installation/' + uuid
      else:
        url = gbif_baseurl + 'installation/' + uuid + '/' + x

    res = gbif_GET(url, args, **kwargs)
    return {'meta': get_meta(res), 'data': parse_results(res, uuid)}

  if len2(data) == 1:
    return getdata(data, uuid, args, **kwargs)
  else:
    return [getdata(x, uuid, args, **kwargs) for x in data]
