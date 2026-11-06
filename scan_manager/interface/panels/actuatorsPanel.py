# libraries
import sys
from PyQt6.QtWidgets import (
    QGroupBox,QVBoxLayout,
    QListWidget, QListWidgetItem,
    QApplication
)



from laplace_log import log

# project
from ..widgets.actuator_control_widget import ActuatorControlWidget


class ActuatorsPanel(QGroupBox):

    def __init__(self):        
        super().__init__("Actuators (motors, gas, etc.)")

        self.actuator_widgets = {}
        self.actuator_widget_items = {}
        self.set_up()  # build the elements
        self.actions() # defines the panel actions

    def set_up(self) -> None:
        '''
        Build the panel widgets.
        '''
        panel_layout = QVBoxLayout(self)   # create the layout
        self.list_widget = QListWidget()   # create the widget list
        panel_layout.addWidget(self.list_widget)  # add the widget list to the layout
        list_header = ActuatorControlWidget.make_header()

        item = QListWidgetItem()
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, list_header)

    def update_actuator_widget(self, address: str, status: dict) -> None:

        for motor in status['motors'].values():
                    name = motor['name']
                    position = motor['position']
                    try : 
                        actuator_widgets = self.actuator_widgets[address]
                    except Exception as e :
                        log.error(f'self.actuator_widgets[address] could not be accessed {e}')
                        return
                    try : 
                        widget = actuator_widgets[name]
                    except Exception as e: 
                        log.error(f'actuator_widgets[name] could not be accessed {e}')
                        return
                    try : 
                        widget.update_position(position)
                        widget.update_status_available(True)
                    except Exception as e:
                        log.error(f'Could not update position: {e}')

    def update_actuators_unavailable(self, address:str) -> None:
        actuator_widgets = self.actuator_widgets.get(address)
        log.debug(f'Actuator widgets: {actuator_widgets}')
        for widget in actuator_widgets.values():
            widget.update_status_available(False)

    def remove_all(self)-> None:
        if self.actuator_widgets:
            for i in range(self.list_widget.count()):
                list_item = self.list_widget.item(0)
                self.list_widget.removeItemWidget(list_item)
                self.list_widget.takeItem(0)

            for actuator_widget_dict in self.actuator_widgets.values():
                for actuator_widget in actuator_widget_dict.values():
                    del actuator_widget

        self.actuator_widget_items = {}
        self.actuator_widgets = {}    
                    
    def add_actuator_widgets_from_status(self, address: str, status: dict) -> None:

        log.info(f'actuator status to add to interface: {status['motors']}')

        for index, motor in status['motors'].items():
            self.add_actuator_widget(
                address,
                motor['name'],
                int(index),
                motor['position']
            )
            

    def add_actuator_widget(self, address: str, name: str, index: int, position: float, motor_count:int = 1):
        new_widget = ActuatorControlWidget(address=address, name=name, index=index, motor_count= motor_count)
        self.actuator_widgets.setdefault(address, {})[name] = new_widget

        item = QListWidgetItem(self.list_widget)          # create a new list item
        self.actuator_widget_items.setdefault(address, {})[name] = item
        item.setSizeHint(new_widget.sizeHint())           # set the size of the item
        self.list_widget.addItem(item)                    # add the new item in the list
        self.list_widget.setItemWidget(item, new_widget)  # assign the new widget to the item
        try: 
            self.actuator_widgets[address][name].update_position(position)
        except Exception as e:
            log.error(f'Could not update position {e}')

    def get_all_actuators_config(self) -> dict:
        config = dict({})
        for address, motor in self.actuator_widgets.items():
            for name, widget in motor.items():
                if widget.scan: 
                    log.debug(f'Address: {address}, name: {name}')
                    attr_dict = widget.get_attributes()
                    config.setdefault(address, {})[name] = attr_dict
                    
                else: 
                    log.info(f'{address}, {name} is set as not scanned')

        return config




if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = ActuatorsPanel()
    
    actuators = {'tcp://147.250.140.85:5555': ['name1', 'name2', 'name3'], 
            'tcp://147.250.140.86:5555': ['name4', 'name5', 'name6'],
            'tcp://147.250.140.87:5555': ['name', 'name_', 'name+']}

    for address, name_list in actuators.items():
        for name in name_list :
            window.add_actuator_widget(address, name)
    window.resize(350, 150)
    window.show()

    sys.exit(app.exec())