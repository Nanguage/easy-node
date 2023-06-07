import typing as T

from qtpy import QtWidgets, QtCore

if T.TYPE_CHECKING:
    from .graphics.node_item import NodeItem


class FlowCommand(QtWidgets.QUndoCommand):
    pass


class NodeItemMoveCommand(FlowCommand):
    def __init__(
            self, node_item: "NodeItem",
            pos_old: QtCore.QPointF,
            pos_new: QtCore.QPointF,):
        super().__init__()
        self.node_item = node_item
        self.pos_old = pos_old
        self.pos_new = pos_new

    def undo(self):
        self.node_item.setPos(self.pos_old)

    def redo(self):
        self.node_item.setPos(self.pos_new)
