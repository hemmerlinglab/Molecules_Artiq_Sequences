import numpy as np
import lmfit
from lmfit import Minimizer, Parameters, report_fit



# define objective function: returns the array to be minimized
# function to minimize
def fcn2min(params, x, data, plot_fit = False):
    a = params['a']
    #w = params['w']
    x_offset = params['x_offset']
    y_offset = params['y_offset']
    T = params['T']
    
    iso_abund = 1.0/100.0 * np.array([12.887, 31.896, 16.098, 16.098, 21.754, 14.216, 14.216, 3.023, 0.126])
    freqs = np.array([-508.89, 0, -250.78, 589.75, 531.11, 835.19, 1153.68, 1190.36, 1888.80])
    M = np.array([176,174,173,173,172,171,171,170,168])
    amu = 1.6605390666050e-27 # kg/nucleon
    c = 299792458
    kB = 1.380649e-23
    yb_174_freq = 751.52653349e12
    m = M*amu
    freqs = freqs*(10**6)+yb_174_freq
   # print(freqs)

    ampl = []
    for k in range(len(iso_abund)):
        ampl.append(params['a' + str(k)])

    if plot_fit == False:
        freqs = freqs - x_offset

        model = y_offset

        for k in range(len(iso_abund)):
            model += a * ampl[k] * iso_abund[k] * np.sqrt(m[k]/(kB*T))/freqs[k] * np.exp( -(m[k]*(c**2)*(x - freqs[k])**2)/(2.0*T*kB*freqs[k]**2) )
            #print(model)
        return model - data
    else:
        x_plot = np.linspace(np.min(x), np.max(x), 200)
        
        freqs = freqs - x_offset

        model = y_offset
        for k in range(len(iso_abund)):
            model += a * ampl[k] * iso_abund[k] * np.sqrt(m[k]/(kB*T))/freqs[k] * np.exp( -(m[k]*c**2*(x_plot - freqs[k])**2)/(2.0*T*kB*freqs[k]**2) )
            #print(model)
        
        return (x_plot, model)

#170 3.023 1190.36
#171 14.216 835.19, 1153.68
#172 21.754 531.11
#173 16.098 -250.78, 589.75
#174 31.896 0
#176 12.887 -509

def fit_yb_T(x, y):
        params = Parameters()
 
        params.add('a', value=-5.0, min=-10.0, max=0.0, vary = True)
        #params.add('w', value=50.0, min=1.0, max=2000, vary = True)
        params.add('x_offset', value=50, min=np.min(x), max = np.max(x), vary = True)
        params.add('y_offset', value=0.0, min=-2.0, max=2.0, vary = True)
        params.add('T', value = 1.0, min=0.0, max=100.0, vary = True)

         
        iso_abund = np.array([12.887, 31.896, 16.098, 16.098, 21.754, 14.216, 14.216, 3.023, 0.126])
        for k in range(len(iso_abund)):
            params.add('a' + str(k), value = 1.0, min = 0.0, max = 10.0, vary = True)


        # print(params)
        # do fit, here with leastsq model
        minner = Minimizer(fcn2min, params, fcn_args=(x, y))
        result = minner.minimize()
        
        # Store the Confidence data from the fit
        con_report = lmfit.fit_report(result.params)
        
        (x_plot, model) = fcn2min(result.params, x, y, plot_fit = True)

        return (x_plot, model, result)

