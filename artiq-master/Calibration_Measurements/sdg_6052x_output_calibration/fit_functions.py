import numpy as np

from fit_wrappers   import run_fit


####################################################
# Helper functions
####################################################

def gaussian(x, x_cnt, A, w):

    return A * np.exp( -(x - x_cnt)**2/(2.0 * w**2) )

def lorentzian(x, x_cnt, A, w):

    return A * w**2/((x - x_cnt)**2 + w**2)

####################################################
# Fit exp rise
####################################################

def fcn2min_exp(params, x, flags):

    G = params['G']
    p = params['p']
    Vsat = params['Vsat']

    model = G * x/(1 + np.abs(G * x/Vsat)**(2 * p))**(1/(2*p))

    #model = np.sqrt(10**(model/10))

    #model = np.log10(model**2) * 10.0

    return model


def fit_exp(x, y, vary = True):

    fcn2min_type = fcn2min_exp
     
    # Parameters to vary
    parameter_dict = {
            'p' : [ 1.5, 0, 1e3, vary ],
            'G'   : [ 0.5, 0, 1e3, vary ],
            'Vsat'   : [ 0.34, 0, 1e3, vary ],
            }

    # Flags to set
    flags = { 
            }

    print(parameter_dict)

    return run_fit(x, y, fcn2min_type, parameter_dict, flags)



