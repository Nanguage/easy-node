import typing as T
from .node import Node
from .edge import Edge
from ..utils import layout_graph

if T.TYPE_CHECKING:
    from ..widgets.scene import GraphicsScene


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
            setting = self.scene.editor.setting.node_item_setting
            node.create_item(self.scene)
            if node.item_setting is None:
                node.item_setting = setting

    def remove_node(self, node: Node):
        self.nodes.remove(node)
        if self.scene:
            self.scene.removeItem(node.item)
        for port in node.input_ports:
            for edge in port.edges:
                self.remove_edge(edge)
        for port in node.output_ports:
            for edge in port.edges:
                self.remove_edge(edge)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)
        if self.scene:
            edge.create_item(self.scene)
            setting = self.scene.editor.setting.edge_item_setting
            if edge.item_setting is None:
                edge.item_setting = setting
        edge.source_port.edges.append(edge)
        edge.target_port.edges.append(edge)

    def remove_edge(self, edge: Edge):
        self.edges.remove(edge)
        edge.source_port.edges.remove(edge)
        edge.target_port.edges.remove(edge)
        if self.scene:
            self.scene.removeItem(edge.item)

    def create_items(self):
        if self.scene:
            editor_setting = self.scene.editor.setting
            for node in self.nodes:
                node.create_item(self.scene)
                if node.item_setting is None:
                    node.item_setting = editor_setting.node_item_setting
            for edge in self.edges:
                edge.create_item(self.scene)
                if edge.item_setting is None:
                    edge.item_setting = editor_setting.edge_item_setting

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
