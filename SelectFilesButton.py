#### Adapted with minor variation from: https://codereview.stackexchange.com/questions/162920/file-selection-button-for-jupyter-notebook

import traitlets
from ipywidgets import widgets
from IPython.display import display
from tkinter import Tk, filedialog
import os


class SelectFilesButton(widgets.Button):
    """A file widget that leverages tkinter.filedialog."""

    def __init__(self):
        super(SelectFilesButton, self).__init__()
        # Add the selected_files trait
        self.add_traits(files=traitlets.traitlets.List())
        # Create the button.
        self.description = "Select Files"
        self.icon = "square-o"
        self.style.button_color = "orange"
        # Set on click behavior.
        self.on_click(self.select_files)

    @staticmethod
    def select_files(b):
        """Generate instance of tkinter.filedialog.

        Parameters
        ----------
        b : obj:
            An instance of ipywidgets.widgets.Button 
        """
        # Create Tk root
        root = Tk()
        # Hide the main window
        root.withdraw()
        # Raise the root to the top of all windows.
        root.call('wm', 'attributes', '.', '-topmost', True)
        # List of selected fileswill be set to b.value
        b.files = [filedialog.askdirectory()]

        b.description = os.path.split(b.files[0])[-1]##"Files Selected"
        b.icon = "check-square-o"
        b.style.button_color = "lightgreen"
