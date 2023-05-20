import typing as T
from qtpy import QtWidgets, QtGui, QtCore

from ..setting import EdgeItemSetting  # type: ignore

if T.TYPE_CHECKING:
    from ..model import Edge, Port  # type: ignore


class EdgeItemBase(QtWidgets.QGraphicsPathItem):
    def __init__(
            self, parent: T.Optional[QtWidgets.QGraphicsItem] = None,
            setting: T.Optional[EdgeItemSetting] = None):
        super().__init__(parent)
        if setting is None:
            setting = EdgeItemSetting()
        self.setting = setting
        self.setup_pens_and_brushs()

    def setup_pens_and_brushs(self):
        self._pen = QtGui.QPen(
            QtGui.QColor(self.setting.color),
            self.setting.width)
        self._set_pen_style(self._pen, self.setting.style)
        self._pen_selected = QtGui.QPen(
            QtGui.QColor(self.setting.color_selected),
            self.setting.width_selected)
        self._set_pen_style(self._pen_selected, self.setting.style_selected)
        self._brush = QtCore.Qt.NoBrush

    @staticmethod
    def _set_pen_style(pen: QtGui.QPen, style: str):
        if style == "dashed":
            pen.setStyle(QtCore.Qt.DashLine)  # type: ignore
        elif style == "dotted":
            pen.setStyle(QtCore.Qt.DotLine)  # type: ignore
        else:
            pen.setStyle(QtCore.Qt.SolidLine)  # type: ignore

    @property
    def source_pos(self) -> QtCore.QPointF:
        pass

    @property
    def target_pos(self) -> QtCore.QPointF:
        pass

    def update_path(self):
        is_bazel = self.setting.bazel
        if not is_bazel:
            self.update_path_direct()
        else:
            self.update_path_bazel()

    def update_path_direct(self):
        source_pos = self.source_pos
        target_pos = self.target_pos
        path = QtGui.QPainterPath(source_pos)
        path.lineTo(target_pos)
        self.setPath(path)

    def update_path_bazel(self):
        path = QtGui.QPainterPath()
        s = self.source_pos
        t = self.target_pos
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


class EdgeItem(EdgeItemBase):
    def __init__(
            self, edge: "Edge",
            parent: T.Optional[QtWidgets.QGraphicsItem] = None,
            setting: T.Optional[EdgeItemSetting] = None):
        super().__init__(parent, setting)
        self.edge = edge
        self.setFlag(
            QtWidgets.QGraphicsItem.ItemIsSelectable)  # type: ignore

    @property
    def source_pos(self) -> QtCore.QPointF:
        return self.edge.source_port.item.scenePos()

    @property
    def target_pos(self) -> QtCore.QPointF:
        return self.edge.target_port.item.scenePos()


class EdgeDragItem(EdgeItemBase):
    def __init__(
            self, fixed_port: "Port",
            parent: QtWidgets.QGraphicsItem,
            setting: T.Optional[EdgeItemSetting] = None
            ) -> None:
        super().__init__(parent, setting)
        self.fixed_port = fixed_port
        self.movable_pos = fixed_port.item.scenePos()

    @property
    def source_pos(self) -> QtCore.QPointF:
        if self.fixed_port.type == "in":
            return self.movable_pos
        else:
            return self.fixed_port.item.scenePos()

    @property
    def target_pos(self) -> QtCore.QPointF:
        if self.fixed_port.type == "in":
            return self.fixed_port.item.scenePos()
        else:
            return self.movable_pos
