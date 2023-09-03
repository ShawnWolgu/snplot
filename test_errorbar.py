from snplot.data import markdata_errorbar
import snplot
import pandas as pd

df1 = pd.read_csv('./samples/Akhondzadeh_001.csv')
x_ = df1['x_0']
y_ = df1['target']
yerr_x_upper = df1['x_1']
yerr_y_upper = df1['upper']
yerr_x_lower = df1['x_2']
yerr_y_lower = df1['lower']

data = markdata_errorbar(x_, y_, yerr_x_upper, yerr_y_upper, yerr_x_lower, yerr_y_lower, 'test_errorbar', segment=1)
pplot = snplot.plot.xyplot([data], "test_errorbar")
# pplot.show()
pplot.expand_args()
pplot.show_tk()
