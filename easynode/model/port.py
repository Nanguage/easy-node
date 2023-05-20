import typing as T

if T.TYPE_CHECKING:
    from .node import Node
    from ..widgets.port_item import PortItem


class Port():
    def __init__(self, name: str) -> None:
        self.name = name
        self.node: T.Optional["Node"] = None
        self.item: T.Optional["PortItem"] = None
        self.type: T.Optional[str] = None


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
