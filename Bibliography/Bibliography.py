class Bibliography(object):
    def __init__(self):
        import ipywidgets as wg
        import numpy as np
        
        
        from SelectFilesTab import SelectFilesTab
        from ArticleDetailsTab import ArticleDetailsTab
        from HostTab import HostTab
        from ElectrochemistryTab import ElectrochemistryTab
        from CharacterisationTab import CharacterisationTab
        
        
        self._select_files_tab = SelectFilesTab()
        self._article_details_tab = ArticleDetailsTab()
        self._host_tab = HostTab()
        self._electrochemistry_tab = ElectrochemistryTab()
        self._characterisation_tab = CharacterisationTab()
        
        def on_confirm_save_location_clicked(b):
            ## If creating a new file:
            if len(self._select_files_tab.save_new_csv_button.files) > 0:
                self.save_path = self._select_files_tab.save_new_csv_button.files[0].name ## saveas method returns wrapper rather than string
                self._select_files_tab.confirmed_location_label.value = "Saving new data"                
            
            
            ## If loading from a previous .csv database:
            elif len(self._select_files_tab.select_previous_files_button.files) > 0:
                self.save_path=self._select_files_tab.select_previous_files_button.files[0]
                self._select_files_tab.reload_values(save_path=self.save_path, save_method="from_csv")
                
            ## If converting old directory with .npy files to .csv:
            elif len(self._select_files_tab.convert_to_csv_button.files) > 0:
                print("Conversion method in use")
                    


        def on_confirm_dropdown_clicked(b):
            if self._select_files_tab.using_dropdown == True:

                self._select_files_tab.reload_from_csv()
                if "save_path" in vars(self._select_files_tab):
                    self.save_path = self._select_files_tab.save_path
                
                self._article_details_tab.reload_values(selected_article_df=self._select_files_tab._selected_article_df,
                                                        save_path = self.save_path)
                self._concat_label = self._article_details_tab._get_concat_label()
                
                self._host_tab.reload_values(selected_article_df=self._select_files_tab._selected_article_df,
                                             save_path=self.save_path)
                self._characterisation_tab.reload_values(save_path=self.save_path, concat_label=self._concat_label)

                
        self._select_files_tab.confirm_save_location_button.on_click(on_confirm_save_location_clicked)
        self._select_files_tab.confirm_dropdown_selection.on_click(on_confirm_dropdown_clicked)
        
        def on_save_article_clicked(b):
            self._article_details_tab.save_values(save_path=self.save_path)
            self._concat_label = self._article_details_tab._get_concat_label()
            print(self._concat_label)
        self._article_details_tab.save_button.on_click(on_save_article_clicked)
        
        def on_save_host_values_clicked(b):
            
            self._host_tab.sample_self.save_values(save_path=self.save_path, concat_label=self._concat_label)
            self._host_tab.save_values()
        self._host_tab.save_button.on_click(on_save_host_values_clicked)
        
        def on_save_electrochem_clicked(b):
            self._electrochemistry_tab.save_values(save_path=self.save_path, concat_label=self._concat_label)
        self._electrochemistry_tab.save_button.on_click(on_save_electrochem_clicked)    
        
        def on_save_characterisation_clicked(b):
            self._characterisation_tab.save_values(save_path=self.save_path, concat_label=self._concat_label)
        self._characterisation_tab.save_button.on_click(on_save_characterisation_clicked)
        
        self.tab = wg.Tab([self._select_files_tab.vbox,
                           self._article_details_tab.vbox,
                           self._host_tab.vbox,
                           self._electrochemistry_tab.vbox,
                           self._characterisation_tab.vbox
                          ]) 
        
        tab_names = ["Save and reload",
                     "Article details", 
                     "Host", 
                     "Electrochemistry",
                     "Characterisation"
                    ]
        for n, names in enumerate(tab_names):
            self.tab.set_title(n, names)