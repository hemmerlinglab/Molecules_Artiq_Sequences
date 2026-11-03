import numpy as np
import lmfit
import copy

from lmfit import Minimizer, Parameters, report_fit


class Color:
    RED   = '\033[91m'
    GREEN = '\033[92m'
    BLUE  = '\033[94m'
    RESET = '\033[0m'


##########################################################################
# Fit Wrapper Functions
##########################################################################

def get_fit_parameters(d):

    # extracts fit parameters and their stderr
   
    fit_pars = {}

    for k in d.keys():

        fit_pars[k] = [d[k].value, d[k].stderr]

    return fit_pars


###############################################

def paramsdict2params(params_dict):

    params = Parameters()

    for p in params_dict.keys():
    
        params.add(p, 
                   value    = params_dict[p][0], 
                   min      = params_dict[p][1], 
                   max      = params_dict[p][2], 
                   vary     = params_dict[p][3]
                   )
    return params


###############################################

def fcn2min_wrapper(params, fcn2min_type, x, data, flags, plot_fit = False, no_of_points = 2000):

    if plot_fit == False:
        x_fit = x
    else:
        x_fit = np.linspace(np.min(x), np.max(x), no_of_points)

    model = fcn2min_type(params, x_fit, flags)

    if plot_fit == False:
        return model - data
    else:
        return (x_fit, model)


###############################################

def run_fit(x, y, fcn2min_type, params_dict, flags):
    
    # note that the param_counter is an index, but the function takes the number of params

    params = paramsdict2params(params_dict)

    # do fit, here with leastsq model
    minner = Minimizer(fcn2min_wrapper, params, fcn_args=(fcn2min_type, x, y, flags))
    result = minner.minimize()
    
    if 'expand' in flags.keys():
        x_expand = [np.min(x) - flags['expand'], np.max(x) + flags['expand']]
    else:
        x_expand = x

    (xf, yf)         = fcn2min_wrapper(result.params, fcn2min_type, x_expand, y, flags, plot_fit = True)
    
    yf_res           = fcn2min_wrapper(result.params, fcn2min_type, x, y, flags, plot_fit = False, no_of_points = len(x))
    
    residuals = yf_res

    # Printing params

    print()
    print('*' * 30)
    print('Initial parameters')
    print('*' * 30)

    print_params(params)
    
    print('*' * 30)
    print('Optimized parameters')
    print('*' * 30)
    
    print_params(result.params)

    return (result, xf, yf, residuals)


###########################################################################################
# Print initial and optimized parameters
###########################################################################################

def print_params(params):

    par_arr = {}

    print()

    longest_key_length = max([len(k) for k in params.keys()])

    for k in sorted(params.keys()):

        par = params[k]

        #print("{0:7} : {2:8.2f} <= {1:8.2f} +/- {4:5.2f} <= {3:8.2f}".format(k, par.value, par.min, par.max, par.stderr))

        print_single_param(params, k, longest_key_length = longest_key_length)

        par_arr[k] = {
                'min' : par.min,
                'max' : par.max,
                'val' : par.value,
                'err' : par.stderr
                }

    print()

    return par_arr


###############################################

def print_single_param(params, key, 
                       longest_key_length = 1, 
                       no_of_digits = 2):

    par = params[key]
    
    if par.stderr == None:
        err = 'N/A'
    else:
        err = '{0:8.{1}f}'.format(par.stderr, no_of_digits)

    my_str = "\033[94m{0:{5}}\033[0m : {2:8.{6}f} <= {1:8.{6}f} +/- {4} <= {3:8.{6}f}".format(key, par.value, par.min, par.max, err, longest_key_length, no_of_digits)

    print(my_str)

    return my_str


###############################################

def get_single_param(params, par_key):

    par_arr = []
    for k in sorted(params.keys()):

        par = params[k]
        
        if par_key in k:

            par_arr.append(par.value)

    return np.array(sorted(par_arr))


