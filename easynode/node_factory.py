import typing as T

from .model import Node
from .widgets.node_list import NodeList


class NodeFactoryTable(object):
    def __init__(self) -> None:
        self.table: T.Dict[str, T.Type[Node]] = {}

    def register(self, *factories: T.Type[Node]) -> None:
        for factory in factories:
            self.table[factory.type_name()] = factory

    def create_node_list_widget(self) -> NodeList:
        return NodeList(node_factory_table=self)

    def __getitem__(self, key: str) -> T.Type[Node]:
        return self.table[key]

    def __contains__(self, key: str) -> bool:
        return key in self.table
