import numpy as np
from matplotlib import rcParams
from matplotlib import ticker
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

def plotargs_apply(ax,plotargs):
    if 'xlabel' in plotargs.keys():
        ax.set_xlabel(plotargs['xlabel'])
    if 'ylabel' in plotargs.keys():
        ax.set_ylabel(plotargs['ylabel'])
    if 'xlim' in plotargs.keys():
        ax.set_xlim(plotargs['xlim'])
    if 'ylim' in plotargs.keys():
        ax.set_ylim(plotargs['ylim'])
    if 'xscale' in plotargs.keys():
        ax.set_xscale(plotargs['xscale'])
        if plotargs['xlim'][0] <= 0:
            ax.set_xlim([None, None])
    if 'yscale' in plotargs.keys():
        ax.set_yscale(plotargs['yscale'])
        if plotargs['ylim'][0] <= 0:
            ax.set_ylim([None, None])
    if 'xticks' in plotargs.keys():
        ax.set_xticks(plotargs['xticks'])
    if 'yticks' in plotargs.keys():
        ax.set_yticks(plotargs['yticks'])
    if 'legendloc' in plotargs.keys():
        ax.legend(loc=plotargs['legendloc'])
    if 'havelegend' in plotargs.keys():
        if plotargs['havelegend'] == False:
            ax.legend().set_visible(False)
        else:
            ax.legend().set_visible(True)
    return ax

def expdata_deal(expdata,interval=1):
    expdata.columns = ['0','1']
    expdata = expdata[expdata['0']!='--'].reset_index(drop = True)
    expdata = expdata[expdata['1']!='--'].reset_index(drop = True).astype('float')
    expdata = expdata.iloc[np.arange(0,len(expdata),interval)]
    return expdata
