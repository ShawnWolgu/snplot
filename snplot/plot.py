from . import data
from .style import *
from .function import rcparams_predeal, rcparams_update, rcparams_combine, convert_config, trans_to_xy, calc_ipf, add_text, spherical_triangle_area_vectorized, generate_diffusion_kernel
from .tkwindow import tkwindow
from .colormap import contour_colormap
from os import path as p
from multimethod import multimethod
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams, patches
from matplotlib.path import Path
from matplotlib.cm import ScalarMappable
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
from scipy.signal import convolve2d
from scipy import signal

import json

class xyplot:
    rc_params = {
        'legend.loc': 'best',
        'legend.frameon': True,
        'legend.framealpha': 0.5,
        'legend.fontsize' : 2.,
        'legend.title_fontsize': 2.,
        'legend.edgecolor': 'black',
        'figure.figsize': (7.5, 6),
        'lines.markersize': 0.8,
        'lines.linewidth': 0.5,
        'font.size': 2.5,
        'snplot.color_dict': 0,
        'snplot.color_wheel': 0,
        'snplot.scatter.fill': False
    }

    @multimethod
    def __init__(self):
        self.dataset = []
        self.plotset = []
        self.fig_name = "fig"
        self.case_path = './'
        self.plotargs = {}
        self.style = style_default()
        self.rc_params = rcparams_update(self.rc_params, self.style.params)
        self.fig, self.ax = None, None
        self.have_colorbar = False
        self.legend = None

    @multimethod
    def __init__(self, dataset:list, fig_name:str = "fig", case_path:str = "./", style:str = 'default', **plotargs):
        self.dataset = dataset
        self.plotset = []
        self.fig_name = fig_name
        self.case_path = case_path
        self.plotargs = plotargs
        self.style = self.get_style(style)
        self.rc_params = rcparams_update(self.rc_params, self.style.params)
        self.have_colorbar = False
        self.legend = None

    def add_data(self, d:data.xydata):
        self.dataset.append(d)

    def load_plot(self):
        try:
            plt.close(self.plt)
        except Exception:
            pass
        # print(self.plotargs)
        combined_rcp = rcparams_combine(self.style.params, self.rc_params)
        rcParams.update(rcparams_predeal(combined_rcp,self.rc_params['figure.figsize'][0]))
        self.fig, self.ax = plt.subplots()
        self.plotset = []
        for id,idata in enumerate(self.dataset):
            dict_id = self.rc_params['snplot.color_dict']
            id = (id + self.rc_params['snplot.color_wheel']) % len(self.style.color_dict[dict_id].keys())
            if idata.plottype in ['line', 'mark', 'dash', 'linemark', "mark_errorbar", "mark_color"]:
                self.add_plot(idata, id)
            else:
                break
        self.ax.tick_params(which = "both", direction="in")
        if self.have_colorbar:
            self.fig.colorbar(self.colorbar_mappable ,ax=self.ax)
        if self.plotargs!={}:
            if 'havelegend' not in self.plotargs.keys():
                self.plotargs['havelegend'] = True
            self.plotargs_apply()
        else:
            self.plotargs['havelegend'] = True
            self.plotargs_apply()

    @multimethod
    def add_plot(self, data:data.markdata, id:int):
        cmap = self.style.color_dict[self.rc_params['snplot.color_dict']]
        color = cmap[list(cmap.keys())[id]]
        if data.color is not None:
            color = data.color
        if data.fill:
            p, = self.ax.plot(data.x, data.y, self.style.markers[id], markerfacecolor = color, label = data.label)
        else:
            p, = self.ax.plot(data.x, data.y, self.style.markers[id], markeredgecolor = color, label = data.label)
        self.plotset.append((p,))

    @multimethod
    def add_plot(self, data:data.linedata, id:int):
        cmap = self.style.color_dict[self.rc_params['snplot.color_dict']]
        color = cmap[list(cmap.keys())[id]]
        if data.color is not None:
            color = data.color
        p, = self.ax.plot(data.x, data.y, data.linetype, color = color, label = data.label)
        self.plotset.append((p,))

    @multimethod
    def add_plot(self, data:data.dashdata, id:int):
        cmap = self.style.color_dict[self.rc_params['snplot.color_dict']]
        color = cmap[list(cmap.keys())[id]]
        if data.color is not None:
            color = data.color
        p, = self.ax.plot(data.x, data.y, linestyle='dashed', color = color, label = data.label)
        self.plotset.append((p,))

    @multimethod
    def add_plot(self, data:data.linemarkdata, id:int):
        cmap = self.style.color_dict[self.rc_params['snplot.color_dict']]
        color = cmap[list(cmap.keys())[id]]
        if data.color is not None:
            color = data.color
        if data.consistent:
            if data.fill:
                p, = self.ax.plot(data.x, data.y, marker = self.style.markers[id], markerfacecolor = color, linestyle = '-', color = color, label = data.label)
            else:
                p, = self.ax.plot(data.x, data.y, marker = self.style.markers[id], markeredgecolor = color, linestyle = '-', color = color, label = data.label)
            self.plotset.append((p,))
        else:
            if data.fill:
                p1, = self.ax.plot(data.x, data.y, self.style.markers[id], markerfacecolor = color, label = data.label)
                p2, = self.ax.plot(data.lx, data.ly, '-', color = color, label = data.label_l)
            else:
                p1, = self.ax.plot(data.x, data.y, self.style.markers[id], markeredgecolor = color, label = data.label)
                p2, = self.ax.plot(data.lx, data.ly, '-', color = color, label = data.label_l)
            self.plotset.append((p1,p2))

    @multimethod
    def add_plot(self, data:data.markdata_errorbar, id:int):
        cmap = self.style.color_dict[self.rc_params['snplot.color_dict']]
        color = cmap[list(cmap.keys())[id]]
        if data.color is not None:
            color = data.color
        ewidth = 0.5*rcParams['lines.linewidth']
        capsize =0.4*rcParams['lines.markersize']
        if data.fill:
            self.ax.errorbar(data.x, data.y, data.yerr, fmt = 'none', ecolor=color, elinewidth=ewidth, capsize = capsize, barsabove=False)
            p, = self.ax.plot(data.x, data.y, self.style.markers[id], markerfacecolor = color, label = data.label)
        else:
            self.ax.errorbar(data.x, data.y, data.yerr, fmt = 'none', ecolor=color, elinewidth=ewidth, capsize = capsize, barsabove=False)
            p, = self.ax.plot(data.x, data.y, self.style.markers[id], markeredgecolor = color, label = data.label, markerfacecolor='white')
        self.plotset.append((p,))

    @multimethod
    def add_plot(self, data:data.markdata_color, id:int):
        # The color logic has not been synchronized with the other plot types
        if self.rc_params['snplot.scatter.fill']:
            cmap = self.style.color_dict[self.rc_params['snplot.color_dict']]
            ec = cmap[list(cmap.keys())[self.rc_params['snplot.color_wheel']]]
            p, = self.ax.scatter(data.x, data.y, c=data.z, edgecolors=ec,marker=self.style.markers[id], label = data.label, cmap = self.style.cmap, vmin = data.vmin, vmax = data.vmax)
            self.plotset.append((p,))
        else:
            norm = plt.Normalize(vmin=data.vmin, vmax=data.vmax)(data.z)
            cmap = self.style.cmap
            cols = cmap(norm)
            p, = self.ax.scatter(data.x, data.y, c='none', edgecolors= cols, marker=self.style.markers[id], label = data.label)
            self.plotset.append((p,))
        cmap = self.style.cmap
        norm = plt.Normalize(vmin=data.vmin, vmax=data.vmax)
        self.colorbar_mappable = ScalarMappable(norm=norm, cmap=cmap)
        self.have_colorbar = True

    def plotargs_apply(self):
        if 'xlabel' in self.plotargs.keys():
            self.ax.set_xlabel(self.plotargs['xlabel'])
        if 'ylabel' in self.plotargs.keys():
            self.ax.set_ylabel(self.plotargs['ylabel'])
        if 'xlim' in self.plotargs.keys():
            self.ax.set_xlim(self.plotargs['xlim'])
        if 'ylim' in self.plotargs.keys():
            self.ax.set_ylim(self.plotargs['ylim'])
        if 'xscale' in self.plotargs.keys():
            self.ax.set_xscale(self.plotargs['xscale'])
            if self.plotargs['xlim'][0] <= 0:
                self.ax.set_xlim([None, None])
        if 'yscale' in self.plotargs.keys():
            self.ax.set_yscale(self.plotargs['yscale'])
            if self.plotargs['ylim'][0] <= 0:
                self.ax.set_ylim([None, None])
        if 'xticks' in self.plotargs.keys():
            self.ax.set_xticks(self.plotargs['xticks'])
        if 'yticks' in self.plotargs.keys():
            self.ax.set_yticks(self.plotargs['yticks'])
        if 'legendloc' in self.plotargs.keys():
            if self.legend is not None:
                self.legend.loc = self.plotargs['legendloc']
            else:
                self.legend = self.ax.legend(loc = self.plotargs['legendloc'])
        if 'havelegend' in self.plotargs.keys():
            if 'legend.title' in self.plotargs.keys():
                legend_title = self.plotargs['legend.title']
            else:
                legend_title = None
            if 'markerfirst' in self.plotargs.keys():
                mkf = self.plotargs['markerfirst']
            else:
                mkf = True
            if self.legend is not None:
                self.legend.remove()
            if self.plotargs['havelegend'] == False:
                self.legend = self.ax.legend().set_visible(False)
            else:
                hdlength = 2
                for iset in self.plotset:
                    if len(iset) > 1:
                        hdlength = 3
                label_list = [i[0]._label for i in self.plotset]
                self.legend = self.ax.legend(
                    self.plotset, label_list, numpoints=1, 
                    handlelength=hdlength, 
                    title=legend_title,
                    markerfirst=mkf,
                    handler_map={tuple: HandlerTuple(ndivide=None)}
                ).set_visible(True)

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

    def set_havelegend(self, have:bool):
        self.rc_params['havelegend'] = have

    def set_legendtitle(self, title:str):
        self.plotargs['legend.title'] = title

    def set_plotarg(self, key:str, value):
        self.plotargs[key] = value

    def get_style(self, style:str):
        if style == 'default':
            return style_default()
        if style == 'default_mf':
            return style_default_mf()
        else:
            return style_default()

    def export_config(self, path:str = None):
        config = {}
        path = "./" + self.fig_name + '_config.json' if path is None else path
        config.update(self.plotargs)
        config['style'] = self.style.name
        config['rcparams'] = self.rc_params
        json.dump(config, open(path, 'w'),indent = 4)

    def import_config(self, path:str = None):
        path = "./" + self.fig_name + '_config.json' if path is None else path
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
        self.plotargs['havelegend'] = True
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
        'snplot.color_dict': 0,
        'snplot.color_wheel': 0,
        'snplot.outercontourwidth': 0.15
    }

    def __init__(self, dataset:list, fig_name:str = " ", case_path:str = "./", style:str = 'default', **plotargs):
        self.dataset = dataset
        self.fig_name = fig_name
        self.case_path = case_path
        self.plotargs = plotargs
        self.style = self.get_style(style)
        self.rc_params = rcparams_update(self.rc_params, self.style.params)
        self.have_colorbar = False

    def add_data(self, d:data.eulerdata):
        self.dataset.append(d)

    def load_plot(self):
        try:
            plt.close(self.plt)
        except:
            pass
        combined_rcp = rcparams_combine(self.style.params, self.rc_params)
        rcParams.update(rcparams_predeal(combined_rcp,self.rc_params['figure.figsize'][0]))
        cd = self.style.color_dict[self.rc_params['snplot.color_dict']]
        color_list = list(cd.keys())
        fig, ax = plt.subplots()
        for id,idata in enumerate(self.dataset):
            id = (id + self.rc_params['snplot.color_wheel']) % len(color_list)
            if type(idata) is not tuple: 
                if idata.plottype != 'pole_figure':
                    raise ValueError('Data type error!')
                ax.plot(idata.x, idata.y, '-', color = cd[color_list[id]])
                ax.plot(idata.x[0], idata.y[0], 'o', color = cd[color_list[id]])
                ax.plot(idata.x[-1], idata.y[-1], 's', color = cd[color_list[id]])
                add_text(ax, idata.label, idata.x[0], idata.y[0], pos=idata.label_pos, color = cd[color_list[id]])
            else:
                linetypes = ['-', '--', '-.', ':']
                for idd, ituple in enumerate(idata):
                    if ituple.plottype != 'pole_figure':
                        raise ValueError('Data type error!')
                    ax.plot(ituple.x, ituple.y, linetypes[idd], color = cd[color_list[id]])
                    ax.plot(ituple.x[0], ituple.y[0], 'o', color = cd[color_list[id]])
                    ax.plot(ituple.x[-1], ituple.y[-1], 's', color = cd[color_list[id]])
                add_text(ax, idata[0].label, idata[0].x[0], idata[0].y[0], pos=idata[0].label_pos, color = cd[color_list[id]])
        circlep = np.arange(0,2.2*np.pi,0.1*np.pi)
        circlex = np.sin(circlep)
        circley = np.cos(circlep)
        outercontourwidth = self.rc_params['snplot.outercontourwidth'] * self.rc_params['figure.figsize'][0]
        ax.plot(circlex,circley,'k-', linewidth = outercontourwidth)

        ax.axis('off')
        self.fig, self.ax = fig, ax
        if self.have_colorbar:
            self.fig.colorbar(self.ax.collections[0], ax=self.ax)
        if self.plotargs!={}:
            self.ax = self.plotargs_apply()
    
    def plotargs_apply(self):
        if 'xlabel' in self.plotargs.keys():
            self.ax.set_xlabel(self.plotargs['xlabel'])
        if 'ylabel' in self.plotargs.keys():
            self.ax.set_ylabel(self.plotargs['ylabel'])
        if 'xlim' in self.plotargs.keys():
            self.ax.set_xlim(self.plotargs['xlim'])
        if 'ylim' in self.plotargs.keys():
            self.ax.set_ylim(self.plotargs['ylim'])
        if 'xscale' in self.plotargs.keys():
            self.ax.set_xscale(self.plotargs['xscale'])
            if self.plotargs['xlim'][0] <= 0:
                self.ax.set_xlim([None, None])
        if 'yscale' in self.plotargs.keys():
            self.ax.set_yscale(self.plotargs['yscale'])
            if self.plotargs['ylim'][0] <= 0:
                self.ax.set_ylim([None, None])
        if 'xticks' in self.plotargs.keys():
            self.ax.set_xticks(self.plotargs['xticks'])
        if 'yticks' in self.plotargs.keys():
            self.ax.set_yticks(self.plotargs['yticks'])
        if 'legendloc' in self.plotargs.keys():
            self.ax.legend(loc=self.plotargs['legendloc'])
        if 'havelegend' in self.plotargs.keys():
            if self.plotargs['havelegend'] == False:
                self.ax.legend().set_visible(False)
            else:
                self.ax.legend().set_visible(True)
        return self.ax

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
        'snplot.color_dict': 0,
        'snplot.color_wheel': 0,
        'snplot.outercontourwidth': 0.15
    }

    def load_plot(self):
        try:
            plt.close(self.plt)
        except:
            pass
        combined_rcp = rcparams_combine(self.style.params, self.rc_params)
        rcParams.update(rcparams_predeal(combined_rcp,self.rc_params['figure.figsize'][0]))
        cd = self.style.color_dict[self.rc_params['snplot.color_dict']]
        color_list = list(cd.keys())
        fig, ax = plt.subplots()

        ipf_axis = np.hstack((np.ones((31,1)),np.arange(0,1.001+1/30,1/30)[:31].reshape(31,1),np.ones((31,1))))
        pts = np.array([[]])
        for iaxis in ipf_axis:
            pts = np.append(pts,trans_to_xy(calc_ipf(iaxis))[:2])
        pts = pts.reshape(-1,2)
        outercontourwidth = self.rc_params['snplot.outercontourwidth'] * self.rc_params['figure.figsize'][0]
        ax.plot(pts[:,0],pts[:,1],'k-', linewidth = outercontourwidth)
        ax.plot([0,1.4141/3.4141],[0,0],'k-', linewidth = outercontourwidth)
        ax.plot([0,1/2.732],[0,1/2.732],'k-', linewidth = outercontourwidth)

        for id,idata in enumerate(self.dataset):
            id = (id + self.rc_params['snplot.color_wheel']) % len(color_list)
            if type(idata) is not tuple: 
                if idata.plottype != 'inverse_pole_figure':
                    raise ValueError('Data type error!')
                ax.plot(idata.x, idata.y, '-', color = cd[color_list[id]])
                ax.plot(idata.x[0], idata.y[0], 'o', color = cd[color_list[id]])
                ax.plot(idata.x[-1], idata.y[-1], 's', color = cd[color_list[id]])
                add_text(ax, idata.label, idata.x[0], idata.y[0], pos=idata.label_pos, color = cd[color_list[id]])
            else:
                linetypes = ['-', '--', '-.', ':']
                for idd, ituple in enumerate(idata):
                    if ituple.plottype != 'inverse_pole_figure':
                        raise ValueError('Data type error!')
                    ax.plot(ituple.x, ituple.y, linetypes[idd%4], color = cd[color_list[id]])
                    ax.plot(ituple.x[0], ituple.y[0], 'o', color = cd[color_list[id]])
                    ax.plot(ituple.x[-1], ituple.y[-1], 's', color = cd[color_list[id]])
                add_text(ax, idata[0].label, idata[0].x[0], idata[0].y[0], pos=idata[0].label_pos, color = cd[color_list[id]])
        ax.axis('off')
        self.fig, self.ax = fig, ax
        if self.have_colorbar:
            self.fig.colorbar(self.ax.collections[0], ax=self.ax)
        if self.plotargs!={}:
            self.ax = self.plotargs_apply(self.ax,self.plotargs)


