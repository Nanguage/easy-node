import typing as T
from qtpy import QtWidgets, QtGui

from ..setting import PortItemSetting  # type: ignore


class PortItem(QtWidgets.QGraphicsItem):
    def __init__(
            self,
            parent: T.Optional[QtWidgets.QWidget] = None,
            setting: T.Optional["PortItemSetting"] = None
            ) -> None:
        super().__init__(parent)
        if setting is None:
            setting = PortItemSetting()
        self.setting = setting

    def init_pen_and_brush(self):
        QColor = QtGui.QColor
        QPen = QtGui.QPen
        QBrush = QtGui.QBrush
        setting = self.setting
        self.pen = QPen(
            QColor(setting.color_outline),
            setting.outline_width)
        self.brush = QBrush(QColor(setting.color_background))

    def paint(self,
              painter: QtGui.QPainter,
              option: QtWidgets.QStyleOptionGraphicsItem,
              widget: T.Optional[QtWidgets.QWidget] = None):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        radius = self.setting.radius
        painter.drawEllipse(
            -radius, -radius, radius * 2, radius * 2)
