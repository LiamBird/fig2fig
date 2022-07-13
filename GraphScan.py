import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as wg
import os
import glob

from PIL import Image
import io
from IPython.display import display
from matplotlib.patches import Rectangle
from SelectFilesButton import SelectFilesButton

from datetime import datetime

# Annotate class used with minor variation from: https://stackoverflow.com/a/12057517 
class Annotate(object):
    def __init__(self, ax):
#         self.ax = plt.gca()
        self.ax = ax
        self.rect = Rectangle((0,0), 0.1, 0.1)
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        plt.show()
    def on_press(self, event):
        print('press')
        self.x0 = event.xdata
        self.y0 = event.ydata

    def on_release(self, event):
        print('release')
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        self.ax.figure.canvas.draw()
        
########## Load reload ##########
class _LoadReload(object):
    def __init__(self):    
        self._reload = False
        B_select_previous_files = SelectFilesButton()
        B_select_new_files = SelectFilesButton()
        B_confirm_save_location = wg.Button(description="Confirm directory")
        L_confirm_save_location = wg.Label(value="Please select a directory")       
        self.B_confirm_image_load = wg.Button(description="Confirm image")
        self.L_confirm_image = wg.Label(value="Click to confirm selection")
        
        image_types = ["*.png", "*.jpg", "*.jpeg", "*.eps"]
        
        self.vbox = wg.VBox([
            wg.HBox([wg.Label("Reload previous data"), B_select_previous_files]),
            wg.HBox([wg.Label("Create new data"), B_select_new_files]),
            wg.HBox([B_confirm_save_location, L_confirm_save_location])
        ])
        
        def on_B_confirm_save_location(b):
            if len(B_select_previous_files.files) > 0:
                self.save_directory = B_select_previous_files.files[0]
                L_confirm_save_location.value = self.save_directory
                self._reload = True
            elif len(B_select_new_files.files) > 0:
                self.save_directory = B_select_new_files.files[0]
                L_confirm_save_location.value = self.save_directory
                self._reload = False
            else:
                L_confirm_save_location.value = "No directory selected"
                self._reload = None
                
            available_images = [item for sublist in [glob.glob(os.path.join(self.save_directory, extension)) for extension in image_types] for item in sublist]
            fnames = [os.path.split(fname)[1] for fname in available_images]
            
            if self._reload == True:
                previously_scanned = [name for name in  os.listdir(self.save_directory) if os.path.isdir(os.path.join(self.save_directory, name))]
                options_list = [name for name in fnames if name.split(".")[0] in previously_scanned]
            else:
                options_list = fnames
                
            self.RB_raw_image = wg.RadioButtons(description="Available files", 
                                                     options=options_list)
            self.vbox.children = list(self.vbox.children)+[wg.VBox([self.RB_raw_image,
                                                                    wg.HBox([self.B_confirm_image_load,
                                                                            self.L_confirm_image])])]
        B_confirm_save_location.on_click(on_B_confirm_save_location)

