from cmcrameri import cm
from .colormap import cm_pure, cm_pure2, cm_snplot, cm_zepeda, cm_dislocation

class style:
    def __init__(self, params, color_dict, markers, name) -> None:
        self.params = params
        self.color_dict = color_dict
        self.markers = markers
        self.name = name

class style_default(style):
    def __init__(self) -> None:
        params = {
            'font.family':'sans-serif',
            'font.sans-serif':'Helvetica',
            'font.style':'normal',
            'font.weight':'normal',
            'lines.markerfacecolor':'None',
            'lines.markeredgewidth':0.2,
            'patch.facecolor':'None',
            'patch.linewidth':0.2,
            'legend.fancybox': False,
            'xtick.minor.visible': False,
            'snplot.scatter.fill':False,
            'xtick.major.pad': 1.0,
            'ytick.major.pad': 1.0,
            'xtick.major.size': 1.,
            'ytick.major.size': 1.,
            'axes.labelpad': 1., 
            'legend.frameon': False,
            'legend.fontsize': 1.8,
            'legend.title_fontsize': 1.8,
            'lines.linewidth' : 0.33,
            'lines.markersize' : 1.15,
            'font.size': 1.8
        }
        color_dict = [
            cm_pure, cm_pure2, cm_snplot, cm_zepeda, cm_dislocation
        ]
        markers = ['s', 'o', '^', 'v', 'D', '<', '>', 'h', 'p', 'd', 'P', 'X']
        super().__init__(params, color_dict, markers, 'default')
        self.cmap = cm.batlow 

class style_default_mf(style):
    def __init__(self) -> None:
        params = {
            'font.family':'sans-serif',
            'font.sans-serif':'Helvetica',
            'font.style':'normal',
            'font.weight':'normal',
            'lines.markerfacecolor':'None',
            'lines.markeredgewidth':0.2,
            'patch.facecolor':'None',
            'patch.linewidth':0.2,
            'legend.fancybox': False,
            'xtick.minor.visible': False,
            'snplot.scatter.fill':True,
            'xtick.major.pad': 1.0,
            'ytick.major.pad': 1.0,
            'xtick.major.size': 1.,
            'ytick.major.size': 1.,
            'axes.labelpad': 0.8
        }
        color_dict = [
            cm_pure, cm_pure2, cm_snplot, cm_zepeda, cm_dislocation
        ]
        markers = ['s', 'o', '^', 'v', 'D', '<', '>', 'h', 'p', 'd', 'P', 'X']
        super().__init__(params, color_dict, markers, 'default_mf')
        self.cmap = cm.batlow 
