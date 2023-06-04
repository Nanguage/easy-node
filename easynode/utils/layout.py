import typing as T

if T.TYPE_CHECKING:
    from ..model import Graph, Node


def determine_levels(graph: "Graph") -> T.Dict[int, int]:
    """Determine levels of nodes in graph."""
    levels: T.Dict[int, int] = {}

    def get_level(node: "Node") -> int:
        if node.id in levels:
            return levels[node.id]
        if len(node.input_edges) == 0:
            levels[node.id] = 0
            return 0
        input_nodes = [
            e.source_port.node
            for e in node.input_edges
        ]
        level = max([get_level(n) for n in input_nodes]) + 1  # type: ignore
        levels[node.id] = level
        return level

    for node in graph.nodes:
        get_level(node)
    return levels


def node_sort_key(node: "Node") -> int:
    """Sort key for nodes."""
    out_edges = node.output_edges
    if len(out_edges) == 0:
        return 0
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
        padding_level: float = 100.0,
        padding_node: float = 20.0,
        start_pos: T.Tuple[float, float] = (10.0, 10.0),
        ) -> None:
    """Layout graph.

    Args:
        graph: Graph.
        direction: Direction of layout. Options: "LR", "TB".
            Default: "LR".
        padding_level: Padding between levels.
            Default: 100.0
        padding_node: Padding between nodes.
            Default: 20.0
        start_pos: Start position of layout.
            Default: (0.0, 0.0)
    """
    level_to_nodes = get_level_to_nodes(graph)
    # layout nodes
    level_offset = 0.0
    level_nodes = list(level_to_nodes.items())
    level_nodes.sort(key=lambda x: x[0])
    for _, nodes in level_nodes:
        node_offset = 0.0
        max_size = 0.0
        for node in nodes:
            assert node.item is not None
            width = node.item.boundingRect().width()
            height = node.item.boundingRect().height()
            if direction == "TB":
                node.item.setPos(
                    start_pos[0] + node_offset,
                    start_pos[1] + level_offset
                )
                node_offset += width + padding_node
                max_size = max(max_size, height)
            else:  # "LR"
                node.item.setPos(
                    start_pos[0] + level_offset,
                    start_pos[1] + node_offset
                )
                node_offset += height + padding_node
                max_size = max(max_size, width)
        level_offset += max_size + padding_level
