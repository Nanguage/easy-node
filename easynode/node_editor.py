import typing as T

from qtpy import QtWidgets

from .graphics.scene import GraphicsScene
from .graphics.view import GraphicsView
from .setting import EditorSetting
from .node_factory import NodeFactoryTable


class NodeEditor(QtWidgets.QWidget):
    def __init__(
            self,
            parent: T.Optional[QtWidgets.QWidget] = None,
            setting: T.Optional[EditorSetting] = None,
            style_sheet: T.Optional[str] = None,
            ) -> None:
        super().__init__(parent)
        if setting is None:
            setting = EditorSetting()
        self.setting = setting
        self.init_layout()
        self.load_style_sheet(style_sheet)
        self.factory_table = NodeFactoryTable()

    def create_node(self, type_name: str):
        factory = self.factory_table.table.get(type_name)
        if factory is None:
            raise ValueError(f"Node type {type_name} not found")
        node = factory.create_node()
        self.scene.graph.add_node(node)

    def init_layout(self):
        self.resize(800, 600)
        self.setWindowTitle("EasyNode")

        self.scene = GraphicsScene(self)
        self.scene.editor = self

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.view = GraphicsView(self.scene, self)
        self.layout.addWidget(self.view)

    def load_style_sheet(self, style_sheet: T.Optional[str] = None):
        app = QtWidgets.QApplication.instance()
        if style_sheet is None:
            try:
                import qdarktheme
                app.setStyleSheet(qdarktheme.load_stylesheet())  # type: ignore
            except ImportError:
                pass
        else:
            app.setStyleSheet(style_sheet)  # type: ignore
