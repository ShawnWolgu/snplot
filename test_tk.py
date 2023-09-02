import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from copy import deepcopy
from snplot.data import linedata, markdata
from snplot.plot import xyplot
import pandas as pd

# Create controllers for each key in the JSON data
def create_controller(frame, key, value, args,row_num):
    label = ctk.CTkLabel(frame, text=key)

    if isinstance(value, str):
        entry = ctk.CTkEntry(frame)
        entry.insert(tk.END, value)
        entry.bind("<FocusOut>", lambda event: update_dict_entry(args, key, entry.get()))
        label.grid(row=row_num, column=0, sticky="e")
        entry.grid(row=row_num, column=1, sticky="w")
        return entry

    if isinstance(value, bool):
        label.grid(row=row_num, column=0, sticky="e")
        button_frame = ctk.CTkFrame(frame)
        button_frame.grid(row=row_num, column=1, columnspan=2, sticky="w")
        button_on = ctk.CTkButton(button_frame, text="On", command=lambda key=key: update_dict_entry(args, key, True))
        button_off = ctk.CTkButton(button_frame, text="Off", command=lambda key=key: update_dict_entry(args, key, False))
        button_on.grid(row=0, column=0, sticky="w")
        button_off.grid(row=0, column=1, sticky="w")
        print(value)
        if value:
            print("light on")
        return button_frame

    if isinstance(value, int):
        lim_1, lim_2 = min(value*0,value*2), max(value*0,value*2)
        if abs(lim_1 - lim_2)<1e-5:
            lim_2 += 1
        scale = ctk.CTkSlider(frame, from_=lim_1, to=lim_2, command=lambda value: update_dict_entry(args, key, int(scale.get())))
        scale.set(value)
        label.grid(row=row_num, column=0, sticky="e")
        scale.grid(row=row_num, column=1, sticky="w")
        return scale

    if isinstance(value, float):
        lim_1, lim_2 = min(value*0,value*2), max(value*0,value*2)
        if abs(lim_1 - lim_2)<1e-5:
            lim_2 += 1
        scale = ctk.CTkSlider(frame, from_=lim_1, to=lim_2, command=lambda value: update_dict_entry(args, key, float(scale.get())))
        scale.set(value)
        label.grid(row=row_num, column=0, sticky="e")
        scale.grid(row=row_num, column=1, sticky="w")
        return scale
    
    if isinstance(value, tuple):
        tuple_frame = ctk.CTkFrame(frame)
        tuple_frame.grid(row=row_num, column=1, columnspan=2, sticky="w")
        label.grid(row=row_num, column=0, sticky="e")
        label.configure(anchor="e")
        if len(value) > 2:
            messagebox.showwarning("Unsupported Type", f"Type not supported for key: {key}")
            exit()
        key_1 = f"{key}[0]"
        lim_1_1, lim_1_2 = min(value[0]*0,value[0]*2), max(value[0]*0,value[0]*2)
        if abs(lim_1_1 - lim_1_2)<1e-5:
            lim_1_2 += 1
        scale_1 = ctk.CTkSlider(tuple_frame, from_=lim_1_1, to=lim_1_2, command=lambda value: update_dict_entry(args, key_1, float(scale_1.get())))
        print(value[0], lim_1_1, lim_1_2, key)
        scale_1.set(value[0])
        scale_1.grid(row=0, column=0, sticky="w")
        key_2 = f"{key}[1]"
        lim_2_1, lim_2_2 = min(value[1]*0,value[1]*2), max(value[1]*0,value[1]*2)
        if abs(lim_2_1 - lim_2_2)<1e-5:
            lim_2_2 += 1
        scale_2 = ctk.CTkSlider(tuple_frame, from_=lim_2_1, to=lim_2_2, command=lambda value: update_dict_entry(args, key_2, float(scale_2.get())))
        scale_2.set(value[1])
        scale_2.grid(row=0, column=1, sticky="w")
        return tuple_frame
    messagebox.showwarning("Unsupported Type", f"Type not supported for key: {key}")

def update_dict_entry(args, key, value):
    print(f"Updating {key} to {value}")
    if key in args.keys():
        args[key] = value
    elif "[" in key and "]" in key:
        key, index = key.split("[")
        index = int(index[:-1])
        if key in args.keys():
            tuple_list = list(args[key])
            tuple_list[index] = value
            args[key] = tuple(tuple_list)
        else:
            messagebox.showwarning("Key Error", f"Key not found: {key}")
    else:
        messagebox.showwarning("Key Error", f"Key not found: {key}")
    xyplot.export_config("./test_curve.json")
    update_plot(args,xyplot)

def create_controllers(json_data):
    controllers = {}

    row_num = 0
    for key, value in json_data.items():
        controller = create_controller(controllers_frame, key, value, json_data, row_num)
        controllers[key] = controller
        row_num += 1

    return controllers

def update_plot(args, plot:xyplot):
    # Get user-defined values from the controllers
    try:
        matplotlib.pyplot.clf()
    except:
        pass
    plot.update_args(args)
    plot.load_plot()
     # Clear the previous plot within the plot_frame
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Embed the plot within the plot_frame
    canvas = FigureCanvasTkAgg(plot.fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


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

ctk.set_appearance_mode("light")
window = ctk.CTk()
window.title("SNPLOT")

plot_frame = ctk.CTkFrame(window, width=400, height=400)
plot_frame.pack(side="left")

controllers_frame = ctk.CTkFrame(window, width=200, height=400)
controllers_frame.pack(side="right")
dict_arg = deepcopy({**xyplot.plotargs, **xyplot.rc_params})
controllers = create_controllers(dict_arg)
update_plot(dict_arg, xyplot)

window.mainloop()
