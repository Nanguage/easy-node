import typing as T

from qtpy import QtWidgets

from .graphics.scene import GraphicsScene
from .graphics.view import GraphicsView
from .setting import EditorSetting
from .node_factory import NodeFactoryTable
from .widgets.custom_tab import CustomTabWidget


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
        self.factory_table = NodeFactoryTable()
        self.scenes: T.List[GraphicsScene] = []
        self.views: T.List[GraphicsView] = []
        self.current_view: T.Optional[GraphicsView] = None
        self.init_layout()
        self.load_style_sheet(style_sheet)

    @property
    def current_scene(self) -> GraphicsScene:
        if self.current_view is None:
            raise ValueError("No current view")
        else:
            return self.current_view.scene()

    def create_node(self, type_name: str):
        factory = self.factory_table.table.get(type_name)
        if factory is None:
            raise ValueError(f"Node type {type_name} not found")
        node = factory.create_node()
        self.current_scene.graph.add_node(node)

    def init_layout(self):
        self.resize(800, 600)
        self.setWindowTitle("EasyNode")

        self.tabs = CustomTabWidget(self)
        self.tabs.add_btn.clicked.connect(self.add_scene_and_view)
        self.tabs.tabCloseRequested.connect(self.delete_tab)
        self.add_scene_and_view()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.tabs)

    def add_scene_and_view(self):
        scene = GraphicsScene(self)
        scene.editor = self
        view = GraphicsView(scene, self)
        self.scenes.append(scene)
        self.views.append(view)
        new_scene_idx = len(self.scenes)
        self.tabs.addTab(view, f"scene {new_scene_idx}")
        new_view_idx = len(self.views)
        self.tabs.setCurrentIndex(new_view_idx)
        self.current_view = view

    def delete_tab(self, index: int):
        self.tabs.removeTab(index)
        view = self.views.pop(index)
        self.scenes.remove(view.scene())

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
