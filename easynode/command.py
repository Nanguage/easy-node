import typing as T

from qtpy import QtWidgets, QtCore

if T.TYPE_CHECKING:
    from .graphics.node_item import NodeItem


class FlowCommand(QtWidgets.QUndoCommand):
    def __init__(self):
        super().__init__()
        self._first_redo = True

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


class NodeItemsMoveCommand(FlowCommand):
    def __init__(
            self, node_items: T.List["NodeItem"],
            pos_diff: QtCore.QPointF):
        super().__init__()
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

    @property
    def scene(self):
        return self.items[0].scene()

    def create_items_group(self):
        return self.scene.createItemGroup(self.items)

    def destroy_items_group(self, group):
        self.scene.destroyItemGroup(group)
