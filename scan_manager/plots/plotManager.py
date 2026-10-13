
import qdarkstyle
import pathlib

from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout,
    QGridLayout, QPushButton, 
    QLabel, QComboBox
)
from PyQt6.QtGui import QIcon


from .plotWindow import PlotWindow
from laplace_log import log



class PlotManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.available_actuators = {}
        self.available_diagnostics = {}
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

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        panel_layout = QVBoxLayout(central_widget)
        plot_config = QGroupBox('Plot Configuration')

        config_layout = QGridLayout(self)   # create the layout
        plot_config.setLayout(config_layout)
        self.plot_type_menu = QComboBox()
        self.plot_type_menu.addItems(['x-y', 'multi x-y', 'xyz'])
        self.x_axis_box = QComboBox()
        self.y_axis_box = QComboBox()
        self.third_coordinate_box = QComboBox()
        self.add_plot_btn = QPushButton('(+)')

        config_layout.addWidget(self.plot_type_menu, 0, 0)
        config_layout.addWidget(self.x_axis_box, 0, 1)
        config_layout.addWidget(self.y_axis_box, 0, 2)
        config_layout.addWidget(self.third_coordinate_box, 0, 3)
        config_layout.addWidget(self.add_plot_btn, 0, 4)


        panel_layout.addWidget(plot_config)  # add the widget list to the layout

    def update_interface(self, actuators: dict, diagnostics: dict):
        self.available_actuators = actuators
        self.available_diagnostics = diagnostics

        for address, status in self.available_actuators.items() :
            print(f'Actuators at {address} in Plot Manager: {status}')
            

        for address, status in self.available_diagnostics.items():
            print(f'Diagnostics at {address}in Plot Manager: {status}')


