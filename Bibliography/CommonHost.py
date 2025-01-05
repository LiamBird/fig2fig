class _CommonHost(object):
    def __init__(commonhost_self):
        '''
        Subsection of Host tab for saving descriptors common to all entered host types.
        Individual host samples are defined in _HostSample() accordion defined separately to enable common values to be passed to all entered hosts. 
        
        Updated from version 1: Reformatted to fit on laptop screen better for ease of reference
                                Dropdowns for values with category inputs - hence separate definition of different parameter inputs which were all treated as text in version 1
                                Extra fields for measurands and methods for rarely-reported values
        '''
        
        import ipywidgets as wg
        import numpy as np
        import os
        
        ## 02/12/2024 - added sulfur doping and C/X ratio as radiobuttons
        
        
        ## Common parameters dictionary
        ## Note that some of the displayed labels differ from the dictionary keys for ease of display
        commonhost_self.common_dict = {"Carbon type": wg.Text(description="Carbon type", value=None),
                                        "Carbon source": wg.Text(description="Carbon source", value=None),
                                        "Sulfur loading method": wg.Text(description="Sulfur loading method", value=None),
                                        "Sulfur loading (wt%)": wg.Text(description="Sulfur loading (wt%)", value=None),
                                        "Sulfur loading (mg/ cm2)": wg.Text(description="Areal loading (mg/cm2)", value=None),
                                        "Surface area (cm2/g)": wg.Text(description="Surface area", value=None),
                                        "Pore volume": wg.Text(description="Pore volume", value=None),
                                        "Typical pore widths": wg.Text(description="Typical pore widths", value=None),
                                        "Pore method": wg.Dropdown(description="Pore method", options=["", "BET/ MBET", "DFT", "BJH", "HK"]),
                                        "SSA pore measurand": wg.Dropdown(description="Sample measured", options=["", "Carbon only", "Carbon+sulfur", "Electrode"]),
                                        "Host conductivity": wg.Text(description="Conductivity", value=None),
                                        "Host conductivity units": wg.Text(description="Units", value=None),
                                        "Conductivity method": wg.Dropdown(description="Conductivity method", options=["", "4-point probe", "Pellet", "Other"]),
                                        "Conductivity measurand": wg.Dropdown(description="Sample measured", options=["", "Carbon only", "Carbon+sulfur", "Electrode"]),
                                        "Binder": wg.Text(description="Binder", value=None),
                                        "Binder content (wt%)": wg.Text(description="Content (wt%)", value=None),
                                        "Conductive additive": wg.Text(description="Conductive additive", value=None),
                                        "Conductive additive content (wt%)": wg.Text(description="Content (wt%)", value=None),
                                        "Electrode solvent": wg.Text(description="Electrode solvent"),
                                        "Electrode thickness": wg.Text(description="Electrode thickness"),
                                        "Electrode thickness method": wg.Dropdown(description="Thickness method", options=["", "Micrometer", "Doctor blade", "SEM", "Density"]),
                                      ## DOPANTS AND FUNCTIONAL GROUPS
                                       "Nitrogen content": wg.FloatText(description="Nitrogen"),
                                       "Nitrogen units": wg.RadioButtons(options=["at%", "wt%", "C/N ratio", "Present not stated"]),
                                       "Oxygen content": wg.FloatText(description="Oxygen"),
                                       "Oxygen units": wg.RadioButtons(options=["at%", "wt%", "C/O ratio", "Present not stated"]),
                                       "Sulfur content": wg.FloatText(description="Sulfur"),
                                    "Sulfur units": wg.RadioButtons(options=["at%", "wt%", "C/S ratio", "Present not stated"]),
                                       "Functionalisation method": wg.Dropdown(description="Functionalisation method", options=["", "In precursor", "Surface treatment", "Other"]),
                                       "Other functionalisation method": wg.Text(description="Other functionalisation method"),
                                      }
        
        ## Boolean list of common values
        ## Differentiated by dictionary key, not by label! (for ease of display)
        ## Descriptors that are common to all entered hosts are marked as True
        ## Information is used by 'Update common' button defined in HostTab class to transfer from common fields to sample accordion
        commonhost_self.common_checkbox = dict([(keys, wg.Checkbox(description="", indent=False)) 
                                                for keys, values in commonhost_self.common_dict.items()])
        
        
        
        ## VBox to combine text entry fields/ dropdowns with corresponding Boolean checkboxes
        ## Manually defined so that related fields can be placed in HBoxes next to each other where useful to do so. 
        commonhost_self.common_vbox = wg.VBox([wg.HBox([commonhost_self.common_dict["Carbon type"], commonhost_self.common_checkbox["Carbon type"]]),
                                                        wg.HBox([commonhost_self.common_dict["Carbon source"], commonhost_self.common_checkbox["Carbon source"]]),
                                                        wg.HBox([commonhost_self.common_dict["Sulfur loading method"], commonhost_self.common_checkbox["Sulfur loading method"]]),
                                                        wg.HBox([commonhost_self.common_dict["Sulfur loading (wt%)"], commonhost_self.common_checkbox["Sulfur loading (wt%)"],
                                                                commonhost_self.common_dict["Sulfur loading (mg/ cm2)"], commonhost_self.common_checkbox["Sulfur loading (mg/ cm2)"]]),
                                                        wg.HBox([commonhost_self.common_dict["Surface area (cm2/g)"], commonhost_self.common_checkbox["Surface area (cm2/g)"],
                                                                commonhost_self.common_dict["Pore volume"], commonhost_self.common_checkbox["Pore volume"]]),
                                                        wg.HBox([commonhost_self.common_dict["Typical pore widths"], commonhost_self.common_checkbox["Typical pore widths"]]),
                                                        wg.HBox([commonhost_self.common_dict["SSA pore measurand"], commonhost_self.common_checkbox["SSA pore measurand"],
                                                                commonhost_self.common_dict["Pore method"], commonhost_self.common_checkbox["Pore method"]]),
                                                        wg.HBox([commonhost_self.common_dict["Binder"], commonhost_self.common_checkbox["Binder"],
                                                                commonhost_self.common_dict["Binder content (wt%)"], commonhost_self.common_checkbox["Binder content (wt%)"]]),
                                                        wg.HBox([commonhost_self.common_dict["Conductive additive"], commonhost_self.common_checkbox["Conductive additive"],
                                                                commonhost_self.common_dict["Conductive additive content (wt%)"], commonhost_self.common_checkbox["Conductive additive content (wt%)"]]),
                                                        wg.HBox([commonhost_self.common_dict["Electrode solvent"], commonhost_self.common_checkbox["Electrode solvent"]]),
                                                        wg.HBox([commonhost_self.common_dict["Electrode thickness"], commonhost_self.common_checkbox["Electrode thickness"],
                                                                commonhost_self.common_dict["Electrode thickness method"], commonhost_self.common_checkbox["Electrode thickness method"]]),
                                                        ## ADDITION OF DOPANTS AND FUNCTIONAL GROUPS
                                                        wg.Label(value="Dopants and functional groups"),
                                                        wg.HBox([commonhost_self.common_dict["Nitrogen content"], commonhost_self.common_checkbox["Nitrogen content"], commonhost_self.common_dict["Nitrogen units"], commonhost_self.common_checkbox["Nitrogen units"]]),
                                                        wg.HBox([commonhost_self.common_dict["Oxygen content"],  commonhost_self.common_checkbox["Oxygen content"], commonhost_self.common_dict["Oxygen units"], commonhost_self.common_checkbox["Oxygen content"]]),
                                               wg.HBox([commonhost_self.common_dict["Sulfur content"],  commonhost_self.common_checkbox["Sulfur content"], commonhost_self.common_dict["Sulfur units"], commonhost_self.common_checkbox["Sulfur content"]]),
                                                        wg.HBox([commonhost_self.common_dict["Functionalisation method"], commonhost_self.common_checkbox["Functionalisation method"],
                                                                 commonhost_self.common_dict["Other functionalisation method"], commonhost_self.common_checkbox["Other functionalisation method"]])
                                        ])
        ## Display VBox with header
        ## TODO: format header to be more visually apparent for clarity
        commonhost_self.vbox = wg.VBox([wg.Label("Common values")]+[commonhost_self.common_vbox])
        
        
    ## Reload values function triggered by confirming save location in load/ reload tab
    ## Trigger function defined in outer Bibliography class to enable save path to be passed from load/reload tab to host tab
    def reload_values(commonhost_self, host_data_values):
        import pandas as pd
        import numpy as np
        commonhost_fields = [*commonhost_self.common_dict.keys()]

        for name in commonhost_fields:
            if name in host_data_values.columns:
                try:
                    if len(np.unique(host_data_values[name]))==1:
                        commonhost_self.common_dict[name].value = np.unique(host_data_values[name])[0]
                        commonhost_self.common_checkbox[name].value = True
                except:
                    pass