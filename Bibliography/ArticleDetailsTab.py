class ArticleDetailsTab(object):
    def __init__(article_self):
        import ipywidgets as wg
        import numpy as np
        import os
        
        article_self.fields = ["First author", "Year", "Optional label"]
        article_self.entries = {"First author": wg.Text(description="First author", value=""),
                               "Year": wg.IntText(description="Year"),
                                "Optional label": wg.Text(description="Optional label", value=""),
                                "doi": wg.Text(description="doi", value="")}
        
#         article_self.entries = dict([(keys, wg.Text(description=keys, value="")) for keys in article_self.fields])
        article_self.LiSTAR = wg.Checkbox(description="LiSTAR affiliated?")                   ## Originally aimed to track whether LiSTAR results are consistent with SOTA - actually rarely-used
        
        article_self.save_button = wg.Button(description="Save")                             ## Button - TODO set save function!
        article_self.save_label = wg.Label(value="No values saved this session")             ## Label to confirm whether values saved and how recently
        

                
        article_self.vbox = wg.VBox([*article_self.entries.values()]+          ## Text entry boxes for each field
                                    [article_self.LiSTAR]+                                   ## LiSTAR checkbox
                                    [wg.HBox([article_self.save_button, article_self.save_label])])    ## Save button and confirmation label
        
    ## Reload values button triggered by 'confirm' button in selectfiles tab
    ## Function set in outer Bibliography class
    def reload_values(article_self, selected_article_df, save_path, data_from_csv=True):
        import os
        
        if data_from_csv == True:
            article_details_fields = article_self.fields+["doi"]
            reloaded_values = dict([(name, selected_article_df[name].iloc[0]) 
                                             for name in article_self.entries.keys() if name in selected_article_df.columns])
            for keys, values in reloaded_values.items():    ## Appears to do the same thing twice? TODO: Check whether redundant   
                if "LiSTAR_affiliated" in keys:  ## Sets boolean checkbox value (separate from dictionary with author, year, and optional label)
                    article_self.LiSTAR.value = reloaded_values["LiSTAR_affiliated"]
                else:
                    if keys != "Year":
                        if keys in reloaded_values.keys():
                            article_self.entries[keys].value = str(values)
                    else:
                        article_self.entries["Year"].value = int(values)
            
            article_self.save_label.value = "Reloaded values from {}".format(os.path.split(save_path)[-1]) ## Updates confirmation value
        else:
            print("Article details not yet saved")
            
    def save_values(article_self, save_path="test"):
        from datetime import datetime
        import pandas as pd
        import os
        
        concat_label = article_self._get_concat_label()
        article_details = dict([(keys, values.value) for keys, values in article_self.entries.items()])
        article_details.update([("concat_label", concat_label)])
        
        article_details.update([("LiSTAR_affiliated", article_self.LiSTAR.value)])
        
        
        ## Testing only
        if save_path == "test":
            save_path = "test_data.csv"
        setattr(article_self, "_output", article_details)
        
        df_to_save = pd.DataFrame(dict([(keys, [values]) for keys, values in article_details.items()]))
        print(save_path)
        df_to_save.to_csv(save_path)
        
        print(article_details.keys())
#         np.save(os.path.join(save_path, "article_details.npy"), article_details, allow_pickle=True)
        save_time = datetime.now()
        article_self.save_label.value = "Values saved at: "+save_time.strftime("%H:%M:%S")
        
    def _get_concat_label(article_self):
        return " ".join((article_self.entries["First author"].value, 
                         str(article_self.entries["Year"].value),
                         article_self.entries["Optional label"].value))
#         return " ".join((values.value for values in article_self.entries.values()))