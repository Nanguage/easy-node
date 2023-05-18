import typing as T
import os.path as osp

from qtpy import QtWidgets

from .widgets.scene import GraphicsScene
from .widgets.view import GraphicsView
from .setting import GraphicsViewSetting, GraphicsSceneSetting


HERE = osp.dirname(osp.abspath(__file__))


class NodeEditor(QtWidgets.QWidget):
    def __init__(
            self,
            parent: T.Optional[QtWidgets.QWidget] = None,
            graphics_scene_setting: T.Optional[GraphicsSceneSetting] = None,
            graphics_view_setting: T.Optional[GraphicsViewSetting] = None,
            ) -> None:
        super().__init__(parent)
        self.graphics_scene_setting = graphics_scene_setting
        self.graphics_view_setting = graphics_view_setting
        self.init_layout()
        self.load_style_sheet(osp.join(HERE, "qss/node.qss"))

    def init_layout(self):
        self.resize(800, 600)
        self.setWindowTitle("EasyNode")

        self.scene = GraphicsScene(self, self.graphics_scene_setting)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.view = GraphicsView(
            self.scene, self, self.graphics_view_setting)
        self.layout.addWidget(self.view)

        # self.try_add_items()
        self.test_add_elements()

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

    def test_add_elements(self):
        from .model.node import Node

        n = Node(type_name="Test", name="test1")
        n.create_view(self.scene)

        text_edit = QtWidgets.QTextEdit()
        n = Node(
            type_name="TextNode", name="test2",
            widget=text_edit)
        n.create_view(self.scene)

    def load_style_sheet(self, path: str):
        with open(path, "r") as f:
            app = QtWidgets.QApplication.instance()
            app.setStyleSheet(f.read())  # type: ignore
