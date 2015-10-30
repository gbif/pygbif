def len2(x):
	if x.__class__ is str:
		return len([x])
	else:
		return len(x)

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
