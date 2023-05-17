import typing as T
from .node import Node
from .edge import Edge


class Graph:
    def __init__(self) -> None:
        self.nodes: T.Dict[str, Node] = dict()
        self.edges: T.Dict[str, Edge] = dict()

    def add_node(self, node: Node):
        pass

    def remove_node(self, node: Node):
        pass

    def add_edge(self, edge: Edge):
        pass

    def remove_edge(self, edge: Edge):
        pass
