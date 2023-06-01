import typing as T

from qtpy import QtCore, QtWidgets

from ..graphics.port_item import PortItem
from .edge import Edge
from ..setting import PortSetting

if T.TYPE_CHECKING:
    from .node import Node
    from ..graphics.scene import GraphicsScene


class Port(QtCore.QObject):
    edge_added = QtCore.Signal(Edge)
    edge_removed = QtCore.Signal(Edge)

    def __init__(
            self, name: str,
            setting: T.Optional["PortSetting"] = None
            ) -> None:
        super().__init__()
        self.name = name
        self.node: T.Optional["Node"] = None
        self.item: T.Optional["PortItem"] = None
        self.type: T.Optional[str] = None
        self.edges: T.List["Edge"] = []
        self.edge_added.connect(self.on_edge_added)
        self.edge_removed.connect(self.on_edge_removed)
        self._setting = setting

    @property
    def setting(self) -> "PortSetting":
        if self._setting is not None:
            return self._setting
        else:
            node = self.node
            if (node is not None) and (node.item is not None):
                return node.item.setting.port_setting
            else:
                return PortSetting()

    def on_edge_added(self, edge: Edge):
        self.edges.append(edge)

    def on_edge_removed(self, edge: Edge):
        self.edges.remove(edge)

    @property
    def index(self) -> int:
        if self.node is None:
            raise ValueError("Node is not set")
        if self.type == "in":
            return self.node.input_ports.index(self)
        else:
            return self.node.output_ports.index(self)

    def create_item(self, scene: "GraphicsScene"):
        assert self.node is not None
        node_item = self.node.item
        assert node_item is not None
        ni_setting = node_item.setting
        item = PortItem(
            self, node_item, self.setting.item_setting)
        y = node_item.header_height
        y += ni_setting.space_between_title_and_content
        y += self.setting.height * self.index
        y += self.setting.height / 2
        y -= self.setting.item_setting.radius / 2
        if self.type == 'in':
            item.setPos(0, y)
        else:
            item.setPos(node_item.width, y)
        self.item = item


class DataPort(Port):
    def __init__(
            self, name: str,
            data_type: type = object,
            data_range: object = None,
            data_default: object = None) -> None:
        super().__init__(name)
        self.data_type = data_type
        self.data_range = data_range
        self.data_default = data_default
        self.widget: T.Optional[QtWidgets.QWidget] = None

    @property
    def is_active(self) -> bool:
        return len(self.edges) == 0

    def on_edge_added(self, edge: Edge):
        super().on_edge_added(edge)
        if (not self.is_active) and (self.widget):
            self.widget.setEnabled(False)

    def on_edge_removed(self, edge: Edge):
        super().on_edge_removed(edge)
        if self.is_active and (self.widget):
            self.widget.setEnabled(True)

    def get_port_widget(self) -> QtWidgets.QWidget:
        from ..widgets.port_widget import (
            TextPortWidget, IntPortWidget
        )
        if self.data_type is str:
            self.widget = TextPortWidget(self)
        elif self.data_type is int:
            self.widget = IntPortWidget(self)
        else:
            self.data_default = None
            self.widget = TextPortWidget(self)
        return self.widget
