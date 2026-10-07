# libraries
from PyQt6.QtCore import pyqtSignal, QObject
from pandas import DataFrame

from laplace_server.server_lhc import ServerLHC
from laplace_server.protocol import DEVICE_SCAN
from laplace_server.server_controller import ServerController

from laplace_log import log

# project
from ..core.data.experimentalData import ExperimentalData
from ..utils.config_helper import get_from_config

class ScanManager(QObject):
    on_server_address = pyqtSignal(str)  # transmit the scan server address
    on_actuators_dict_received = pyqtSignal(dict) 
    on_actuators_position_update_received = pyqtSignal(dict) 
    on_diagnostics_dict_received = pyqtSignal(dict) 
    on_scan_DataFrame = pyqtSignal(DataFrame)

    
    def __init__(self):
        super().__init__()

        self.server_controller = ServerController()
        self.experimental_data = ExperimentalData()
  
    def server_launch(self, server_state: bool) -> None:
        '''
        Start or stop the scan server.
        
            Args:
                server_state: (bool) 
                    True to start the server, False to stop it.
        '''

        if server_state: # if on
            
            # get the server port
            port = get_from_config(
                module="server", 
                item="port", 
                default_value="7531", 
                type=str
            )
            
            # create the server
            self.serv = ServerLHC(
                name="Scan", 
                address=f"tcp://*:{port}", 
                freedom=0, 
                device=DEVICE_SCAN,
                data={},
                empty_data_after_get=True
            )

            # define the functions used by the server on specific messages. 
                
            # when the CMD_SAVE is received, emit a signal to change the saving path
            self.serv.set_on_saving_path_changed(
                self.server_controller.on_saving_path_changed
            )
            # when CMD_SCAN is received, emit signal to update the scanner
            self.serv.set_on_scan(
                self.server_controller.on_scan
            )

            self.serv.set_on_set_actuators(
                self.server_controller.on_set_actuators
            )

            self.serv.set_on_set_diagnostics(
                self.server_controller.on_set_diagnostics
            )

            self.serv.set_on_update_actuator_positions(
                self.server_controller.on_new_actuator_pos_received
            )

            self.server_controller.scan_received.connect(
                self._scan_received
            )
           

            self.serv.start() # start the server

            # emit a signal to transmit the server address to the ExecutionPanel
            self.on_server_address.emit(f"{self.serv.server_ip}:{self.serv.server_port}")
            self.configure_actuators()
            self.configure_diagnostics()
        
        else:                # else means server off
            self.serv.stop() # stop the server
            log.info("Server stopped.")

    def _scan_received(self, data: dict)->None:
        self.experimental_data.add_shot(master_raw_data=data)
        log.info(f'Experimental data frame: {self.experimental_data.dataframe}')
        self.on_scan_DataFrame.emit(self.experimental_data.dataframe)
        

    def configure_actuators(self) -> None:
        '''
        Configure actuators .
        Configures the actuators on the interface from list of available actuators in Master
        Signal comes from server controller 
        '''

        
        self.server_controller.set_actuators_dict_received.connect(
            self.on_actuators_dict_received
        ) 
        
        try: 
            self.server_controller.actuators_pos_update_received.connect(
                    self.on_actuators_position_update_received
                )
        except Exception as e:
            log.error(f'Exception {e} occurred on registering position update')

    def configure_diagnostics(self) -> None:
        '''
        Configure actuators .
        Configures the actuators on the interface from list of available actuators in Master
        Signal comes from server controller 
        '''

        
        self.server_controller.set_diagnostics_dict_received.connect(
            self.on_diagnostics_dict_received
        ) 
   

    def start_scan(self, scan_settings: dict) -> None:
        log.debug(f'Starting scan with settings: {scan_settings}')
        self.serv.set_data(scan_settings)

    def stop_scan(self):
        pass