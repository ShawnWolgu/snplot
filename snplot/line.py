import numpy as np
import pandas as pd 
from matplotlib import rcParams
import matplotlib.pyplot as plt
import os

class xydata:
    def __init__(self, x_, y_):
        self.x = np.array(x_)
        self.y = np.array(y_)
        self.plottype = None
    def as_mark(self):
        self.plottype = 'mark'
    def as_line(self):
        self.plottype = 'line'
    def as_dash(self):
        self.plottype = 'dash'

class markdata(xydata):
    def __init__(self, x_, y_):
        super().__init__(x_, y_)
        self.plottype = 'mark'

class linedata(xydata):
    def __init__(self, x_, y_):
        super().__init__(x_, y_)
        self.plottype = 'line'

class dashdata(xydata):
    def __init__(self, x_, y_):
        super().__init__(x_, y_)
        self.plottype = 'dash'

class xyplot:
    def __init__(self):
        self.dataset = []
        self.fig_name = None
        self.case_path = './'
        self.plotargs = {}
        self.style = 'default'
