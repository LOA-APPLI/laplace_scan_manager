# libraries
import sys
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel,
    QApplication, QTableWidget, 
    QTableWidgetItem
)
from PyQt6.QtCore import pyqtSignal
from laplace_log import log


class ScanPanel(QGroupBox):
    load_scan_config_signal = pyqtSignal()
    start_scan_signal = pyqtSignal(dict)
    stop_scan_signal = pyqtSignal()

    def __init__(self):        
        super().__init__("Scan config")

        self.set_up()  # build the elements
        self.actions() # defines the panel actions
        self.scan_settings = dict({})

    def set_up(self) -> None:

        self.scan_table = QTableWidget()
        self.scan_table.setColumnCount(6)
        self.scan_table.setHorizontalHeaderLabels(
            ["Rank", "Address", "Control", "Range", "Step", "Points"]
        )

        self.total_points_label = QLabel("0 points")

        self.load_button = QPushButton("Load")
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scan_table)
        main_layout.addWidget(self.total_points_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        main_layout.addLayout(button_layout)

    def actions(self):
        # click load button to emit signal caught by ScanWindow
        self.load_button.clicked.connect(self.load_scan_config_signal)
        self.start_button.clicked.connect(self.start_scan)
        #self.stop_button.clicked.connect(self.stop_scan_signal)

    def start_scan(self):
        """Emit the start_scan_signal with the current scan settings."""
        if self.scan_settings:
            self.start_scan_signal.emit(self.scan_settings)
        else:
            log.warning("No scan settings available to start the scan.")

    def load_scan_config(self, settings: dict) -> None:
        """Load scan settings into the scan table."""
        
        self.scan_table.setRowCount(0)
        total_points = 1
        for address, controls in settings.items():
            sorted_controls = sorted(
                controls.items(),
                key=lambda item: item[1]['rank']
            )
            self.scan_settings[address] = sorted_controls
            for name, scan in sorted_controls:
                current = scan['current']
                start = scan['start']
                stop = scan['stop']
                spacing = scan['step']
                rank = scan['rank']

                # Number of positions, including both endpoints.
                if spacing != 0:
                    points = int(round((stop - start) / spacing)) + 1
                else:
                    points = 1
                total_points *= points

                row = self.scan_table.rowCount()
                self.scan_table.insertRow(row)

                # Rank
                self.scan_table.setItem(
                    row, 0,
                    QTableWidgetItem(str(rank))
                )

                # Address
                self.scan_table.setItem(
                    row, 1,
                    QTableWidgetItem(str(address))
                )

        #        # Control name
                self.scan_table.setItem(
                    row, 2,
                    QTableWidgetItem(name)
                )

        #         # Range
                range_text = f"{start:g} → {stop:g}"
                self.scan_table.setItem(
                    row, 3 ,
                    QTableWidgetItem(range_text)
                )

        #         # Spacing
                spacing_text = f"{spacing:g}"
                self.scan_table.setItem(
                    row, 4,
                    QTableWidgetItem(spacing_text)
                )

        #         # Number of points
                self.scan_table.setItem(
                    row, 5,
                    QTableWidgetItem(str(points))
                )
     
        self.total_points_label.setText(
            f"{total_points:,} scan points"
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = ScanPanel()
    scan_settings = {
        1: {
            "name": "X position",
            "start": -2,
            "stop": 2,
            "spacing": 0.2,
            "unit": "mm",
        },
        2: {
            "name": "Y position",
            "start": 10,
            "stop": 50,
            "spacing": 5,
            "unit": "mm",
        },
    }
    window.load_scan_settings(scan_settings)
    window.resize(600, 300)
    window.show()

    sys.exit(app.exec())