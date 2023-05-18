import typing as T
from qtpy import QtWidgets


class PortItem(QtWidgets.QGraphicsItem):
    def __init__(
            self,
            parent: T.Optional[QtWidgets.QWidget] = None,
            ) -> None:
        super().__init__(parent)
