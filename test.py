from snplot.data import linedata, linemarkdata, markdata
from snplot.plot import xyplot
import pandas as pd

df1 = pd.read_csv("./samples/stress_grain_001.csv")
x_ = df1["e33"]
y_ = df1["s33"]
df2 = pd.read_csv("./samples/stress_grain_011.csv")
lx_ = df2["e33"]
ly_ = df2["s33"]
linemarkdata = linemarkdata(x_, y_, lx_, ly_, "test_curve", segment=10)
df3 = pd.read_csv("./samples/stress_grain_011.csv")
x_ = df3["e33"]
y_ = df3["s33"]*2
linedata = linedata(x_, y_, "test_curve2")
df4 = pd.read_csv("./samples/stress_grain_011.csv")
x_ = df3["e33"]
y_ = df3["s33"]*1/2
markdata = markdata(x_, y_, "test_curve3", segment=100)
data = [linemarkdata, linedata, markdata]
xyplot = xyplot(data, "test_curve")
# xyplot.import_config("./test_curve.json")
xyplot.expand_args()
xyplot.show_tk()

