from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout
)

from .graphs import GraphMaker

from PyQt6.QtGui import QIcon
import pathlib
import qdarkstyle

import pandas as pd 
from laplace_log import log

class PlotWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.graphs = []
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

        self.panel_layout = QVBoxLayout(central_widget)

    def add_plot(self, plotType: str, axes: dict, plot_title: str="Plot title"):
        self.setVisible(True)
        log.info(f'Plot type: {plotType}, axes: {axes}')
        graph = GraphMaker.create(plot_type=plotType, axes=axes, title=plot_title)
        self.panel_layout.addWidget(graph.graph)
        self.graphs.append(graph)
        self.activateWindow()
        
    def update_plots(self, data:pd.DataFrame):
        for graph in self.graphs:
            graph.update(data)

