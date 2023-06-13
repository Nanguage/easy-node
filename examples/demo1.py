from qtpy import QtWidgets
from easynode import (
    NodeEditor, NodeFactory, Edge,
    Port, DataPort
)


app = QtWidgets.QApplication([])
editor = NodeEditor()
graph = editor.current_scene.graph


class TestNode1(NodeFactory):
    input_ports = [
        Port(name="in1"),
        Port(name="in2")
    ]
    output_ports = [
        Port(name="out1"),
    ]


class TestNode2(NodeFactory):
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

n1 = TestNode1.create_node()
n2 = TestNode1.create_node()
n3 = TestNode2.create_node()
e1 = Edge(n1.output_ports[0], n3.input_ports[0])
e2 = Edge(n2.output_ports[0], n3.input_ports[1])

graph.add_nodes(n1, n2, n3)
graph.add_edges(e1, e2)

graph.auto_layout()

editor.show()
app.exec_()
