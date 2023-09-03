from snplot.data import linedata, markdata
from snplot.plot import xyplot
from snplot.tkwindow import tkwindow
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
xyplot = xyplot(data, "test_curve")
xyplot.import_config("./test_curve.json")
xyplot.expand_args()

window = tkwindow(xyplot)
window.mainloop()
