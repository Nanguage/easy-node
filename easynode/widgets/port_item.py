import typing as T
from qtpy import QtWidgets, QtGui, QtCore

from ..setting import PortItemSetting  # type: ignore

if T.TYPE_CHECKING:
    from ..model.port import Port  # type: ignore


class PortItem(QtWidgets.QGraphicsItem):
    def __init__(
            self,
            parent: T.Optional[QtWidgets.QWidget] = None,
            port: "Port" = None,
            setting: T.Optional["PortItemSetting"] = None
            ) -> None:
        super().__init__(parent)
        self.port = port
        if setting is None:
            setting = PortItemSetting()
        self.setting = setting
        self.setAcceptHoverEvents(True)
        self.hovered = False
        self.setup_pens_and_brushs()

    def setup_pens_and_brushs(self):
        QColor = QtGui.QColor
        QPen = QtGui.QPen
        QBrush = QtGui.QBrush
        setting = self.setting
        self.pen = QPen(
            QColor(setting.color_outline),
            setting.outline_width)
        self.brush = QBrush(QColor(setting.color_background))
        self.brush_hovered = QBrush(QColor(
            setting.color_background_hover))

    def hoverEnterEvent(self, event) -> None:
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event) -> None:
        self.hovered = False
        self.update()

    def paint(self,
              painter: QtGui.QPainter,
              option: QtWidgets.QStyleOptionGraphicsItem,
              widget: T.Optional[QtWidgets.QWidget] = None):
        if self.hovered:
            painter.setBrush(self.brush_hovered)
        else:
            painter.setBrush(self.brush)
        painter.setPen(self.pen)
        radius = self.setting.radius
        painter.drawEllipse(
            -radius, -radius, radius * 2, radius * 2)

    def boundingRect(self) -> QtCore.QRectF:
        radius = self.setting.radius
        outline_width = self.setting.outline_width
        return QtCore.QRectF(
            -radius - outline_width, -radius - outline_width,
            radius * 2 + outline_width * 2, radius * 2 + outline_width * 2
        ).normalized()
