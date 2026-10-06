# libraries
from PyQt6.QtWidgets import (
    QGroupBox, QGridLayout, QRadioButton,
    QCheckBox, QLineEdit, QPushButton, 
    QLabel, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from laplace_log import log

# project
from ...utils.config_helper import get_from_config, set_in_config


class ExecutionPanel(QGroupBox):
    '''
    Panel handling execution mode and data source configuration.
    A lock button allows to enable / disable every widget.
    '''
    # signal indicating that the server checkbox state changed
    server_state_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__("Execution & Data Configuration")

        self.set_up()  # build the elements
        self.actions() # defines the panel actions


    def set_up(self) -> None:
        '''
        Function made to create and set the elements
        of the ExecutionPanel class.
        '''
        exc_layout = QGridLayout(self)

        # Online execution
        self.server_checkbox = QCheckBox("Run online (start server)")
        self.server_entry = QLineEdit("")  # indicates the optimization server address
        self.server_entry.setReadOnly(True)




        # Lock
        self.lock_button = QPushButton("🔒 Lock configuration")
        self.lock_button.setCheckable(True)

        # exc_layout
        exc_layout.addWidget(self.server_checkbox, 0, 0)
        exc_layout.addWidget(QLabel("Server address:"), 0, 1)
        exc_layout.addWidget(self.server_entry, 0, 2)
        exc_layout.addWidget(self.lock_button, 0, 3, alignment=Qt.AlignmentFlag.AlignRight)



        # get the default execution (reading and saving) path
            # get and set default saving path
        default_saving_path = get_from_config(
            module="interface",
            item="default_saving_path",
            default_value="",
            type=str
        )
        self.save_path_tmp = default_saving_path   # path update when the panel is unlocked
        self.set_path_saving(default_saving_path)
        
            # get and set default reading path
        default_reading_path = get_from_config(
            module="interface",
            item="default_reading_path",
            default_value="",
            type=str
        )
        self.read_path_tmp = default_reading_path
        self.set_path_reading(default_reading_path)


    def actions(self) -> None:
        '''
        Defines the actions of the ExecutionPanel class.
        '''
        # when the server checkbox is toggled, emit a PyQt6 signal (to start server)
        self.server_checkbox.toggled.connect(self.update_online_state)
        

        
        # when the lock_button is pressed, enable / disable the widgets
        self.lock_button.toggled.connect(self.set_locked)


        



    def on_read_path_changed(self, path: str) -> None:
        '''
        Change the default reading path in 'config.ini' and
        display it in the logs.
        '''
        set_in_config(
            module="interface",
            item="default_reading_path",
            val=path,
        )
        log.debug(f"Reading folder modified, new reading folder: {path}")


    def on_save_path_changed(self, path: str) -> None:
        '''
        Change the default saving path in 'config.ini' and
        display it in the logs.
        '''
        set_in_config(
            module="interface",
            item="default_saving_path",
            val=path
        )
        log.debug(f"Saving folder modified, new saving folder: {path}")


    def update_online_state(self, checked: bool) -> None:
        '''
        Change the server state and emit the realted signal.
        '''
        if not self.lock_button.isChecked():       # if the lock button is not pressed
            self.server_entry.setEnabled(checked)  # enable / disable the server address label
                
        log.debug("Server box checked." if checked else "Server box unchecked.")
        self.server_state_changed.emit(checked)  # emit a signal to start / stop the server


    def set_locked(self, locked: bool) -> None:
        '''
        Enable / disable every widget of the panel when
        the lock button is clicked.
        '''
        # list of widgets to lock
        widgets = [
            self.server_checkbox,
        ]

        for w in widgets: # for every widget
            w.setEnabled(not locked) # lock / unlock it (locked = True means disable -> Enable = False)


        # change the button text 
        self.lock_button.setText(
            "🔓 Unlock configuration" if locked else "🔒 Lock configuration"
        )
        log.debug("Configuration locked." if locked else "Configuration unlocked.")





    ### helpers

    def get_execution(self) -> dict[str, bool | str]:
        '''
        Return the execution dictionary defining the
        online / offline, reading and saving procedure. 
        '''
        execution = {}
        execution["is_online"] = self.is_online_enabled()
        execution["saving_path"] = self.get_path_saving()
        execution["server_address"] = self.get_server_address()

        return execution


        # checkers
    def is_online_enabled(self) -> bool:
        return self.server_checkbox.isChecked()

    def is_locked(self) -> bool:
        return self.lock_button.isChecked()


    def get_path_saving(self) -> str:
        pass
    
    def get_server_address(self) -> str:
        return self.server_entry.text().strip()

        
        ### setters
    def set_path_reading(self, path: str) -> None:
        if not self.is_locked():
            log.info(f"Reading path setted: '{path}'")
        else:
            log.info(f"Configuration locked, reading path unchanged before unlocking.")
        self.read_path_tmp = path
    
    def set_path_saving(self, path: str) -> None:
        if not self.is_locked():
            log.info(f"Saving path setted: '{path}'")

        else:
            log.info(f"Configuration locked, saving path unchanged before unlocking.")
        self.save_path_tmp = path
    
    def set_server_address(self, address: str) -> None:
        return self.server_entry.setText(address)
