# libraries
import pathlib

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QCheckBox, 
    QLabel, QDoubleSpinBox, QApplication, 
    QAbstractSpinBox, QSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from ...utils.check_IP_address import validate_address
from ...utils.widget_utils import (STATE_WIDTH, SCAN_WIDTH, RANK_WIDTH, 
                                   ADDRESS_WIDTH, NAME_WIDTH, SPIN_WIDTH, UNIT_WIDTH)
from laplace_log import log


class ActuatorControlWidget(QWidget):
    '''
    Define the actuator control line. 
    '''

    def __init__(self, address: str, name: str, index: int, motor_count: int):
        '''
            Args:
                definition: (dict)
                    dictionary with address, actuator name and number
        '''
        super().__init__() # Inheritance from QWidget
        self.address = None
        self.name = None 
        self.index = None
        self.motor_count = motor_count

        try : 
            self.define(address, name, index)
        except Exception as e:
            log.error(f'Could not define actuator, invalid definition')
            log.error(f'Exception: {e}')

        self.set_up()  # builds the input widget
        self.actions() # defines the actions of InputWidget

    def define(self, address: str, name: str, index: int):
        if not validate_address(address):
            raise ValueError(f'{address} is not a valid address')
        else: 
            self.address = address
            self.name = name
            self.index = index


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
        self.state_icon.setFixedWidth(STATE_WIDTH)
        self.state_icon.setPixmap(self.disconnected_icon.pixmap(16, 16)) 
        self.state_icon.setToolTip("Current state")
        line_layout.addWidget(self.state_icon)

        # ip_port
        self.address_label = QLabel()
        self.address_label.setText(self.address or "Unknown")
        self.address_label.setEnabled(False)
        self.address_label.setFixedWidth(ADDRESS_WIDTH)
        self.address_label.setToolTip("Actuator IP:port")
        line_layout.addWidget(self.address_label)

        # index_label
        self.index_label =  QLabel()
        self.index_label.setText(str(self.index))
        self.index_label.setEnabled(False)
        self.index_label.setFixedWidth(RANK_WIDTH)
        self.index_label.setToolTip("Index")
        line_layout.addWidget(self.index_label)

        # name
        self.name_label = QLabel()
        self.name_label.setText(self.name or "Unknown")
        self.name_label.setEnabled(False)
        self.name_label.setFixedWidth(NAME_WIDTH)
        self.name_label.setToolTip("Actuator name")
        line_layout.addWidget(self.name_label)

        # position 
        self.current_pos_spin = QDoubleSpinBox()
        self.current_pos_spin.setButtonSymbols(
            QAbstractSpinBox.ButtonSymbols.NoButtons
            )
        self.current_pos_spin.setDecimals(3)
        self.current_pos_spin.setEnabled(False)
        self.current_pos_spin.setFixedWidth(SPIN_WIDTH)
        self.current_pos_spin.setToolTip("Current position")
        line_layout.addWidget(self.current_pos_spin)

        # Min spinBox
        self.min_spin = QDoubleSpinBox()
        self.min_spin.setDecimals(3)
        self.min_spin.setEnabled(True)
        self.min_spin.setFixedWidth(SPIN_WIDTH)
        self.min_spin.setToolTip("Lower bound")
        line_layout.addWidget(self.min_spin)

        # Max spinBox
        self.max_spin = QDoubleSpinBox()
        self.max_spin.setDecimals(3)
        self.max_spin.setEnabled(True)
        self.max_spin.setFixedWidth(SPIN_WIDTH)
        self.max_spin.setToolTip("Higher bound")
        line_layout.addWidget(self.max_spin)

        # Stepsize spinBox
        self.stepsize_spin = QDoubleSpinBox()
        self.stepsize_spin.setDecimals(3)
        self.stepsize_spin.setEnabled(True)
        self.stepsize_spin.setFixedWidth(SPIN_WIDTH)
        self.stepsize_spin.setToolTip("Step size")
        line_layout.addWidget(self.stepsize_spin)

        # Unit
        self.unit_label = QLabel()
        self.unit_label.setText("Unknown")
        self.unit_label.setFixedWidth(UNIT_WIDTH)
        self.unit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.unit_label.setToolTip("Input unit")
        line_layout.addWidget(self.unit_label)

        # scanning rank
        self.rank_input =  QSpinBox()
        self.rank_input.setMinimum(0)
        self.rank_input.setMaximum(10)
        self.rank_input.setButtonSymbols(
                    QAbstractSpinBox.ButtonSymbols.NoButtons
                    )
        self.rank_input.setFixedWidth(RANK_WIDTH)
        self.rank_input.setToolTip(f"Rank 0 outer, rank 1 inner - defined as in a for loop")
        line_layout.addWidget(self.rank_input)

        # scan
        self.scan_checkbox = QCheckBox()
        self.scan_checkbox.setToolTip(f"Check this box to scan")
        self.scan_checkbox.setFixedWidth(SCAN_WIDTH)
        line_layout.addWidget(self.scan_checkbox)

    @staticmethod
    def make_header() -> QWidget:
        header_widget = QWidget()

        line_layout = QHBoxLayout(header_widget)
        line_layout.setContentsMargins(4, 2, 4, 2)
        line_layout.setSpacing(8)

        # State
        status_label = QLabel("State")
        status_label.setFixedWidth(STATE_WIDTH)
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
   
        # Scan
        scan_label = QLabel("Scan")
        scan_label.setFixedWidth(SCAN_WIDTH)
        scan_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Rank
        rank_label = QLabel("Rank")
        rank_label.setFixedWidth(RANK_WIDTH)
        rank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Address
        address_label = QLabel("IP:port")
        address_label.setFixedWidth(ADDRESS_WIDTH)

        # Motor Index
        index_label = QLabel("Index")
        index_label.setFixedWidth(RANK_WIDTH)

        # Name
        name_label = QLabel("Name")
        name_label.setFixedWidth(NAME_WIDTH)

        # Current position
        current_label = QLabel("Current")
        current_label.setFixedWidth(SPIN_WIDTH)
        current_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Minimum
        min_label = QLabel("Min")
        min_label.setFixedWidth(SPIN_WIDTH)
        min_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # Maximum
        max_label = QLabel("Max")
        max_label.setFixedWidth(SPIN_WIDTH)
        max_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Step
        step_label = QLabel("Step")
        step_label.setFixedWidth(SPIN_WIDTH)
        step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Unit
        unit_label = QLabel("Unit")
        unit_label.setFixedWidth(UNIT_WIDTH)
        unit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        line_layout.addWidget(status_label)
        line_layout.addWidget(address_label)
        line_layout.addWidget(index_label)
        line_layout.addWidget(name_label)
        line_layout.addWidget(current_label)
        line_layout.addWidget(min_label)
        line_layout.addWidget(max_label)
        line_layout.addWidget(step_label)
        line_layout.addWidget(unit_label)
        line_layout.addWidget(rank_label)
        line_layout.addWidget(scan_label)

        return header_widget

    @property
    def scan(self):
        return self.scan_checkbox.isChecked()

    def actions(self) -> None:
        '''
        Defines the actions of the InputWidget class.
        '''
        # when the input state is changed, change the icon and enable / disable the spin boxes
        self.scan_checkbox.stateChanged.connect(self.on_state_changed)
        


    def update_position(self, position: float)-> None:
        self.current_pos_spin.setValue(position)

    def update_status_available(self, available: bool)-> None:
        if available:
            self.state_icon.setPixmap(self.connected_icon.pixmap(16, 16)) 
        else:
            self.state_icon.setPixmap(self.disconnected_icon.pixmap(16, 16)) 

    def get_attributes(self)->dict:
        attr_dict = dict({})
        attr_dict['current'] = self.current_pos_spin.value()
        attr_dict['start'] = self.min_spin.value()
        attr_dict['stop'] = self.max_spin.value()
        attr_dict['step'] = self.stepsize_spin.value()
        attr_dict['rank'] = self.rank_input.value()
        attr_dict['index'] = int(self.index_label.text())
        attr_dict['motor count'] = self.motor_count

    
        log.info(f'Attributes for {self.address}, {self.name}: {attr_dict}')
        return attr_dict

        
    def on_state_changed(self, enabled: bool) -> None:
        '''
        '''
        pass




if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = ActuatorControlWidget('147.250.140.85:7531', 'name')
    window.resize(350, 150)
    window.show()

    sys.exit(app.exec())