########## Setting Axes ##########
class _Axis(object):
    def __init__(self, figsize):
        self.O_image_display = wg.Output()
        
        self.E_xaxis_min = wg.FloatText(description="x min")
        self.E_xaxis_max = wg.FloatText(description="x max")
        self.E_yaxis_min = wg.FloatText(description="y min")
        self.E_yaxis_max = wg.FloatText(description="y max")
        
        self.B_show_graph = wg.Button(description="Show graph")
        self.B_manual_select_area = wg.Button(description="Manually select area")
        self.B_confirm_manual_selection = wg.Button(description="Confirm manual selection")
        self.B_confirm_axis_lims = wg.Button(description="Confirm")
        self.B_save_axis_lims = wg.Button(description="Save")
        
        self.L_confirm_manual = wg.Label(value="Automatic")
        self.L_save_confirm = wg.Label(value="No values saved this session")
        
        self.manual_select = False
        
        def make_plot(b):
            with self.O_image_display:
                f, self.ax = plt.subplots(figsize=figsize)
        self.O_image_display.on_displayed(make_plot)
        
        def on_show_graph(b):
            ## self._image_name set in GUI
            self.raw_image = plt.imread(os.path.join(os.path.split(self.save_data_path)[0],
                                                     self._image_name))
            self.ax.imshow(self.raw_image)
        self.B_show_graph.on_click(on_show_graph)
        
        def on_manual_select_area(b):
            self.L_confirm_manual.value = "Click and drag graph area"
            self.selection = Annotate(self.ax)
        self.B_manual_select_area.on_click(on_manual_select_area)
        
        def on_confirm_manual_selection(b):
            self.manual_select = True
            self.confirmed_rectangle = Rectangle((self.selection.x0, self.selection.y0),
                                          (self.selection.x1-self.selection.x0),
                                          (self.selection.y1-self.selection.y0),
                                          facecolor="red", 
                                          alpha=0.5)
            self.selection.rect.remove()
            self.ax.add_patch(self.confirmed_rectangle)
            self.ax.figure.canvas.draw()
            self.L_confirm_manual.value = "Manual selection confirmed"
        self.B_confirm_manual_selection.on_click(on_confirm_manual_selection)
        
        def on_confirm_axis_clicked(b):
            if self.manual_select == False:
                self._reload_function()
                mid_row = int(self.raw_image.shape[0]/2)
                bottom_x = mid_row+np.argmin(np.sum(np.sum(self.raw_image[mid_row:, :], axis=1), axis=1))
                top_x = np.argmin(np.sum(np.sum(self.raw_image[:mid_row, :], axis=1), axis=1))
                
                mid_col = int(self.raw_image.shape[1]/2)
                left_y = np.argmin(np.sum(np.sum(self.raw_image[:, :mid_col], axis=0), axis=1))
                right_y = mid_col+np.argmin(np.sum(np.sum(self.raw_image[:, mid_col:], axis=0), axis=1))
                
            else:
                self.confirmed_rectangle.remove()
                left_y = int(self.selection.x0)
                right_y = int(self.selection.x1)
                top_x = int(self.selection.y0)
                bottom_x = int(self.selection.y1)
                
            self.axis_limits= {"bottom_x": bottom_x,
                    "left_y": left_y,
                    "top_x": top_x,
                    "right_y": right_y}
            self.axis_limits.update([("image_width", right_y-left_y)])
            self.axis_limits.update([("image_height", bottom_x-top_x)])
            self.axis_limits.update([("x_axis_extent", self.E_xaxis_max.value-self.E_xaxis_min.value)])
            self.axis_limits.update([("y_axis_extent", self.E_yaxis_max.value-self.E_yaxis_min.value)])
            self.axis_limits.update([("x_min", self.E_xaxis_min.value)])
            self.axis_limits.update([("x_max", self.E_xaxis_max.value)])
            self.axis_limits.update([("y_min", self.E_yaxis_min.value)])
            self.axis_limits.update([("y_max", self.E_yaxis_max.value)])
            
            self.cropped_image = self.raw_image[top_x:bottom_x, 
                                                left_y:right_y]
            
            self._show_cropped_image()
        self.B_confirm_axis_lims.on_click(on_confirm_axis_clicked)
        
        def on_save_clicked(b):
            np.save(os.path.join(self.save_data_path, "axis_limits.npy"),
                    self.axis_limits, allow_pickle=True)
            np.save(os.path.join(self.save_data_path, "cropped_image.npy"),
                    self.cropped_image, allow_pickle=True)
            self.L_save_confirm.value = "Data saved {}".format(datetime.now().strftime("%H:%M:%S"))
        self.B_save_axis_lims.on_click(on_save_clicked)
                
        self.vbox = wg.VBox([wg.HBox([self.B_show_graph]),
                             wg.HBox([self.E_xaxis_min, self.E_xaxis_max]),
                             wg.HBox([self.E_yaxis_min, self.E_yaxis_max]),
                             wg.HBox([self.B_manual_select_area, self.B_confirm_manual_selection]),
                             wg.HBox([self.B_confirm_axis_lims, self.B_save_axis_lims, self.L_save_confirm]),
                             self.O_image_display
                            ])
        
    def _show_cropped_image(self):
        self.ax.imshow(self.cropped_image,
                           extent=(self.axis_limits["x_min"],
                                   self.axis_limits["x_max"],
                                   self.axis_limits["y_min"],
                                   self.axis_limits["y_max"]))
        self.ax.set_aspect(self.axis_limits["x_axis_extent"]/
                           self.axis_limits["y_axis_extent"])
        plt.tight_layout()
        
    def _reload_function(self):
        if "axis_limits.npy" in os.listdir(self.save_data_path):
            self.axis_limits = np.load(os.path.join(self.save_data_path, "axis_limits.npy"), allow_pickle=True).item()
            self.E_xaxis_min.value = self.axis_limits["x_min"]
            self.E_xaxis_max.value = self.axis_limits["x_max"]
            self.E_yaxis_min.value = self.axis_limits["y_min"]
            self.E_yaxis_max.value = self.axis_limits["y_max"]
        if "cropped_image.npy" in os.listdir(self.save_data_path):
            self.cropped_image = np.load(os.path.join(self.save_data_path, "cropped_image.npy"), allow_pickle=True)
            self._show_cropped_image()
            
