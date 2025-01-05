class _HostSample(object):
    def __init__(host_self, test=False):
        '''
        Subsection of Host tab for individual entries
        '''
        import ipywidgets as wg
        import numpy as np
        import os

        ## 05/01/2024 Added checkboxes and details boxes for sulfur loading methods
        
        host_self.sample_dict = {"Host label": wg.Text(description="Host label", value=None),
                                    "Carbon type": wg.Text(description="Carbon type", value=None),
                                    "Carbon source": wg.Text(description="Carbon source", value=None),
                                    "Sulfur loading method": wg.Text(description="Sulfur loading method", value=None),
                                     "Sulfur method thermal checkbox": wg.Checkbox(description="Thermal"), ## New sulfur loading methods start
                                    "Sulfur method thermal details": wg.Text(value="155 degC 12 hours"),
                                    "Sulfur method chemical checkbox": wg.Checkbox(description="Chemical "),
                                    "Sulfur method chemical details": wg.Text(value="Na2S2O3"),
                                    "Sulfur method solution checkbox": wg.Checkbox(description="Solution"),
                                    "Sulfur method solution details": wg.Text(value="CS2"),  ## New sulfur loading methods end
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
                                    "Electrode thickness method": wg.Dropdown(description="Thickness method", 
                                                                              options=["", "Micrometer", "Doctor blade", "SEM", "Density"]),
                                    "Sulfur present in XRD": wg.RadioButtons(description="S$_{8}$ peaks visible in XRD?",
                                                                             options=["No data", "True", "False"],
                                                                             value="No data"),
                                    "Nitrogen content": wg.FloatText(description="Nitrogen"),
                                    "Nitrogen units": wg.RadioButtons(options=["at%", "wt%", "C/N ratio", "Present not stated"]),
                                    "Oxygen content": wg.FloatText(description="Oxygen"),
                                    "Oxygen units": wg.RadioButtons(options=["at%", "wt%", "C/O ratio", "Present not stated"]),
                                    "Sulfur content": wg.FloatText(description="Sulfur"),
                                    "Sulfur units": wg.RadioButtons(options=["at%", "wt%", "C/S ratio", "Present not stated"]),
                                    "Functionalisation method": wg.Dropdown(description="Functionalisation method", 
                                                                            options=["", "In precursor", "Surface treatment", "Other"]),
                                    "Other functionalisation method": wg.Text(description="Other functionalisation method"),}
                
        host_self.vbox = wg.VBox([host_self.sample_dict["Host label"],
                                    host_self.sample_dict["Carbon type"],
                                    host_self.sample_dict["Carbon source"],
                                    wg.Label(value="Sulfur loading methods"), ## New sulfur loading methods start
                                    wg.HBox([host_self.sample_dict["Sulfur method thermal checkbox"],
                                             host_self.sample_dict["Sulfur method thermal details"]]),
                                   wg.HBox([host_self.sample_dict["Sulfur method chemical checkbox"],
                                             host_self.sample_dict["Sulfur method chemical details"]]),
                                   wg.HBox([host_self.sample_dict["Sulfur method solution checkbox"],
                                             host_self.sample_dict["Sulfur method solution details"]]),                                 
                                            host_self.sample_dict["Sulfur loading method"], ## New sulfur loading methods end
                                    wg.HBox([host_self.sample_dict["Sulfur loading (wt%)"],
                                                host_self.sample_dict["Sulfur loading (mg/ cm2)"]]),
                                    wg.HBox([host_self.sample_dict["Surface area (cm2/g)"],
                                                host_self.sample_dict["Pore volume"]]),
                                    wg.HBox([host_self.sample_dict["Typical pore widths"]]),
                                    wg.HBox([host_self.sample_dict["SSA pore measurand"],
                                                host_self.sample_dict["Pore method"]]),
                                    wg.HBox([host_self.sample_dict["Binder"],
                                                host_self.sample_dict["Binder content (wt%)"]]),
                                    wg.HBox([host_self.sample_dict["Conductive additive"],
                                                host_self.sample_dict["Conductive additive content (wt%)"]]),
                                                host_self.sample_dict["Electrode solvent"],
                                    wg.HBox([host_self.sample_dict["Electrode thickness"],
                                                host_self.sample_dict["Electrode thickness method"]]),
                                    wg.HBox([host_self.sample_dict["Sulfur present in XRD"]]),
                                    wg.Label(value="Functional groups"),
                                    wg.HBox([host_self.sample_dict["Nitrogen content"], host_self.sample_dict["Nitrogen units"]]),
                                    wg.HBox([host_self.sample_dict["Oxygen content"], host_self.sample_dict["Oxygen units"]]),
                                    wg.HBox([host_self.sample_dict["Sulfur content"], host_self.sample_dict["Sulfur units"]]),
                                    wg.HBox([host_self.sample_dict["Functionalisation method"],
                                             host_self.sample_dict["Other functionalisation method"]])
                                        ])
        if test == True:
            host_self.sample_dict["Host label"].value = "Things"
        
        
    def reload_values(host_self, host_data_values, XRD_data):
        import ipywidgets as wg
        import numpy as np
        
        host_self.host_data_values = host_data_values
        
        
        for keys, values in host_self.sample_dict.items():
#             if type(values.value) == type(None):
#                 print(keys)
            try:
                if keys in host_data_values.keys():
                    if type(values.value) != type(None):
                        values.value = str(host_data_values[keys])
            except:
                pass
                
        if type(XRD_data) != type(None):
            print("Received XRD data OK")
            host_key = str(host_self.sample_dict["Host label"].value)
            if host_self.sample_dict["Host label"].value in XRD_data.keys():
                if type(XRD_data[host_key]) == type(None):
                    host_self.sample_dict["Sulfur present in XRD"].value = "No data"
                elif XRD_data[host_key] == True:
                    host_self.sample_dict["Sulfur present in XRD"].value = "True"
                else:
                    host_self.sample_dict["Sulfur present in XRD"].value = "False"                 
