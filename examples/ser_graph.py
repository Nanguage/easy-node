from pathlib import Path
from easynode.model import Port, DataPort, Edge, Node
from easynode.node_editor import NodeEditor
from qtpy import QtWidgets

app = QtWidgets.QApplication([])
editor = NodeEditor()
graph = editor.current_scene.graph


class TestNode(Node):
    input_ports = [
        Port(name="in1"),
        Port(name="in2"),
    ]
    output_ports = [
        Port(name="out1"),
    ]


class TestNode2(Node):
    theme_color = "#ff22aa"
    input_ports = [
        DataPort(name="in1", data_type=int),
        DataPort(name="in2", data_type=float),
    ]


class TestNode3(Node):
    input_ports = [
        Port(name="in1"),
        Port(name="in2"),
    ]
    output_ports = [
        Port(name="out1"),
    ]

    def create_widget(cls):
        return QtWidgets.QTextEdit()


editor.factory_table.register(TestNode, TestNode2, TestNode3)
n1 = editor.create_node("TestNode")
n2 = editor.create_node("TestNode2")
n3 = editor.create_node("TestNode")
n4 = editor.create_node("TestNode2")
n5 = editor.create_node("TestNode3")
graph.add_nodes(n1, n2, n3, n4, n5)
graph.add_edge(Edge(n1.output_ports[0], n2.input_ports[0]))
graph.add_edge(Edge(n3.output_ports[0], n5.input_ports[0]))
graph.add_edge(Edge(n5.output_ports[0], n4.input_ports[0]))

graph.auto_layout()

test_dir = Path("./tmp")
test_dir.mkdir(exist_ok=True)
test_json = test_dir / "test.json"

with open(test_json, 'w') as f:
    data_str = graph.serialize()
    f.write(data_str)

editor.load_graph_from_json_file(str(test_json))

editor.show()
app.exec_()
