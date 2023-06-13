import typing as T

from qtpy import QtCore

from ..graphics.edge_item import EdgeItem
from ..setting import EdgeItemSetting

if T.TYPE_CHECKING:
    from .port import Port
    from .graph import Graph


class Edge(QtCore.QObject):
    selected_changed = QtCore.Signal(bool)

    def __init__(
            self, source_port: "Port", target_port: "Port",
            item_setting: T.Optional[EdgeItemSetting] = None,
            ) -> None:
        super().__init__()
        self.source_port = source_port
        self.target_port = target_port
        self.item: T.Optional[EdgeItem] = None
        self.graph: T.Optional["Graph"] = None
        self.item_setting = item_setting

    def create_item(
            self,
            setting: T.Optional[EdgeItemSetting] = None,
            ) -> "EdgeItem":
        setting = self.item_setting or setting
        item = EdgeItem(self, None, setting)
        if self.source_port.item is not None:
            item.update_path()
        self.item = item
        return item

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Edge):
            return NotImplemented
        return (
            (self.source_port == other.source_port) and
            (self.target_port == other.target_port)
        )

    def __hash__(self):
        s_port = self.source_port
        t_port = self.target_port
        s_node = s_port.node
        t_node = t_port.node
        return hash((
            (id(s_node), s_port.index),
            (id(t_node), t_port.index)
        ))