########## Lines CRates
class CRate_entry(object):
    def __init__(self, crate_data_reload=None):
        if crate_data_reload == None:
            crate_dict = dict([(wg.FloatText(description="CRate {}".format(1), min=0, value=0),
                                wg.HBox([wg.FloatText(description="Start", min=0, step=1),
                                         wg.FloatText(description="End", min=0, step=1)]))])
        else:
            crate_dict = {}
            for n, (keys, values) in enumerate(crate_data_reload.items()):
                if type(keys) == str:
                    rate = float(keys.split("_")[0])
                else:
                    rate = keys
                    
                crate_dict.update([(wg.FloatText(description="CRate {}".format(n+1), min=0, value=keys),
                                    wg.HBox([wg.FloatText(description="Start", min=0, value=values[0], step=1),
                                         wg.FloatText(description="End", min=0, value=values[1], step=1)]))])                    
                    

        crate_entries = wg.VBox([wg.HBox([keys, values]) for keys, values in crate_dict.items()])
        add_line_button = wg.Button(description="Add CRate")
        remove_line_button = wg.Button(description="Remove last CRate")

        def on_add_line_button_clicked(b):
            crate_dict.update([(wg.FloatText(description="CRate {}".format(len(crate_dict)+1), min=0),
                                wg.HBox([wg.FloatText(description="Start", min=0, step=1),
                                         wg.FloatText(description="End", min=0, step=1)]))])
            crate_entries.children = tuple(list(crate_entries.children)+[wg.HBox([[*crate_dict.keys()][-1], 
                                                                                  [*crate_dict.values()][-1]])])

        def on_remove_last_line_button_clicked(b):
            if len(crate_dict)>1: 
                crate_dict.pop([*crate_dict.keys()][-1])
                crate_entries.children = tuple(list(crate_entries.children)[:-1])

        add_line_button.on_click(on_add_line_button_clicked)
        remove_line_button.on_click(on_remove_last_line_button_clicked)

        self.entry = wg.VBox([wg.HBox([add_line_button, remove_line_button]),
                                   crate_entries])
        
def add_line_entry(line_label_entry="", 
                    color="#000000", 
                   crate_data_reload=None):
    line_label_instruction = wg.Label(value="Enter plot name")
    line_label_entry = wg.Text(value=line_label_entry)
    color_picker = wg.ColorPicker(concise=False,
                   description="Line color",
                   value=color,
                   disabled=False)
    crate_data = CRate_entry(crate_data_reload=crate_data_reload)
    return wg.VBox([wg.HBox([line_label_instruction, line_label_entry]),
                                 color_picker,
                                      crate_data.entry
                                     ])

def hex_to_rgb(hex_color):
    R = int(hex_color[1:3], 16)/255
    G = int(hex_color[3:5], 16)/255
    B = int(hex_color[5:7], 16)/255
    A = 1
    return[R, G, B, A]

