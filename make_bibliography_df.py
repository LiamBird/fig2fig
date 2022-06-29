## Created 06/05/2022
## Updated 18/06/2022 - includes XRD sulfur

import pandas as pd
import os
import numpy as np



def make_bibliography_df(directory="fig2fig_data"):
    all_data_files = os.listdir(directory)

    entry_data = {}
    for folder in all_data_files:
        entry_data.update([(folder, {})])
        for fname in next(os.walk(os.path.join('fig2fig_data', folder)))[2]:

            if ".npy" in fname:
                entry_data[folder].update([(fname.strip(".npy"), np.load(os.path.join("fig2fig_data", folder, fname),
                                                                         allow_pickle=True).item())])
        try:
            for host_idx, host_data in entry_data[folder]['Saved_host_values'].items():
                host_data.update([("Scanned data", [])])

            for subdir in next(os.walk(os.path.join('fig2fig_data', folder)))[1]:
                if 'line_data' in os.listdir(os.path.join('fig2fig_data', folder, subdir)):
                    available_data = os.listdir(os.path.join('fig2fig_data', folder, subdir, 'line_data'))
                    for dataset in available_data:
                        for host_idx, host_data in entry_data[folder]['Saved_host_values'].items():
                            if host_data['Host label'] == dataset.strip('.npy'):
                                host_data['Scanned data'].append(os.path.join('fig2fig_data', folder, subdir, 'line_data', dataset))  

        except:
            print("Skipping {}".format(folder))

    column_sources = ['article_details', 'electrolyte_details', 'Saved_common_names_values']
    all_column_names = np.unique([item for sublist in\
     [item for sublist in\
      [[[*entry[key].keys()] for key in column_sources] for entry in entry_data.values()] for item in sublist]\
    for item in sublist])
    all_column_names = np.hstack((all_column_names, 
                                  np.full((1), "Host label"),
                                  np.full((1), "Scanned data"),
                                  np.full((1), "Sulfur XRD")))
    combined_data = dict([(column, 
                          []) for column in all_column_names])

    for fname, dataset in entry_data.items():
        for host_idx, host_dict in dataset["Saved_host_values"].items():
            column_names_check = dict([(column, False) for column in all_column_names])

            for label in ['article_details', 'electrolyte_details']:
                for column in all_column_names:
                    if column in dataset[label].keys():
                        combined_data[column].append(dataset[label][column])
                        column_names_check[column] = True

            for key, value in host_dict.items():
                combined_data[key].append(host_dict[key])
                column_names_check[key] = True

            if "Sulfur_XRD_data" in dataset.keys():
                combined_data["Sulfur XRD"].append([values for keys, values in dataset["Sulfur_XRD_data"].items() 
                                           if keys==host_dict["Host label"]][0])
                column_names_check["Sulfur XRD"] = True

            skipped_keys = [key for key, value in column_names_check.items() if value==False]
            for key in skipped_keys:
                combined_data[key].append(np.nan)
            
    df = pd.DataFrame(combined_data)
    return df
