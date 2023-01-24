import typing as T

from ..qt.node_view import NodeView

if T.TYPE_CHECKING:
    from ..qt.graphics_scene import GraphicsScene


class Node:

    @property
    def title(self) -> str:
        return self.__class__.__name__

    def create_view(self, scene: "GraphicsScene"):
        view = NodeView(None, self)
        scene.addItem(view)
