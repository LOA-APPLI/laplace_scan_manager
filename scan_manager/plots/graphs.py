from .interface.graph_styleSheet import Dark_StyleSheet

from PyQt6.QtWidgets import QWidget
import pyqtgraph as pg
from collections import deque
from abc import abstractmethod


class Graph(QWidget):
    def __init__(self):
        super().__init__()

        self.graph = pg.GraphicsLayoutWidget()
        self.graph.ci.setContentsMargins(5, 5, 5, 5)
        self.plot = self.graph.addPlot()
        
        self.x_label = ""
        self.y_label = ""
        self.x_units = ""
        self.y_units = ""

        self.plot.setTitle("Graph title")

    @abstractmethod
    def update_graph(self, data: dict):
        pass

    @abstractmethod
    def clear_graph(self):
        pass


class RollingGraph(Graph, Dark_StyleSheet):
    def __init__(self):
        super().__init__(device)
        
        self.x = deque(maxlen=1000)
        self.y = deque(maxlen=1000)
        self.set_dark_mode()
        self.set_labels() # From Dark_StyleSheet
   
    def update_graph(self, data: dict):
        x = data.get('x', 0)
        y = data.get('y', 0)
        self.x.append(x)
        self.y.append(y)
        self.curve.setData(list(self.x), list(self.y))

    def clear_graph(self):
        self.x.clear()
        self.y.clear()



class StaticGraph(Graph, Dark_StyleSheet):
    def __init__(self):
        super().__init__(device)
        self.set_dark_mode()
        self.set_axes() # From Dark_StyleSheet
        self.set_labels() # From Dark_StyleSheet

    def update_graph(self, data: dict):
        self.x = data.get('x', 0)
        self.y = data.get('y', 0)
        self.curve.setData(list(self.x), list(self.y))

class DensityGraph(Graph, Dark_StyleSheet):
    def __init__(self):
        super().__init__()
        
        self.img_item = pg.ImageItem()
        self.plot.addItem(self.img_item)    
        self.plot.setAspectLocked(True, ratio=1.0)      

        self.set_2D_plot_darkstyle()

    def resize(self, w_h_tuple: tuple): 
        width, height = w_h_tuple
        width = int(width/10)
        height = int(height/10)
        self.plot.setAspectLocked(True, ratio=width/height)
        self.img_item.setRect(0, 0, width, height)
        for axis in ['left', 'bottom', 'right', 'top']:
            self.plot.hideAxis(axis)
          
    def update_graph(self, data: dict):
        image = data.get('image', None)
        if image is not None:
            self.img_item.setImage(image)  # Transpose for correct orientation


class GraphMaker:
    _graph_types = {
        'x-y': RollingGraph,
        'multi x-y': StaticGraph,
        'xyz': DensityGraph}

    @classmethod
    def create(cls, graph_type) -> Graph:
        graph_type = device.graph_type
        graph_type_class = cls._graph_types.get(graph_type)
        if graph_type is None:
            pass
        elif not graph_type_class:
            raise ValueError(f"Unknown graph type: {graph_type}")
        return graph_type_class(device)
    
class GraphUpdater:
    def __init__(self, graph: Graph):
        self.graph = graph
    
    def update(self, data: dict):
        """Update the graph with new data - delegates to graph's own method"""
        self.graph.update_graph(data)



if __name__ == "__main__":
    app = pg.mkQApp()
    device_def = dict({('name', 'Dummy device 1'),
                             ('address', ""),
                             ('type', 'dummy device 2D')})
    device = Devices.DeviceMaker.create(device_def)
    print(device)
    graph = GraphMaker.create(device)
    graph.graph.setGeometry(100, 30, 800, 400)
    graph.graph.show()
    pg.exec()