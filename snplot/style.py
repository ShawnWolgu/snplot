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
            'snplot.scatter.fill':False
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
            'snplot.scatter.fill':True
        }
        color_dict = {
            'grey':'#6c6c6c',
            'red':'#c82f27',
            'yellow':'#d99f42',
            'green':'#63b84e',
            'cyan':'#58a7a2',
            'blue':'#4064af',
            'purple':'#673695',
            'violet':'#b83c7d',
            'orange':'#a2462d',
            'grass':'#8f9b47',
            'dark_green':'#446e53',
            'light_blue':'#508090',
            'mild_blue':'#3c3f8b',
            'mild_purple':'#823a7e'
        }
        markers = ['s', 'o', '^', 'v', 'D', '<', '>', 'h', 'p', 'd', 'P', 'X']
        super().__init__(params, color_dict, markers, 'default_mf')
        self.cmap = cm.batlow 
