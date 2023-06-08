import typing as T

from qtpy import QtWidgets, QtCore

from .graphics.node_item import NodeItem
from .graphics.edge_item import EdgeItem

if T.TYPE_CHECKING:
    from .graphics.scene import GraphicsScene
    from .graphics.view import GraphicsView


class FlowCommand(QtWidgets.QUndoCommand):
    def __init__(self, view: "GraphicsView"):
        super().__init__()
        self._first_redo = True
        self.view = view

    @property
    def scene(self) -> "GraphicsScene":
        return self.view.scene()

    def redo(self):
        # skip first redo,
        # because it will be called when command is pushed
        if self._first_redo:
            self._first_redo = False
            return
        self._redo()

    def _redo(self):
        pass

    def undo(self):
        self._undo()

    def _undo(self):
        pass


class FlowItemsCommand(FlowCommand):
    items: T.List[QtWidgets.QGraphicsItem]

    def create_items_group(self):
        return self.scene.createItemGroup(self.items)

    def destroy_items_group(self, group):
        self.scene.destroyItemGroup(group)


class NodeItemsMoveCommand(FlowItemsCommand):
    def __init__(
            self, view: "GraphicsView",
            node_items: T.List["NodeItem"],
            pos_diff: QtCore.QPointF):
        super().__init__(view)
        self.items = node_items
        self.pos_diff = pos_diff

    def _undo(self):
        group = self.create_items_group()
        group.setPos(-self.pos_diff)
        self.destroy_items_group(group)

    def _redo(self):
        group = self.create_items_group()
        group.setPos(self.pos_diff)
        self.destroy_items_group(group)


class RemoveItemsCommand(FlowItemsCommand):
    def __init__(
            self, view: "GraphicsView",
            items: T.List[QtWidgets.QGraphicsItem]):
        super().__init__(view)
        self.items = items

    def _undo(self):
        for item in self.items:
            if isinstance(item, NodeItem):
                self.scene.graph.add_node(item.node)
            elif isinstance(item, EdgeItem):
                self.scene.graph.add_edge(item.edge)

    def _redo(self):
        for item in self.items:
            if isinstance(item, NodeItem):
                self.scene.graph.remove_node(item.node)
            elif isinstance(item, EdgeItem):
                self.scene.graph.remove_edge(item.edge)