class _Lines(object):
    def __init__(self, figsize):
        self.O_display_graph = wg.Output()
        self.B_show_graph = wg.Button(description="Show graph")
        self.B_add_line = wg.Button(description="Add line")
        self.B_remove_line = wg.Button(description="Remove last line")
        self.B_save_lines = wg.Button(description="Save lines")
                
        self.L_save_lines_confirm = wg.Label(value="No lines saved this session")
        
        self.line_entry_dict = {1: add_line_entry()}
        self.line_entry_accordion = wg.Accordion([value for value in self.line_entry_dict.values()])
        
        for nname, name in enumerate(self.line_entry_dict.keys()):
            self.line_entry_accordion.set_title(nname, name)
        
        def make_plot(b):
            with self.O_display_graph:
                f, self.ax = plt.subplots(figsize=figsize)
        self.O_display_graph.on_displayed(make_plot)
        
        def on_show_graph(b):
            self._reload_function()
        self.B_show_graph.on_click(on_show_graph)
            
        
        def on_add_line(b):
            self.line_entry_dict.update([(len(self.line_entry_dict)+1,
                                           add_line_entry())])
            self.line_entry_accordion.children = [value for value in self.line_entry_dict.values()]
            for nname, name in enumerate(self.line_entry_dict.keys()):
                self.line_entry_accordion.set_title(nname, name)
        self.B_add_line.on_click(on_add_line)
        
        def on_remove_line(b):
            if len(self.line_entry_dict) > 1:
                self.line_entry_dict.pop(len(self.line_entry_dict))
                self.line_entry_accordion.children = [value for value in self.line_entry_dict.values()]
                for nname, name in enumerate(self.line_entry_dict.keys()):
                    self.line_entry_accordion.set_title(nname, name)
        self.B_remove_line.on_click(on_add_line)
        
        def on_save_crates(b):
            saved_line_properties = {}
            for key, values in self.line_entry_dict.items():
                line_entries = {}
                line_entries.update([("Line name", values.children[0].children[1].value)])
                line_entries.update([("Hex color", values.children[1].value)])
                
                crates = {}
                for crate_entries in values.children[-1].children[1].children:
                    rate = crate_entries.children[0].value
                    start = int(crate_entries.children[1].children[0].value)
                    stop = int(crate_entries.children[1].children[1].value)
                    if rate in crates.keys():
                        rate = str(rate)+"_1"
                    else:
                        rate = str(rate)+"_0"
                    crates.update([(rate, [start, stop])])
                line_entries.update([("CRates", crates)])
                saved_line_properties.update([(key, line_entries)])
                
            np.save(os.path.join(self.save_data_path, "line_properties.npy"),
                   saved_line_properties, allow_pickle=True)
            self.L_save_lines_confirm.value = "Data saved {}".format(datetime.now().strftime("%H:%M:%S")) 
        self.B_save_lines.on_click(on_save_crates)
        
        self.vbox = wg.VBox([self.B_show_graph,
                             self.O_display_graph,
                             wg.HBox([self.B_add_line, self.B_remove_line]),
                             self.line_entry_accordion,
                             wg.HBox([self.B_save_lines, self.L_save_lines_confirm])])
        
    def _reload_function(self):
        if "axis_limits.npy" in os.listdir(self.save_data_path):
            self.axis_limits = np.load(os.path.join(self.save_data_path, "axis_limits.npy"), allow_pickle=True).item()
        if "cropped_image.npy" in os.listdir(self.save_data_path):
            self.cropped_image = np.load(os.path.join(self.save_data_path, "cropped_image.npy"), allow_pickle=True)
            self.ax.imshow(self.cropped_image,
                           extent=(self.axis_limits["x_min"],
                                   self.axis_limits["x_max"],
                                   self.axis_limits["y_min"],
                                   self.axis_limits["y_max"]))
            self.ax.set_aspect(self.axis_limits["x_axis_extent"]/
                           self.axis_limits["y_axis_extent"])
            
        if "line_properties.npy" in os.listdir(self.save_data_path):
            reloaded_line_properties = np.load(
            os.path.join(self.save_data_path, 'line_properties.npy'),
            allow_pickle=True).item()

            self.line_entry_dict = {}

            for keys, values in reloaded_line_properties.items():
                self.line_entry_dict.update([(keys,
                                              add_line_entry(line_label_entry=values["Line name"],
                                                             color=values["Hex color"],
                                                             crate_data_reload=values["CRates"]))])
                self.line_entry_accordion.children = [*self.line_entry_dict.values()]
                for nname, name in enumerate(self.line_entry_dict.keys()):
                    self.line_entry_accordion.set_title(nname, name)
                    
########## Masks
def pixels_to_array(self, axis, pos):
    if axis == "x":
        pixels_per_division = self.axis_limits["image_width"]/(self.axis_limits["x_max"]-self.axis_limits["x_min"])
        try:
            return int(pixels_per_division*(pos-self.axis_limits["x_min"]))
        except:
            return np.nan
    if axis == "y":
        pixels_per_division = self.axis_limits["image_height"]/(self.axis_limits["y_max"]-self.axis_limits["y_min"])
        try:
            return int(self.axis_limits["image_height"]-pixels_per_division*(pos-self.axis_limits["y_min"]))
        except:
            return np.nan
    
def array_to_pixels(self, axis, pos):
    if axis == "x":
        division_per_pixel = (self.axis_limits["x_max"]-self.axis_limits["x_min"])/self.axis_limits["image_width"]
        try:
            return int(division_per_pixel*pos)
        except:
            return np.nan
    if axis == "y":
        division_per_pixel = (self.axis_limits["y_max"]-self.axis_limits["y_min"])/self.axis_limits["image_height"]
        try:
            return int(self.axis_limits["y_max"]-division_per_pixel*pos)    
        except:
            return np.nan
    
