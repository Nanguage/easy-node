import typing as T

from qtpy import QtWidgets, QtCore

from .graphics.scene import GraphicsScene
from .graphics.view import GraphicsView
from .setting import EditorSetting
from .widgets.custom_tab import CustomTabWidget
from .model.node import Node
from .model.graph import Graph


class NodeEditor(QtWidgets.QWidget):
    scene_added = QtCore.Signal(GraphicsScene)
    scene_removed = QtCore.Signal(GraphicsScene)
    view_changed = QtCore.Signal(GraphicsView)

    def __init__(
            self,
            parent: T.Optional[QtWidgets.QWidget] = None,
            setting: T.Optional[EditorSetting] = None,
            style_sheet: T.Optional[str] = None,
            init_scene: bool = True,
            ) -> None:
        super().__init__(parent)
        if setting is None:
            setting = EditorSetting()
        self.setting = setting
        self.factory_table = {}
        self.scenes: T.List[GraphicsScene] = []
        self.views: T.List[GraphicsView] = []
        self.current_view: T.Optional[GraphicsView] = None
        self.init_layout()
        if init_scene:
            self.add_scene_and_view()
        self.load_style_sheet(style_sheet)
        self.tabs.currentChanged.connect(self._on_tab_changed)

    def register_factory(self, *factories: T.Type[Node]) -> None:
        for factory in factories:
            self.factory_table[factory.type_name()] = factory

    def _on_tab_changed(self, index: int):
        index -= 1
        if index == -1:
            self.current_view = None
        else:
            self.current_view = self.views[index]
        self.view_changed.emit(self.current_view)

    @property
    def current_scene(self) -> GraphicsScene:
        if self.current_view is None:
            raise ValueError("No current view")
        else:
            return self.current_view.scene()

    def create_node(
            self, type_name,
            node_name: T.Optional[str] = None,
            **attrs) -> Node:
        factory = self.factory_table.get(type_name)
        if factory is None:
            raise ValueError(f"Node type {type_name} not found")
        node = factory(name=node_name, **attrs)
        return node

    def init_layout(self):
        self.resize(800, 600)
        self.setWindowTitle("EasyNode")

        self.tabs = CustomTabWidget(self)
        self.tabs.add_btn.clicked.connect(self.add_scene_and_view)
        self.tabs.tabCloseRequested.connect(self.delete_tab)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.tabs)

    def _get_new_tab_name(self) -> str:  # type: ignore
        tab_names = [
            self.tabs.tabText(i) for i in range(self.tabs.count())]
        for i in range(1, len(tab_names) + 2):
            if f"scene {i}" not in tab_names:
                return f"scene {i}"

    def add_scene_and_view(
            self, *,
            tab_name: T.Optional[str] = None
            ) -> T.Tuple[GraphicsScene, GraphicsView]:
        scene = GraphicsScene(self)
        view = GraphicsView(scene, self)
        self.scenes.append(scene)
        self.scene_added.emit(scene)
        self.views.append(view)
        if tab_name is None:
            tab_name = self._get_new_tab_name()
        new_tab_idx = self.tabs.addTab(view, tab_name)
        self.tabs.setCurrentIndex(new_tab_idx)
        self.current_view = view
        return scene, view

    def delete_tab(self, index: int):
        self.tabs.removeTab(index)
        view = self.views.pop(index-1)
        scene = view.scene()
        self.scene_removed.emit(scene)
        self.scenes.remove(scene)
        # set current view
        if len(self.views) == 0:
            self.current_view = None
        else:
            new_idx = self.tabs.currentIndex()
            self.current_view = self.views[new_idx-1]

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

    def load_graph(self, data_str: str):
        Graph.deserialize(data_str, self, add_to_editor=True)

    def load_graph_from_json_file(self, file_path: str):
        with open(file_path, 'r') as f:
            data_str = f.read()
        self.load_graph(data_str)
