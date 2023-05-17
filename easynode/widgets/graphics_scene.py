import math
import typing as T
from dataclasses import dataclass

from qtpy import QtWidgets, QtCore, QtGui


@dataclass
class GraphicsSceneSetting:
    width: int = 8000
    height: int = 8000
    background_color: str = "#393939"
    draw_grid: bool = True
    grid_size: int = 25
    grid_color_dense: str = "#2f2f2f"
    grid_color_loose: str = "#191919"
    grid_loose_per_dense: int = 4


class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(
            self,
            parent: T.Optional[QtWidgets.QWidget] = None,
            setting: T.Optional[GraphicsSceneSetting] = None):
        super().__init__(parent)
        if setting is None:
            setting = GraphicsSceneSetting()
        self.setting = setting
        w, h = setting.width, setting.height
        self.setSceneRect(0, 0, w, h)
        self.setBackgroundBrush(QtGui.QColor(setting.background_color))
        self.pen_grid_dense = QtGui.QPen(
            QtGui.QColor(self.setting.grid_color_dense))
        self.pen_grid_loose = QtGui.QPen(
            QtGui.QColor(self.setting.grid_color_loose))

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
