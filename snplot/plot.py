from . import data
from .style import *
from .snplot import load_plot, show_plot
import matplotlib.pyplot as plt
import json

class xyplot:
    def __init__(self):
        self.dataset = []
        self.fig_name = None
        self.case_path = './'
        self.plotargs = {}
        self.style = style_default()
        self.fig, self.ax = None, None
    def __init__(self, dataset:list, fig_name:str = " ", case_path:str = "./", style:str = 'default', **plotargs):
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
    def set_xlabel(self, xlabel:str):
        self.plotargs['xlabel'] = xlabel
    def set_ylabel(self, ylabel:str):
        self.plotargs['ylabel'] = ylabel
    def set_xlim(self, xlim:tuple):
        self.plotargs['xlim'] = xlim
    def set_ylim(self, ylim:tuple):
        self.plotargs['ylim'] = ylim
    def set_xscale(self, xscale:str):
        self.plotargs['xscale'] = xscale
    def set_yscale(self, yscale:str):
        self.plotargs['yscale'] = yscale
    def set_xticks(self, xticks:float):
        self.plotargs['xticks'] = xticks
    def set_yticks(self, yticks:float):
        self.plotargs['yticks'] = yticks
    def set_legendloc(self, loc:str):
        self.plotargs['legendloc'] = loc
    def set_marksize(self, size:float):
        if 'mark_plotargs' in self.plotargs:
            self.plotargs['mark_plotargs'] = {}
            self.plotargs['mark_plotargs']['markersize'] = size
        else:
            self.plotargs['mark_plotargs'] = {'markersize':size}
    def get_style(self, style:str):
        if style == 'default':
            return style_default()
        else:
            return style_default()
    def load_plot(self):
        try:
            plt.close(self.plt)
        except:
            pass
        self.fig, self.ax = load_plot(self, **self.plotargs) 
    def show(self):
        show_plot(self.fig, self.ax)
    def export_config(self, path:str = None):
        config = {}
        path = self.case_path + self.fig_name + '.json' if path is None else path
        config.update(self.plotargs)
        config['style'] = self.style.name
        json.dump(config, open(path, 'w'),indent = 4)
    def import_config(self, path:str = None):
        path = self.case_path + self.fig_name + '.json' if path is None else path
        config = json.load(open(path, 'r'))
        self.style = self.get_style(config['style'])
        config.pop('style')
        self.plotargs.update(config)
    def fill_plotargs(self):
        if ~hasattr(self, 'ax'):
            self.load_plot()
        self.plotargs['xlabel'] = self.ax.get_xlabel()
        self.plotargs['ylabel'] = self.ax.get_ylabel()
        self.plotargs['xlim'] = self.ax.get_xlim()
        self.plotargs['ylim'] = self.ax.get_ylim()
        self.plotargs['xscale'] = self.ax.get_xscale()
        self.plotargs['yscale'] = self.ax.get_yscale()
        self.plotargs['xticks'] = self.ax.get_xticks()[1] - self.ax.get_xticks()[0]
        self.plotargs['yticks'] = self.ax.get_yticks()[1] - self.ax.get_yticks()[0]
        self.plotargs['legendloc'] = self.ax.legend.loc if hasattr(self.ax.legend,'loc') is True else 'best'
        self.plotargs['figsize'] = tuple(self.fig.get_size_inches())
        scale = self.plotargs['figsize'][1]
        mark_plotargs = {
            'markerfacecolor' : 'None',
            'markeredgewidth' : 0.2 * scale,
            'markersize' : 0.8 * scale
        }
        mark_plotargs.update(self.plotargs['mark_plotargs'] if 'mark_plotargs' in self.plotargs.keys() else {})
        self.plotargs['mark_plotargs'] = mark_plotargs
