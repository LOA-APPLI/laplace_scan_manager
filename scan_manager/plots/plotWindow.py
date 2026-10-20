from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout
)

from .graphs import GraphMaker

from PyQt6.QtGui import QIcon
import pathlib
import qdarkstyle
from laplace_log import log

class PlotWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.set_up()

    def set_up(self):

        p = pathlib.Path(__file__)
        self.setVisible(False)

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

    def add_plot(self, plotType: str, axes: tuple):
        self.setVisible(True)
        self.plot_type = plotType
        if plotType == 'x-y':
            self.variables = axes[0:1]
        else : 
            pass
        log.info(f'Plot type: {plotType}, axes: {axes}')


        