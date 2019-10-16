import lmfit
import numpy as np
from lmfit import Minimizer, Parameters, report_fit

def fcn2min(params, x, data, return_plot = False):
	A = params['amp']
	f = params['freq']
	d = params['dlt']
	x = np.arange(599)

	model = -A*np.cos(1/(f*2*np.pi)*x - d)

	if return_plot == False:
		return model - data
	else:
		return x, model

def my_fit(x, y):
	params = Parameters()

	params.add('amp',value=1.0,min=1.99,max=2.01)
	params.add('freq',value=1.0,max=100)
	params.add('dlt',value=1.0,min=0.0,max=0.1)

	minner = Minimizer(fcn2min, params, fcn_args=(x, y))
	result = minner.minimize()

	return result