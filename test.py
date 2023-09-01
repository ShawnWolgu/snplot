from snplot.data import linedata, markdata
import pandas as pd

df1 = pd.read_csv("./samples/stress_grain_001.csv")
x_ = df1["e33"]
y_ = df1["s33"]
data = [markdata(x_, y_, "001")]
df2 = pd.read_csv("./samples/stress_grain_011.csv")
x_ = df2["e33"]
y_ = df2["s33"]
data.append(linedata(x_, y_, "011"))

from snplot.plot import xyplot
xyplot = xyplot(data, "stress-strain", "./", {}, "default")

from snplot.snplot import load_plot, show_plot
fig, ax = load_plot(xyplot)
show_plot(fig, ax)




