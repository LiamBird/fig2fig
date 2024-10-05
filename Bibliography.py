import ipywidgets as wg
import numpy as np
import re

from datetime import datetime
import os

from SelectFilesButton import SelectFilesButton

class Bibliography(object):
    def __init__(self):
        self._version = "05.10.2024"#
        self._change_log = ["09.04.2022: Created version",
                            "18.06.2022: Added XRD data tab",
                            "29.06.2022: Added LiSTAR affiliation checkbox",
                            "30.11.2022: Updated with voltage ranges in electrolyte tab  (NB does not reload correctly)",
                            "05.10.2024: Repaired voltage ranges not reloading"]
        
        self._reload = None
        self._label_layout = wg.Layout(width="20%")
        self._entry_layout = wg.Layout(width="20%")
        
### RELOAD OR NEW
        selected_previous_files = SelectFilesButton()
        save_new_files = SelectFilesButton()
        confirm_save_location = wg.Button(description="Confirm")
        confirmed_location_label = wg.Label(value="Please select a directory")
        
        def on_confirm_save_location_click(b):
            if len(selected_previous_files.files) > 0:
                self.save_directory = selected_previous_files.files[0]
                confirmed_location_label.value = self.save_directory
                self._reload = True

                _reload_article_details()
                _reload_host_details()
                _reload_common_host_details()
                _reload_electrolyte_details()
                
            elif len(save_new_files.files) >0:
                self.save_directory = save_new_files.files[0]
                confirmed_location_label.value = self.save_directory
                self._reload = False
            else:
                confirmed_location_label.value = "No directory selected"
                self._reload = None
                
        confirm_save_location.on_click(on_confirm_save_location_click)

        select_files_vbox = wg.VBox([
            wg.HBox([wg.Label(value="Reload previous data", layout=self._label_layout),
                     selected_previous_files]),
            wg.HBox([wg.Label(value="Create new data", layout=self._label_layout),
                     save_new_files]),
            wg.HBox([confirm_save_location, confirmed_location_label])])
        
### ARTICLE DETAILS
        article_fields = ["First author", "Year", "Optional label"]
        reloaded_article_details = dict([(key, '') for key in article_fields])

        def _reload_article_details():
            if self._reload == True:
                reloaded_article_details = np.load(os.path.join(self.save_directory,
                                                                "article_details.npy"),
                                                   allow_pickle=True).item()
                for keys, values in reloaded_article_details.items():
                    if "LiSTAR" not in keys:
                        entry = [entries for names, entries in article_dict.items() if names.value==keys][0]
                        entry.value = values        
                    else:
                        listar_cbox.value = reloaded_article_details["LiSTAR affiliated"]
                                
        article_dict = dict([(wg.Label(value=key, layout=self._label_layout),
                              wg.Text(value=value, layout=self._entry_layout)) for key, value in 
                             reloaded_article_details.items()])
        
        article_save_button = wg.Button(description="Save article details")
        article_save_label = wg.Label(value="Not yet saved")
        
        listar_label = wg.Label(value="LiSTAR affiliated")
        listar_cbox = wg.Checkbox(value=False)
                
        def on_article_save_button_clicked(b):
            article_values = dict([(keys.value, values.value) for keys, values in article_dict.items()])
            article_values.update([("LiSTAR affiliated", listar_cbox.value)])
            np.save(os.path.join(self.save_directory, "article_details.npy"), article_values, allow_pickle=True)
            article_save_label.value = "Data saved {}".format(datetime.now().strftime("%H:%M:%S"))
            
        article_save_button.on_click(on_article_save_button_clicked)
        article_vbox = wg.VBox([wg.HBox([keys, values]) for keys, values in article_dict.items()]+
                               [wg.HBox([listar_label, listar_cbox])]+
                               [wg.HBox([article_save_button, article_save_label])])
            
        
### HOST LABEL
        common_host_labels = ["Carbon type", "Carbon source", "Surface area (cm2/g)", "Pore volume", "Host conductivity", "Host conductivity units", "Sulfur loading (wt%)", "Sulfur loading (mg/ cm2)", "Sulfur loading method", "Typical pore widths", "Conductive additive", "Conductive additive content (wt%)", "Binder", "Binder content (wt%)", "Electrode solvent", "Electrode thickness"]
    ## Added electrode thickness 30/11/2022
        self.reloaded_host_details = {1: dict([(key, '') for key in common_host_labels])}
        
