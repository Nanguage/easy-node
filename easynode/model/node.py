import typing as T

from ..widgets.node_item import NodeItem
from ..setting import NodeViewSetting

if T.TYPE_CHECKING:
    from ..widgets.scene import GraphicsScene
    from qtpy.QtWidgets import QWidget


class Port():
    def __init__(self, name: str) -> None:
        self.name = name
        self.node: T.Optional[Node] = None


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


class Node(object):
    def __init__(
            self,
            type_name: str,
            name: str,
            input_ports: T.Optional[T.List[Port]] = None,
            output_ports: T.Optional[T.List[Port]] = None,
            widget: T.Optional["QWidget"] = None
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
        self.widget = widget

    @property
    def title(self) -> str:
        return self.type_name + ": " + self.name

    def create_view(
            self, scene: "GraphicsScene",
            setting: T.Optional[NodeViewSetting] = None):
        view = NodeItem(None, self, setting)
        scene.addItem(view)
