from . import data
from .style import *
from .snplot import plotargs_apply
from .function import rcparams_predeal, convert_config, trans_to_xy, calc_ipf
from .tkwindow import tkwindow
from os import path as p
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from copy import deepcopy
import json

class xyplot:
    rc_params = {
        'legend.loc': 'best',
        'legend.frameon': True,
        'legend.framealpha': 0.5,
        'legend.fontsize' : 2.,
        'legend.edgecolor': 'black',
        'figure.figsize': (7, 6),
        'lines.markersize': 0.8,
        'lines.linewidth': 0.5,
        'font.size': 2.5,
    }

    def __init__(self):
        self.dataset = []
        self.fig_name = None
        self.case_path = './'
        self.plotargs = {}
        self.style = style_default()
        self.fig, self.ax = None, None
        self.have_colorbar = False

    def __init__(self, dataset:list, fig_name:str = " ", case_path:str = "./", style:str = 'default', **plotargs):
        self.dataset = dataset
        self.fig_name = fig_name
        self.case_path = case_path
        self.plotargs = plotargs
        self.style = self.get_style(style)
        self.have_colorbar = False

    def add_data(self, d:data.xydata):
        self.dataset.append(d)

    def load_plot(self):
        try:
            plt.close(self.plt)
        except:
            pass
        combined_rcp = deepcopy({**self.rc_params, **self.style.params})
        rcParams.update(rcparams_predeal(combined_rcp,self.rc_params['figure.figsize'][0]))
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
            elif idata.plottype == 'mark_color':
                if self.style.params['snplot.scatter.fill']:
                    ax.scatter(idata.x, idata.y, c=idata.z, marker=self.style.markers[id], label = idata.label, cmap = self.style.cmap, vmin = idata.vmin, vmax = idata.vmax)
                else:
                    norm = plt.Normalize(vmin=idata.vmin, vmax=idata.vmax)(idata.z)
                    cmap = self.style.cmap
                    cols = cmap(norm)
                    ax.scatter(idata.x, idata.y, c='none', edgecolors= cols, marker=self.style.markers[id], label = idata.label)
                self.have_colorbar = True
            else:
                break
        ax.legend(frameon=False)
        ax.tick_params(which = "both", direction="in")
        if self.have_colorbar:
            fig.colorbar(ax.collections[0], ax=ax)
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

    def set_xticks(self, xticks):
        self.plotargs['xticks'] = xticks

    def set_yticks(self, yticks):
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
        self.plotargs['xticks'] = self.ax.get_xticks()
        self.plotargs['yticks'] = self.ax.get_yticks()
        plt.close(self.fig)

    def update_args(self, input_args:dict):
        for key in input_args.keys():
            if key in self.plotargs.keys():
                self.plotargs[key] = input_args[key]
            elif key in self.rc_params.keys():
                self.rc_params[key] = input_args[key]
            else:
                pass

    def save(self):
        if ~hasattr(self, 'ax'):
            self.load_plot()
        save_path = p.join(self.case_path, self.fig_name + '.png')
        self.fig.savefig(save_path, dpi = 300, bbox_inches='tight')

class pole_figure:
    rc_params = {
        'figure.figsize': (6, 6),
        'lines.markersize': 0.8,
        'lines.linewidth': 0.5,
        'font.size': 2.5,
    }

    def __init__(self):
        self.dataset = []
        self.fig_name = None
        self.case_path = './'
        self.plotargs = {}
        self.style = style_default()
        self.fig, self.ax = None, None
        self.have_colorbar = False

    def __init__(self, dataset:list, fig_name:str = " ", case_path:str = "./", style:str = 'default', **plotargs):
        self.dataset = dataset
        self.fig_name = fig_name
        self.case_path = case_path
        self.plotargs = plotargs
        self.style = self.get_style(style)
        self.have_colorbar = False

    def add_data(self, d:data.eulerdata):
        self.dataset.append(d)

    def load_plot(self):
        try:
            plt.close(self.plt)
        except:
            pass
        combined_rcp = deepcopy({**self.rc_params, **self.style.params})
        rcParams.update(rcparams_predeal(combined_rcp,self.rc_params['figure.figsize'][0]))
        cd = self.style.color_dict
        color_list = list(cd.keys())
        fig, ax = plt.subplots()
        for id,idata in enumerate(self.dataset):
            id = id % len(color_list)
            if idata.plottype != 'pole_figure':
                raise ValueError('Data type error!')
            ax.plot(idata.x, idata.y, '-', color = cd[color_list[id]])
            ax.plot(idata.x[0], idata.y[0], 'o', color = cd[color_list[id]])
            ax.plot(idata.x[-1], idata.y[-1], 's', color = cd[color_list[id]])
            ax.text(idata.x[0], idata.y[0], idata.label, color = cd[color_list[id]])

        circlep = np.arange(0,2.2*np.pi,0.1*np.pi)
        circlex = np.sin(circlep)
        circley = np.cos(circlep)
        ax.plot(circlex,circley,'k-')

        ax.axis('off')
        if self.have_colorbar:
            fig.colorbar(ax.collections[0], ax=ax)
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
        plt.close(self.fig)

    def update_args(self, input_args:dict):
        for key in input_args.keys():
            if key in self.plotargs.keys():
                self.plotargs[key] = input_args[key]
            elif key in self.rc_params.keys():
                self.rc_params[key] = input_args[key]
            else:
                pass

    def save(self):
        if ~hasattr(self, 'ax'):
            self.load_plot()
        save_path = p.join(self.case_path, self.fig_name + '.png')
        self.fig.savefig(save_path, dpi = 300, bbox_inches='tight')

class inverse_pole_figure(pole_figure):
    rc_params = {
        'figure.figsize': (8, 5.656),
        'lines.markersize': 0.8,
        'lines.linewidth': 0.5,
        'font.size': 2.5,
    }

    def load_plot(self):
        try:
            plt.close(self.plt)
        except:
            pass
        combined_rcp = deepcopy({**self.rc_params, **self.style.params})
        rcParams.update(rcparams_predeal(combined_rcp,self.rc_params['figure.figsize'][0]))
        cd = self.style.color_dict
        color_list = list(cd.keys())
        fig, ax = plt.subplots()

        ipf_axis = np.hstack((np.ones((31,1)),np.arange(0,1.001+1/30,1/30)[:31].reshape(31,1),np.ones((31,1))))
        pts = np.array([[]])
        for iaxis in ipf_axis:
            pts = np.append(pts,trans_to_xy(calc_ipf(iaxis)))
        pts = pts.reshape(-1,2)
        ax.plot(pts[:,0],pts[:,1],'k-')
        ax.plot([0,1.4141/3.4141],[0,0],'k-')
        ax.plot([0,1/2.732],[0,1/2.732],'k-')

        for id,idata in enumerate(self.dataset):
            id = id % len(color_list)
            if idata.plottype != 'inverse_pole_figure':
                raise ValueError('Data type error!')
            ax.plot(idata.x, idata.y, '-', color = cd[color_list[id]])
            ax.plot(idata.x[0], idata.y[0], 'o', color = cd[color_list[id]])
            ax.plot(idata.x[-1], idata.y[-1], 's', color = cd[color_list[id]])
            ax.text(idata.x[0], idata.y[0], idata.label, color = cd[color_list[id]])

        ax.axis('off')
        if self.have_colorbar:
            fig.colorbar(ax.collections[0], ax=ax)
        if self.plotargs!={}:
            ax = plotargs_apply(ax,self.plotargs)
        self.fig, self.ax = fig, ax