class _Masks(object):
    def __init__(self, figsize):
        self.O_display_graph = wg.Output()
        
        self.B_show_graph = wg.Button(description="Show graph")
        B_add_mask = wg.Button(description="Add new mask")
        B_confirm_mask = wg.Button(description="Confirm current")
        B_clear_all = wg.Button(description="Clear all")
        self.B_apply_all = wg.Button(description="Apply all")
        
        self.L_mask_save = wg.Label(value="No masks saved this session")
        
        self.mask_list = {}
        self.confirmed_rectangles = []
        
        def make_plot(b):
            with self.O_display_graph:
                f, self.ax = plt.subplots(figsize=figsize) 
        self.O_display_graph.on_displayed(make_plot)      
        
        def on_show_graph(b):
            self._reload_function()
            self.ax.imshow(self.cropped_image,
                           extent=(self.axis_limits["x_min"],
                                   self.axis_limits["x_max"],
                                   self.axis_limits["y_min"],
                                   self.axis_limits["y_max"]))
            self.ax.set_aspect(self.axis_limits["x_axis_extent"]/
                           self.axis_limits["y_axis_extent"])
        self.B_show_graph.on_click(on_show_graph) 
        
        def on_add_mask(b):
            self.current_mask = Annotate(self.ax)
        B_add_mask.on_click(on_add_mask)
        
        def on_confirm_mask_clicked(b):
            self.mask_list.update([("mask "+str(len(self.mask_list)+1),
                                    [min([int(self.current_mask.y0), int(self.current_mask.y1)]),
                                     max([int(self.current_mask.y0), int(self.current_mask.y1)]),
                                     min([int(self.current_mask.x0), int(self.current_mask.x1)]),
                                     max([int(self.current_mask.x0), int(self.current_mask.x1)])
                                    ])])
            self.confirmed_rectangles.append(Rectangle((self.current_mask.x0, self.current_mask.y0),
                                                      (self.current_mask.x1-self.current_mask.x0),
                                                      (self.current_mask.y1-self.current_mask.y0),
                                                      facecolor="red", 
                                                      alpha=0.5))
            self.current_mask.rect.remove()
            self.ax.add_patch(self.confirmed_rectangles[-1])
            self.ax.figure.canvas.draw()
            self.current_mask = Annotate(self.ax)
        B_confirm_mask.on_click(on_confirm_mask_clicked)      
        
        def apply_masks_clicked(b):
            self._reload_function()
            [mask.remove() for mask in self.confirmed_rectangles]
            self.masked_img = np.zeros((self.cropped_image.shape))
            for x in range(self.cropped_image.shape[0]):
                for y in range(self.cropped_image.shape[1]):
                    self.masked_img[x, y, :] = self.cropped_image[x, y, :]

            for key, mask in self.mask_list.items():
                X0 = int(pixels_to_array(self, "x", mask[2]))
                X1 = int(pixels_to_array(self, "x", mask[3]))
                Y0 = int(pixels_to_array(self, "y", mask[1]))
                Y1 = int(pixels_to_array(self, "y", mask[0]))
                self.masked_img[Y0:Y1, X0:X1, :] = [1, 1, 1, 1]
                
            self.ax.cla()
            self.ax.imshow(self.masked_img,
                                extent=(self.axis_limits['x_min'], self.axis_limits['x_max'],
                                        self.axis_limits['y_min'], self.axis_limits['y_max']),
                               aspect=self.axis_limits['x_axis_extent']/self.axis_limits['y_axis_extent'])
            np.save(os.path.join(self.save_data_path,
                                 "masked_cropped_img.npy"),
                    self.masked_img, 
                   allow_pickle=True)
            self.L_mask_save.value = "Data saved {}".format(datetime.now().strftime("%H:%M:%S"))
        self.B_apply_all.on_click(apply_masks_clicked)        
                
        self.vbox = wg.VBox([self.B_show_graph,
                             wg.HBox([B_add_mask, B_confirm_mask]),
                             self.O_display_graph,
                             wg.HBox([self.B_apply_all, B_clear_all, self.L_mask_save])])
        
    def _reload_function(self):
        if "axis_limits.npy" in os.listdir(self.save_data_path):
            self.axis_limits = np.load(os.path.join(self.save_data_path, "axis_limits.npy"), allow_pickle=True).item()
            
        if "masked_cropped_img.npy" in os.listdir(self.save_data_path):
            self.masked_img = np.load(os.path.join(self.save_data_path, "masked_cropped_img.npy"), allow_pickle=True)
            self.ax.imshow(self.masked_img,
                           extent=(self.axis_limits["x_min"],
                                   self.axis_limits["x_max"],
                                   self.axis_limits["y_min"],
                                   self.axis_limits["y_max"]))
            self.ax.set_aspect(self.axis_limits["x_axis_extent"]/
                           self.axis_limits["y_axis_extent"])
            
        if "cropped_image.npy" in os.listdir(self.save_data_path):
            self.cropped_image = np.load(os.path.join(self.save_data_path, "cropped_image.npy"), allow_pickle=True)
            self.ax.imshow(self.cropped_image,
                           extent=(self.axis_limits["x_min"],
                                   self.axis_limits["x_max"],
                                   self.axis_limits["y_min"],
                                   self.axis_limits["y_max"]))
            self.ax.set_aspect(self.axis_limits["x_axis_extent"]/
                           self.axis_limits["y_axis_extent"])
            