#         self.reloaded_host_details = reloaded_host_details
        def _reload_host_details():
            if self._reload == True:
                self.reloaded_host_details = np.load(os.path.join(self.save_directory, "Saved_host_values.npy"),
                                                allow_pickle=True).item()
                accordion.children = tuple([])
                for idx, values in self.reloaded_host_details.items():
                    host_removal_button = wg.Button(description="Remove host {}".format(idx))
                    host_removal_button.on_click(on_host_removal_button_clicked)
                    
                    host_info = {}
                    for label in ["Host label"]+common_host_labels:
                        try:
                            host_info.update([(wg.Label(label, layout=self._label_layout),
                                               wg.Text(value=self.reloaded_host_details[idx][label],
                                                       layout=self._entry_layout))])
                        except:
                            host_info.update([(wg.Label(label, layout=self._label_layout),
                                               wg.Text(value='',
                                                       layout=self._entry_layout))])
                            
#                     host_info = dict([(wg.Label(label, layout=self._label_layout), 
#                                        wg.Text(value=self.reloaded_host_details[idx][label],
#                                                layout=self._entry_layout)) for label in ["Host label"]+common_host_labels])
                    host_entry = wg.VBox([host_removal_button]+
#                                          [wg.HBox([wg.Label(value="Host label", layout=self._label_layout),
#                                         wg.Text(value=self.reloaded_host_details[idx]["Host label"], layout=self._entry_layout)])]+
                                  [wg.HBox([key, value]) for key, value in host_info.items()])
                    accordion_dict.update([(idx,
                                            host_entry)])

                accordion.children += tuple([values for values in accordion_dict.values() 
#                                              if values not in accordion.children
                                            ])
                for title, (index, _) in zip([*accordion_dict.keys()], enumerate(accordion.children)):
                    accordion.set_title(index, "Host {}".format(title))
                    
                
        def on_host_removal_button_clicked(b):
            host_label = int(re.findall("\d+", b.description)[0])
            accordion_dict.pop(host_label)
            accordion.children = tuple([values for values in accordion_dict.values()])
            for title, (index, _) in zip([*accordion_dict.keys()], enumerate(accordion.children)):
                accordion.set_title(index, "Host {}".format(title))

        idx = 1
        host_removal_button = wg.Button(description="Remove host {}".format(idx))
        host_removal_button.on_click(on_host_removal_button_clicked)
        host_info = dict([(wg.Label(label, layout=self._label_layout), 
                         wg.Text(layout=self._entry_layout)) for label in common_host_labels])
        host_entry = wg.VBox([host_removal_button]+
                              [wg.HBox([wg.Label(value="Host label", layout=self._label_layout),
                                        wg.Text(value="", layout=self._entry_layout)])]+
                              [wg.HBox([key, value]) for key, value in host_info.items()])
        accordion_dict = {1: host_entry}

        def adding_new_host(idx):
            print("Running adding new host {}".format(idx))
            host_removal_button = wg.Button(description="Remove host {}".format(idx))
            host_removal_button.on_click(on_host_removal_button_clicked)
            host_info = dict([(wg.Label(label, layout=self._label_layout), 
                             wg.Text(layout=self._entry_layout)) for label in common_host_labels])
            host_entry = wg.VBox([host_removal_button]+
                                 [wg.HBox([wg.Label(value="Host label", layout=self._label_layout),
                                        wg.Text(value="", layout=self._entry_layout)])]+
                                  [wg.HBox([key, value]) for key, value in host_info.items()])
            accordion_dict.update([(idx,
                                    host_entry)])

            accordion.children += tuple([values for values in accordion_dict.values() if values not in accordion.children])

            for title, (index, _) in zip([*accordion_dict.keys()], enumerate(accordion.children)):
                accordion.set_title(index, "Host {}".format(title))

                
        
        common_host_values = dict([(label, wg.Text(layout=self._entry_layout)) for label in common_host_labels])
        common_host_checkboxes = dict([(label, 
                                          wg.Checkbox(description="Common", indent=False)) for label in common_host_labels])
        common_cbox = wg.VBox([wg.HBox([wg.Label(value=label, layout=self._label_layout),
                          common_host_values[label],
                          common_host_checkboxes[label]]) for label in common_host_labels])
        
        self.common_cbox = common_cbox
        
        def _reload_common_host_details():
            if self._reload == True:
                reload_common_bool = np.load(os.path.join(self.save_directory, "Saved_common_bools_values.npy"),
                                             allow_pickle=True).item()
                reload_common_names = np.load(os.path.join(self.save_directory, "Saved_common_names_values.npy"),
                                            allow_pickle=True).item()
                
                for name in reload_common_bool.keys():
                    entry = [label.children[1] for label in common_cbox.children if label.children[0].value==name]
                    checkbox = [label.children[2] for label in common_cbox.children if label.children[0].value==name]
                    if len(entry) > 0:
                        entry[0].value = reload_common_names[name]
                        checkbox[0].value = reload_common_bool[name]          
                    else:
                        print(name)
                        
        common_update = wg.Button(description="Update common")
        add_new_host = wg.Button(description="Add new host")
        save_values = wg.Button(description="Save")
        save_confirm = wg.Label(value="No saved data")

        def on_add_new_host_clicked(b):
            try:
                current_acc_idx = np.max([*accordion_dict.keys()])
            except:
                current_acc_idx = 0

            adding_new_host(current_acc_idx+1)

        def on_common_update_clicked(b):
            common_names = [key for key, value in common_host_checkboxes.items() if value.value==True]
            for host_key, host_values in accordion_dict.items():
                for child in host_values.children[1:]: ## Starts at 1 because idx=0 is remove button
                    if child.children[0].value in common_names:
                        child.children[1].value = common_host_values[child.children[0].value].value
                    elif child.children[0].value != "Host label":
                        child.children[1].value = ""

        def on_save_values_clicked(b):
            accordion_values = {}

            for host_key, host_values in accordion_dict.items():
                accordion_values.update([(host_key, 
                                         {})])
                for entry in host_values.children[1:]:
                    accordion_values[host_key].update([(entry.children[0].value, entry.children[1].value)])

            common_names_values = {}
            common_bools_values = {}

            for child in common_cbox.children:
                common_bools_values.update([(child.children[0].value,
                                             child.children[2].value)])
                if child.children[2].value == True:
                    common_names_values.update([(child.children[0].value,
                                                 child.children[1].value)])
                else:
                    common_names_values.update([(child.children[0].value,
                                                 '')])

            np.save(os.path.join(self.save_directory, "Saved_host_values.npy"), accordion_values, allow_pickle=True)
            np.save(os.path.join(self.save_directory, "Saved_common_names_values.npy"), common_names_values, allow_pickle=True)
            np.save(os.path.join(self.save_directory, "Saved_common_bools_values.npy"), common_bools_values, allow_pickle=True)

            save_confirm.value = "Data saved {}".format(datetime.now().strftime("%H:%M:%S"))



        add_new_host.on_click(on_add_new_host_clicked)
        common_update.on_click(on_common_update_clicked)
        save_values.on_click(on_save_values_clicked)

        common = wg.VBox([common_cbox,
                          common_update,
                          add_new_host,
                          wg.HBox([save_values, save_confirm])])



        accordion = wg.Accordion([value for value in accordion_dict.values()])
        for title, (index, _) in zip([*accordion_dict.keys()], enumerate(accordion.children)):
            accordion.set_title(index, "Host {}".format(title))

        host_vbox = wg.VBox([common]+
                       [accordion])

