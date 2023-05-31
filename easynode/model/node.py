import typing as T

from .port import Port
from ..widgets.node_item import NodeItem
from ..setting import NodeItemSetting

if T.TYPE_CHECKING:
    from ..widgets.scene import GraphicsScene
    from qtpy.QtWidgets import QWidget
    from .edge import Edge


class Node(object):
    def __init__(
            self,
            type_name: str,
            name: str,
            input_ports: T.Optional[T.List[Port]] = None,
            output_ports: T.Optional[T.List[Port]] = None,
            widget: T.Optional["QWidget"] = None,
            item_setting: T.Optional[NodeItemSetting] = None,
            **attrs
            ) -> None:
        self.type_name = type_name
        self.name = name
        self.widget: T.Optional["QWidget"] = None
        if input_ports is None:
            input_ports = []
        if output_ports is None:
            output_ports = []
        self.input_ports = input_ports
        self.output_ports = output_ports
        for port in input_ports:
            port.type = "in"
            port.node = self
        for port in output_ports:
            port.type = "out"
            port.node = self
        self.widget = widget
        self.item: T.Optional["NodeItem"] = None
        self.graph: T.Optional["GraphicsScene"] = None
        self.item_setting = item_setting
        self.attrs = attrs

    @property
    def id(self) -> int:
        return id(self)

    @property
    def title(self) -> str:
        return self.type_name + ": " + self.name

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f"{cls_name}({self.title})"

    def create_item(self, scene: "GraphicsScene"):
        item = NodeItem(None, self, self.item_setting)
        if 'pos' in self.attrs:
            pos = self.attrs['pos']
            assert isinstance(pos, tuple)
            item.setPos(*pos)
        scene.addItem(item)
        self.item = item

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