########## Scan
def graph_scan(self, target_color, color_tolerance, margin=10):
    y_markers = []
    rgb = hex_to_rgb(target_color)
    cycle_step = self.axis_limits["image_width"]/(self.axis_limits["x_axis_extent"])
    slices = []
    
    for cycle in range(int(self.axis_limits["x_max"]-self.axis_limits["x_min"])):
        slice_min = int(cycle*cycle_step)
        slice_max = int((cycle+1)*(cycle_step))
        if slice_max > self.axis_limits["image_width"]-margin:
            slice_max = self.axis_limits["image_width"]-margin
        if slice_min < margin:
            slice_min = margin
        
        mask_slice = self.masked_img[margin:-margin, slice_min:slice_max, :]
        slices.append(mask_slice)
        color_true = np.zeros((mask_slice.shape[0], mask_slice.shape[1]), dtype=mask_slice.dtype)
        red = abs(mask_slice[:, :, 0]-rgb[0]) < color_tolerance
        green = abs(mask_slice[:, :, 1]-rgb[1]) < color_tolerance
        blue = abs(mask_slice[:, :, 2]-rgb[2]) < color_tolerance
        rgb_true = np.nonzero((red==True) & (green==True) & (blue==True))
        
        if rgb_true[0].shape[0]>0:
            y_markers.append(array_to_pixels(self, "y", np.nanmedian(rgb_true[0])+margin))
        else:
            y_markers.append(np.nan)
    return y_markers

### Monochrome scan added 13/07/2022
def _sub_monochrome(self, cycle, n_plots, min_marker_size=5, margin=10):
    cycle_step = self.axis_limits["image_width"]/(self.axis_limits["x_axis_extent"])
    slices = []
    
    slice_min = int(cycle*cycle_step)
    slice_max = int((cycle+1)*(cycle_step))
    if slice_max > self.axis_limits["image_width"]-margin:
        slice_max = self.axis_limits["image_width"]-margin
    if slice_min < margin:
        slice_min = margin

    slice_img = self.masked_img[margin:-margin, slice_min:slice_max, :]
    slice_sum = np.sum(np.sum(slice_img, axis=2), axis=1)

    bkg_sum = slice_img.shape[1]*slice_img.shape[2]
    non_bkg = margin+np.argwhere(slice_sum<bkg_sum).flatten()
    try:
        plot_id = dict([(n, {"start": None,
                             "end": None}) for n in range(n_plots)])

        plot_id[min(plot_id.keys())]["start"] = non_bkg[0]
        plot_id[max(plot_id.keys())]["end"] = non_bkg[-1]

        starts = []
        ends = []

        for n in range(1, non_bkg.shape[0]-1):
            if non_bkg[n]-non_bkg[n-1] > min_marker_size:
                starts.append(non_bkg[n])
            elif non_bkg[n+1]-non_bkg[n] > min_marker_size:
                ends.append(non_bkg[n])

        for key, value in [*plot_id.items()][1:]:
            value["start"] = starts[key-1]
        for key, value in [*plot_id.items()][:-1]:
            value["end"] = ends[key]
            
    except:
        plot_id = dict([(n, {"start": np.nan,
                             "end": np.nan}) for n in range(n_plots)])
        
    return plot_id

