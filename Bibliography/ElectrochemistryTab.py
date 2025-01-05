class ElectrochemistryTab(object):
    def __init__(electrochem_self):
        import ipywidgets as wg
        
        electrochem_self.entries = {"Electrolyte salt": wg.Text(description="Electrolyte salt", value="LiTFSI"),
                                    "Salt content": wg.FloatText(description="Salt content", value=1),
                                    "salt_units": wg.RadioButtons(options=["M", "wt%"], value="M"),
                                    "LiNO3 content": wg.FloatText(description="LiNO$_{3}$ content"),
                                    "LiNO3_units": wg.RadioButtons(options=["M", "wt%"], value="M"),
                                    "Electrolyte solvent": wg.Text(description="Electrolyte solvent", value="1:1 DOL DME"),
                                    "Electrolyte volume (uL)": wg.FloatText(description="Electrolyte volume $\mu$L"),
                                    "E/S ratio (uL/g)": wg.FloatText(description="E/S ratio ($\mu$L/g)"),
                                    "Separator type": wg.Text(description="Separator type"),
                                    "Cell type": wg.Text(description="Cell type"),
                                    "Maximum voltage": wg.FloatText(description="Maximum voltage"),
                                    "Minimum voltage": wg.FloatText(description="Minimum voltage"),
                                    "Common voltage range": wg.Checkbox(description="Same voltage range for all rates?",
                                                                        value=True)}
        
        electrochem_self.save_button = wg.Button(description="Save")
        electrochem_self.save_label = wg.Label(value="No values saved yet")
        
        electrochem_self.vbox = wg.VBox([electrochem_self.entries["Electrolyte salt"],
                                         wg.HBox([electrochem_self.entries["Salt content"], electrochem_self.entries["salt_units"]]),
                                         wg.HBox([electrochem_self.entries["LiNO3 content"], electrochem_self.entries["LiNO3_units"]]),
                                         electrochem_self.entries["Electrolyte solvent"],
                                         wg.HBox([electrochem_self.entries["Electrolyte volume (uL)"],
                                                  electrochem_self.entries["E/S ratio (uL/g)"]]),
                                         electrochem_self.entries["Separator type"],
                                         electrochem_self.entries["Cell type"],
                                         electrochem_self.entries["Common voltage range"],
                                         wg.HBox([electrochem_self.entries["Maximum voltage"],
                                                  electrochem_self.entries["Minimum voltage"]]),
                                         wg.HBox([electrochem_self.save_button, electrochem_self.save_label])])
        
    def save_values(electrochem_self, save_path, concat_label):
        from datetime import datetime
        import pandas as pd
        
        electrochem_values = dict([(keys, values.value) for keys, values in electrochem_self.entries.items()])

        existing_data = pd.read_csv(save_path, index_col=0)
        electrochem_data = existing_data.copy()
        
        for keys, values in electrochem_values.items(): 
            electrochem_data.loc[electrochem_data["concat_label"]==concat_label, keys] = values
            
        electrochem_data.to_csv(save_path)
                
        now = datetime.now()        
        electrochem_self.save_label.value = "Values saved at: "+now.strftime("%H:%M:%S")
        
    def reload_values(electrochem_self, save_path, concat_label):
        import pandas as pd

        existing_data = pd.read_csv(save_path, index_col=0)

        for keys, values in electrochem_self.entries.items():
            if keys in existing_data.columns:
                ## TODO - tidy up if possible - unclear why this is so picky!!
                if type(electrochem_self.entries[keys].value) == str:
                    electrochem_self.entries[keys].value = str(existing_data.loc[existing_data["concat_label"]==concat_label][keys].iloc[0])
                elif type(electrochem_self.entries[keys].value) == float:
                    electrochem_self.entries[keys].value = float(existing_data.loc[existing_data["concat_label"]==concat_label][keys].iloc[0])
                elif type(electrochem_self.entries[keys].value) == bool:
                    electrochem_self.entries[keys].value = bool(existing_data.loc[existing_data["concat_label"]==concat_label][keys].iloc[0])       