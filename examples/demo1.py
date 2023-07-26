from qtpy import QtWidgets
from easynode import (
    NodeEditor, Edge, Node,
    Port, DataPort
)


app = QtWidgets.QApplication([])
editor = NodeEditor(init_scene=True)
graph = editor.current_scene.graph


class TestNode1(Node):
    input_ports = [
        Port(name="in1"),
        Port(name="in2")
    ]
    output_ports = [
        Port(name="out1"),
    ]


class TestNode2(Node):
    theme_color = "#ff0000"

    input_ports = [
        DataPort(name="in1", data_type=int, data_range=(0, 100)),
        DataPort(name="in2", data_type=float, data_default=2.0),
        DataPort(name="in3", data_type=str)
    ]
    output_ports = [
        Port(name="out1"),
    ]


class TestNode3(Node):
    input_ports = [
        Port(name="in1"),
    ]

    def create_widget(self):
        return QtWidgets.QTextEdit()


editor.factory_table.register(TestNode1)
editor.factory_table.register(TestNode2)
editor.factory_table.register(TestNode3)

n1 = TestNode1()
n2 = TestNode1()
n3 = TestNode2()
# create node using `editor.create_node`
n4 = editor.create_node("TestNode3")
e1 = Edge(n1.output_ports[0], n3.input_ports[0])
e2 = Edge(n2.output_ports[0], n3.input_ports[1])
e3 = n3.create_edge(n4, 0, 0)

graph.add_nodes(n1, n2, n3, n4)
graph.add_edges(e1, e2, e3)

graph.auto_layout()

editor.show()
app.exec_()
