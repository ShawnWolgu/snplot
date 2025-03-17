from snplot.data import eulerdata
from snplot.plot import pole_figure as pf
from snplot.plot import inverse_pole_figure as ipf
from pandas import read_csv
from os import path

dataset = []
label_pos = ['b','u','ul','ur','b','b', 'ur']
for idx, case in enumerate(["001", "111", "112", "213", "101", "102", "212"]):
    csvpath = path.join("~/Works/2023/0619_SRS Manuscript/0912_Cases/02_Al_fit/5E7_cases/", case, "euler_angle_grain.csv")
    try:
        euler = read_csv(csvpath)
    except:
        print("No file: {}".format(csvpath))
        continue
    phi1 = euler[["phi1"]]
    Phi = euler[["PHI"]]
    phi2 = euler[["phi2"]]
    
    data = eulerdata(phi1, Phi, phi2, case, segment=10, label_pos=label_pos[idx])
    data.to_inverse_pole_figure('z')
    dataset.append(data)

pf = ipf(dataset,"test_pf")
pf.show_tk()