def monochrome(self, n_plots, plot_id="all", min_marker_size=4, margin=10):
    import warnings
    warnings.filterwarnings(action="ignore", category=RuntimeWarning)
    
    y = dict([(keys, []) for keys in range(n_plots)])
    
    for cycle in range(int(self.axis_limits["x_max"]-self.axis_limits["x_min"])):
        cycle_capacity = _sub_monochrome(self, cycle, n_plots, min_marker_size, margin)
        for keys, values in cycle_capacity.items():
            y[keys].append(array_to_pixels(self, "y", np.nanmean([*values.values()])))
    if plot_id == "all":        
        return y
    else:
        return y[plot_id]

class _Scan(object):
    def __init__(self):
        self.B_get_lines = wg.Button(description="Get line details")
        self.CB_monochrome = wg.Checkbox(description="Monochrome graph?", value=False)
        self.B_display_graph = wg.Button(description="Display graph")
        self.B_save_data = wg.Button(description="Save")
        self.L_save_confirm = wg.Label(value="No values saved this session")
        self.E_set_margin = wg.FloatText(description="Set margin pixels", value=10)
        self.O_graph_display = wg.Output()
        
        self.VB_trace_lines_box = wg.VBox([])
        
        self.tolerance_slider = wg.FloatSlider(min=0, max=1, step=0.05, value=0.3)
        
        def make_plot(b):
            with self.O_graph_display:
                f, self.ax = plt.subplots()
        self.O_graph_display.on_displayed(make_plot)
        
        def on_get_lines(b):
            self._reload_function()
            host_details = np.load(os.path.join(os.path.dirname(self.save_data_path),
                                                                'Saved_host_values.npy'), 
                                                allow_pickle=True).item()
            host_list = [values["Host label"] for values in host_details.values()]
            line_properties = np.load(os.path.join(self.save_data_path, "line_properties.npy"),
                                             allow_pickle=True).item()

            trace_lines = []
            
            for number, line in line_properties.items():
                line_name = wg.Label(value=line["Line name"])
                line_color = wg.ColorPicker(description="Line color", concise=True,
                                            value=line["Hex color"], disabled=True)
                host_dropdown = wg.Dropdown(options=host_list)
                trace_lines.append(wg.HBox([line_name, line_color, host_dropdown]))
                
            self.VB_trace_lines_box.children = trace_lines
        self.B_get_lines.on_click(on_get_lines)
        
        def scan_lines(b):
            line_properties = np.load(os.path.join(self.save_data_path, "line_properties.npy"),
                                             allow_pickle=True).item()
            self.lines = []
            
            for nline, line in enumerate(line_properties.values()):
                if self.CB_monochrome.value == False:
                    y_data = graph_scan(self, target_color=line["Hex color"], color_tolerance=0.3)
                    scanned, = self.ax.plot(np.arange(self.axis_limits["x_min"],
                                                      self.axis_limits["x_max"])+0.5, y_data, "o")
                    self.lines.append(scanned)
                else: ## ADDED
                    y_data = monochrome(self, n_plots=len(line_properties),
                                        plot_id=nline, min_marker_size=4, margin=1)
                    scanned, = self.ax.plot(np.arange(self.axis_limits["x_min"],
                                                      self.axis_limits["x_max"])+0.5, y_data, "o")
                    self.lines.append(scanned)

            def update(tolerance, margin):
                for nline, line in enumerate(line_properties.values()):
                    if self.CB_monochrome.value == False:
                        y_data = graph_scan(self, target_color=line["Hex color"], color_tolerance=tolerance, margin=int(margin))
                        self.lines[nline].set_ydata(y_data)
                    else: ## ADDED
                        y_data = monochrome(self, n_plots=len(line_properties), plot_id=nline, min_marker_size=4, margin=int(margin))
                        self.lines[nline].set_ydata(y_data)
                    
            wg.interact(update, tolerance=self.tolerance_slider, 
                        margin=self.E_set_margin)
        self.B_display_graph.on_click(scan_lines)
        
        def on_Scan_confirm_traced_lines(b):
            self.capacity_data = {}
            line_properties = np.load(os.path.join(self.save_data_path, 'line_properties.npy'),
                                      allow_pickle=True).item()
            
            for n, child in enumerate(self.VB_trace_lines_box.children):
                hex_color = child.children[1].value
                host_association = child.children[2].value
                line_association = child.children[0].value
                capacity = self.lines[n].get_ydata()
                crates = [values for values in line_properties.values() if values["Line name"] == line_association][0]["CRates"]

                cycle_data = []

                for keys, values in crates.items():
                    if type(keys) == str:
                        rate = float(keys.split("_")[0])
                    else:
                        rate = keys

                    cycle_numbers = np.arange(min(values), max(values))
                    rate_column = np.full((max(values)-min(values)), rate)
                    capacity_column = capacity[min(values):max(values)] 

                    cycle_data.append(np.vstack((cycle_numbers, rate_column, capacity_column)))

                self.capacity_data.update([(host_association,
                                       np.hstack((cycle_data)))])

            if "line_data" not in os.listdir(self.save_data_path):
                os.mkdir(os.path.join(self.save_data_path, "line_data"))

            for keys, values in self.capacity_data.items():
                symbols = ["/", "\\", ":"]
                for symbol in symbols:
                    if symbol in keys:
                        name = keys.replace(symbol, " ")
                    else:
                        name = keys

                np.save(os.path.join(self.save_data_path, "line_data", "{}.npy".format(name)), 
                        values, allow_pickle=True)
            self.L_save_confirm.value = "Data saved {}".format(datetime.now().strftime("%H:%M:%S"))
        self.B_save_data.on_click(on_Scan_confirm_traced_lines) 
        
        self.vbox = wg.VBox([self.B_get_lines, self.B_display_graph, self.VB_trace_lines_box, 
                             self.CB_monochrome, self.O_graph_display,
                             wg.HBox([self.B_save_data, self.L_save_confirm])
                            ])
        
    def _reload_function(self):
        if "axis_limits.npy" in os.listdir(self.save_data_path):
            self.axis_limits = np.load(os.path.join(self.save_data_path, "axis_limits.npy"), allow_pickle=True).item()
            
        if "masked_cropped_img.npy" in os.listdir(self.save_data_path):
            self.masked_img = np.load(os.path.join(self.save_data_path, "masked_cropped_img.npy"), allow_pickle=True)
            self.ax.imshow(self.masked_img,
                           extent=(self.axis_limits["x_min"],
                                   self.axis_limits["x_max"],
                                   self.axis_limits["y_min"],
                                   self.axis_limits["y_max"]))
            self.ax.set_aspect(self.axis_limits["x_axis_extent"]/
                           self.axis_limits["y_axis_extent"])
            
        elif "cropped_image.npy" in os.listdir(self.save_data_path):
            self.cropped_image = np.load(os.path.join(self.save_data_path, "cropped_image.npy"), allow_pickle=True)
            self.ax.imshow(self.cropped_image,
                           extent=(self.axis_limits["x_min"],
                                   self.axis_limits["x_max"],
                                   self.axis_limits["y_min"],
                                   self.axis_limits["y_max"]))
            self.ax.set_aspect(self.axis_limits["x_axis_extent"]/
                           self.axis_limits["y_axis_extent"])
            
