import matplotlib, datetime
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .config import *
from tkinter import messagebox
import customtkinter as ctk
from copy import deepcopy

class tkwindow:
    ctl_number = 0
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
        self.label_list = []
        self.controllers = self.create_controllers()
        self.create_config_buttons()
        self.create_export_button()
        self.create_status_monitor()

    def create_controllers(self):
        controllers = {}
        row_num = 0
        for key, value in self.arg_dict.items():
            controller = self.create_controller(key, value, row_num)
            if controller is not None:
                controllers[key] = controller
                if isinstance(value, int) or isinstance(value, float):
                    row_num += 2
                elif isinstance(value, tuple):
                    row_num += 2
                else:
                    row_num += 1
        self.ctl_number = row_num
        return controllers

    def create_controller(self, key, value, row_num):
        slider_width = 100
        label = ctk.CTkLabel(self.controllers_frame, text=property_label[key])
        label.grid(row=row_num, column=0, sticky="e")
        self.label_list.append(label)
    
        if isinstance(value, str):
            entry = ctk.CTkEntry(self.controllers_frame)
            entry.insert(ctk.END, value)
            entry.bind("<FocusOut>", lambda event: self.update_dict_n_controllers(key, entry.get()))
            entry.grid(row=row_num, column=1, sticky="w")
            return [entry]
    
        if isinstance(value, bool):
            checkbox = ctk.CTkCheckBox(self.controllers_frame, text="", command=lambda: self.update_dict_n_controllers(key, bool(checkbox.get())))
            checkbox.grid(row=row_num, column=1, sticky="w")
            if value:
                checkbox.select()
            else:
                checkbox.deselect()
            return [checkbox]

        if isinstance(value, int):
            _frame = ctk.CTkFrame(self.controllers_frame)
            _frame.grid(row=row_num, column=1, rowspan=2, sticky="w")
            lim_1, lim_2 = min(value*0,value*2), max(value*0,value*2)
            if abs(lim_1 - lim_2)<1e-5:
                lim_2 += 1
            scale = ctk.CTkSlider(_frame, from_=lim_1, to=lim_2, width=slider_width, command=lambda value: self.update_dict_n_controllers(key, int(scale.get())))
            scale.set(value)
            scale.grid(row=0, column=0, sticky="w")
            number = ctk.CTkEntry(_frame, width=slider_width)
            number.insert(ctk.END, value)
            number.bind("<FocusOut>", lambda event: self.update_dict_n_controllers(key, int(number.get())))
            number.grid(row=1, column=0, sticky="w")
            return [scale, number]
        
        if isinstance(value, float):
            _frame = ctk.CTkFrame(self.controllers_frame)
            _frame.grid(row=row_num, column=1, rowspan=2, sticky="w")
            lim_1, lim_2 = min(value*0,value*2), max(value*0,value*2)
            if abs(lim_1 - lim_2)<1e-5:
                lim_2 += 1
            scale = ctk.CTkSlider(_frame, from_=lim_1, to=lim_2, width=slider_width, command=lambda value: self.update_dict_n_controllers(key, float(scale.get())))
            scale.set(value)
            scale.grid(row=0, column=0, sticky="w")
            number = ctk.CTkEntry(_frame, width=slider_width)
            number.insert(ctk.END, value)
            number.bind("<FocusOut>", lambda event: self.update_dict_n_controllers(key, float(number.get())))
            number.grid(row=1, column=0, sticky="w")
            return [scale, number]
        
        if isinstance(value, tuple):
            _frame = ctk.CTkFrame(self.controllers_frame)
            _frame.grid(row=row_num, column=1, columnspan=2, rowspan=2, sticky="w")
            if len(value) > 2:
                messagebox.showwarning("Unsupported Type", f"Type not supported for key: {key}")
                exit()
            key_1 = f"{key}[0]"
            lim_1_1, lim_1_2 = min(value[0]*0,value[0]*2), max(value[0]*0,value[0]*2)
            lim_1_2 += 1 if abs(lim_1_1 - lim_1_2)<1e-5 else 0
            scale_1 = ctk.CTkSlider(_frame, from_=lim_1_1, to=lim_1_2, width=slider_width, command=lambda value: self.update_dict_n_controllers(key_1, float(scale_1.get())))
            scale_1.set(value[0])
            scale_1.grid(row=0, column=0, sticky="w")
            number_1 = ctk.CTkEntry(_frame, width=slider_width)
            number_1.insert(ctk.END, value[0])
            number_1.bind("<FocusOut>", lambda event: self.update_dict_n_controllers(key_1, float(number_1.get())))
            number_1.grid(row=1, column=0, sticky="w")
            key_2 = f"{key}[1]"
            lim_2_1, lim_2_2 = min(value[1]*0,value[1]*2), max(value[1]*0,value[1]*2)
            lim_2_2 += 1 if abs(lim_2_1 - lim_2_2)<1e-5 else 0
            scale_2 = ctk.CTkSlider(_frame, from_=lim_2_1, to=lim_2_2, width=slider_width, command=lambda value: self.update_dict_n_controllers(key_2, float(scale_2.get())))
            scale_2.set(value[1])
            scale_2.grid(row=0, column=1, sticky="w")
            number_2 = ctk.CTkEntry(_frame, width=slider_width)
            number_2.insert(ctk.END, value[1])
            number_2.bind("<FocusOut>", lambda event: self.update_dict_n_controllers(key_2, float(number_2.get())))
            number_2.grid(row=1, column=1, sticky="w")
            return [scale_1, number_1, scale_2, number_2]

        messagebox.showwarning("Unsupported Type", f"Type not supported for key: {key}")
        return None

    def refresh_controllers(self):
        for _, controller_lists in self.controllers.items():
            for controller in controller_lists:
                controller.destroy()
        for label in self.label_list:
            label.destroy()
        self.label_list = []
        self.controllers = self.create_controllers()
        self.read_config_button.grid(row=self.ctl_number+1, column=0, sticky="w")
        self.write_config_button.grid(row=self.ctl_number+1, column=1, sticky="w")
        self.export_button.grid(row=self.ctl_number+2, column=0, sticky="w")
        self.status_monitor.grid(row=self.ctl_number+3, column=0, sticky="w")

    def update_dict_n_controllers(self, key, value):
        print(f"Updating {key} to {value}")
        if key in self.arg_dict.keys():
            self.arg_dict[key] = value
            refresh_controllers(key, [value], self.controllers)
        elif "[" in key and "]" in key:
            key, index = key.split("[")
            index = int(index[:-1])
            if key in self.arg_dict.keys():
                tuple_list = list(self.arg_dict[key])
                tuple_list[index] = value
                self.arg_dict[key] = tuple(tuple_list)
                refresh_controllers(key, tuple_list, self.controllers)
            else:
                messagebox.showwarning("Key Error", f"Key not found: {key}")
        else:
            messagebox.showwarning("Key Error", f"Key not found: {key}")
        self.update_plot()

    def create_config_buttons(self):
        self.read_config_button = ctk.CTkButton(self.controllers_frame, text="Read Config", command=self.load_config)
        self.read_config_button.grid(row=self.ctl_number+1, column=0, sticky="w")
        self.write_config_button = ctk.CTkButton(self.controllers_frame, text="Write Config", command=self.rewrite_config)
        self.write_config_button.grid(row=self.ctl_number+1, column=1, sticky="w")
    
    def create_export_button(self):
        self.export_button = ctk.CTkButton(self.controllers_frame, text="Export Graph", command=self.export_plot)
        self.export_button.grid(row=self.ctl_number+2, column=0, sticky="w")

    def create_status_monitor(self):
        self.status_monitor = ctk.CTkTextbox(self.controllers_frame, width=400, height=20)
        self.status_monitor.configure(state="disabled")
        self.status_monitor.grid(row=self.ctl_number+3, column=0, columnspan=3, rowspan=2, sticky="w")

    def update_status_monitor(self, text):
        self.status_monitor.configure(state="normal")
        self.status_monitor.delete(1.0, ctk.END)
        data_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_monitor.insert(ctk.END, f"{data_stamp} {text}\n")
        self.status_monitor.configure(state="disabled")

    def rewrite_config(self):
        config_name = "./config.json"
        self.plot_obj.export_config(config_name)
        self.update_status_monitor("Config written " + config_name)

    def load_config(self):
        config_name = "./config.json"
        self.plot_obj.import_config(config_name)
        self.arg_dict = deepcopy({**self.plot_obj.plotargs, **self.plot_obj.rc_params})
        self.update_status_monitor("Config loaded " + config_name)
        self.refresh_controllers()
        self.update_plot()

    def export_plot(self):
        self.plot_obj.save()
        self.update_status_monitor("Plot exported")

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

    def start(self):
        self.update_plot()
        self.window.mainloop()

def refresh_controllers(key, value, controllers):
    value_list = [element for element in value for i in range(2)]
    for (ictl, ival) in zip(controllers[key],value_list):
        if isinstance(ictl, ctk.CTkSlider):
            lim_1, lim_2 = min(ival*0,ival*2), max(ival*0,ival*2)
            if abs(lim_1 - lim_2)<1e-5:
                lim_2 += 1
                ictl.set(ival)
                ictl.configure(from_ = lim_1, to = lim_2)
        elif isinstance(ictl, ctk.CTkEntry):
            ictl.delete(0, ctk.END)
            ictl.insert(ctk.END, ival)
