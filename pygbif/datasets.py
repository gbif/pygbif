import sys
import json
from simplejson import JSONDecodeError
from gbifutils import *

def dataset_metrics(uuid, **kwargs):
	'''
	Get details on a GBIF dataset.

	:param uuid: (character) One or more dataset UUIDs. See examples.
	:param **kwargs: Further named parameters.

	References: http://www.gbif.org/developer/registry#datasetMetrics

	Usage:
	pygbif.dataset_metrics(uuid='3f8a1297-3259-4700-91fc-acc4170b27ce')
	pygbif.dataset_metrics(uuid='66dd0960-2d7d-46ee-a491-87b9adcfe7b1')
	pygbif.dataset_metrics(uuid=['3f8a1297-3259-4700-91fc-acc4170b27ce',
		 '66dd0960-2d7d-46ee-a491-87b9adcfe7b1'])
	'''
	def getdata(x, **kwargs):
		url = baseurl + 'dataset/' + x + '/metrics'
		return gbif_GET(url, {}, **kwargs)

	if len2(uuid) == 1:
		return getdata(uuid)
	else:
		return [getdata(x) for x in uuid]

def len2(x):
	if x.__class__ is str:
		return len([x])
	else:
		return len(x)

def datasets(data = 'all', type = None, uuid = None, query = None, id = None,
							limit = 100, start = None, **kwargs):
	'''
	Search for datasets and dataset metadata.

	:param data: The type of data to get. Default is all data.
	:param type: Type of dataset, options include OCCURRENCE, etc.
	:param uuid: UUID of the data node provider. This must be specified if data
		 is anything other than 'all'.
	:param query: Query term(s). Only used when data='all'
	:param id: A metadata document id.

	References http://www.gbif.org/developer/registry#datasets

	Usage:
	pygbif.datasets(limit=5)
	pygbif.datasets(type="OCCURRENCE")
	pygbif.datasets(uuid="a6998220-7e3a-485d-9cd6-73076bd85657")
	pygbif.datasets(data='contact', uuid="a6998220-7e3a-485d-9cd6-73076bd85657")
	pygbif.datasets(data='metadata', uuid="a6998220-7e3a-485d-9cd6-73076bd85657")
	pygbif.datasets(data='metadata', uuid="a6998220-7e3a-485d-9cd6-73076bd85657", id=598)
	pygbif.datasets(data=['deleted','duplicate'])
	pygbif.datasets(data=['deleted','duplicate'], limit=1)
	'''
	args = {'q': query, 'limit': limit, 'offset': start}
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
				url = baseurl + 'dataset'
			else:
				if id is not None and x is 'metadata':
					url = baseurl + 'dataset/metadata/' + id + '/document'
				else:
					url = baseurl + 'dataset/' + x
		else:
			if x is 'all':
				url = baseurl + 'dataset/' + uuid
			else:
				url = baseurl + 'dataset/' + uuid + '/' + x

		res = gbif_GET(url, args, **kwargs)
		# return {'meta': get_meta(res), 'data': parse_results(res, uuid)}
		return res

	# Get data
	if len2(data) ==1:
		return getdata(data, uuid, args, **kwargs)
	else:
		return [getdata(x, uuid, args, **kwargs) for x in data]

def check_data(x,y):
	if len2(x) == 1:
		testdata = [x]
	else:
		testdata = x

	for z in testdata:
		if z not in y:
			raise TypeError(z + ' not one of the choices')

def get_meta(x):
  if has_meta(x):
  	return [x[y] for y in ['offset','limit','endOfRecords']]
  else:
  	return None

def has_meta(x):
	tmp = [y in x.keys() for y in ['offset','limit','endOfRecords']]
	return True in tmp

if __name__ == "__main__":
    import doctest
    doctest.testmod()
