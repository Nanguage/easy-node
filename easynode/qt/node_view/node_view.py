import typing as T
from dataclasses import dataclass

from qtpy import QtWidgets, QtGui, QtCore

if T.TYPE_CHECKING:
    from ...model.node import Node


@dataclass
class NodeViewSetting:
    title_color: str = "#ffffff"
    title_font_size: int = 10
    title_padding: float = 5.0
    title_area_height: float = 24.0
    title_area_color: str = "#FF33363"
    background_color: str = "#E0222222"
    default_width: float = 200.0
    outline_radius: float = 10.0
    outline_color: str = "#7F000000"  # alpha, R, G, B
    outline_color_selected: str = "#FFFFA637"


class NodeView(QtWidgets.QGraphicsItem):
    def __init__(
            self, parent: QtWidgets.QWidget,
            node: "Node",
            setting: T.Optional[NodeViewSetting] = None):
        super().__init__(parent=parent)
        if setting is None:
            setting = NodeViewSetting()
        self.setting = setting
        self.node = node
        self.init_layout()
        self.setup_pens_and_brushs()

    def setup_pens_and_brushs(self):
        QColor = QtGui.QColor
        QPen = QtGui.QPen
        QBrush = QtGui.QBrush
        setting = self.setting
        self.pen_outline = QPen(QColor(setting.outline_color))
        self.pen_outline_selected = QPen(QColor(setting.outline_color_selected))
        self.brush_title_area = QBrush(QColor(setting.title_area_color))
        self.brush_background = QBrush(QColor(setting.background_color))

    def init_layout(self):
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.init_title()
        self.init_content()

    def init_title(self):
        title_color = QtGui.QColor(self.setting.title_color)
        title_font = QtGui.QFont(None, self.setting.title_font_size)
        self.title = QtWidgets.QGraphicsTextItem(self)
        self.title.setDefaultTextColor(title_color)
        self.title.setFont(title_font)
        self.title.setPlainText(self.node.title)
        width, _ = self.size
        padding = self.setting.title_padding
        self.title.setPos(padding, 0)
        self.title.setTextWidth(width - 2 * padding)

    def init_content(self):
        if self.node.widget is not None:
            radius = self.setting.outline_radius
            title_height = self.setting.title_area_height
            width, height = self.size
            self.widget_proxy = QtWidgets.QGraphicsProxyWidget(self)
            self.node.widget.setGeometry(
                radius, title_height + radius,
                width - 2 * radius, height - 2 * radius - title_height
            )
            self.widget_proxy.setWidget(self.node.widget)

    def boundingRect(self) -> QtCore.QRectF:
        width, _ = self.size
        radius = self.setting.outline_radius
        x = 2 * width + radius
        return QtCore.QRectF(
            0, 0, x, x
        ).normalized()

    @property
    def size(self) -> T.Tuple[int, int]:
        width = self.setting.default_width
        height = 250
        return width, height

    def paint(self,
              painter: QtGui.QPainter,
              option: QtWidgets.QStyleOptionGraphicsItem,
              widget: T.Optional[QtWidgets.QWidget] = None) -> None:
        width, height = self.size
        title_height = self.setting.title_area_height
        outline_radius = self.setting.outline_radius
        # title area
        path_title = QtGui.QPainterPath()
        path_title.setFillRule(QtCore.Qt.WindingFill)
        path_title.addRoundedRect(0, 0, width, title_height, outline_radius, outline_radius)
        path_title.addRect(0, title_height - outline_radius, outline_radius, outline_radius)
        path_title.addRect(width - outline_radius, title_height - outline_radius, outline_radius, outline_radius)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.brush_title_area)
        painter.drawPath(path_title.simplified())
        # body area
        path_body = QtGui.QPainterPath()
        path_body.setFillRule(QtCore.Qt.WindingFill)
        path_body.addRoundedRect(0, title_height, width, height - title_height, outline_radius, outline_radius)
        path_body.addRect(0, title_height, outline_radius, outline_radius)
        path_body.addRect(width-outline_radius, title_height, outline_radius, outline_radius)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.brush_background)
        painter.drawPath(path_body.simplified())
        # outline
        path_outline = QtGui.QPainterPath()
        path_outline.addRoundedRect(0, 0, width, height, outline_radius, outline_radius)
        painter.setPen(self.pen_outline if not self.isSelected() else self.pen_outline_selected)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(path_outline)

