class HostTab(object):
    def __init__(hosttab_self):
        
        from CommonHost import _CommonHost
        from HostSample import _HostSample
        from SampleList_add import _SampleList_add
        
        import ipywidgets as wg
        import numpy as np
        import os
        
        hosttab_self.commonhost_self = _CommonHost()
        hosttab_self.sample_self = _SampleList_add()
        
        hosttab_self.save_button = wg.Button(description="Save")        
        hosttab_self.update_common_button = wg.Button(description="Update common")
        hosttab_self.add_new_host_button = wg.Button(description="Add new host")
        hosttab_self.save_confirm_label = wg.Label(value="No new values saved this session")
        
        def on_update_common_clicked(b):
            for sample_keys, sample_values in hosttab_self.sample_self.sample_list.items():
                for host_keys, host_values in sample_values.sample_dict.items():
                    if host_keys in hosttab_self.commonhost_self.common_checkbox.keys():
                        if hosttab_self.commonhost_self.common_checkbox[host_keys].value == True:
                            host_values.value = hosttab_self.commonhost_self.common_dict[host_keys].value
                            
        def on_add_new_host_clicked(b):
            hosttab_self.sample_self.add_new_host_general(reload_values=None)

        hosttab_self.update_common_button.on_click(on_update_common_clicked)
        hosttab_self.add_new_host_button.on_click(on_add_new_host_clicked)
        
        hosttab_self.vbox = wg.VBox([hosttab_self.commonhost_self.vbox,
                                     wg.HBox([hosttab_self.save_button, hosttab_self.save_confirm_label]),
                                     hosttab_self.add_new_host_button,
                                     hosttab_self.update_common_button,
                                     hosttab_self.sample_self.accordion])
        
    def reload_values(hosttab_self, selected_article_df, save_path):
        host_details_fields = list(hosttab_self.sample_self.sample_list["Host 1"].sample_dict.keys())
              
        
        ## Making container
        host_details_from_csv = dict([("Host {}".format(n+1), 
                  dict([(field, None) for field in host_details_fields])) for n in range(len(selected_article_df))])
        
        hosttab_self.commonhost_self.reload_values(selected_article_df)

        
        for n in range(len(selected_article_df)):
            for field in host_details_fields:
                if field in selected_article_df.columns: ## Some extra fields in new fig2fig version
                    host_details_from_csv["Host {}".format(n+1)][field] = selected_article_df[field].iloc[n]
                
            hosttab_self.sample_self.reload_values(reload_values=host_details_from_csv, XRD_data=None)

    def save_values(hosttab_self):
        from datetime import datetime
        save_time = datetime.now()        
        # Actual save function performed elsewhere
        hosttab_self.save_confirm_label.value = "Values saved at: "+save_time.strftime("%H:%M:%S")
        