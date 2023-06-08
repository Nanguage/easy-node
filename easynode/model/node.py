import typing as T
from dataclasses import asdict

from qtpy import QtCore

from .port import Port, DataPort
from ..graphics.node_item import NodeItem
from ..setting import NodeItemSetting

if T.TYPE_CHECKING:
    from ..graphics.scene import GraphicsScene
    from qtpy.QtWidgets import QWidget
    from .edge import Edge


class Node(QtCore.QObject):
    selected_changed = QtCore.Signal(bool)
    position_changed = QtCore.Signal(QtCore.QPointF)

    def __init__(
            self,
            name: str,
            type_name: T.Optional[str] = None,
            input_ports: T.Optional[T.List[Port]] = None,
            output_ports: T.Optional[T.List[Port]] = None,
            widget: T.Optional["QWidget"] = None,
            item_setting: T.Optional[NodeItemSetting] = None,
            **attrs
            ) -> None:
        super().__init__()
        self.status = "normal"
        if type_name is None:
            type_name = self.__class__.__name__
        self.type_name = type_name
        self.name = name
        self.init_ports(input_ports, output_ports)
        self.widget: T.Optional["QWidget"] = widget
        self.item: T.Optional["NodeItem"] = None
        self.graph: T.Optional["GraphicsScene"] = None
        self.item_setting = item_setting
        self.attrs = attrs

    def init_ports(
            self,
            input_ports: T.Optional[T.List[Port]] = None,
            output_ports: T.Optional[T.List[Port]] = None
            ):
        if input_ports is None:
            input_ports = []
        if output_ports is None:
            output_ports = []
        self.input_ports = input_ports
        self.output_ports = output_ports
        for tp, ports in zip(("in", "out"), (input_ports, output_ports)):
            for port in ports:
                port.type = tp
                port.node = self

    @property
    def id(self) -> int:
        return id(self)

    @property
    def title(self) -> str:
        return self.type_name + ": " + self.name

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f"{cls_name}({self.title})"

    def create_item(
            self,
            setting: T.Optional[NodeItemSetting] = None
            ) -> "NodeItem":
        setting = self.item_setting or setting
        item = NodeItem(None, self, setting)
        if 'pos' in self.attrs:
            pos = self.attrs['pos']
            assert isinstance(pos, tuple)
            item.setPos(*pos)
        self.item = item
        return item

    @property
    def input_edges(self) -> T.List["Edge"]:
        edges = []
        for port in self.input_ports:
            edges.extend(port.edges)
        return edges

    @property
    def output_edges(self) -> T.List["Edge"]:
        edges = []
        for port in self.output_ports:
            edges.extend(port.edges)
        return edges

    def serialize(self) -> T.Dict[str, T.Any]:
        attrs = self.attrs.copy()
        if self.item is not None:
            attrs['pos'] = (self.item.pos().x(), self.item.pos().y())
        setting = None
        if self.item_setting is not None:
            setting = asdict(self.item_setting)
        return {
            "type_name": self.type_name,
            "name": self.name,
            "input_ports": [p.serialize() for p in self.input_ports],
            "output_ports": [p.serialize() for p in self.output_ports],
            "attrs": self.attrs,
            "setting": setting,
        }

    @classmethod
    def deserialize(
            cls,
            scene: "GraphicsScene",
            data: T.Dict[str, T.Any],
            ) -> "Node":
        editor = scene.editor
        type_name = data['type_name']
        if type_name in editor.factory_table:
            factory = editor.factory_table[type_name]
            node = factory.create_node()
            node.name = data['name']
        else:
            setting = cls._deserialize_setting(data['setting'])
            input_ports = cls._deserialize_ports(data['input_ports'])
            output_ports = cls._deserialize_ports(data['output_ports'])
            node = Node(
                data['name'],
                type_name=data['type_name'],
                input_ports=input_ports,
                output_ports=output_ports,
                setting=setting,
            )
        node.attrs = data['attrs']
        return node

    @staticmethod
    def _deserialize_setting(
            data: T.Optional[T.Dict[str, T.Any]]
            ) -> T.Optional[NodeItemSetting]:
        setting = None
        if data is not None:
            setting = NodeItemSetting(**data)
        return setting

    @staticmethod
    def _deserialize_ports(
            data: T.List[T.Dict[str, T.Any]],
            ) -> T.List[T.Union[Port, DataPort]]:
        ports = []
        port: T.Union[Port, DataPort]
        for port_data in data:
            if 'data_type' in port_data:
                port = DataPort.deserialize(port_data)
            else:
                port = Port.deserialize(port_data)
            ports.append(port)
        return ports
