from .interface.graph_styleSheet import Dark_StyleSheet

from PyQt6.QtWidgets import QWidget
import pyqtgraph as pg
from abc import abstractmethod

import pandas as pd
from laplace_log import log

class Graph(QWidget):
    def __init__(self, axes: dict, title: str):
        super().__init__()

        self.graph = pg.GraphicsLayoutWidget()
        self.graph.ci.setContentsMargins(5, 5, 5, 5)
        self.plot = self.graph.addPlot()
        
        self.x_label = axes['x']
        self.y_label = axes['y']
        self.x_units = ""
        self.y_units = ""

        self.plot.setTitle(title)

    @abstractmethod
    def update(self, data: pd.DataFrame):
        pass

    @abstractmethod
    def clear_graph(self):
        pass

class XYGraph(Graph, Dark_StyleSheet):
    def __init__(self, axes: dict, title):
        super().__init__(axes=axes, title=title)
        self.set_dark_mode()
        self.set_axes() # From Dark_StyleSheet
        self.set_labels() # From Dark_StyleSheet
        self.axes = {k: axes[k] for k in ['x', 'y']}
        self.data = {}

    def update(self, data: pd.DataFrame):
        x_values = data[self.axes['x']].tolist()
        y_values = data[self.axes['y']].tolist()   
        log.info(f'x-values: {x_values}, y-values: {y_values}')    
        self.curve.setData(list(x_values), list(y_values))
        
class GraphMaker:
    _plot_types = {
        'x-y': XYGraph,
        'multi x-y': XYGraph}

    @classmethod
    def create(cls, plot_type, axes, title) -> Graph:
        plot_type_class = cls._plot_types.get(plot_type)
        if plot_type is None:
            pass
        elif not plot_type_class:
            raise ValueError(f"Unknown graph type: {plot_type}")
        return plot_type_class(axes, title=title)
    


