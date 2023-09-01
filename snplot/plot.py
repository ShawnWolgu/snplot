from . import data
from .style import *

class xyplot:
    def __init__(self):
        self.dataset = []
        self.fig_name = None
        self.case_path = './'
        self.plotargs = {}
        self.style = style_default()
    def __init__(self, dataset:list, fig_name:str, case_path:str, plotargs:dict, style:str):
        self.dataset = dataset
        self.fig_name = fig_name
        self.case_path = case_path
        self.plotargs = plotargs
        self.style = self.get_style(style)
    def add_data(self, d:data.xydata):
        self.dataset.append(d)
    def set_fig_name(self, name:str):
        self.fig_name = name
    def set_case_path(self, path:str):
        self.case_path = path
    def set_plotargs(self, args:dict):
        self.plotargs = args
    def set_style(self, style:str):
        self.style = self.get_style(style)
    def get_style(self, style:str):
        if style == 'default':
            return style_default()
        else:
            return style_default()
