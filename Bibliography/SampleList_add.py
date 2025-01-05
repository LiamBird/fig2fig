## General addition of host version

class _SampleList_add(object):
    def __init__(sample_self, test=False):
        
        from CommonHost import _CommonHost
        from HostSample import _HostSample
        
        import ipywidgets as wg
        import numpy as np
        
        ## Initialise with 1 Host:
        sample_self.sample_list = {"Host 1": _HostSample(test=test)}
        
        add_host_button = wg.Button(description="Add host")
        sample_self.accordion_dict = {"Host 1": wg.VBox([sample_self.sample_list["Host 1"].vbox])}
        
        sample_self.accordion = wg.Accordion([*sample_self.accordion_dict.values()])
        sample_self.rename_accordion()
        
        sample_self.remove_button_dict = {"Host 1": wg.VBox([])}
        
    def add_new_host_general(sample_self, reload_values=None):
        ## Check maximum name:
        import re
        import numpy as np
        import ipywidgets as wg
        from HostSample import _HostSample

        
        last_host = np.max([int(re.findall("\d+", keys)[0]) for keys in sample_self.sample_list.keys()])
        
        ## Add a new Host object to the sample_dict
        sample_self.sample_list.update([("Host {}".format(last_host+1), _HostSample())])
        sample_self.remove_button_dict.update([("Host {}".format(last_host+1), 
                                                wg.Button(description="Remove host {}".format(last_host+1)))])
                
        def on_remove_button_clicked(b):
            sample_self.remove_host_button(b)
        
        sample_self.remove_button_dict["Host {}".format(last_host+1)].on_click(on_remove_button_clicked)
        
        ## If reloading, add the new values, otherwise skip
        if type(reload_values) != type(None): 
            sample_self.sample_list["Host {}".format(last_host+1)].reload_values(reload_values, XRD_data=None)
            
        else:
            sample_self.accordion_dict = dict([(list_keys, wg.VBox([sample_self.remove_button_dict[list_keys],
                                                                        sample_self.sample_list[list_keys].vbox])) 
                                                   for list_keys, list_values in sample_self.sample_list.items()])
            
           
        sample_self.accordion.children = [*sample_self.accordion_dict.values()] ## Update children rather than accordion to update in place
        sample_self.rename_accordion()
        
        
    def rename_accordion(sample_self):
        for title, (index, _) in zip([*sample_self.accordion_dict.keys()], enumerate(sample_self.accordion.children)):
            sample_self.accordion.set_title(index, "{}".format(title))
            
    def remove_host_button(sample_self, b):
        import re
        host_id = int(re.findall("\d+", b.description)[0])
        host_name = "Host {}".format(host_id)
        if host_name in sample_self.sample_list.keys():
            sample_self.sample_list.pop(host_name)
            sample_self.accordion_dict.pop(host_name)
                
        sample_self.accordion.children = [*sample_self.accordion_dict.values()] ## Update children rather than accordion to update in place
        sample_self.rename_accordion()
        
    def reload_values(sample_self, reload_values, XRD_data):
#         print("reload_clicked")
        import ipywidgets as wg

        for keys, values in reload_values.items():
            if keys in sample_self.sample_list.keys():
                sample_self.sample_list[keys].reload_values(values, XRD_data)
            else:
                sample_self.add_new_host_general(reload_values=values)
                sample_self.accordion_dict = dict([(list_keys, wg.VBox([sample_self.remove_button_dict[list_keys],
                                                                        sample_self.sample_list[list_keys].vbox])) 
                                                   for list_keys, list_values in sample_self.sample_list.items()])

        sample_self.accordion.children = [*sample_self.accordion_dict.values()] ## Update children rather than accordion to update in place
        sample_self.rename_accordion()
        
    def save_values(sample_self, save_path, concat_label):
        import numpy as np
        import os
        import pandas as pd
        
#         import warnings
#         warnings.filterwarnings(action="ignore", message="SettingWithCopyWarning") ## TODO work out why the copy warning appears and fix properly!

        existing_data = pd.read_csv(save_path, index_col=0)
        host_data = existing_data.copy()
        sample_self._host_data = host_data
        
        host_values_arr = np.array([[value.value for value in sample_values.sample_dict.values()] for sample_key, sample_values in sample_self.sample_list.items()]).T
        host_keys = [*[*sample_self.sample_list.values()][0].sample_dict.keys()]
        host_dict = dict([(key, list(host_values_arr[nkey])) for nkey, key in enumerate(host_keys)])
               
        def cont_keyword(df, keyword, column="Host label", case=True):
            return df[df[column].astype(str).str.contains(keyword, case)]

        for sample_keys, sample_values in sample_self.sample_list.items():
            host_label = sample_values.sample_dict["Host label"].value
            
            if host_keys[0] not in host_data.columns: ## If this is the first host to be entered and new columns need to be made:
                print("first entry to be added")
                for host_label, host_value in host_dict.items():
                    for idx in host_data.index:
                        
                        host_data.loc[idx, host_label] = host_value[idx]
#                         print(idx, host_value[idx])
            else:
                current_entry = cont_keyword(host_data, host_label)

                if len(current_entry) == 0: ## If the entry is not in the dataframe:
                    current_length = max(host_data.index)
                    new_idx = current_length+1

                    for column in host_data.columns:
                        if column not in host_keys:
                            host_data.loc[new_idx, column] = host_data.loc[current_length, column]
                        else:
                            host_data.loc[new_idx, column] = sample_values.sample_dict[column].value

                if len(cont_keyword(host_data, host_label)) == 1: ## If the entry is in the dataframe:
                    for column in host_keys:
                        host_data.loc[current_entry.index, column] = sample_values.sample_dict[column].value

        for name in host_data["Host label"]:
#             print(name)
            if name not in host_dict["Host label"]: ## Checks dataframe for extraneous names and removes them
#                 print(host_dict["Host label"])
                index_to_drop = host_data.loc[host_data["Host label"]==name].index[0]
                host_data.drop(index_to_drop, inplace=True)

        host_data.reset_index(drop=True, inplace=True)
        
        host_data.to_csv(save_path)