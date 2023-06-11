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
        self._setup_pens_and_brushs()

    def _setup_pens_and_brushs(self):
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
    def source_pos(self) -> QtCore.QPointF:  # type: ignore
        pass

    @property
    def target_pos(self) -> QtCore.QPointF:  # type: ignore
        pass

    def update_path(self):
        is_bazel = self.setting.bazel
        if not is_bazel:
            self._update_path_direct()
        else:
            self._update_path_bazel()

    def _update_path_direct(self):
        source_pos = self.source_pos
        target_pos = self.target_pos
        path = QtGui.QPainterPath(source_pos)
        path.lineTo(target_pos)
        self.setPath(path)

    def _update_path_bazel(self):
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

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemSelectedChange:
            self.edge.selected_changed.emit(value)
        return super().itemChange(change, value)

    @property
    def source_pos(self) -> QtCore.QPointF:
        item = self.edge.source_port.item
        assert item is not None
        return item.scenePos()

    @property
    def target_pos(self) -> QtCore.QPointF:
        item = self.edge.target_port.item
        assert item is not None
        return item.scenePos()

    def paint(
            self,
            painter: QtGui.QPainter,
            option: QtWidgets.QStyleOptionGraphicsItem,
            widget: T.Optional[QtWidgets.QWidget] = None
            ) -> None:
        if self.edge.source_port.item is None:
            return
        if self.edge.target_port.item is None:
            return
        super().paint(painter, option, widget)


class EdgeDragItem(EdgeItemBase):
    def __init__(
            self, fixed_port: "Port",
            parent: T.Optional[QtWidgets.QGraphicsItem] = None,
            setting: T.Optional[EdgeItemSetting] = None
            ) -> None:
        super().__init__(parent, setting)
        self.fixed_port = fixed_port
        assert fixed_port.item is not None
        self._fixed_item = fixed_port.item
        self.movable_pos = fixed_port.item.scenePos()

    @property
    def source_pos(self) -> QtCore.QPointF:
        if self.fixed_port.type == "in":
            pos = self.movable_pos
        else:
            pos = self._fixed_item.scenePos()
        return pos

    @property
    def target_pos(self) -> QtCore.QPointF:
        if self.fixed_port.type == "in":
            pos = self._fixed_item.scenePos()
        else:
            pos = self.movable_pos
        return pos

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(
            self.source_pos, self.target_pos).normalized()

    def create_edge(self, movable_port: "Port") -> "Edge":
        from ..model import Edge  # type: ignore
        if self.fixed_port.type == "in":
            if movable_port.type == "in":
                raise ValueError("Can't connect in to in")
            edge = Edge(movable_port, self.fixed_port)
        else:
            if movable_port.type == "out":
                raise ValueError("Can't connect out to out")
            edge = Edge(self.fixed_port, movable_port)
        if edge.source_port.node is edge.target_port.node:
            raise ValueError("Can't connect in the same node")
        return edge
