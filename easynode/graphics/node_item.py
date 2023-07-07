import typing as T
from enum import Enum

from qtpy import QtWidgets, QtGui, QtCore

from ..setting import NodeItemSetting  # type: ignore
from ..model.port import DataPort  # type: ignore
from .port_item import PortItem

if T.TYPE_CHECKING:
    from ..model import Node, Port  # type: ignore
    from .view import GraphicsView


class NodeTitleItem(QtWidgets.QGraphicsTextItem):
    def __init__(self, parent: "NodeItem"):
        super().__init__(parent=parent)
        self.node_item = node_item = parent
        setting = node_item.setting
        title_color = QtGui.QColor(setting.title_color)
        title_font = QtGui.QFont(
            setting.title_font_family,
            setting.title_font_size)
        self.setDefaultTextColor(title_color)
        self.setFont(title_font)
        self.setPlainText(node_item.node.title)
        padding = setting.title_padding
        self.setPos(padding, 0)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)  # type: ignore
        self._edit_mode = False

    def start_edit(self):
        if self._edit_mode:
            return
        self._edit_mode = True
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)  # type: ignore
        self.setFocus()

    def finish_edit(self):
        self._edit_mode = False
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)  # type: ignore
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)
        self.clearFocus()
        self.node_item.node.title = self.toPlainText()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:  # type: ignore
            self.finish_edit()
        else:
            super().keyPressEvent(event)

    def focusOutEvent(self, event):
        self.finish_edit()
        super().focusOutEvent(event)


class MovementState(Enum):
    mouse_pressed = 0
    mouse_released = 1
    position_changed = 2


