import typing as T
from dataclasses import asdict

if T.TYPE_CHECKING:
    from ..node_editor import NodeEditor
    from ..model.port import Port
    from ..model.node import Node
    from ..model.edge import Edge
    from ..model.graph import SubGraph, Graph


def serialize_port(port: "Port") -> T.Dict[str, T.Any]:
    from ..model.port import DataPort
    data: T.Dict[str, T.Any] = {
        "name": port.name,
        "type": port.type,
        "setting": asdict(port.setting),
    }
    if isinstance(port, DataPort):
        widget_value = None
        if port.widget is not None:
            widget_value = port.widget.value
        data.update({
            "data_type": port.data_type.__name__,
            "data_range": port.data_range,
            "data_default": port.data_default,
            "widget_args": port.widget_args,
            "widget_value": widget_value,
        })
    return data


def serialize_node(node: "Node") -> T.Dict[str, T.Any]:
    attrs = node.attrs.copy()
    if node.item is not None:
        attrs['pos'] = [node.item.pos().x(), node.item.pos().y()]
    setting = None
    if node.item_setting is not None:
        setting = asdict(node.item_setting)
    return {
        "id": id(node),
        "type_name": node.type_name(),
        "name": node.name,
        "input_ports": [serialize_port(p) for p in node.input_ports],
        "output_ports": [serialize_port(p) for p in node.output_ports],
        "attrs": node.attrs,
        "setting": setting,
    }


def deserialize_node(
        data: T.Dict[str, T.Any],
        editor: "NodeEditor"
        ) -> "Node":
    type_name = data['type_name']
    if type_name in editor.factory_table:
        node = deserialize_node_with_factory(data, editor)
    else:
        raise ValueError(f"Unknown node type: {type_name}")
    node.attrs = data['attrs']
    return node


def deserialize_node_with_factory(
        data: T.Dict[str, T.Any],
        editor: "NodeEditor",
        ) -> "Node":
    from ..model.port import DataPort
    type_name = data['type_name']
    factory = editor.factory_table[type_name]
    node = factory()
    node.name = data['name']
    for port in node.input_ports:
        if isinstance(port, DataPort):
            port_data = data['input_ports'][port.index]
            assert isinstance(port_data, dict)
            widget_value = port_data.get("widget_value")
            port.widget_init_value = widget_value
    return node


def serialize_edge(edge: "Edge") -> T.Dict[str, T.Any]:
    s_port = edge.source_port
    t_port = edge.target_port
    assert s_port.node is not None
    assert t_port.node is not None
    return {
        "source": {
            "node_id": id(s_port.node),
            "port_idx": s_port.index,
        },
        "target": {
            "node_id": id(t_port.node),
            "port_idx": t_port.index,
        },
    }


def deserialize_edges(
        edges_data: T.List[T.Dict[str, T.Any]],
        id2node: T.Dict[int, "Node"],
        ) -> T.List["Edge"]:
    from ..model.edge import Edge
    edges = []
    for edge_data in edges_data:
        s_data = edge_data['source']
        t_data = edge_data['target']
        source_node = id2node[s_data['node_id']]
        target_node = id2node[t_data['node_id']]
        source_port = source_node.output_ports[s_data['port_idx']]
        target_port = target_node.input_ports[t_data['port_idx']]
        edge = Edge(source_port, target_port)
        edges.append(edge)
        source_port.edge_added.emit(edge)
        target_port.edge_added.emit(edge)
    return edges


def serialize_nodes_and_edges(
        nodes: T.List["Node"],
        edges: T.List["Edge"],
        ) -> T.Dict[str, T.Any]:
    nodes_data = [serialize_node(node) for node in nodes]
    edges_data = [serialize_edge(edge) for edge in edges]
    return {
        "nodes": nodes_data,
        "edges": edges_data,
    }


def serialize_subgraph(
        graph: "SubGraph",
        ) -> T.Dict[str, T.Any]:
    nodes = graph.nodes
    edges = graph.edges
    data = serialize_nodes_and_edges(nodes, edges)
    data.update({
        "type": "subgraph",
    })
    return data


def deserialize_nodes_and_edges(
        data: T.Dict[str, T.Any],
        editor: "NodeEditor",
        ) -> T.Tuple[T.List["Node"], T.List["Edge"]]:
    nodes: T.List["Node"] = []
    id2node: T.Dict[int, "Node"] = {}
    for node_data in data['nodes']:
        node = deserialize_node(node_data, editor)
        nodes.append(node)
        id2node[node_data['id']] = node
    edges = deserialize_edges(data['edges'], id2node)
    return nodes, edges


def deserialize_subgraph(
        data: T.Dict[str, T.Any],
        editor: "NodeEditor",
        ) -> "SubGraph":
    from ..model.graph import SubGraph
    nodes, _ = deserialize_nodes_and_edges(data, editor)
    return SubGraph(nodes)


def deserialize_graph(
        data: T.Dict[str, T.Any],
        editor: "NodeEditor",
        add_to_editor: bool = True,
        ) -> "Graph":
    nodes, edges = deserialize_nodes_and_edges(data, editor)
    if add_to_editor:
        editor.add_scene_and_view()
        scene = editor.current_scene
        graph = scene.graph
    else:
        from ..model.graph import Graph
        graph = Graph()
    graph.add_nodes(*nodes)
    graph.add_edges(*edges)
    return graph
