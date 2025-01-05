class SelectFilesTab(object):
    def __init__(selectfiles_self):
        """
        Tab for specifying whether to reload previous data or create new files
        """
        
        import ipywidgets as wg
        import numpy as np
        import os
        
        from SelectFileGeneralButton import SelectFileGeneralButton
        
        select_previous_files_label = wg.Label(value="Reload previous data")                     
        selectfiles_self.select_previous_files_button = SelectFileGeneralButton(function="askopenfilename", label="csv database")           ## Button to open file explorer for reloading existing dataset
        selectfiles_self.convert_to_csv_button = SelectFileGeneralButton(function="askopenfilename", label="Convert .npy to .csv")
        
        selectfiles_self.select_from_database = wg.Dropdown(options=["No csv selected"])
        selectfiles_self.confirm_dropdown_selection = wg.Button(description="Confirm")
        
        save_new_files_label = wg.Label(value="Create new data")                                 ## Label
        selectfiles_self.save_new_csv_button = SelectFileGeneralButton(function="asksaveasfile")                                    ## Button to open file explorer for creating new file
        
        selectfiles_self.confirm_save_location_button = wg.Button(description="Confirm")                ## Button to confirm selection and set variable name
        selectfiles_self.confirmed_location_label = wg.Label(value="Please select a directory")  ## Instruction
        
        
        ## Arranging widgets for display in 'tab'
        selectfiles_self.vbox = wg.VBox([wg.HBox([select_previous_files_label,
                                                  selectfiles_self.select_previous_files_button,
                                                  selectfiles_self.convert_to_csv_button,
                                                  ]),
                                         wg.HBox([save_new_files_label, selectfiles_self.save_new_csv_button]),
                                         wg.HBox([selectfiles_self.confirm_save_location_button, selectfiles_self.confirmed_location_label]),
                                         wg.HBox([selectfiles_self.select_from_database, selectfiles_self.confirm_dropdown_selection])])
        
    ## Function triggered by clicking 'confirm' button
    ## Trigger function in 'Bibliography' class: uses this function, with save_path string and reload boolean provided by Bibliography
    def reload_values(selectfiles_self, save_path, save_method=None, reload=True):
        import pandas as pd
        import numpy as np
        import os
        
        if reload == True:
            selectfiles_self.confirmed_location_label.value = "Reloading values from {}".format(os.path.split(save_path)[-1])
        else:
            selectfiles_self.confirmed_location_label.value = "Saving values to {}".format(os.path.split(save_path)[-1])
            
        ## For reloading from .csv database:
        if save_method == "from_csv":
            selectfiles_self._database = pd.read_csv(save_path, index_col=0)  
            if "concat_label" not in selectfiles_self._database.columns:
                ## From https://stackoverflow.com/a/39291596
                make_concat_labels = selectfiles_self._database[["First author", "Year", "Optional label"]].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
                concat_labels = np.unique(make_concat_labels)
                
                fixed_df = selectfiles_self._database
                fixed_df["concat_label"] = make_concat_labels
                fixed_df.to_csv(save_path)
                                
            else:
                concat_labels = np.unique(selectfiles_self._database["concat_label"])
            
            selectfiles_self.using_dropdown = True
            selectfiles_self.select_from_database.options = list(concat_labels)
            
            
    def reload_from_csv(selectfiles_self):
        ## Used when second confirm button is clicked
        import pandas as pd
        import numpy as np
        import glob
        import os
        
        if selectfiles_self.using_dropdown == True:
            concat_label_value = selectfiles_self.select_from_database.value
            selected_article_df = selectfiles_self._database.loc[selectfiles_self._database["concat_label"]==concat_label_value]
#             print("reload_from_csv, True for selectfiles_self.using_dropdown, sets concat_label_value as: "+concat_label_value)
            
            if len(selectfiles_self.select_from_database.options) > 1:
                print("reloading from multiple - need to create new save path")
                old_versions = len(glob.glob(os.path.join("{}*.csv".format(concat_label_value))))
                if old_versions == 0:
#                     print("No previous versions exist")
                    selected_article_df.to_csv("{}.csv".format(concat_label_value))
                    setattr(selectfiles_self, "save_path",  "{}.csv".format(concat_label_value))
#                     print("Local save_path set to: "+selectfiles_self.save_path)
                else:
#                     print("Previous version exists - appending to prevent overwrite")

                    selected_article_df.to_csv("{}({}).csv".format(concat_label_value, old_versions+1))
                    setattr(selectfiles_self, "save_path", "{}({}).csv".format(concat_label_value, old_versions+1))
#                     print("Local save_path set to: "+selectfiles_self.save_path)

                            
            setattr(selectfiles_self, "_selected_article_df",  selected_article_df)
        
            
    ## NB if doing conversion, remember to set _selected_article_df as input