import numpy as np
from .function import interpolate_data, interpolate_data_xbase

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
    def interpolate(self, jump:float):
        self.x, self.y = interpolate_data(self._x, self._y, jump)

class markdata(xydata):
    def __init__(self, x_, y_, label:str, segment:int=1):
        super().__init__(x_, y_, label)
        self.plottype = 'mark'
        self.x = self._x[0::segment]
        self.y = self._y[0::segment]
    def set_segment(self, segment:int):
        print("set segment in markdata class")
        self.x = self._x[0::segment]
        self.y = self._y[0::segment]

class linedata(xydata):
    def __init__(self, x_, y_, label:str):
        super().__init__(x_, y_, label)
        self.plottype = 'line'

class dashdata(xydata):
    def __init__(self, x_, y_, label:str):
        super().__init__(x_, y_, label)
        self.plottype = 'dash'

class linemarkdata(markdata):
    def __init__(self, x_, y_, lx_, ly_, label:str, segment:int=1):
        super().__init__(x_, y_, label, segment)
        self._lx = np.array(lx_)
        self._ly = np.array(ly_)
        self.lx = self._lx
        self.ly = self._ly
        self.plottype = 'linemark'
    def interpolate(self, jump:float):
        self.x, self.y = interpolate_data(self._x, self._y, jump)
        self.lx, self.ly = interpolate_data(self._lx, self._ly, jump)

class markdata_errorbar(markdata):
    def __init__(self, x_, y_, yerr_, label:str, segment:int=1):
        super().__init__(x_, y_, label, segment)
        if isinstance(yerr_, float):
            self._yerr = np.ones(shape=(2,len(x_))) * yerr_
        elif len(np.array(yerr_).shape) == 1:
            self._yerr = np.array([yerr_, yerr_])
        else:
            self._yerr = np.array(yerr_)
        self.plottype = 'mark_errorbar'
        self.set_segment(segment)
    def __init__(self, x_, y_, yerr_up, yerr_low, label: str, segment: int = 1):
        super().__init__(x_, y_, label, segment)
        self._yerr = np.array([yerr_low, yerr_up])
        self.plottype = 'mark_errorbar'
        self.set_segment(segment)
    def __init__(self, x_, y_, yerr_up_x, yerr_up_y, yerr_low_x, yerr_low_y, label: str, segment: int = 1):
        super().__init__(x_, y_, label, segment)
        yerr_up = interpolate_data_xbase(np.array(yerr_up_x), np.array(yerr_up_y), self._x)
        yerr_low = interpolate_data_xbase(np.array(yerr_low_x), np.array(yerr_low_y), self._x)
        self._yerr = np.array([self._y - yerr_low, yerr_up - self._y])
        self._yerr[self._yerr < 0] = 0
        self.plottype = 'mark_errorbar'
        self.set_segment(segment)
    def set_segment(self, segment:int):
        print("set segment in markdata_errorbar class")
        self.x = self._x[0::segment]
        self.y = self._y[0::segment]
        self.yerr = self._yerr[:, 0::segment]
    def interpolate(self, jump: float):
        self.x, self.y = interpolate_data(self._x, self._y, jump)
        _, self._yerr[0,:] = interpolate_data(self._x, self._yerr[0,:], jump)
        _, self._yerr[1,:] = interpolate_data(self._x, self._yerr[1,:], jump)
