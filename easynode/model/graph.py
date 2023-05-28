import typing as T
from .node import Node
from .edge import Edge

if T.TYPE_CHECKING:
    from ..widgets.scene import GraphicsScene


class Graph:
    def __init__(self, scene: "GraphicsScene") -> None:
        self.nodes: T.List[Node] = []
        self.edges: T.List[Edge] = []
        self.scene = scene

    def add_node(self, node: Node):
        self.nodes.append(node)
        setting = self.scene.editor.setting.node_item_setting
        node.create_item(self.scene, setting)

    def remove_node(self, node: Node):
        self.nodes.remove(node)
        self.scene.removeItem(node.item)
        for port in node.input_ports:
            for edge in port.edges:
                self.remove_edge(edge)
        for port in node.output_ports:
            for edge in port.edges:
                self.remove_edge(edge)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)
        setting = self.scene.editor.setting.edge_item_setting
        edge.create_item(self.scene, setting)
        edge.source_port.edges.append(edge)
        edge.target_port.edges.append(edge)

    def remove_edge(self, edge: Edge):
        self.edges.remove(edge)
        edge.source_port.edges.remove(edge)
        edge.target_port.edges.remove(edge)
        self.scene.removeItem(edge.item)
