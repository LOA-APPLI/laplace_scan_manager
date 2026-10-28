from .interface.graph_styleSheet import Dark_StyleSheet

from PyQt6.QtWidgets import QWidget
import pyqtgraph as pg
from abc import abstractmethod

import pandas as pd
from laplace_log import log
from typing import Optional

class Graph(QWidget):
    def __init__(self, title: str, axes: dict, labels: Optional[dict] = None):
        super().__init__()

        if labels is None:
            labels = axes
        self.graph = pg.GraphicsLayoutWidget()
        self.graph.ci.setContentsMargins(5, 5, 5, 5)
        self.plot = self.graph.addPlot()
        
        self.x_label = labels['x']
        self.y_label = labels['y']
        self.x_units = ""
        self.y_units = ""

        self.plot.setTitle(title)

    @abstractmethod
    def update(self, data: pd.DataFrame, actuators: list[str]): 
        pass

    @abstractmethod
    def clear_graph(self):
        pass

class Multi_XY(Graph, Dark_StyleSheet):
    def __init__(self, axes: dict, title, labels: Optional[dict] = None):
        super().__init__(axes=axes, title=title, labels=labels)

        self.data = {}
        self.tolerances = {}
        self.set_dark_mode(); self.set_axes(); self.set_labels()
        self.axes = {k: axes[k] for k in ['x', 'y']}

        self.legend = self.plot.addLegend()
        self.curves = {}        # key -> PlotDataItem
        self.names = {}         # key -> currently displayed name

    def _set_legend_name(self, key, item, name):
        if self.names.get(key) == name:
            return
        if self.names.get(key):             # already in legend: remove, then re-add
            self.legend.removeItem(item)
        if name:
            self.legend.addItem(item, name)
        self.names[key] = name


    def update(self, data, actuators):
        x, y = self.axes['x'], self.axes['y']
        group_by = [a for a in actuators if a in data.columns and a not in (x, y)]
        curves = self.split_into_curves(data, group_by, self.tolerances)

        varying = [i for i in range(len(group_by))
                if len({k[i] for k, _, _ in curves}) > 1]

        for key, label, sub in curves:
            item = self.curves.get(key)
            if item is None:
                pen = pg.mkPen(pg.intColor(len(self.curves), hues=9), width=2)
                item = self.plot.plot(pen=pen, symbol='o')
                self.curves[key] = item
            item.setData(sub[x].to_numpy(), sub[y].to_numpy())

            name = ", ".join(f"{group_by[i]}={label[group_by[i]]:g}" for i in varying)
            self._set_legend_name(key, item, name)



    def split_into_curves(self, df: pd.DataFrame, group_by: list[str],
                        tolerances: dict[str, float] | None = None):
        """Return a list of (key, label, sub_df), one entry per curve.

        Rows belong to the same curve when all `group_by` actuators have the
        same value (within tolerance). Acquisition order is preserved.
        """
        tolerances = tolerances or {}
        if not group_by:
            return [((), {}, df)]

        keys = [
            (df[a] / tolerances[a]).round() if tolerances.get(a) else df[a]
            for a in group_by
        ]
        curves = []
        for key, sub in df.groupby(keys, sort=False, dropna=False):
            key = key if isinstance(key, tuple) else (key,)
            label = {a: sub[a].iloc[0] for a in group_by}
            curves.append((key, label, sub))
        return curves

class XYGraph(Graph, Dark_StyleSheet):
    def __init__(self, axes: dict, title, labels: Optional[dict] = None):
        super().__init__(axes=axes, title=title, labels=labels)
        self.set_dark_mode()
        self.set_axes() # From Dark_StyleSheet
        self.set_labels() # From Dark_StyleSheet
        self.axes = {k: axes[k] for k in ['x', 'y']}
        self.data = {}

    def update(self, data: pd.DataFrame, actuators: list[str]= []):
        x_values = data[self.axes['x']].tolist()
        y_values = data[self.axes['y']].tolist()   
        log.info(f'x-values: {x_values}, y-values: {y_values}')    
        self.curve.setData(list(x_values), list(y_values))
        
class GraphMaker:
    _plot_types = {
        'x-y': XYGraph,
        'multi x-y': Multi_XY}

    @classmethod
    def create(cls, plot_type, title, axes, labels: Optional[dict] = None) -> Graph:
        plot_type_class = cls._plot_types.get(plot_type)
        if plot_type is None:
            pass
        elif not plot_type_class:
            raise ValueError(f"Unknown graph type: {plot_type}")
        return plot_type_class(axes, title=title, labels=labels)
    


