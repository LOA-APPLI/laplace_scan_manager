
import qdarkstyle
import pathlib
from pandas import DataFrame

from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout,
    QGridLayout, QPushButton, 
    QLabel, QComboBox, QLineEdit
)
from PyQt6.QtGui import QIcon


from .plotWindow import PlotWindow
from laplace_log import log
from ..utils.widget_utils import (STATE_WIDTH, SCAN_WIDTH, RANK_WIDTH, 
                                   ADDRESS_WIDTH, NAME_WIDTH, SPIN_WIDTH, UNIT_WIDTH)


class PlotManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.available_actuators = []
        self.available_diagnostics = []
        self.plots = {}
        self.set_up()    
        self.actions() 
        self.plot_window = PlotWindow()
        self.new_device = False
        
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

        graph_name_label = QLabel('Graph name')
        self.graph_name = QLineEdit('Title')
        self.graph_name.setFixedWidth(ADDRESS_WIDTH)

        self.plot_type_menu.addItems(['x-y', 'multi x-y', 'xyz'])
        x_axis_label = QLabel('x-axis')
        self.x_axis_box = QComboBox()
        self.x_axis_box.setFixedWidth(ADDRESS_WIDTH)
        x_axis_name_label = QLabel("x label")
        self.x_axis_name = QLineEdit("")
        self.x_axis_name.setFixedWidth(ADDRESS_WIDTH)

        y_axis_label = QLabel('y-axis')
        self.y_axis_box = QComboBox()
        self.y_axis_box.setFixedWidth(ADDRESS_WIDTH)
        y_axis_name_label = QLabel("y label")
        self.y_axis_name = QLineEdit("")
        self.y_axis_name.setFixedWidth(ADDRESS_WIDTH)

        z_axis_label = QLabel('z-axis')
        self.z_axis_box = QComboBox()
        self.z_axis_box.setFixedWidth(ADDRESS_WIDTH)
        z_axis_name_label = QLabel("z label")
        self.z_axis_name = QLineEdit("")
        self.z_axis_name.setFixedWidth(ADDRESS_WIDTH)

        self.add_plot_btn = QPushButton('Add (+)')
        self.add_plot_btn.setFixedWidth(ADDRESS_WIDTH)

        config_layout.addWidget(plot_type_label, 0, 0)
        config_layout.addWidget(x_axis_label, 0, 1)
        config_layout.addWidget(y_axis_label, 0, 2)
        config_layout.addWidget(z_axis_label, 0, 3)
        

        config_layout.addWidget(self.plot_type_menu, 1, 0)
        config_layout.addWidget(self.x_axis_box, 1, 1)
        config_layout.addWidget(self.y_axis_box, 1, 2)
        config_layout.addWidget(self.z_axis_box, 1, 3)

        config_layout.addWidget(self.add_plot_btn, 1, 4)

        config_layout.addWidget(graph_name_label, 2, 0)
        config_layout.addWidget(x_axis_name_label, 2, 1)
        config_layout.addWidget(y_axis_name_label, 2, 2)
        config_layout.addWidget(z_axis_name_label, 2, 3)

        config_layout.addWidget(self.graph_name, 3, 0)
        config_layout.addWidget(self.x_axis_name, 3, 1)
        config_layout.addWidget(self.y_axis_name, 3, 2)
        config_layout.addWidget(self.z_axis_name, 3, 3)

        panel_layout.addWidget(plot_config)  # add the widget list to the layout

    def actions(self):
        self.add_plot_btn.clicked.connect(self.add_plot)

    def add_plot(self):
        axes = ['x', 'y', 'z']
        variables = dict(zip(axes, [self.x_axis_box, self.y_axis_box, self.z_axis_box]))
        names = dict(zip(axes, [self.x_axis_name, self.y_axis_name, self.z_axis_name]))
        for axis, name in names.items():
            if name.text() is "":
                names[axis] = variables[axis].currentText()
            else:
                names[axis] = name.text()

        self.plot_window.add_plot(plotType = self.plot_type_menu.currentText(),
                                  axes = names, plot_title=self.graph_name.text())

    def update_interface(self, actuators: dict, diagnostics: dict):

        for status in actuators.values() :
            for motor in status['motors']:
                name = motor['name']
                if name not in self.available_actuators:
                    self.new_device = True
                    self.available_actuators.append(name)            

        for status in diagnostics.values():
            name = status['name']
            for plottable in status['plottables_list']:
                plottable_label = name + ":" + plottable
                if plottable_label not in self.available_diagnostics:
                    self.new_device = True
                    self.available_diagnostics.append(plottable_label)
        if self.new_device:
            self.x_axis_box.clear()
            self.y_axis_box.clear()
            self.z_axis_box.clear()
            self.x_axis_box.addItems(self.available_actuators)
            self.y_axis_box.addItems(self.available_actuators)
            self.y_axis_box.addItems(self.available_diagnostics)
            self.z_axis_box.addItems(self.available_diagnostics)
        self.new_device = False

    def update_data(self, df: DataFrame) -> None:
        self.plot_window.update_plots(df)
