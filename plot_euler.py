from snplot.data import eulerdata
from snplot.plot import inverse_pole_figure
import numpy as np

target = np.array([[ 45, 40, 40],
                   [100, 40, 75],
                   [ 15, 57, 45],
                   [ 12, 12, 11]])
dataset = []
pos = ['b', 'b', 'r', 'r']
for itar in range(4):
    idata = eulerdata([target[itar,0]], [target[itar,1]], [target[itar,2]],label = 'Axis '+str(itar), label_pos=pos[itar])
    idata.to_inverse_pole_figure('z')
    dataset.append(idata)
ipf = inverse_pole_figure(dataset,'euler_test')
ipf.show_tk()
