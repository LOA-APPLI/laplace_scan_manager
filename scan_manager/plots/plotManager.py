
import qdarkstyle
import pathlib

from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import (
    QGroupBox, QGridLayout, QRadioButton,
    QCheckBox, QLineEdit, QPushButton, 
    QLabel, QFileDialog
)
from PyQt6.QtGui import QIcon


from .plotWindow import PlotWindow



class PlotManager(QWidget):
    def __init__(self):
        super().__init__()

        self.available_keys = [""]  
        self.plots = {}     
        self.set_up()     


    def set_up(self) -> None:
        '''
        Configure the window layout and appearance.

        Sets the window title, size, icon, stylesheet, and initializes
        the main vertical layout containing the "+" button and the plot grid.
        '''
        p = pathlib.Path(__file__)

        # window
        self.setWindowTitle("Plot Manager")
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6'))
        self.setGeometry(120, 30, 750, 300)

        # icon
        icon_path = p.parent / 'icons'
        self.setWindowIcon(QIcon(str(icon_path / 'LOA.png')))