import numpy as np
from .function import interpolate_data

class xydata:
    def __init__(self, x_, y_, label:str):
        self.x = np.array(x_)
        self._x = np.array(x_)
        self.y = np.array(y_)
        self._y = np.array(y_)
        self.label = label
        self.plottype = None
    def as_mark(self):
        self.plottype = 'mark'
    def as_line(self):
        self.plottype = 'line'
    def as_dash(self):
        self.plottype = 'dash'
    def interpolate(self, interval:float):
        self.x, self.y = interpolate_data(self._x, self._y, interval)

class markdata(xydata):
    def __init__(self, x_, y_, label:str, interval:int=1):
        super().__init__(x_, y_, label)
        self.plottype = 'mark'
        self.x = self._x[0::interval]
        self.y = self._y[0::interval]
    def set_interval(self, interval:int):
        self.x = self._x[0::interval]
        self.y = self._y[0::interval]

class linedata(xydata):
    def __init__(self, x_, y_, label:str):
        super().__init__(x_, y_, label)
        self.plottype = 'line'

class dashdata(xydata):
    def __init__(self, x_, y_, label:str):
        super().__init__(x_, y_, label)
        self.plottype = 'dash'

