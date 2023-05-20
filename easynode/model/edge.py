import typing as T

from .port import Port

from ..widgets.edge_item import EdgeItem
from ..setting import EdgeItemSetting

if T.TYPE_CHECKING:
    from ..widgets.scene import GraphicsScene


class Edge:
    def __init__(
            self, source_port: Port, target_port: Port,
            ) -> None:
        self.source_port = source_port
        self.target_port = target_port
        self.item: T.Optional[EdgeItem] = None

    def create_item(
            self, scene: "GraphicsScene",
            setting: T.Optional[EdgeItemSetting] = None):
        item = EdgeItem(self, None, setting)
        scene.addItem(item)
        self.item = item
