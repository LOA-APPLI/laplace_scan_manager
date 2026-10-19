
import qdarkstyle
import pathlib
import pandas as pd

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

        self.data = pd.DataFrame()
        self.available_actuators = []
        self.available_diagnostics = []
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
        self.setGeometry(120, 30, 750, 100)

        # icon
        icon_path = p.parent / 'icons'
        self.setWindowIcon(QIcon(str(icon_path / 'LOA.png')))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        panel_layout = QVBoxLayout(central_widget)
        plot_config = QGroupBox('Plot Configuration')

        config_layout = QGridLayout(self)   # create the layout
        plot_config.setLayout(config_layout)
        plot_type_label = QLabel('Plot type')
        self.plot_type_menu = QComboBox()
        self.plot_type_menu.addItems(['x-y', 'multi x-y', 'xyz'])
        x_axis_label = QLabel('x-axis')
        self.x_axis_box = QComboBox()
        y_axis_label = QLabel('y-axis')
        self.y_axis_box = QComboBox()
        third_coor_label = QLabel('3rd coor')
        self.third_coordinate_box = QComboBox()
        self.add_plot_btn = QPushButton('Add (+)')

        config_layout.addWidget(plot_type_label, 0, 0)
        config_layout.addWidget(x_axis_label, 0, 1)
        config_layout.addWidget(y_axis_label, 0, 2)
        config_layout.addWidget(third_coor_label, 0, 3)

        config_layout.addWidget(self.plot_type_menu, 1, 0)
        config_layout.addWidget(self.x_axis_box, 1, 1)
        config_layout.addWidget(self.y_axis_box, 1, 2)
        config_layout.addWidget(self.third_coordinate_box, 1, 3)

        config_layout.addWidget(self.add_plot_btn, 1, 4)

        panel_layout.addWidget(plot_config)  # add the widget list to the layout

    def actions(self):
        pass

    def update_interface(self, actuators: dict, diagnostics: dict):

        for address, status in actuators.items() :
            for motor in status['motors']:
                name = motor['name']
                if name not in self.available_actuators:
                    self.available_actuators.append(name)            

        for address, status in diagnostics.items():
            for plottable in status['plottables_list']:
                if plottable not in self.available_diagnostics:
                    self.available_diagnostics.append(plottable)

        log.info(f'actuators: {self.available_actuators}, diagnostics: {self.available_diagnostics}')

        self.x_axis_box.clear()
        self.y_axis_box.clear()
        self.third_coordinate_box.clear()
        self.x_axis_box.addItems(self.available_actuators)
        self.y_axis_box.addItems(self.available_actuators)
        self.y_axis_box.addItems(self.available_diagnostics)
        self.third_coordinate_box.addItems(self.available_diagnostics)

    def update_data(self, df: pd.DataFrame) -> None:
        self.data = df
        log.info(f'New dataframe: {self.data}')
