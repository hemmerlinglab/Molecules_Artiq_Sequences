import numpy as np
import lmfit
from lmfit import Minimizer, Parameters, report_fit

"""
Scan Number to fit the Data: 135535
Moly Information:
    Isotope: abundance, freq
    Mo100:  9.63, -0.7945 GHz?
    Mo98 : 24.13, -0.2938
    Mo96 : 16.68, 0
    Mo94 :  9.25, -0.4107
    Mo92 : 14.84, -0.9144
    Mo97 :  9.55, -0.0180
    Mo95 : 15.92, -0.3028


"""

# define objective function: returns the array to be minimized
# function to minimize
def fcn2min(params, x, data, freqs = [], plot_fit = False):
    w = params['w']
    x_offset = params['x_offset']
    y_offset = params['y_offset']
    
    #iso_abund = 1.0/100.0 * np.array([9.63,24.13,16.68,9.25,14.84,9.55,15.92])
    
    ampl = []
    for k in range(len(freqs)):
        ampl.append(params['a' + str(k)])

    if plot_fit == False:
        freqs = freqs - x_offset

        model = y_offset

        for k in range(len(freqs)):
            model += ampl[k] * np.exp( -(x - freqs[k])**2/(2.0*w**2) )
 
        return model - data
    else:
        x_plot = np.linspace(np.min(x), np.max(x), 500)
        
        freqs = freqs - x_offset

        model = y_offset
        for k in range(len(freqs)):
            model += ampl[k] * np.exp( -(x_plot - freqs[k])**2/(2.0*w**2) )
        
        return (x_plot, model)


def fit_mo(x, y):
        params = Parameters()
 
        params.add('w', value=50.0, min=1.0, max=200, vary = True)
        params.add('x_offset', value=-100.0, min=np.min(x), max = np.max(x), vary = True)
        params.add('y_offset', value=0.0, min=-2.0, max=2.0, vary = True)

        
        freqs = np.array([-0.7945,-0.2938,-0.0180,0,+0.3028,+0.4107,0.9144]) * 1000 # in MHz
        #iso_abund =  np.array([9.63,24.13,16.68,9.25,14.84,9.55,15.92])
        for k in range(len(freqs)):
            params.add('a' + str(k), value = -1.0, min = -10.0, max = 0.0, vary = True)


        # do fit, here with leastsq model
        minner = Minimizer(fcn2min, params, fcn_args=(x, y, freqs))
        result = minner.minimize()
        
        # Store the Confidence data from the fit
        con_report = lmfit.fit_report(result.params)
        
        (x_plot, model) = fcn2min(result.params, x, y, freqs = freqs, plot_fit = True)

        return (x_plot, model, result)