class NodeItem(QtWidgets.QGraphicsItem):
    def __init__(
            self,
            node: "Node",
            parent: T.Optional[QtWidgets.QGraphicsItem] = None,
            setting: T.Optional[NodeItemSetting] = None):
        super().__init__(parent=parent)
        if setting is None:
            setting = NodeItemSetting()
        self.setting: NodeItemSetting = setting
        self.node = node
        self._init_layout()
        self._setup_pens_and_brushs()
        self.painted = False
        self.setZValue(1)
        self._movement_state = MovementState.mouse_released
        self._movement_start_pos = QtCore.QPointF(0, 0)

    @property
    def view(self) -> "GraphicsView":
        return self.scene().views()[0]

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        child_item = self.get_item_at(event.scenePos())
        if isinstance(child_item, PortItem):
            child_item.mousePressEvent(event)
        else:
            self._movement_state = MovementState.mouse_pressed
            self._movement_start_pos = self.pos()
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        if self._movement_state == MovementState.position_changed:
            pos_diff = self.pos() - self._movement_start_pos
            self.view.selected_node_items_moved.emit(pos_diff)
        self._movement_state = MovementState.mouse_released
        super().mouseReleaseEvent(event)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemSelectedChange:
            self.node.selected_changed.emit(value)
        elif change == QtWidgets.QGraphicsItem.ItemPositionChange:
            self.node.position_changed.emit(value)
            if self._movement_state == MovementState.mouse_pressed:
                self._movement_state = MovementState.position_changed
        return super().itemChange(change, value)

    def get_item_at(
            self, pos: QtCore.QPointF
            ) -> T.Optional[QtWidgets.QGraphicsItem]:
        return self.scene().itemAt(
            pos.x(), pos.y(), QtGui.QTransform())

    def _setup_pens_and_brushs(self):
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
        self.brush_status = {
            status: QBrush(QColor(color))
            for status, color in setting.status_to_color.items()
        }

    def _init_layout(self):
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        self._init_content()
        self._init_title()

    def _init_title(self):
        self.title = NodeTitleItem(self)

    def _init_content(self):
        self.content_widget = widget = QtWidgets.QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        self._init_ports(layout)
        if self.node.widget is not None:
            self.node.widget.setParent(widget)
            self.node.widget.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.node.widget)
        title_height = self.setting.title_area_height
        outline_width = self.setting.outline_width
        widget.move(outline_width, title_height)
        self.widget_proxy = QtWidgets.QGraphicsProxyWidget(parent=self)
        self.widget_proxy.setWidget(widget)

    def _init_ports(self, layout: QtWidgets.QVBoxLayout):
        in_ports = self.node.input_ports
        out_ports = self.node.output_ports
        ports_widget = QtWidgets.QWidget(parent=self.content_widget)
        ports_layout = QtWidgets.QVBoxLayout()
        space = self.setting.space_between_title_and_content
        ports_layout.setContentsMargins(0, space, 0, 0)
        ports_layout.setSpacing(0)
        ports_widget.setLayout(ports_layout)
        max_port_idx = max(len(in_ports), len(out_ports))
        for idx in range(max_port_idx):
            row = QtWidgets.QWidget(parent=ports_widget)
            row_layout = QtWidgets.QHBoxLayout()
            row_layout.setContentsMargins(0, 0, 0, 0)
            row.setLayout(row_layout)
            row.setFixedHeight(self.setting.port_setting.height)
            for tp, ports in zip(['in', 'out'], [in_ports, out_ports]):
                if idx < len(ports):
                    port = ports[idx]
                    port_label = self._get_port_label(port, tp)
                    row_layout.addWidget(port_label)
                    row_layout.setSpacing(1)
                    if tp == 'in':
                        if isinstance(port, DataPort):
                            port_widget = port.get_port_widget()
                            row_layout.addWidget(port_widget)
                        row_layout.addSpacing(
                            self.setting.port_setting.space_between_in_and_out)
                        row_layout.addStretch()
                else:
                    row_layout.addStretch()
            ports_layout.addWidget(row)
        layout.addWidget(ports_widget)

    def _get_port_label(
            self, port: "Port", tp: str,
            ) -> QtWidgets.QLabel:
        align_left = QtCore.Qt.AlignLeft  # type: ignore
        align_right = QtCore.Qt.AlignRight  # type: ignore
        align_v_center = QtCore.Qt.AlignVCenter  # type: ignore
        setting = self.setting.port_setting
        padding = setting.item_setting.radius
        port_label = QtWidgets.QLabel(port.name)
        if tp == 'in':
            port_label.setAlignment(align_left | align_v_center)
            port_label.setStyleSheet(
                f"padding-left: {padding}px; color: white;")
        else:
            port_label.setAlignment(align_right | align_v_center)
            port_label.setStyleSheet(
                f"padding-right: {padding + 3}px; color: white;")
        font = QtGui.QFont(
            setting.label_font_family,
            setting.label_font_size)
        port_label.setFont(font)
        return port_label

    def boundingRect(self) -> QtCore.QRectF:
        width, height = self.size
        return QtCore.QRectF(
            0, 0, width, height
        ).normalized()

    @property
    def width(self) -> float:
        min_width = max(
            self.setting.default_width,
            self.title.boundingRect().width(),
            self.content_widget.width()
        )
        if self.node.widget is not None:
            w = max(self.node.widget.width(), min_width)
        else:
            w = max(self.content_widget.width(), min_width)
        w += 2 * self.setting.outline_width
        return w

    @property
    def height(self) -> float:
        h = (
            self.setting.title_area_height
            + self.setting.outline_radius
            + self.content_widget.height()
        )
        return h

    @property
    def size(self) -> T.Tuple[float, float]:
        return self.width, self.height

    @property
    def header_height(self) -> float:
        return (
            self.setting.title_area_height +
            self.setting.status_bar_height
        )

    def paint(self,
              painter: QtGui.QPainter,
              option: QtWidgets.QStyleOptionGraphicsItem,
              widget: T.Optional[QtWidgets.QWidget] = None) -> None:
        if not self.painted:  # first paint
            self.painted = True
            self._init_port_items()
        self._paint_title(painter)
        self._paint_status_bar(painter)
        self._paint_body(painter)
        self._paint_outline(painter)

    def _paint_title(self, painter: QtGui.QPainter):
        width = self.width
        height = self.setting.title_area_height
        outline_radius = self.setting.outline_radius
        path_title = QtGui.QPainterPath()
        path_title.setFillRule(QtCore.Qt.WindingFill)  # type: ignore
        path_title.addRoundedRect(
            0, 0, width, height, outline_radius, outline_radius)
        path_title.addRect(
            0, height - outline_radius, outline_radius, outline_radius)
        path_title.addRect(
            width - outline_radius, height - outline_radius,
            outline_radius, outline_radius)
        painter.setPen(QtCore.Qt.NoPen)  # type: ignore
        painter.setBrush(self.brush_title_area)
        painter.drawPath(path_title.simplified())

    def _paint_status_bar(self, painter: QtGui.QPainter):
        height = self.setting.status_bar_height
        width = self.width
        title_height = self.setting.title_area_height
        path_status_bar = QtGui.QPainterPath()
        path_status_bar.setFillRule(QtCore.Qt.WindingFill)  # type: ignore
        path_status_bar.addRect(0, title_height, width, height)
        painter.setPen(QtCore.Qt.NoPen)  # type: ignore
        status = self.node.status
        painter.setBrush(self.brush_status[status])
        painter.drawPath(path_status_bar.simplified())

    def _paint_body(self, painter: QtGui.QPainter):
        header_height = self.header_height
        width = self.width
        body_height = self.height - header_height
        outline_radius = self.setting.outline_radius
        path_body = QtGui.QPainterPath()
        path_body.setFillRule(QtCore.Qt.WindingFill)  # type: ignore
        path_body.addRoundedRect(
            0, header_height, width, body_height,
            outline_radius, outline_radius)
        path_body.addRect(0, header_height, outline_radius, outline_radius)
        path_body.addRect(
            width-outline_radius, header_height,
            outline_radius, outline_radius)
        painter.setPen(QtCore.Qt.NoPen)  # type: ignore
        painter.setBrush(self.brush_background)
        painter.drawPath(path_body.simplified())

    def _paint_outline(self, painter: QtGui.QPainter):
        width, height = self.size
        outline_radius = self.setting.outline_radius
        path_outline = QtGui.QPainterPath()
        path_outline.addRoundedRect(
            0, 0, width, height, outline_radius, outline_radius)
        painter.setPen(
            self.pen_outline if not self.isSelected()
            else self.pen_outline_selected)
        painter.setBrush(QtCore.Qt.NoBrush)  # type: ignore
        painter.drawPath(path_outline)

    def _init_port_items(self):
        in_ports = self.node.input_ports
        out_ports = self.node.output_ports
        for ports in [in_ports, out_ports]:
            for port in ports:
                port.create_item()
