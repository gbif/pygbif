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
