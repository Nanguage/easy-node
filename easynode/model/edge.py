import typing as T

from .port import Port

from ..widgets.edge_item import EdgeItem
from ..setting import EdgeItemSetting

if T.TYPE_CHECKING:
    from ..widgets.scene import GraphicsScene
    from .graph import Graph


class Edge:
    def __init__(
            self, source_port: Port, target_port: Port,
            item_setting: T.Optional[EdgeItemSetting] = None,
            ) -> None:
        self.source_port = source_port
        self.target_port = target_port
        self.item: T.Optional[EdgeItem] = None
        self.graph: T.Optional["Graph"] = None
        self.item_setting = item_setting

    def create_item(self, scene: "GraphicsScene"):
        item = EdgeItem(self, None, self.item_setting)
        scene.addItem(item)
        self.item = item
