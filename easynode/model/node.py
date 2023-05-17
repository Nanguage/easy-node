import typing as T

from ..widgets.node_view import NodeView

if T.TYPE_CHECKING:
    from ..widgets.graphics_scene import GraphicsScene
    from qtpy.QtWidgets import QWidget


class NodeBase:
    def __init__(self) -> None:
        self.widget: T.Optional["QWidget"] = None
        self.init_widget()

    def init_widget(self):
        pass


class Node(NodeBase):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__()

    @property
    def title(self) -> str:
        return self.__class__.__name__

    def create_view(self, scene: "GraphicsScene"):
        view = NodeView(None, self)
        scene.addItem(view)
