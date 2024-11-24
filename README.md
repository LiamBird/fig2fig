# fig2fig
Read figures from figures: interpolate numerical data from figures presented in articles to find quantitative comparisons

__For version 1 implementation, see:__ https://pubs.acs.org/doi/10.1021/acsmaterialslett.4c01646

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

For any issues, contact Liam (liam.bird@eng.ox.ac.uk)

For detailed instructions, see the [wiki](https://github.com/LiamBird/fig2fig/wiki) (https://github.com/LiamBird/fig2fig/wiki)




