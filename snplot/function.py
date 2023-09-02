import numpy as np
from scipy.interpolate import interp1d

def interpolate_data(x, y, interval):
    x_min = int(min(x) // interval)
    x_max = int(max(x) // interval)
    x_new = np.arange(x_min, x_max + 1) * interval
    f = interp1d(x, y)
    y_new = f(x_new)
    return x_new, y_new

def rcparams_scale(rcparams, scale):
    for key in rcparams.keys():
        if type(rcparams[key]) == int or type(rcparams[key]) == float:
            if 'alpha' in key: continue
            rcparams[key] *= scale
    return rcparams


def convert_config(args):
    if "xlim" in args.keys():
        args['xlim'] = tuple(args['xlim'])
    if "ylim" in args.keys():
        args['ylim'] = tuple(args['ylim'])
    if "figure.figsize" in args.keys():
        args['figure.figsize'] = tuple(args['figure.figsize'])
    return args

