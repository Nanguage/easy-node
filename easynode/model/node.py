import typing as T
from copy import copy

from qtpy import QtCore

from .port import Port
from ..graphics.node_item import NodeItem
from ..setting import NodeItemSetting

if T.TYPE_CHECKING:
    from qtpy.QtWidgets import QWidget
    from .edge import Edge


class Node(QtCore.QObject):
    selected_changed = QtCore.Signal(bool)
    position_changed = QtCore.Signal(QtCore.QPointF)

    _instance_count = 0
    input_ports: T.List[Port] = []
    output_ports: T.List[Port] = []
    item_setting: NodeItemSetting = NodeItemSetting()
    theme_color: str = "#ffffff"

    def __init__(
            self,
            name: T.Optional[str] = None,
            **attrs
            ) -> None:
        super().__init__()
        self.status = "normal"
        if name is None:
            name = str(self._instance_count)
        self.name = name
        self.__class__._instance_count += 1
        self._init_ports()
        self.widget: T.Optional["QWidget"] = self.create_widget()
        self.item: T.Optional["NodeItem"] = None
        self.item_setting = copy(self.item_setting)
        self.item_setting.title_color = self.theme_color
        self.attrs = attrs
        self.position_changed.connect(self._on_position_changed)
        self._title = self.type_name() + ": " + self.name

    @classmethod
    def type_name(cls) -> str:
        return cls.__name__

    def create_widget(self) -> T.Optional["QWidget"]:
        return None

    def create_edge(
            self, other: "Node",
            source_port_idx: int, target_port_idx: int) -> "Edge":
        from .edge import Edge
        source_port = self.output_ports[source_port_idx]
        target_port = other.input_ports[target_port_idx]
        e = Edge(source_port, target_port)
        return e

    def _init_ports(self):
        cls = self.__class__
        input_ports = [
            port.blueprint_copy() for port in cls.input_ports
        ]
        output_ports = [
            port.blueprint_copy() for port in cls.output_ports
        ]
        self.input_ports = input_ports
        self.output_ports = output_ports
        for tp, ports in zip(("in", "out"), (input_ports, output_ports)):
            for port in ports:
                port.type = tp
                port.node = self

    def _on_position_changed(self, pos: QtCore.QPointF):
        pos_attr = [pos.x(), pos.y()]
        self.attrs['pos'] = pos_attr

    @property
    def id(self) -> int:
        return id(self)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value
        if self.item is not None:
            self.item.update()

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f"{cls_name}({self.title})"

    def create_item(
            self,
            setting: T.Optional[NodeItemSetting] = None
            ) -> "NodeItem":
        setting = self.item_setting or setting
        item = NodeItem(self, None, setting)
        if 'pos' in self.attrs:
            pos = self.attrs['pos']
            assert isinstance(pos, list)
            item.setPos(*pos)
        self.item = item
        return item

    @property
    def input_edges(self) -> T.List["Edge"]:
        edges: T.List["Edge"] = []
        for port in self.input_ports:
            edges.extend(port.edges)
        return edges

    @property
    def output_edges(self) -> T.List["Edge"]:
        edges: T.List["Edge"] = []
        for port in self.output_ports:
            edges.extend(port.edges)
        return edges
