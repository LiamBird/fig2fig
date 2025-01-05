## Consolidating previous variations on SelectFileButton

import traitlets
from ipywidgets import widgets
from IPython.display import display
from tkinter import Tk, filedialog
import os

class SelectFileGeneralButton(widgets.Button):
    """
    Allowed functions: 'askdirectory', 'askopenfilename', 'asksaveasfile'
    Code adapted with minor variation from: https://codereview.stackexchange.com/questions/162920/file-selection-button-for-jupyter-notebook

    """
    def __init__(self, function="askdirectory", label=None):
        super(SelectFileGeneralButton, self).__init__()
        self.add_traits(files=traitlets.traitlets.List())        
        self.icon = "square-o"
        self.style.button_color = "orange"
        self.on_click(self.select_files)
        
        button_label_dict = {'askdirectory': "Select folder",
                             'askopenfilename': "Select file",
                             'asksaveasfile': "Save as..."}
        self._function = function
        
        if type(label) == type(None):
            self.description = button_label_dict[function]
        else:
            self.description = label
        
        
    @staticmethod
    def select_files(b):
        import os
        root = Tk()
        root.withdraw()
        root.call("wm", "attributes", ".", "-topmost", True)
        if b._function == "askdirectory":
            b.files = [filedialog.askdirectory()]
            b.description = os.path.split(b.files[0])[-1]

        if b._function == "askopenfilename":
            b.files = [filedialog.askopenfilename()]
            b.description = os.path.split(b.files[0])[-1]

        if b._function == "asksaveasfile":
            files = [('csv Files', "*.csv")] 
            b.files = [filedialog.asksaveasfile(filetypes = files, defaultextension = files)]
            b.description = os.path.split(b.files[0].name)[-1] ## saveasfile returns a io wrapper rather than a string?

        b.icon = "check-square-o"
        b.style.color = "lightgreen"