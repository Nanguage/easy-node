import typing as T

from qtpy import QtWidgets

from .graph_scene import GraphScene
from .graph_view import GraphView


class NodeEditor(QtWidgets.QWidget):
    def __init__(self, parent: T.Optional[QtWidgets.QWidget]=None) -> None:
        super().__init__(parent)
        self.init_layout()

    def init_layout(self):
        self.resize(800, 600)
        self.setWindowTitle("EasyNode")

        self.scene = GraphScene(self)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.view = GraphView(self.scene, self)
        self.layout.addWidget(self.view)

        self.try_add_items()

    def try_add_items(self):
        # for learn API
        from qtpy.QtGui import QBrush, QPen, QColor, QFont
        from qtpy.QtCore import Qt
        green_brush = QBrush(Qt.green)
        outline_pen = QPen("#ffffff")
        outline_pen.setWidth(2)
        rect = self.scene.addRect(20, 20, 90, 90, outline_pen, green_brush)
        rect.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)

        text = self.scene.addText("This is awesome text!", QFont("Ubuntu"))
        text.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        text.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QtWidgets.QPushButton("Hello!")
        proxy1 = self.scene.addWidget(widget1)
        proxy1.setPos(30, 30)

        widget2 = QtWidgets.QTextEdit()
        proxy2 = self.scene.addWidget(widget2)
        proxy2.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(30, 200)

        line_pen = QPen("#000000")
        line_pen.setWidth(5)
        line = self.scene.addLine(200, 10, 500, 100, line_pen)
        line.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        line.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
