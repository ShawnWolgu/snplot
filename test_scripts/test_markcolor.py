import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cmcrameri.cm as cmc
from snplot.data import markdata_color
from snplot.plot import xyplot

def plot_rate_SRS(df):
    # Filter the REF column to contain only integers from 0 to 4
    df['REF'] = df['REF'].astype(int)
    df_ref_filtered = df[df['REF'].isin([0, 1, 2, 3, 4, 5])]
    
    min_ = np.log10(df_ref_filtered['DD'].min())
    max_ = np.log10(df_ref_filtered['DD'].max())
    # Set marker shapes based on REF values
    marker_shapes = ['o', 's', '^', 'd', 'v', 'p']
    
    # Create the scatter plot
    # Create the scatter plot with varying marker shapes and colors
    for ref_value, marker_shape in zip(range(6), marker_shapes):
        ref_filtered = df_ref_filtered[df_ref_filtered['REF'] == ref_value]
        plt.scatter(ref_filtered['Rate'], ref_filtered['SRS'], c=np.log10(ref_filtered['DD']), s=50, marker=marker_shape, edgecolors='grey' ,label=f'REF {ref_value}', cmap=cmc.batlow)
        plt.clim(min_, max_)
    
    # Set plot title and labels
    plt.title('Scatter Plot')
    plt.xlabel('Rate')
    plt.ylabel('SRS')
    plt.xscale('log')
    plt.legend()
    
    cbar = plt.colorbar()
    cbar.set_label('log10(DD)')
    
    # Show the plot
    plt.show()


def plot_DD_rate(df):
    # Filter the REF column to contain only integers from 0 to 4
    df['REF'] = df['REF'].astype(int)
    df_ref_filtered = df[df['REF'].isin([0, 1, 2, 3, 4, 5, 6])]
    legend = ['Ha et al. 2020', 'Wang & Shan 2008', 'Zhou et al. 2007', 'Yadav, Chichili & Ramesh 1995', 'Sakino 2021', 'Kabirian, Khan, and Pandey 2014', 'Khan & Liu 2012']

    dataset = []
    for i in range(7):
        coeff = 1
        ref_filtered = df_ref_filtered[df_ref_filtered['REF'] == i]
        dataset.append(markdata_color(coeff * ref_filtered['DD'], ref_filtered['strain rate'], np.log10(ref_filtered['SRS']), legend[i]))

    for idata in dataset:
        idata.set_cmap_range((-2,0))

    plot = xyplot(dataset, "SRS")
    plot.set_xscale('log')
    plot.set_xlim((1e9,1e15))
    plot.set_yscale('log')
    plot.set_ylim((1e-3,1e9))
    plot.set_xlabel('Dislocation Density (m$^{-2}$)')
    plot.set_ylabel('Strain Rate (s$^{-1}$)')
    plot.rc_params['figure.figsize'] = (8,6)
    plot.load_plot()
    
    # Show the plot
    plot.show_tk()

if __name__ == "__main__":
    df = pd.read_csv('/Users/sunxiaochuan/Desktop/Working/0716_SXCpp/SingleCrystalCpp/debug/0712_DataPreparation/03_SRS_Al/SRS_Al.csv')
    plot_DD_rate(df)
    # plot_rate_SRS(df)
