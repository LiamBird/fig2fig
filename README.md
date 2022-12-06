# fig2fig
Read figures from figures: interpolate numerical data from figures presented in articles to find quantitative comparisons

## Required packages
- numpy
- matplotlib.pyplot
- ipywidgets
- matplotlib.patches
- pandas
- datetime
- os
- glob
- re

## How to start
In a Jupyter notebook:

```
%matplotlib nbagg
from Bibliography import Bibliography
from GraphScan import GraphScan
from make_bibliography_df import make_bibliography_df

## To enter data about the article and details of the host:
bib = Bibliography()
bib.tab

## To enter details about different graphs screenshotted from the paper:
graph = GraphScan(figsize=(8, 4))
graph.tab
```

Entered data can be saved in each tab, and can be reloaded through the same interfaces (Bibliography and GraphScan). However, some features (including reloading/ clearing mask data) don't always work and need repair - watch this space!

For any issues, contact Liam (liam.bird@ucl.ac.uk)

## Bibliography

### Save and reload

Using:
```
bib = Bibliography()
bib.tab
```

will open a Jupyter tab widget. 
To begin a new entry, click the button next to 'create new data': this will open a Tkinter-style file dialogue window. Make a new empty directory to contain your saved data files, or select a pre-existing directory. If any Bibliography files are saved to that directory, they will be overwritten on saving. 
Click 'Confirm' to see the text that says 'Please select a directory' change to show the path to your new folder. 

### Article details
Type the identifying details of the paper (last name of the first author, the year of publication, and the optional label). 
The optional label is simply to make it easier to differentiate similar records by the user (e.g. multiple papers labelled 'Li2020'). It is not used in analysis. 




