from qtpy import QtWidgets
from easynode import (
    NodeEditor, Edge, Node,
    Port, DataPort
)


app = QtWidgets.QApplication([])
editor = NodeEditor()
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


editor.factory_table.register(TestNode1)
editor.factory_table.register(TestNode2)

n1 = TestNode1()
n2 = TestNode1()
n3 = TestNode2()
e1 = Edge(n1.output_ports[0], n3.input_ports[0])
e2 = Edge(n2.output_ports[0], n3.input_ports[1])

graph.add_nodes(n1, n2, n3)
graph.add_edges(e1, e2)

graph.auto_layout()

editor.show()
app.exec_()
