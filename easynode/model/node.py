import typing as T

from .port import Port
from ..widgets.node_item import NodeItem
from ..setting import NodeItemSetting

if T.TYPE_CHECKING:
    from ..widgets.scene import GraphicsScene
    from qtpy.QtWidgets import QWidget


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
            setting: T.Optional[NodeItemSetting] = None):
        view = NodeItem(None, self, setting)
        scene.addItem(view)
