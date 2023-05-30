import typing as T
from ..model import Graph, Node


def determine_levels(graph: "Graph") -> T.Dict[int, int]:
    """Determine levels of nodes in graph."""
    levels = {}
    # find zero level nodes
    for node in graph.nodes:
        if len(node.input_edges) == 0:
            levels[node.id] = 0
    # search other levels
    while len(levels) < len(graph.nodes):
        for node in graph.nodes:
            if node.id in levels:
                continue
            level = 0
            for edge in node.input_edges:
                s_node = edge.source_port.node
                assert s_node is not None
                if s_node.id in levels:
                    level = max(level, levels[s_node.id] + 1)
    return levels


def node_sort_key(node: "Node") -> int:
    """Sort key for nodes."""
    out_edges = node.output_edges
    return max([  # type: ignore
        e.target_port.index
        for e in out_edges
    ])


def get_level_to_nodes(
        graph: "Graph") -> T.Dict[int, T.List["Node"]]:
    levels = determine_levels(graph)
    level_to_nodes: T.Dict[int, T.List["Node"]] = {}
    for node in graph.nodes:
        level = levels[node.id]
        if level not in level_to_nodes:
            level_to_nodes[level] = []
        level_to_nodes[level].append(node)
    # sort nodes in each level
    for level, nodes in level_to_nodes.items():
        level_to_nodes[level] = sorted(
            nodes, key=node_sort_key)
    return level_to_nodes


def layout_graph(
        graph: "Graph",
        direction: str = "LR",
        padding_level: int = 100,
        padding_node: int = 20,
        ) -> None:
    """Layout graph.

    Args:
        graph: Graph.
        direction: Direction of layout. Options: "LR", "TB".
            Default: "LR".
        padding_level: Padding between levels.
            Default: 100.
        padding_node: Padding between nodes.
            Default: 20.
    """
    # TODO
    level_to_nodes = get_level_to_nodes(graph)
    # layout nodes
    level_offset = 0.0
    for level, nodes in level_to_nodes.items():
        node_offset = 0.0
        max_size = 0.0
        for node in nodes:
            assert node.item is not None
            if direction == "TB":
                node.item.setPos()
            else:  # "LR"
                node.item.setPos()
            offset += padding_node
