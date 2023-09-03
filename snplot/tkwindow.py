import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import customtkinter as ctk
from copy import deepcopy

class tkwindow:
    def __init__(self, plot_obj, width=900, height=600):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        self.window = ctk.CTk()
        self.window.title("SNPLOT")
        self.plot_frame = ctk.CTkFrame(self.window, width=2/3*width, height=height)
        self.plot_frame.pack(side="left")
        self.controllers_frame = ctk.CTkFrame(self.window, width=1/3*width, height=height)
        self.controllers_frame.pack(side="right")
        self.plot_obj = plot_obj
        self.arg_dict = deepcopy({**plot_obj.plotargs, **plot_obj.rc_params})
        self.controllers = self.create_controllers()

    def create_controllers(self):
        controllers = {}
        row_num = 0
        for key, value in self.arg_dict.items():
            controller = self.create_controller(key, value, row_num)
            controllers[key] = controller
            row_num += 1
        return controllers

    def create_controller(self, key, value, row_num):
        label = ctk.CTkLabel(self.controllers_frame, text=key)
    
        if isinstance(value, str):
            entry = ctk.CTkEntry(self.controllers_frame)
            entry.insert(ctk.END, value)
            entry.bind("<FocusOut>", lambda event: self.update_dict_entry(key, entry.get()))
            label.grid(row=row_num, column=0, sticky="e")
            entry.grid(row=row_num, column=1, sticky="w")
            return entry
    
        if isinstance(value, bool):
            label.grid(row=row_num, column=0, sticky="e")
            button_frame = ctk.CTkFrame(self.controllers_frame)
            button_frame.grid(row=row_num, column=1, columnspan=2, sticky="w")
            button_on = ctk.CTkButton(button_frame, text="On", command=lambda key=key: self.update_dict_entry(key, True))
            button_off = ctk.CTkButton(button_frame, text="Off", command=lambda key=key: self.update_dict_entry(key, False))
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
            scale = ctk.CTkSlider(self.controllers_frame, from_=lim_1, to=lim_2, command=lambda value: self.update_dict_entry(key, int(scale.get())))
            scale.set(value)
            label.grid(row=row_num, column=0, sticky="e")
            scale.grid(row=row_num, column=1, sticky="w")
            return scale
    
        if isinstance(value, float):
            lim_1, lim_2 = min(value*0,value*2), max(value*0,value*2)
            if abs(lim_1 - lim_2)<1e-5:
                lim_2 += 1
            scale = ctk.CTkSlider(self.controllers_frame, from_=lim_1, to=lim_2, command=lambda value: self.update_dict_entry(key, float(scale.get())))
            scale.set(value)
            label.grid(row=row_num, column=0, sticky="e")
            scale.grid(row=row_num, column=1, sticky="w")
            return scale
        
        if isinstance(value, tuple):
            tuple_frame = ctk.CTkFrame(self.controllers_frame)
            tuple_frame.grid(row=row_num, column=1, columnspan=2, sticky="w")
            label.grid(row=row_num, column=0, sticky="e")
            label.configure(anchor="e")
            if len(value) > 2:
                messagebox.showwarning("Unsupported Type", f"Type not supported for key: {key}")
                exit()
            key_1 = f"{key}[0]"
            lim_1_1, lim_1_2 = min(value[0]*0,value[0]*2), max(value[0]*0,value[0]*2)
            lim_1_2 += 1 if abs(lim_1_1 - lim_1_2)<1e-5 else 0
            scale_1 = ctk.CTkSlider(tuple_frame, from_=lim_1_1, to=lim_1_2, command=lambda value: self.update_dict_entry(key_1, float(scale_1.get())))
            scale_1.set(value[0])
            scale_1.grid(row=0, column=0, sticky="w")
            key_2 = f"{key}[1]"
            lim_2_1, lim_2_2 = min(value[1]*0,value[1]*2), max(value[1]*0,value[1]*2)
            lim_2_2 += 1 if abs(lim_2_1 - lim_2_2)<1e-5 else 0
            scale_2 = ctk.CTkSlider(tuple_frame, from_=lim_2_1, to=lim_2_2, command=lambda value: self.update_dict_entry(key_2, float(scale_2.get())))
            scale_2.set(value[1])
            scale_2.grid(row=0, column=1, sticky="w")
            return tuple_frame

        messagebox.showwarning("Unsupported Type", f"Type not supported for key: {key}")
        return None

    def update_dict_entry(self, key, value):
        print(f"Updating {key} to {value}")
        if key in self.arg_dict.keys():
            self.arg_dict[key] = value
        elif "[" in key and "]" in key:
            key, index = key.split("[")
            index = int(index[:-1])
            if key in self.arg_dict.keys():
                tuple_list = list(self.arg_dict[key])
                tuple_list[index] = value
                self.arg_dict[key] = tuple(tuple_list)
            else:
                messagebox.showwarning("Key Error", f"Key not found: {key}")
        else:
            messagebox.showwarning("Key Error", f"Key not found: {key}")
        self.plot_obj.export_config("./test_curve.json")
        self.update_plot()

    def update_plot(self):
        try:
            matplotlib.pyplot.clf()
        except:
            pass
        self.plot_obj.update_args(self.arg_dict)
        self.plot_obj.load_plot()
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(self.plot_obj.fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def mainloop(self):
        self.window.mainloop()
