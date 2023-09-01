import numpy as np

class xydata:
    def __init__(self, x_, y_, label:str):
        self.x = np.array(x_)
        self.y = np.array(y_)
        self.label = label
        self.plottype = None
    def as_mark(self):
        self.plottype = 'mark'
    def as_line(self):
        self.plottype = 'line'
    def as_dash(self):
        self.plottype = 'dash'

class markdata(xydata):
    def __init__(self, x_, y_, label:str):
        super().__init__(x_, y_, label)
        self.plottype = 'mark'

class linedata(xydata):
    def __init__(self, x_, y_, label:str):
        super().__init__(x_, y_, label)
        self.plottype = 'line'

class dashdata(xydata):
    def __init__(self, x_, y_, label:str):
        super().__init__(x_, y_, label)
        self.plottype = 'dash'

