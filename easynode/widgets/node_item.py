import typing as T

from qtpy import QtWidgets, QtGui, QtCore

from ..setting import NodeItemSetting  # type: ignore

if T.TYPE_CHECKING:
    from ..model import Node, Port  # type: ignore


class NodeItem(QtWidgets.QGraphicsItem):
    def __init__(
            self, parent: QtWidgets.QWidget,
            node: "Node",
            setting: T.Optional[NodeItemSetting] = None):
        super().__init__(parent=parent)
        if setting is None:
            setting = NodeItemSetting()
        self.setting: NodeItemSetting = setting
        self.node = node
        self.init_layout()
        self.setup_pens_and_brushs()

    def setup_pens_and_brushs(self):
        QColor = QtGui.QColor
        QPen = QtGui.QPen
        QBrush = QtGui.QBrush
        setting = self.setting
        self.pen_outline = QPen(
            QColor(setting.outline_color),
            setting.outline_width)
        self.pen_outline_selected = QPen(
            QColor(setting.outline_color_selected),
            setting.outline_width)
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
        width = self.width
        padding = self.setting.title_padding
        self.title.setPos(padding, 0)
        self.title.setTextWidth(width - 2 * padding)

    def init_content(self):
        self.content_widget = widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        self.init_ports(layout)
        if self.node.widget is not None:
            self.node.widget.setParent(widget)
            self.node.widget.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.node.widget)
        title_height = self.setting.title_area_height
        outline_width = self.setting.outline_width
        widget.move(outline_width, title_height)
        self.widget_proxy = QtWidgets.QGraphicsProxyWidget(parent=self)
        self.widget_proxy.setWidget(widget)

    def init_ports(self, layout: QtWidgets.QVBoxLayout):
        in_ports = self.node.input_ports
        out_ports = self.node.output_ports
        ports_widget = QtWidgets.QWidget()
        ports_layout = QtWidgets.QVBoxLayout()
        ports_layout.setContentsMargins(0, 0, 0, 0)
        ports_widget.setLayout(ports_layout)
        max_port_idx = max(len(in_ports), len(out_ports))
        for idx in range(max_port_idx):
            port_widget = QtWidgets.QWidget()
            port_layout = QtWidgets.QHBoxLayout()
            port_layout.setContentsMargins(0, 0, 0, 0)
            port_widget.setLayout(port_layout)
            for tp, ports in zip(['in', 'out'], [in_ports, out_ports]):
                port = ports[idx]
                port_label = self._get_port_label(port, tp)
                if idx < len(ports):
                    port_layout.addWidget(port_label)
                else:
                    port_layout.addStretch()
            ports_layout.addWidget(port_widget)
        layout.addWidget(ports_widget)

    def _get_port_label(
            self, port: "Port", tp: str,
            ) -> QtWidgets.QLabel:
        padding = self.setting.port_setting.item_setting.radius
        port_label = QtWidgets.QLabel(port.name)
        if tp == 'in':
            port_label.setAlignment(
                QtCore.Qt.AlignLeft)  # type: ignore
            port_label.setStyleSheet(f"padding-left: {padding}px")
        else:
            port_label.setAlignment(
                QtCore.Qt.AlignRight)  # type: ignore
            port_label.setStyleSheet(f"padding-right: {padding}px")
        return port_label

    def boundingRect(self) -> QtCore.QRectF:
        width, height = self.size
        return QtCore.QRectF(
            0, 0, width, height
        ).normalized()

    @property
    def width(self) -> float:
        if self.node.widget is not None:
            width = self.node.widget.width()
        else:
            width = self.setting.default_width
        width += 2 * self.setting.outline_width
        return width

    @property
    def height(self) -> float:
        height = (
            self.setting.title_area_height
            + self.setting.outline_radius
            + self.content_widget.height()
        )
        return height

    @property
    def size(self) -> T.Tuple[float, float]:
        return self.width, self.height

    def paint(self,
              painter: QtGui.QPainter,
              option: QtWidgets.QStyleOptionGraphicsItem,
              widget: T.Optional[QtWidgets.QWidget] = None) -> None:
        width, height = self.size
        title_height = self.setting.title_area_height
        outline_radius = self.setting.outline_radius
        self.paint_title(width, title_height, outline_radius, painter)
        self.paint_body(width, height, title_height, outline_radius, painter)
        self.paint_outline(width, height, outline_radius, painter)

    def paint_title(
            self, width: float, title_height: float,
            outline_radius: float, painter: QtGui.QPainter):
        path_title = QtGui.QPainterPath()
        path_title.setFillRule(QtCore.Qt.WindingFill)  # type: ignore
        path_title.addRoundedRect(
            0, 0, width, title_height, outline_radius, outline_radius)
        path_title.addRect(
            0, title_height - outline_radius, outline_radius, outline_radius)
        path_title.addRect(
            width - outline_radius, title_height - outline_radius,
            outline_radius, outline_radius)
        painter.setPen(QtCore.Qt.NoPen)  # type: ignore
        painter.setBrush(self.brush_title_area)
        painter.drawPath(path_title.simplified())

    def paint_body(
            self, width: float, height: float, title_height: float,
            outline_radius: float, painter: QtGui.QPainter):
        path_body = QtGui.QPainterPath()
        path_body.setFillRule(QtCore.Qt.WindingFill)  # type: ignore
        path_body.addRoundedRect(
            0, title_height, width, height - title_height,
            outline_radius, outline_radius)
        path_body.addRect(0, title_height, outline_radius, outline_radius)
        path_body.addRect(
            width-outline_radius, title_height, outline_radius, outline_radius)
        painter.setPen(QtCore.Qt.NoPen)  # type: ignore
        painter.setBrush(self.brush_background)
        painter.drawPath(path_body.simplified())

    def paint_outline(
            self, width: float, height: float,
            outline_radius: float, painter: QtGui.QPainter):
        path_outline = QtGui.QPainterPath()
        path_outline.addRoundedRect(
            0, 0, width, height, outline_radius, outline_radius)
        painter.setPen(
            self.pen_outline if not self.isSelected()
            else self.pen_outline_selected)
        painter.setBrush(QtCore.Qt.NoBrush)  # type: ignore
        painter.drawPath(path_outline)
