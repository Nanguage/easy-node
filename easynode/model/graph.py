import typing as T
from qtpy import QtCore
import json

from .node import Node
from .edge import Edge
from ..utils import layout_graph
from ..utils.serialization import (
    serialize_nodes_and_edges,
    deserialize_graph
)

if T.TYPE_CHECKING:
    from ..graphics.scene import GraphicsScene
    from ..node_editor import NodeEditor


class Graph(QtCore.QObject):
    elements_changed = QtCore.Signal()
    node_added = QtCore.Signal(Node)
    node_removed = QtCore.Signal(Node)
    edge_added = QtCore.Signal(Edge)
    edge_removed = QtCore.Signal(Edge)

    def __init__(
            self,
            scene: T.Optional["GraphicsScene"] = None,
            ) -> None:
        super().__init__()
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
        self.node_added.emit(node)
        self.elements_changed.emit()  # type: ignore

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
        self.node_removed.emit(node)
        self.elements_changed.emit()  # type: ignore

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
        self.edge_added.emit(edge)
        self.elements_changed.emit()  # type: ignore

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
        self.edge_removed.emit(edge)
        self.elements_changed.emit()  # type: ignore

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

    def serialize(self) -> str:
        data = serialize_nodes_and_edges(self.nodes, self.edges)
        return json.dumps(data)

    @staticmethod
    def deserialize(
            data_str: str,
            editor: "NodeEditor",
            add_to_editor: bool = True,
            ) -> 'Graph':
        data = json.loads(data_str)
        return deserialize_graph(data, editor, add_to_editor)


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

    def _get_nodes_item_bounding_rect(self) -> QtCore.QRectF:
        rect = QtCore.QRectF()
        for node in self.nodes:
            assert node.item is not None
            rect = rect.united(node.item.sceneBoundingRect())
        return rect

    def join(
            self,
            graph: Graph,
            pos: T.Optional[QtCore.QPointF] = None,
            ) -> None:
        graph.add_nodes(*self.nodes)
        if pos is not None:
            bounding_rect = self._get_nodes_item_bounding_rect()
            top_left = bounding_rect.topLeft()
            for node in self.nodes:
                assert node.item is not None
                attr_pos = node.attrs.get("pos")
                if attr_pos is not None:
                    p = QtCore.QPointF(*attr_pos)
                    node.item.setPos(p)
                offset = node.item.pos() - top_left
                new_pos = pos + offset
                node.item.setPos(new_pos)
        graph.add_edges(*self.edges)
        scene = graph.scene
        assert scene is not None
        scene.clearSelection()
        for node in self.nodes:
            assert node.item is not None
            node.item.setSelected(True)
