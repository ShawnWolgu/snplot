from snplot.data import linedata, linemarkdata, markdata, markdata_errorbar
from snplot.plot import xyplot
import pandas as pd

df1 = pd.read_csv("./samples/stress_grain_001.csv")
x_ = df1["e33"]
y_ = df1["s33"]

df2 = pd.read_csv("./samples/stress_grain_011.csv")
lx_ = df2["e33"]
ly_ = df2["s33"]
linemdata = linemarkdata(x_, y_, lx_, ly_, "test_curve","line", segment=10)

df3 = pd.read_csv("./samples/stress_grain_011.csv")
x_ = df3["e33"]
y_ = df3["s33"]*2
linedata = linemarkdata(x_, y_, label="test_curve2")

df4 = pd.read_csv("./samples/stress_grain_011.csv")
x_ = df3["e33"]
y_ = df3["s33"]*1/2
markdata = markdata(x_, y_, "test_curve3", segment=100)

df_err = pd.read_csv('./samples/Akhondzadeh_001.csv')
x_ = df_err['x_0']
y_ = df_err['target']
yerr_x_upper = df_err['x_1']
yerr_y_upper = df_err['upper']
yerr_x_lower = df_err['x_2']
yerr_y_lower = df_err['lower']
data_err = markdata_errorbar(x_, y_, yerr_x_upper, yerr_y_upper, yerr_x_lower, yerr_y_lower, 'test_errorbar', segment=1)

data = [linemdata, linedata, markdata, data_err]
xyplot = xyplot(data, "test_curve")
xyplot.expand_args()
# xyplot.import_config("./config.json")
xyplot.show_tk()

