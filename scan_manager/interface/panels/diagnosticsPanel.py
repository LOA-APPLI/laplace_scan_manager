# libraries
import sys
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout,
    QListWidget, QListWidgetItem,
    QApplication
)
from laplace_log import log

# project

from ..widgets.diagnostic_control_widget import DiagnosticControlWidget


class DiagnosticsPanel(QGroupBox):

    def __init__(self):        
        super().__init__("Diagnostics")

        self.diagnostic_widgets = dict({})
        self.set_up()  # build the elements
        self.actions() # defines the panel actions

    def set_up(self) -> None:
        '''
        Build the panel widgets.
        '''
        panel_layout = QVBoxLayout(self)   # create the layout
        self.list_widget = QListWidget()   # create the widget list
        panel_layout.addWidget(self.list_widget)  # add the widget list to the layout


    def add_diagnostic_widgets_from_status(self, address: str, status: dict):
        new_widget = DiagnosticControlWidget(address=address, status=status)

        self.diagnostic_widgets[address] = new_widget
        item = QListWidgetItem(self.list_widget)          # create a new list item
        item.setSizeHint(new_widget.sizeHint())           # set the size of the item
        self.list_widget.addItem(item)                    # add the new item in the list
        self.list_widget.setItemWidget(item, new_widget)  # assign the new widget to the item


    def update_diagnostic_widget(self, address: str, status: dict) -> None:

        try:
            diagnostic_widget = self.diagnostic_widgets[address]
        except Exception as e :
            log.error(f'self.diagnostic_widget[address] could not be accessed {e}')
            return
        try : 

            diagnostic_widget.update_status_available(True)
        except Exception as e:
            log.error(f'Could not update position: {e}')

    def update_diagnostic_unavailable(self, address):
        diagnostic_widget = self.diagnostic_widgets.get(address)
        diagnostic_widget.update_status_available(False)

    def actions(self):
        pass

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = DiagnosticsPanel()
    
    diagnostics = {'tcp://147.250.140.85:5555': ['name1', 'name2', 'name3'], 
            'tcp://147.250.140.86:5555': ['name4', 'name5', 'name6'],
            'tcp://147.250.140.87:5555': ['name', 'name_', 'name+']}

    for address, name_list in diagnostics.items():
        for name in name_list :
            window.add_diagnostic_widget(address, name)
    window.resize(350, 150)
    window.show()

    sys.exit(app.exec())