### Electrolyte
#         default_electrolyte_label = wg.Label(value="Default electrolyte: 1:1 v/v DOL:DME with 1M LiTFSI")
#         default_electrolyte_checkbox = wg.Checkbox(description="Default electrolyte", value=True, inset=False)

        LiNO3_content_label = wg.Label(value="LiNO3 content", layout=wg.Layout(width="20%"))
        salt_type_label = wg.Label("Electrolyte salt", layout=wg.Layout(width="20%"))
        electrolyte_solvent_label = wg.Label("Electrolyte solvent", layout=wg.Layout(width="20%"))
        salt_content_label = wg.Label("Salt content", layout=wg.Layout(width="20%"))
    
        LiNO3_content_entry = wg.FloatText(layout=wg.Layout(width="10%"))
        salt_type_entry = wg.Text(value="LiTFSI", layout=wg.Layout(width="10%"))
        salt_content_entry = wg.FloatText(value=1, layout=wg.Layout(width="10%"))
        
        LiNO3_wtpc = wg.Checkbox(description="wt%", value=True, inset=False, layout=wg.Layout(width="15%"))
        LiNO3_mol = wg.Checkbox(description="M", value=False, inset=False, layout=wg.Layout(width="15%"))

        salt_wtpc = wg.Checkbox(description="wt%", value=False, inset=False, layout=wg.Layout(width="15%"))
        salt_mol = wg.Checkbox(description="M", value=True, inset=False, layout=wg.Layout(width="15%"))
        
        electrolyte_solvent_entry = wg.Text(value="1:1 DOL DME")
        electrolyte_save_confirm = wg.Label(value="No saved values")        
        
        separator_type_label = wg.Label(value="Separator type", layout=wg.Layout(width="20%"))
        separator_entry = wg.Text(value="Celgard 2400")
        
        ES_quantity_label = wg.Label("Electrolyte volume (uL)", layout=wg.Layout(width="20%"))
        ES_quantity_entry = wg.FloatText(value=None, layout=wg.Layout(width="10%"))
        ES_ratio_label = wg.Label("E/S ratio (uL/g)", layout=wg.Layout(width="20%"))
        ES_ratio_entry = wg.FloatText(value=None, layout=wg.Layout(width="10%"))
        
        cell_type_label = wg.Label("Cell type", layout=wg.Layout(width="20%"))
        cell_type_entry = wg.Text(value="CR2032")
        
        ## Added 30/11/2022
        minimum_voltage_label = wg.Label("Minimum voltage", layout=wg.Layout(width="20%"))
        minimum_voltage_value = wg.FloatText(value=None, layout=wg.Layout(width="10%"))
        maximum_voltage_label = wg.Label("Maximum voltage", layout=wg.Layout(width="20%"))
        maximum_voltage_value = wg.FloatText(value=None, layout=wg.Layout(width="10%"))                            
        
        electrolyte_save = wg.Button(description="Save")
        def on_electrolyte_save_clicked(b):
            electrolyte_dict = dict([(child.children[0].value, child.children[1].value) for child in 
                                     self.electrolyte_vbox.children[:-1]])
            salt_units = [self.electrolyte_vbox.children[1].children[i].description for i in [2, 3] if self.electrolyte_vbox.children[1].children[i].value==True][0]
            LiNO3_units = [self.electrolyte_vbox.children[2].children[i].description for i in [2, 3] if self.electrolyte_vbox.children[2].children[i].value==True][0]
            electrolyte_dict.update([("LiNO3_units", LiNO3_units)])
            electrolyte_dict.update([("salt_units", salt_units)])
            
            np.save(os.path.join(self.save_directory, 
                                 "electrolyte_details.npy"),
                   electrolyte_dict, allow_pickle=True)
            
            electrolyte_save_confirm.value = "Data saved {}".format(datetime.now().strftime("%H:%M:%S"))

            
        electrolyte_save.on_click(on_electrolyte_save_clicked)
            
        def _reload_electrolyte_details():
            reloaded_electrolyte_values = np.load(os.path.join(self.save_directory,
                                                               "electrolyte_details.npy"), allow_pickle=True).item()
            salt_type_entry.value = reloaded_electrolyte_values["Electrolyte salt"]
            salt_content_entry.value = reloaded_electrolyte_values["Salt content"]
            
            LiNO3_content_entry.value = reloaded_electrolyte_values["LiNO3 content"]
            
            electrolyte_solvent_entry.value = reloaded_electrolyte_values["Electrolyte solvent"]
            
            if reloaded_electrolyte_values["LiNO3_units"] == "M":
                LiNO3_wtpc.value = False
                LiNO3_mol.value = True
            else:
                LiNO3_wtpc.value = True
                LiNO3_mol.value = False
                
            if reloaded_electrolyte_values["salt_units"] == "M":
                salt_wtpc.value = False
                salt_mol.value = True
            else:
                salt_wtpc.value = True
                salt_mol.value = False   
                
            ## Fixed 05.10.2024
            minimum_voltage_value.value = reloaded_electrolyte_values["Minimum voltage"]
            maximum_voltage_value.value = reloaded_electrolyte_values["Maximum voltage"]
                
            if "Separator type" in reloaded_electrolyte_values.keys(): ## Later entries
                separator_entry.value = reloaded_electrolyte_values["Separator type"]
                ES_quantity_entry.value = reloaded_electrolyte_values["Electrolyte volume (uL)"]
                ES_ratio_entry.value = reloaded_electrolyte_values["E/S ratio (uL/g)"]
                try:
                    cell_type_entry.value = reloaded_electrolyte_values["Cell type"]
                except:
                    pass

        electrolyte_vbox = wg.VBox([
            wg.HBox([salt_type_label, salt_type_entry]),
            wg.HBox([salt_content_label, salt_content_entry, salt_wtpc, salt_mol]),
            wg.HBox([LiNO3_content_label, LiNO3_content_entry, LiNO3_wtpc, LiNO3_mol]),
            wg.HBox([electrolyte_solvent_label, electrolyte_solvent_entry]),
            wg.HBox([ES_quantity_label, ES_quantity_entry]),
            wg.HBox([ES_ratio_label, ES_ratio_entry]),
            wg.HBox([separator_type_label, separator_entry]),
            wg.HBox([cell_type_label, cell_type_entry]),
            wg.HBox([minimum_voltage_label, minimum_voltage_value]), ## added
            wg.HBox([maximum_voltage_label, maximum_voltage_value]), ## added
            wg.HBox([electrolyte_save, electrolyte_save_confirm])            
        ])
        self.electrolyte_vbox = electrolyte_vbox
        
