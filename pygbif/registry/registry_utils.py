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
			raise TypeError(z + ' is not one of the choices')

def get_meta(x):
  if has_meta(x):
  	return { z: x[z] for z in ['offset','limit','endOfRecords'] }
  else:
  	return None

def has_meta(x):
	if x.__class__ != dict:
		return False
	else:
		tmp = [y in x.keys() for y in ['offset','limit','endOfRecords']]
		return True in tmp

def parse_results(x, y):
  if y.__class__.__name__ != 'NoneType':
  	if y.__class__ != dict:
  		return x
  	else:
	    if 'endOfRecords' in x.keys():
	      return x['results']
	    else:
	      return x
  else:
    return x['results']
