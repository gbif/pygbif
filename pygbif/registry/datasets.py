from ..gbifutils import *
from .registry_utils import *

def dataset_metrics(uuid, **kwargs):
	'''
	Get details on a GBIF dataset.

	:param uuid: [str] One or more dataset UUIDs. See examples.

	References: http://www.gbif.org/developer/registry#datasetMetrics

	Usage::

			from pygbif import registry
			registry.dataset_metrics(uuid='3f8a1297-3259-4700-91fc-acc4170b27ce')
			registry.dataset_metrics(uuid='66dd0960-2d7d-46ee-a491-87b9adcfe7b1')
			registry.dataset_metrics(uuid=['3f8a1297-3259-4700-91fc-acc4170b27ce', '66dd0960-2d7d-46ee-a491-87b9adcfe7b1'])
	'''
	def getdata(x, **kwargs):
		url = gbif_baseurl + 'dataset/' + x + '/metrics'
		return gbif_GET(url, {}, **kwargs)

	if len2(uuid) == 1:
		return getdata(uuid)
	else:
		return [getdata(x) for x in uuid]

def datasets(data = 'all', type = None, uuid = None, query = None, id = None,
							limit = 100, start = None, **kwargs):
	'''
	Search for datasets and dataset metadata.

	:param data: [str] The type of data to get. Default: 'all'
	:param type: [str] Type of dataset, options include 'OCCURRENCE', etc.
	:param uuid: [str] UUID of the data node provider. This must be specified if data
		 is anything other than 'all'.
	:param query: [str] Query term(s). Only used when `data = 'all'`
	:param id: [int] A metadata document id.

	References http://www.gbif.org/developer/registry#datasets

	Usage::

			from pygbif import registry
			registry.datasets(limit=5)
			registry.datasets(type="OCCURRENCE")
			registry.datasets(uuid="a6998220-7e3a-485d-9cd6-73076bd85657")
			registry.datasets(data='contact', uuid="a6998220-7e3a-485d-9cd6-73076bd85657")
			registry.datasets(data='metadata', uuid="a6998220-7e3a-485d-9cd6-73076bd85657")
			registry.datasets(data='metadata', uuid="a6998220-7e3a-485d-9cd6-73076bd85657", id=598)
			registry.datasets(data=['deleted','duplicate'])
			registry.datasets(data=['deleted','duplicate'], limit=1)
	'''
	args = {'q': query, 'type': type, 'limit': limit, 'offset': start}
	data_choices = ['all', 'organization', 'contact', 'endpoint',
									'identifier', 'tag', 'machinetag', 'comment',
									'constituents', 'document', 'metadata', 'deleted',
									'duplicate', 'subDataset', 'withNoEndpoint']
	check_data(data, data_choices)

	def getdata(x, uuid, args, **kwargs):
		if x not in ['all','deleted','duplicate','subDataset','withNoEndpoint'] and uuid is None:
			raise TypeError('You must specify a uuid if data does not equal all and data does not equal of deleted, duplicate, subDataset, or withNoEndpoint')

		if uuid is None:
			if x is 'all':
				url = gbif_baseurl + 'dataset'
			else:
				if id is not None and x is 'metadata':
					url = gbif_baseurl + 'dataset/metadata/' + id + '/document'
				else:
					url = gbif_baseurl + 'dataset/' + x
		else:
			if x is 'all':
				url = gbif_baseurl + 'dataset/' + uuid
			else:
				url = gbif_baseurl + 'dataset/' + uuid + '/' + x

		res = gbif_GET(url, args, **kwargs)
		return {'meta': get_meta(res), 'data': parse_results(res, uuid)}

	# Get data
	if len2(data) ==1:
		return getdata(data, uuid, args, **kwargs)
	else:
		return [getdata(x, uuid, args, **kwargs) for x in data]
