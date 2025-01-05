class CharacterisationTab(object):
    def __init__(char_self):
        
        import ipywidgets as wg
        import numpy as np
        import os
        import pandas as pd
        
        
        char_self.physical_methods = ["SEM", "XPS", "Raman", "EDX", "TEM", "FTIR" ]
        char_self.physical_measurands = ["Host", "S/C composite", "Electrode", "In-situ", "Post mortem"]
        
        char_self.physical_grid = dict([(method,
               dict([(measurand, wg.Checkbox(description="", indent=False, layout=wg.Layout(width="50pt"))) for measurand in char_self.physical_measurands]))
               for method in char_self.physical_methods])
        
        
        char_self.ec_methods = {"CV (single rate)": {"CV (single rate)": wg.Checkbox(description="CV (single rate)"), 
                                                     "First cycle": wg.Checkbox(description="1st cycle"),
                                                     "Subsequent cycles": wg.Checkbox(description="Subsequent cycles")},
                                "CV (multi rate)": {"CV (multi rate)": wg.Checkbox(description="CV (multi rate)"), 
                                                    "Linear peak current vs. v1/2":  wg.Checkbox(description="Linear peak current vs. $v^{0.5}$")}, 
                                "EIS": {"EIS": wg.Checkbox(description="EIS data"),
                                        "Rest time": wg.Checkbox(description="Rest period"),
                                        "Min/ Max frequency": wg.Checkbox(description="Frequency range", value=True),
                                        "ECM": wg.Checkbox(description="Equiv. circuit model"),
                                        "KK/ error": wg.Checkbox(description="Kramers Kroenig")}
             }
        
        char_self.phys_hbox = wg.HBox([wg.VBox([wg.Label(meas_name) for meas_name in [""]+char_self.physical_measurands])]+
                                 [wg.VBox([wg.Label(value=method_keys)]+[*method_values.values()])
                                  for method_keys, method_values in char_self.physical_grid.items()])
        
        char_self.ec_vbox = wg.VBox([wg.HBox([char_self.ec_methods["CV (single rate)"]["CV (single rate)"],
                  char_self.ec_methods["CV (single rate)"]["First cycle"],
                  char_self.ec_methods["CV (single rate)"]["Subsequent cycles"]]),
         wg.HBox([char_self.ec_methods["CV (multi rate)"]["CV (multi rate)"], 
                  char_self.ec_methods["CV (multi rate)"]["Linear peak current vs. v1/2"]]),
         wg.VBox([char_self.ec_methods["EIS"]["EIS"],
                  wg.HBox([char_self.ec_methods["EIS"]["Rest time"], char_self.ec_methods["EIS"]["Min/ Max frequency"]]),
                  wg.HBox([char_self.ec_methods["EIS"]["ECM"], char_self.ec_methods["EIS"]["KK/ error"]])])
         ])
        
        char_self.save_button = wg.Button(description="Save")
        char_self.save_confirm_label = wg.Label(value="No values saved this session")
        
        char_self.vbox = wg.VBox([wg.Label("Physical characterisation"),
                                 char_self.phys_hbox,
                                 wg.Label("Electrochemical characterisation"),
                                 char_self.ec_vbox,
                                         wg.HBox([char_self.save_button, char_self.save_confirm_label])
                                        ])
        
    def save_values(char_self, save_path, concat_label):
        import pandas as pd
        
        physical_char_values = dict([(" ".join((method, measurand)), char_self.physical_grid[method][measurand].value) for method in char_self.physical_methods for measurand in char_self.physical_measurands])
        
        ec_char_values = dict([(name_key, dict([(detail_key, detail_value.value) for detail_key, detail_value in name_values.items()])) 
                             for name_key, name_values in char_self.ec_methods.items()])
        
        ec_char_values = {**ec_char_values["CV (single rate)"], **ec_char_values["CV (multi rate)"], **ec_char_values["EIS"]} ## probably imperfect, but so far fixed list of keys!
        char_values_merged = {**physical_char_values, **ec_char_values}
        
        existing_data = pd.read_csv(save_path, index_col=0)
        from copy import deepcopy

        ec_char_data = deepcopy(existing_data)

        for keys, values in char_values_merged.items():
            ec_char_data.loc[ec_char_data["concat_label"] == concat_label, keys] = values
            
        ec_char_data.to_csv(save_path)
        
        from datetime import datetime
        
        now = datetime.now()
        char_self.save_confirm_label.value = "Values saved at: "+now.strftime("%H:%M:%S")
        
    def reload_values(char_self, save_path, concat_label):
        import pandas as pd
        
        existing_data = pd.read_csv(save_path, index_col=0)
        ## For physical characterisation:
        for method_key, method_value in char_self.physical_grid.items():
            for measurand_key, measurand_value in method_value.items():
                if " ".join((method_key, measurand_key)) in existing_data.columns:                  
                    bool_result = existing_data.loc[existing_data["concat_label"]==concat_label][" ".join((method_key, measurand_key))].iloc[0]
                    char_self.physical_grid[method_key][measurand_key].value = bool(bool_result)
                
        ## For electrochemical characterisation:
        for method_key, method_value in char_self.ec_methods.items():
            for measurand_key, measurand_value in method_value.items():
                if measurand_key in existing_data.columns:
                    bool_result = existing_data.loc[existing_data["concat_label"]==concat_label][measurand_key].iloc[0] ## Currently unique measurand keys within inner dicts, may need to change
                    char_self.ec_methods[method_key][measurand_key].value = bool(bool_result)