class pole_figure_contour(pole_figure):
    rc_params = {
        'figure.figsize': (8, 6),
        'font.size': 2.5,
        'snplot.outercontourwidth': 0.15,
        'snplot.contour_x_label': 'X',
        'snplot.contour_y_label': 'Y',
        'snplot.contour_resolution': 20,
        'snplot.contour_axis_on': True,
        'snplot.contour.cmap': 'jet',
        'snplot.contour.lim': (0, 50),
        'snplot.contour.gaussian.ratio' : 0.1,
        'snplot.contour.gaussian.sigma' : 0.05
    }
    
    def load_plot(self):
        try:
            plt.close(self.plt)
        except (AttributeError, TypeError):
            pass

        combined_rcp = rcparams_combine(self.style.params, self.rc_params)
        rcParams.update(rcparams_predeal(combined_rcp,self.rc_params['figure.figsize'][0]))
        fig, ax = plt.subplots()

        if type(self.dataset) is list:
            idata = self.dataset[0]
        else:
            idata = self.dataset
        if idata.plottype != 'pole_figure':
            raise ValueError('Data type error!')

        resol = self.rc_params['snplot.contour_resolution']
        x_edges = np.linspace(-1., 1., resol)
        y_edges = np.linspace(-1., 1., resol)

        def inverse_proj(x, y):
            z = (1 - x**2 - y**2)/(1 + x**2 + y**2)
            return np.array([x*(1+z), y*(1+z), z])
        
        dOmega = np.zeros((resol-1,resol-1))
        i, j = np.meshgrid(np.arange(resol-1), np.arange(resol-1), indexing='ij')
        p1 = inverse_proj(x_edges[i], y_edges[j])
        p2 = inverse_proj(x_edges[i+1], y_edges[j])
        p3 = inverse_proj(x_edges[i], y_edges[j+1])
        p4 = inverse_proj(x_edges[i+1], y_edges[j+1])
        area1 = spherical_triangle_area_vectorized(p1, p2, p4)
        area2 = spherical_triangle_area_vectorized(p1, p3, p4)
        dOmega = area1 + area2

        H_raw, _, _ = np.histogram2d(
            idata.x, idata.y, 
            bins=[x_edges, y_edges], 
            weights=idata.weight
        )

        gausigma = self.rc_params['snplot.contour.gaussian.sigma']
        a = self.rc_params['snplot.contour.gaussian.ratio']
        kernel = generate_diffusion_kernel(abs(x_edges[1]-x_edges[0]), gausigma)
        H_smoothed = convolve2d(H_raw, kernel, mode='same', boundary='symm')
        H_final = (1-a)*H_raw + a*H_smoothed
        H_final = H_final * (H_raw.sum() / H_final.sum())
        sum_omega = np.pi * 4/2
        MRD = H_final/dOmega*sum_omega
        
        if contour_colormap.keys().__contains__(self.rc_params['snplot.contour.cmap']):
            cmap = contour_colormap[self.rc_params['snplot.contour.cmap']]
        else:
            cmap = 'jet'

        lim_low, lim_high = self.rc_params['snplot.contour.lim']
        im = ax.imshow(MRD.T, extent=[-1, 1, -1, 1], 
                origin='lower', cmap=cmap, interpolation='bilinear', 
                vmin=lim_low, vmax=lim_high
                )

        patch = patches.Circle((0, 0), radius=1, transform=ax.transData)
        im.set_clip_path(patch)

        if self.have_colorbar:
            fig.colorbar(im, ax=ax, label='MRD', pad=0.1)
        ax.text(1.01, 0.5, self.rc_params['snplot.contour_x_label'], transform=ax.transAxes, ha='left', va='center')
        ax.text(0.5, 1.01, self.rc_params['snplot.contour_y_label'], transform=ax.transAxes, ha='center', va='bottom')
        outercontourwidth = self.rc_params['snplot.outercontourwidth'] * self.rc_params['figure.figsize'][0]
        circlep = np.arange(0,2.2*np.pi,0.01*np.pi)
        circlex = np.sin(circlep)
        circley = np.cos(circlep)
        ax.plot(circlex,circley,'k-', linewidth = outercontourwidth)
        if self.rc_params['snplot.contour_axis_on']:
            ax.plot([-1,1], [0,0], c = 'white',linestyle= "--", dashes=(5,5), linewidth = outercontourwidth * 0.8)
            ax.plot([0,0], [-1,1], c = 'white',linestyle= "--", dashes=(5,5), linewidth = outercontourwidth * 0.8)
        ax.axis('off')
        self.fig, self.ax = fig, ax
        if self.plotargs!={}:
            self.ax = self.plotargs_apply()

