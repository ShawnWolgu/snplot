import numpy as np
from scipy.interpolate import interp1d

def interpolate_data(x, y, jump):
    x_min = int(min(x) // jump)
    x_max = int(max(x) // jump)
    x_new = np.arange(x_min, x_max + 1) * jump
    f = interp1d(x, y)
    y_new = f(x_new)
    return x_new, y_new

def interpolate_data_xbase(x, y, xbase):
    f = interp1d(x, y, fill_value='extrapolate')
    y_new = f(xbase)
    return y_new

def rcparams_predeal(rcparams, scale):
    return_rcparams = {}
    for key in rcparams.keys():
        if "snplot" in key:
            continue
        return_rcparams[key] = rcparams[key]
        if type(rcparams[key]) == int or type(rcparams[key]) == float:
            if 'alpha' in key: continue
            return_rcparams[key] *= scale
    return return_rcparams

def convert_config(args):
    if "xlim" in args.keys():
        args['xlim'] = tuple(args['xlim'])
    if "ylim" in args.keys():
        args['ylim'] = tuple(args['ylim'])
    if "figure.figsize" in args.keys():
        args['figure.figsize'] = tuple(args['figure.figsize'])
    return args

