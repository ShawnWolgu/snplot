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

def Euler_trans(euler_vector, axis = 'z'):
    # Transform Euler angle (ZXZ) to rotation matrix
    euler_vector = euler_vector / 180 * np.pi

    SPH=np.sin(euler_vector[0]); CPH=np.cos(euler_vector[0])
    STH=np.sin(euler_vector[1]); CTH=np.cos(euler_vector[1])
    STM=np.sin(euler_vector[2]); CTM=np.cos(euler_vector[2])
    
    if axis=='x':
        return np.array([CTM*CPH-SPH*STM*CTH,-STM*CPH-SPH*CTM*CTH,SPH*STH])
    if axis=='y':
        return np.array([CTM*SPH+CPH*STM*CTH,-SPH*STM+CPH*CTM*CTH,-STH*CPH])
    if axis=='z':
        return np.array([STH*STM,CTM*STH,CTH])
    else:
        matrix = np.array([[CTM*CPH-SPH*STM*CTH,-STM*CPH-SPH*CTM*CTH,SPH*STH],
              [CTM*SPH+CPH*STM*CTH,-SPH*STM+CPH*CTM*CTH,-STH*CPH],
              [STH*STM,CTM*STH,CTH]]).transpose()
        return np.dot(matrix, axis)

def trans_to_xy(axis_vec):
    axis_vec = axis_vec.reshape(-1)
    axis_temp = axis_vec - np.array([0,0,-1])
    axis_temp = axis_temp / abs(axis_temp[2])
    return (axis_temp - np.array([0,0,1]))[:2]

def calc_ipf(axis_vec):
    axis_vec = axis_vec/np.linalg.norm(axis_vec)
    sorted_axis = np.sort(np.abs(axis_vec),)
    axis_ipf = np.array([sorted_axis[1],sorted_axis[0],sorted_axis[2]])
    return axis_ipf

