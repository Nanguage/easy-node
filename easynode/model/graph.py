import typing as T

from .node import Node
from .edge import Edge
from ..utils import layout_graph

if T.TYPE_CHECKING:
    from ..graphics.scene import GraphicsScene


class Graph:
    def __init__(
            self,
            scene: T.Optional["GraphicsScene"] = None,
            ) -> None:
        self.nodes: T.List[Node] = []
        self.edges: T.List[Edge] = []
        self.scene: T.Optional["GraphicsScene"] = scene

    def add_node(self, node: Node):
        self.nodes.append(node)
        if self.scene:
            editor = self.scene.editor  # type: ignore
            setting = editor.setting.node_item_setting
            if node.item is None:
                node.create_item(setting)
            assert node.item is not None
            self.scene.addItem(node.item)

    def add_nodes(self, *nodes: Node):
        for node in nodes:
            self.add_node(node)

    def remove_node(self, node: Node):
        if node not in self.nodes:
            return
        self.nodes.remove(node)
        if self.scene:
            assert node.item is not None
            self.scene.removeItem(node.item)
        for edge in node.input_edges + node.output_edges:
            self.remove_edge(edge)

    def add_edge(self, edge: Edge):
        if edge in self.edges:
            return
        self.edges.append(edge)
        edge.source_port.edge_added.emit(edge)
        edge.target_port.edge_added.emit(edge)
        if self.scene:
            editor = self.scene.editor  # type: ignore
            setting = editor.setting.edge_item_setting
            if edge.item is None:
                edge.create_item(setting)
            assert edge.item is not None
            self.scene.addItem(edge.item)

    def add_edges(self, *edges: Edge):
        for edge in edges:
            self.add_edge(edge)

    def remove_edge(self, edge: Edge):
        if edge not in self.edges:
            return
        self.edges.remove(edge)
        edge.source_port.edge_removed.emit(edge)
        edge.target_port.edge_removed.emit(edge)
        if self.scene:
            assert edge.item is not None
            self.scene.removeItem(edge.item)

    def create_items(self):
        if self.scene:
            es = self.scene.editor.setting
            for node in self.nodes:
                node.create_item(es.node_item_setting)
                self.scene.addItem(node.item)
            for edge in self.edges:
                edge.create_item(es.edge_item_setting)
                self.scene.addItem(edge.item)

    def auto_layout(
            self,
            direction: str = "LR",
            padding_level: int = 100,
            padding_node: int = 20,
            ) -> None:
        if self.scene:
            layout_graph(
                self, direction=direction,
                padding_level=padding_level,
                padding_node=padding_node
            )
        else:
            raise ValueError("Scene is not set")

    def sub_graph(self, nodes: T.List[Node]) -> "SubGraph":
        return SubGraph(nodes)


class SubGraph:
    def __init__(
            self,
            nodes: T.List[Node],
            ) -> None:
        self.nodes = nodes
        self.edges = self.get_edges()

    def get_edges(self) -> T.List[Edge]:
        edges = set()
        for node in self.nodes:
            for edge in node.input_edges + node.output_edges:
                s_node = edge.source_port.node
                t_node = edge.target_port.node
                if (s_node in self.nodes) and (t_node in self.nodes):
                    edges.add(edge)
        return list(edges)
