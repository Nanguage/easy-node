from easynode.node_editor import NodeEditor
from easynode.model import Node, Port, Graph
from easynode.setting import NodeItemSetting
from qtpy import QtWidgets

app = QtWidgets.QApplication([])
editor = NodeEditor()


class TestNode1(Node):
    input_ports = [
        Port(name="in1"),
        Port(name="in2"),
    ]
    output_ports = [
        Port(name="out1"),
    ]

    item_setting = NodeItemSetting(
        title_area_color="#A0FF0000",
    )


class TestNode2(Node):
    theme_color = "#00FF00"

    input_ports = [
        Port(name="in1"),
    ]
    output_ports = [
        Port(name="out1"),
    ]


editor.factory_table.register(TestNode1, TestNode2)


graph = Graph()

n1 = editor.create_node("TestNode1")
n2 = editor.create_node("TestNode2")
n3 = editor.create_node("TestNode2")
graph.add_nodes(n1, n2, n3)
e1 = n1.create_edge(n2, 0, 0)
e2 = n1.create_edge(n3, 0, 0)
graph.add_edges(e1, e2)

editor.current_scene.graph = graph
graph.auto_layout(direction="LR")

editor.show()
app.exec_()