class inverse_pole_figure_contour(pole_figure):
    rc_params = {
        'figure.figsize': (9, 6),
        'font.size': 2.5,
        'snplot.outercontourwidth': 0.15,
        'snplot.contour_resolution': 20,
        'snplot.contour.cmap': 'jet',
        'snplot.contour.lim': (0, 50),
        'snplot.contour.gaussian.ratio' : 0.1,
        'snplot.contour.gaussian.sigma' : 0.05
    }

    def __init__(self, dataset:list, fig_name:str = " ", case_path:str = "./", style:str = 'default', **plotargs):
        super().__init__(dataset, fig_name, case_path, style, **plotargs)
        ipf_axis = np.hstack((np.ones((31,1)),np.arange(0,1.001+1/30,1/30)[:31].reshape(31,1),np.ones((31,1))))
        pts_list = [
            [0, 0],
            [(np.pi-2)/np.pi, 0],
            *[trans_to_xy(calc_ipf(iaxis))[:2] for iaxis in ipf_axis],
            [1/(1+np.sqrt(3)), 1/(1+np.sqrt(3))],
            [0, 0]
        ]
        self.patch_points = np.array(pts_list).reshape(-1,2)

    def load_plot(self):
        try:
            plt.close(self.plt)
        except (AttributeError, TypeError):
            pass

        combined_rcp = rcparams_combine(self.style.params, self.rc_params)
        rcParams.update(rcparams_predeal(combined_rcp,self.rc_params['figure.figsize'][0]))
        fig, ax = plt.subplots()

        if type(self.dataset) is list:
            idata = self.dataset[0]
        else:
            idata = self.dataset
        if idata.plottype != 'inverse_pole_figure':
            raise ValueError('Data type error!')

        verts = [(ipt[0], ipt[1]) for ipt in self.patch_points]
        outercontourwidth = self.rc_params['snplot.outercontourwidth'] * self.rc_params['figure.figsize'][0]
        patch = patches.PathPatch(
            Path(verts, [Path.MOVETO] + [Path.LINETO]*(len(self.patch_points)-2) + [Path.CLOSEPOLY]),
            facecolor='none',
            lw=outercontourwidth
        )

        resol = self.rc_params['snplot.contour_resolution']
        x_edges = np.linspace(0.0, np.sqrt(2)/(2. + np.sqrt(2)), resol)
        y_edges = np.linspace(0.0, 1./(1. + np.sqrt(3)), resol)
        
        def inverse_proj(x, y):
            z = (1 - x**2 - y**2)/(1 + x**2 + y**2)
            return np.array([x*(1+z), y*(1+z), z])
        
        dOmega = np.zeros((resol-1,resol-1))
        i, j = np.meshgrid(np.arange(resol-1), np.arange(resol-1), indexing='ij')
        p1 = inverse_proj(x_edges[i], y_edges[j])
        p2 = inverse_proj(x_edges[i+1], y_edges[j])
        p3 = inverse_proj(x_edges[i], y_edges[j+1])
        p4 = inverse_proj(x_edges[i+1], y_edges[j+1])
        area1 = spherical_triangle_area_vectorized(p1, p2, p4)
        area2 = spherical_triangle_area_vectorized(p1, p3, p4)
        dOmega = area1 + area2

        H_raw, _, _ = np.histogram2d(
            idata.x, idata.y, 
            bins=[x_edges, y_edges], 
            weights=idata.weight
        )

        gausigma = self.rc_params['snplot.contour.gaussian.sigma']
        a = self.rc_params['snplot.contour.gaussian.ratio']
        kernel = generate_diffusion_kernel(x_edges[1], gausigma)
        H_smoothed = convolve2d(H_raw, kernel, mode='same', boundary='symm')
        H_final = (1-a)*H_raw + a*H_smoothed
        H_final = H_final * (H_raw.sum() / H_final.sum())
        sum_omega = np.pi * 4/48
        MRD = H_final/dOmega*sum_omega
        # non_zero_mrd = MRD[MRD >= 0.01]
        # print(np.mean(non_zero_mrd))

        if contour_colormap.keys().__contains__(self.rc_params['snplot.contour.cmap']):
            cmap = contour_colormap[self.rc_params['snplot.contour.cmap']]
        else:
            cmap = 'viridis'
        
        lim_low, lim_high = self.rc_params['snplot.contour.lim']
        im = ax.imshow(MRD.T, 
                extent=[x_edges.min(), x_edges.max(), y_edges.min(), y_edges.max()],
                origin='lower', 
                cmap=cmap, interpolation='bilinear', 
                vmin=lim_low, vmax=lim_high
                )

        ax.add_patch(patch)
        im.set_clip_path(patch)
        if self.have_colorbar:
            fig.colorbar(im, ax=ax, label='MRD', pad=0.1)

        ax.axis('off')
        self.fig, self.ax = fig, ax
        if self.plotargs!={}:
            self.ax = self.plotargs_apply()

        ax.text(0., 0., "001", ha='right', va='top')
        ax.text(np.sqrt(2)/(2+np.sqrt(2)), 0., "101", ha='left', va='top')
        ax.text(1/(1+np.sqrt(3)), 1/(1+np.sqrt(3)), "111", ha='center', va='bottom')
