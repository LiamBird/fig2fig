"""
Carbon and Li-S cells development
Search query: 
- "lithium sulfur" OR Li-S OR "Lithium-sulfur"
- graphene OR carbon
- NOT IN TITLE: electrolyte, separator
- Excluding: Review articles
- Including: Article
- Date of most recent references saved: 15/07/2022
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import pandas as pd
import re

from datetime import datetime
from matplotlib.ticker import MultipleLocator

## In the data exported as .txt files from Web Of Science, the year is stored in column index 46
## with the column name "PY" 
year_column_idx = 46
year_column_name = "PY"

## Web of Science is able to export 500 records per page, therefore for > 500 records multiple .txt
## files are output. 
## Where all the text files are in the same directory as this code...
tables_read = [pd.read_table(file) for file in glob.glob("*.txt")]
table = pd.concat(tables_read, axis=0)


unique_years, years_counts = np.unique(table["PY"][~np.isnan(table["PY"])], return_counts=True)
years_plot = unique_years[unique_years>2000]
counts_plot = years_counts[unique_years>2000]

f, ax = plt.subplots()
ax.bar(years_plot, counts_plot, facecolor="gainsboro", edgecolor="black")
ax.xaxis.set_major_locator(MultipleLocator(2))
ax.tick_params(which="both", tickdir="in", top=True, right=True)
ax.set_xlabel("Year")
ax.set_ylabel("Number of papers published")
now = datetime.now()
# plt.savefig("Papers_per_year_{}_{}_{}_for_{}_papers.png".format(now.year, now.month, now.day, len(table)),
#             bbox_inches="tight")

