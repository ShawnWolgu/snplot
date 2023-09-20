from snplot.data import eulerdata
from snplot.plot import pole_figure as pf
from snplot.plot import inverse_pole_figure as ipf
from pandas import read_csv
from os import path

dataset = []
for case in ["001", "111", "112", "213", "101", "102", "212"]:
    csvpath = path.join("~/Desktop/Working/0716_SXCpp/SingleCrystalCpp/debug/0912_Fit/02_Al_fit/5E7_cases/", case, "euler_angle_grain.csv")
    euler = read_csv(csvpath)
    phi1 = euler[["phi1"]]
    Phi = euler[["PHI"]]
    phi2 = euler[["phi2"]]
    
    data = eulerdata(phi1, Phi, phi2, case, segment=100)
    data.to_inverse_pole_figure('z')
    dataset.append(data)

pf = ipf(dataset,"test_pf")
pf.show_tk()
