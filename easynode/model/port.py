import typing as T

from ..widgets.port_item import PortItem

if T.TYPE_CHECKING:
    from .node import Node
    from .edge import Edge
    from ..widgets.scene import GraphicsScene
    from ..setting import PortItemSetting


class Port():
    def __init__(self, name: str) -> None:
        self.name = name
        self.node: T.Optional["Node"] = None
        self.item: T.Optional["PortItem"] = None
        self.type: T.Optional[str] = None
        self.edges: T.List["Edge"] = []

    @property
    def index(self) -> int:
        if self.node is None:
            raise ValueError("Node is not set")
        if self.type == "in":
            return self.node.input_ports.index(self)
        else:
            return self.node.output_ports.index(self)

    def create_item(
            self, scene: "GraphicsScene",
            setting: T.Optional["PortItemSetting"] = None):
        assert self.node is not None
        node_item = self.node.item
        assert node_item is not None
        ni_setting = node_item.setting
        item = PortItem(node_item, self, setting)
        y = node_item.header_height
        y += ni_setting.space_between_title_and_content
        y += ni_setting.port_setting.item_setting.radius
        y += ni_setting.port_setting.item_setting.outline_width
        y += ni_setting.port_setting.height * self.index
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
