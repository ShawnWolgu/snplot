from snplot.data import linedata, markdata
import pandas as pd

df1 = pd.read_csv("./samples/stress_grain_001.csv")
x_ = df1["e33"]
y_ = df1["s33"]
data = [markdata(x_, y_, "001")]
data[0].interpolate(0.01)
df2 = pd.read_csv("./samples/stress_grain_011.csv")
x_ = df2["e33"]
y_ = df2["s33"]
data.append(linedata(x_, y_, "011"))

from snplot.plot import xyplot
xyplot = xyplot(data, "test_curve")
xyplot.set_xlim((0,0.1))
xyplot.set_ylim((0,250))
xyplot.set_marksize(10)
xyplot.export_config()
xyplot.fill_plotargs()
xyplot.export_config("./2.json")
xyplot.load_plot()
xyplot.show()
xyplot.export_config("./3.json")