########## GUI ###########
class GraphScan(object):
    def __init__(self, figsize=(4, 4)):
        plt.close("all")
        self.LoadReload = _LoadReload()
        self.Axis = _Axis(figsize=figsize)
        self.Lines = _Lines(figsize=figsize)
        self.Mask = _Masks(figsize=figsize)
        self.Scan = _Scan()
        
        def on_LoadReload_confirm(b):
            self._save_path_top = self.LoadReload.save_directory
            self._image_filename = self.LoadReload.RB_raw_image.value
            self._image_name = self.LoadReload.RB_raw_image.value.split(".")[0]
            if self._image_name not in os.listdir(self._save_path_top):
                os.mkdir(os.path.join(self._save_path_top, 
                                      self._image_name))
            
            self.save_data_path = os.path.join(self._save_path_top,
                                               self._image_name)
            self.Axis.save_data_path = self.save_data_path
            self.Axis._image_name = self._image_filename
            
            self.Lines.save_data_path = self.save_data_path
            self.Mask.save_data_path = self.save_data_path
            self.Scan.save_data_path = self.save_data_path
            
            if self.LoadReload._reload == True:
                self.Axis._reload_function()
                self.Lines._reload_function()
                self.Mask._reload_function()
                self.Scan._reload_function()
            
            self.LoadReload.L_confirm_image.value = "Selected image confirmed"
            
        self.LoadReload.B_confirm_image_load.on_click(on_LoadReload_confirm)
        

        self.tab = wg.Tab([self.LoadReload.vbox,
                           self.Axis.vbox,
                           self.Lines.vbox,
                           self.Mask.vbox,
                           self.Scan.vbox])
        for nname, name in enumerate(["Load data", "Axis limits", "Line data", "Setting masks", "Scan graph"]):
            self.tab.set_title(nname, name)
