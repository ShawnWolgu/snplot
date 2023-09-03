from . import data
from .style import *
from .snplot import plotargs_apply
from .function import rcparams_scale, convert_config
from .tkwindow import tkwindow
import matplotlib.pyplot as plt
from matplotlib import rcParams
from copy import deepcopy
import json

class xyplot:

    rc_params = {
        'legend.loc': 'best',
        'legend.frameon': True,
        'legend.framealpha': 0.5,
        'legend.edgecolor': 'black',
        'figure.figsize': (7, 6),
        'lines.markersize': 0.8,
        'lines.linewidth': 0.5,
    }

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

    def load_plot(self):
        try:
            plt.close(self.plt)
        except:
            pass
        combined_rcp = deepcopy({**self.rc_params, **self.style.params})
        rcParams.update(rcparams_scale(combined_rcp,self.rc_params['figure.figsize'][0]))
        print(rcParams['figure.figsize'])
        color_list = list(self.style.color_dict.keys())
        fig, ax = plt.subplots()
        cd = self.style.color_dict
        for id,idata in enumerate(self.dataset):
            id = id % len(color_list)
            if idata.plottype == 'mark':
                ax.plot(idata.x, idata.y, self.style.markers[id], markeredgecolor = cd[color_list[id]], label = idata.label)
            elif idata.plottype == 'line':
                ax.plot(idata.x, idata.y, '-', color = cd[color_list[id]], label = idata.label)
            elif idata.plottype == 'dash':
                ax.plot(idata.x, idata.y, linestyle='dashed', color = cd[color_list[id]], label = idata.label)
            elif idata.plottype == 'linemark':
                ax.plot(idata.x, idata.y, self.style.markers[id], markeredgecolor = cd[color_list[id]], label = idata.label)
                ax.plot(idata.lx, idata.ly, '-', color = cd[color_list[id]])
            elif idata.plottype == 'mark_errorbar':
                ewidth = 0.5*rcParams['lines.linewidth']
                capsize =0.4*rcParams['lines.markersize']
                ax.errorbar(idata.x, idata.y, idata.yerr, fmt = 'none', ecolor=cd[color_list[id]], elinewidth=ewidth, capsize = capsize, barsabove=False)
                ax.plot(idata.x, idata.y, self.style.markers[id], markeredgecolor = cd[color_list[id]], label = idata.label, markerfacecolor='white')
            else:
                break
        ax.legend(frameon=False)
        ax.tick_params(direction="in")
        if self.plotargs!={}:
            ax = plotargs_apply(ax,self.plotargs)
        self.fig, self.ax = fig, ax

    def show(self):
        self.load_plot()
        plt.show()

    def show_only(self):
        plt.show()

    def show_tk(self):
        tkwindow(self).start()

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
        self.rc_params['legend.loc'] = loc

    def set_marksize(self, size:float):
        self.rc_params['lines.markersize'] = size

    def get_style(self, style:str):
        if style == 'default':
            return style_default()
        else:
            return style_default()

    def export_config(self, path:str = None):
        config = {}
        path = self.case_path + self.fig_name + '.json' if path is None else path
        config.update(self.plotargs)
        config['style'] = self.style.name
        config['rcparams'] = self.rc_params
        json.dump(config, open(path, 'w'),indent = 4)


    def import_config(self, path:str = None):
        path = self.case_path + self.fig_name + '.json' if path is None else path
        config = json.load(open(path, 'r'))
        self.style = self.get_style(config['style'])
        config.pop('style')
        self.rc_params = convert_config(config['rcparams'])
        config.pop('rcparams')
        self.plotargs.update(convert_config(config))
        print(self.plotargs)

    def expand_args(self):
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
        plt.close(self.fig)

    def update_args(self, input_args:dict):
        for key in input_args.keys():
            if key in self.plotargs.keys():
                self.plotargs[key] = input_args[key]
            elif key in self.rc_params.keys():
                self.rc_params[key] = input_args[key]
            else:
                pass
