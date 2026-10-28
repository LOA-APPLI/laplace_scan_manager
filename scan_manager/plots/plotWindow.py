from PyQt6.QtWidgets import (
    QMainWindow, QWidget, 
    QVBoxLayout, QHBoxLayout, 
    QGridLayout, QLabel,
    QComboBox, QPushButton
)

from .graphs import GraphMaker

from PyQt6.QtGui import QIcon
import pathlib
import qdarkstyle
from typing import Optional

import pandas as pd 
from laplace_log import log

class PlotWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.graphs = []
        self.set_up()
        self.actions()

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

        self.panel_layout = QHBoxLayout(central_widget)

        self.graph_layout = QVBoxLayout()
        self.taskbar_layout = QVBoxLayout()

        self.remove_graph = QPushButton("Remove graph")
        self.target_graph = QComboBox()

        self.taskbar_layout.addWidget(self.remove_graph)
        self.taskbar_layout.addWidget(self.target_graph)

        self.panel_layout.addLayout(self.graph_layout)
        self.panel_layout.addLayout(self.taskbar_layout)

    def actions(self) -> None:
        self.remove_graph.clicked.connect(self.destroy_graph)

    def destroy_graph(self) -> None:
        index = self.target_graph.currentIndex()
        graph = self.graphs.pop(index)
        self.graph_layout.removeWidget(graph.graph)
        graph.graph.deleteLater()
        self.target_graph.removeItem(index)

           
    def add_plot(self, plotType: str, axes: dict, plot_title: str="Plot title", labels: Optional[dict] = None):
        self.setVisible(True)
        log.info(f'Plot type: {plotType}, axes: {axes}')
        graph = GraphMaker.create(plot_type=plotType, axes=axes, title=plot_title, labels=labels)
        self.graph_layout.addWidget(graph.graph)
        self.graphs.append(graph)
        self.activateWindow()
        self.target_graph.addItem(plot_title)

    def update_plots(self, data, actuators):
        for graph in self.graphs:
            graph.update(data, actuators)