### XRD data
        XRD_load_host = wg.Button(description="Load host names")
        XRD_save_values = wg.Button(description="Confirm values")
        XRD_save_confirm = wg.Label(value="No values saved this session")
        S_XRD_dict = {}

        def on_available_S_XRD_cbox(b):
            if b["new"] == True:
                S_XRD_dict[b["owner"].description].children[-1].set_trait("disabled", False)
            elif b["new"] == False:
                S_XRD_dict[b["owner"].description].children[-1].set_trait("disabled", True)

        def on_XRD_save_values(b):
            XRD_data = {}

            for keys, values in S_XRD_dict.items():
                if values.children[0].value == True and values.children[-1].value == True and values.children[-1].disabled == False:
                    XRD_data.update([(keys, True)])
                elif values.children[0].value == True and values.children[-1].value == False and values.children[-1].disabled == False:
                    XRD_data.update([(keys, False)])
                elif values.children[0].value == False:
                    XRD_data.update([(keys, None)])
                np.save(os.path.join(self.save_directory, 'Sulfur_XRD_data.npy'), 
                        XRD_data, allow_pickle=True)
            XRD_save_confirm.value = "Data saved {}".format(datetime.now().strftime("%H:%M:%S"))
        XRD_save_values.on_click(on_XRD_save_values)

        def on_XRD_host_load(b):   
            host_details = np.load(os.path.join(self.save_directory, 'Saved_host_values.npy'), allow_pickle=True).item()
            host_labels = [value["Host label"] for value in host_details.values()]

            if "Sulfur_XRD_data.npy" in os.listdir(os.path.join(self.save_directory)):
                loaded_XRD_data = np.load(os.path.join(self.save_directory, "Sulfur_XRD_data.npy"), allow_pickle=True).item()
            else:
                loaded_XRD_data = dict([(name, None) for name in host_labels])
            
            for label in host_labels:
                if label in loaded_XRD_data.keys():
                    if loaded_XRD_data[label] == True:
                        available = True
                        disabled = False
                        present = True
                    elif loaded_XRD_data[label] == False:
                        available = True
                        disabled = False
                        present = False
                    else:
                        available = False
                        disabled = True
                        present = False

                available_S_XRD_cbox = wg.Checkbox(description=label, value=available)
                present_S_XRD_cbox = wg.Checkbox(description="Sulfur present", disabled=disabled, value=present)

                S_XRD = wg.HBox([available_S_XRD_cbox,
                                 present_S_XRD_cbox
                                 ])

                S_XRD_dict.update([(label, S_XRD)])

            for keys, values in S_XRD_dict.items():
                values.children[0].observe(on_available_S_XRD_cbox, names="value")

            XRD_vbox.children = tuple(list(XRD_vbox.children)+list(S_XRD_dict.values()))

        XRD_load_host.on_click(on_XRD_host_load)

        XRD_vbox = wg.VBox([wg.HBox([XRD_load_host, XRD_save_values, XRD_save_confirm])])


### TAB
        self.tab = wg.Tab([select_files_vbox,
                           article_vbox,
                           host_vbox,
                           electrolyte_vbox,
                           XRD_vbox])
        tab_names = ["Save and reload", "Article details", "Host", "Electrochemistry", "Sulfur XRD"] ## renamed electrochemistry tab from electolyte 05.10.2024
        for n, names in enumerate(tab_names):
            self.tab.set_title(n, names)
