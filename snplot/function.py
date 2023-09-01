import numpy as np
from scipy.interpolate import interp1d

def interpolate_data(x, y, interval):
    x_min = int(min(x) // interval)
    x_max = int(max(x) // interval)
    x_new = np.arange(x_min, x_max + 1) * interval
    f = interp1d(x, y)
    y_new = f(x_new)
    return x_new, y_new
