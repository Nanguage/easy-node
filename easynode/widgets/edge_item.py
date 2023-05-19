import typing as T
from qtpy import QtWidgets, QtGui, QtCore

from ..setting import EdgeItemSetting  # type: ignore

if T.TYPE_CHECKING:
    from ..model import Edge  # type: ignore


class EdgeItem(QtWidgets.QGraphicsPathItem):
    def __init__(
            self, parent: QtWidgets.QWidget,
            edge: "Edge",
            setting: T.Optional[EdgeItemSetting] = None):
        super().__init__(parent=parent)
        if setting is None:
            setting = EdgeItemSetting()
        self.setting = setting
        self.edge = edge
        self.setup_pens_and_brushs()
        self.setFlag(
            QtWidgets.QGraphicsItem.ItemIsSelectable)  # type: ignore

    def setup_pens_and_brushs(self):
        self._pen = QtGui.QPen(
            QtGui.QColor(self.setting.color),
            self.setting.width)
        self._pen_selected = QtGui.QPen(
            QtGui.QColor(self.setting.color_selected),
            self.setting.width)
        self._brush = QtCore.Qt.NoBrush

    def update_path(self):
        style = self.setting.style
        if style == "direct":
            self.update_path_direct()
        else:
            self.update_path_bazel()

    def update_path_direct(self):
        source_pos = self.edge.source_port.item.scenePos()
        target_pos = self.edge.target_port.item.scenePos()
        path = QtGui.QPainterPath(source_pos)
        path.lineTo(target_pos)
        self.setPath(path)

    def update_path_bazel(self):
        path = QtGui.QPainterPath()
        s = self.edge.source_port.item.scenePos()
        t = self.edge.target_port.item.scenePos()
        dist = (t.x() - s.x()) * 0.5
        if s.x() > t.x():
            dist *= -1
        path.moveTo(s.x(), s.y())
        path.cubicTo(
            s.x() + dist, s.y(),
            t.x() - dist, t.y(),
            t.x(), t.y()
        )
        self.setPath(path)

    def paint(
            self,
            painter: QtGui.QPainter,
            option: QtWidgets.QStyleOptionGraphicsItem,
            widget: T.Optional[QtWidgets.QWidget] = None
            ) -> None:
        self.update_path()
        if self.isSelected():
            painter.setPen(self._pen_selected)
        else:
            painter.setPen(self._pen)
        painter.setBrush(self._brush)
        painter.drawPath(self.path())
