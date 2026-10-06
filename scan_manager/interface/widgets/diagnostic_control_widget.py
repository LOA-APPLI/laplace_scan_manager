# libraries
import pathlib

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QComboBox, QLabel, QDoubleSpinBox, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from ...utils.check_IP_address import validate_address
from laplace_log import log


class DiagnosticControlWidget(QWidget):
    '''
    Define the diagnostic control line. 
    '''

    def __init__(self, address: str, status: dict):
        '''
            Args:
                definition: 
                    address: IP address of diag server
                    name: diag name
                    plottables: dictionary of format {'plottable_1':float, ..., 'plottable_n':float}
        '''
        super().__init__() # Inheritance from QWidget
        self.address = None
        self.name = None 
        self.plottables_list = None

        try : 
            self.define(address, status)
        except Exception as e:
            log.error(f'Could not define diagnostic, invalid definition')
            log.error(f'Exception: {e}')

        self.set_up()  # builds the input widget
        self.actions() # defines the actions of InputWidget

    def define(self, address: str, status: dict):
        if not validate_address(address):
            raise ValueError(f'{address} is not a valid address')
        else: 
            self.address = address
            self.name = status['name']
            self.plottables_list = status['plottables_list']


    def set_up(self) -> None:

        # input line layout
        line_layout = QHBoxLayout(self)
        line_layout.setContentsMargins(4, 2, 4, 2) # widget margin
        line_layout.setSpacing(8)                  # spacing
        self.setLayout(line_layout)                # set layout

        p = pathlib.Path(__file__)              # get the file path
        icon_path = p.parent.parent / 'icons'   # get the icon folder path

        # build the check and uncheck icons
        self.connected_icon = QIcon(str(icon_path / 'connected.png'))
        self.disconnected_icon = QIcon(str(icon_path / 'disconnected.png'))

        # state icon
        self.state_icon = QLabel()                                     
        self.state_icon.setFixedWidth(20)
        self.state_icon.setPixmap(self.disconnected_icon.pixmap(16, 16)) 
        self.state_icon.setToolTip("Current state")
        line_layout.addWidget(self.state_icon)



        # ip_port
        self.address_label = QLabel()
        self.address_label.setText(self.address or "Unknown")
        self.address_label.setEnabled(False)
        self.address_label.setToolTip("Actuator IP:port")
        line_layout.addWidget(self.address_label)

        # name
        self.name_label = QLabel()
        self.name_label.setText(self.name or "Unknown")
        self.name_label.setEnabled(False)
        self.name_label.setToolTip("Actuator name")
        line_layout.addWidget(self.name_label)

        # Plottables
        self.plottables_combobox = QComboBox()
        for plottable in self.plottables_list:
            self.plottables_combobox.addItem(plottable)
            
        line_layout.addWidget(self.plottables_combobox)




    def actions(self) -> None:
        '''
        Defines the actions of the InputWidget class.
        '''
        pass

    def update_status_available(self, available: bool)-> None:
        if available:
            self.state_icon.setPixmap(self.connected_icon.pixmap(16, 16)) 
        else:
            self.state_icon.setPixmap(self.disconnected_icon.pixmap(16, 16)) 
            
    def on_state_changed(self, enabled: bool) -> None:
        '''
        '''
        pass


    def update_instance_bounds(self) -> None:
        '''
        Update the boundaries in the class instance.
        '''
        pass

    def update_min_max(self) -> None:
        '''
        Update the min and max values of the spin boxes.
        '''
        pass



