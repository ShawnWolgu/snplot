import numpy as np
from matplotlib import rcParams
import matplotlib.pyplot as plt
import os

def plotdata(dataset,fig_name,case_path=os.getcwd(),**plotargs):
    params = {'font.family':'sans-serif','font.sans-serif':'Arial','font.style':'normal','font.weight':'normal','font.size':6}
    rcParams.update(params)
    color_dict = {'grey':'#6c6c6c','red':'#c82f27','yellow':'#d99f42','green':'#63b84e','cyan':'#58a7a2','blue':'#4064af','purple':'#673695','violet':'#b83c7d','orange':'#a2462d','grass':'#8f9b47','dgreen':'#446e53','lblue':'#508090','mblue':'#3c3f8b','mpurple':'#823a7e'}
    color = ['blue','red','green','yellow','purple','grey','violet','orange','lblue','mpurple','blue','red','green','yellow','purple','grey','violet','orange','lblue','mpurple']
    markers = ['o','v','D','p','s','.','^','*','O','>']

    fig,ax = plt.subplots(figsize=(3.5,3))
    for idno,idata in enumerate(dataset):
        if 'markdata' in idata.keys() and 'linedata' in idata.keys():
            ax.plot(idata['markdata'].to_numpy()[:,0],idata['markdata'].to_numpy()[:,1],markers[idno],markerfacecolor="None",markeredgecolor = color_dict[color[idno]],markeredgewidth=0.5,markersize = 4)
            ax.plot(idata['linedata'].to_numpy()[:,0],idata['linedata'].to_numpy()[:,1],'-',color = color_dict[color[idno]],label = idata['label'])
        elif 'markdata' in idata.keys():
            ax.plot(idata['markdata'].to_numpy()[:,0],idata['markdata'].to_numpy()[:,1],markers[idno],markerfacecolor="None",markeredgecolor = color_dict[color[idno]],markeredgewidth=0.5,markersize = 4,label = idata['label'])
        elif 'linedata' in idata.keys():
            ax.plot(idata['linedata'].to_numpy()[:,0],idata['linedata'].to_numpy()[:,1],'-',color = color_dict[color[idno]],label = idata['label'])
        elif 'dashdata' in idata.keys():
            ax.plot(idata['dashdata'].to_numpy()[:,0],idata['dashdata'].to_numpy()[:,1],linestyle='dashed',color = color_dict[color[idno]],label = idata['label'])
        elif 'dotline' in idata.keys():
            ax.plot(idata['dotline'].to_numpy()[:,0],idata['dotline'].to_numpy()[:,1],linestyle='dashed',color = color_dict[color[idno]])
        else:
            break
        ax.legend(frameon=False)
        ax.tick_params(direction="in")
    if plotargs!={}:
        ax = plotargs_apply(ax,plotargs)

    fig.savefig(case_path+'/'+fig_name+'.png',dpi=300)
    plt.close(fig)

def load_plot(a, **plotargs):
    try:
        plt.close(a.fig)
    except:
        pass
    scale = 6
    mark_plotargs = {
        'markerfacecolor' : 'None',
        'markeredgewidth' : 0.2 * scale,
        'markersize' : 0.8 * scale
    }
    mark_plotargs.update(plotargs['mark_plotargs'] if 'mark_plotargs' in plotargs.keys() else {})
    a.style.params['font.size'] *= scale
    rcParams.update(a.style.params)
    color_list = list(a.style.color_dict.keys())
    fig, ax = plt.subplots(figsize=(scale*1.1, scale))
    for idno,idata in enumerate(a.dataset):
        if idata.plottype == 'mark':
            ax.plot(idata.x, idata.y, a.style.markers[idno], markeredgecolor = a.style.color_dict[color_list[idno]], label = idata.label, **mark_plotargs)
        elif idata.plottype == 'line':
            ax.plot(idata.x, idata.y, '-', color = a.style.color_dict[color_list[idno]], label = idata.label)
        elif idata.plottype == 'dash':
            ax.plot(idata.x, idata.y, linestyle='dashed', color = a.style.color_dict[color_list[idno]], label = idata.label)
        else:
            break
    ax.legend(frameon=False)
    ax.tick_params(direction="in")
    if plotargs!={}:
        ax = plotargs_apply(ax,plotargs)
    return fig, ax

def show_plot(fig, ax):
    plt.show()

def plotargs_apply(ax,plotargs):
    if 'xlabel' in plotargs.keys():
        ax.set_xlabel(plotargs['xlabel'])
    if 'ylabel' in plotargs.keys():
        ax.set_ylabel(plotargs['ylabel'])
    if 'xlim' in plotargs.keys():
        ax.set_xlim(plotargs['xlim'])
    if 'ylim' in plotargs.keys():
        ax.set_ylim(plotargs['ylim'])
    if 'xticks' in plotargs.keys():
        ax.set_xticks(np.arange(ax.get_xticks().min(),ax.get_xticks().max()+plotargs['xticks'],plotargs['xticks']))
    if 'yticks' in plotargs.keys():
        ax.set_yticks(np.arange(ax.get_yticks().min(),ax.get_yticks().max()+plotargs['yticks'],plotargs['yticks']))
    if 'legendloc' in plotargs.keys():
        ax.legend(loc=plotargs['legendloc'])
    if 'xscale' in plotargs.keys():
        ax.set_xscale(plotargs['xscale'])
    if 'yscale' in plotargs.keys():
        ax.set_yscale(plotargs['yscale'])
    return ax

def expdata_deal(expdata,interval=1):
    expdata.columns = ['0','1']
    expdata = expdata[expdata['0']!='--'].reset_index(drop = True)
    expdata = expdata[expdata['1']!='--'].reset_index(drop = True).astype('float')
    expdata = expdata.iloc[np.arange(0,len(expdata),interval)]
    return expdata
