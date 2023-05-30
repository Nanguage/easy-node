import math
import typing as T

from qtpy import QtWidgets, QtCore, QtGui

from ..model.graph import Graph  # type: ignore

if T.TYPE_CHECKING:
    from ..node_editor import NodeEditor  # type: ignore


class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, editor: "NodeEditor"):
        super().__init__(editor)
        setting = self.setting = editor.setting.graphics_scene_setting
        w, h = setting.width, setting.height
        self.setSceneRect(0, 0, w, h)
        self.setBackgroundBrush(QtGui.QColor(setting.background_color))
        self.pen_grid_dense = QtGui.QPen(
            QtGui.QColor(self.setting.grid_color_dense))
        self.pen_grid_loose = QtGui.QPen(
            QtGui.QColor(self.setting.grid_color_loose))
        self.editor: T.Optional["NodeEditor"] = None
        self.graph = Graph(self)

    @property
    def graph(self) -> Graph:
        return self._graph

    @graph.setter
    def graph(self, graph: Graph) -> None:
        self._graph = graph
        graph.scene = self
        if self.editor:
            editor_setting = self.editor.setting
            for node in graph.nodes:
                node.create_item(self, editor_setting.node_item_setting)
            for edge in graph.edges:
                edge.create_item(self, editor_setting.edge_item_setting)

    def drawBackground(
            self, painter: QtGui.QPainter,
            rect: T.Union[QtCore.QRectF, QtCore.QRect]) -> None:
        super().drawBackground(painter, rect)
        if self.setting.draw_grid:
            grid_size = self.setting.grid_size
            ratio = self.setting.grid_loose_per_dense
            l, r, t, b = [
                math.floor(rect.left()),
                math.ceil(rect.right()),
                math.floor(rect.top()),
                math.ceil(rect.bottom()),
            ]
            first_l = l - (l % grid_size)
            first_t = t - (t % grid_size)
            lines_dense = []
            lines_loose = []
            for x in range(first_l, r, grid_size):
                line = QtCore.QLineF(x, t, x, b)
                if x % (grid_size * ratio) != 0:
                    lines_dense.append(line)
                else:
                    lines_loose.append(line)
            for y in range(first_t, b, grid_size):
                line = QtCore.QLineF(l, y, r, y)
                if y % (grid_size * ratio) != 0:
                    lines_dense.append(line)
                else:
                    lines_loose.append(line)

            painter.setPen(self.pen_grid_dense)
            painter.drawLines(lines_dense)
            painter.setPen(self.pen_grid_loose)
            painter.drawLines(lines_loose)
