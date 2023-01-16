import typing as T

from qtpy import QtWidgets

from .graph_scene import GraphScene


class NodeEditor(QtWidgets.QWidget):
    def __init__(self, parent: T.Optional[QtWidgets.QWidget]=None) -> None:
        super().__init__(parent)
        self.init_layout()

    def init_layout(self):
        self.resize(800, 600)
        self.setWindowTitle("EasyNode")

        self.scene = GraphScene(self)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.view = QtWidgets.QGraphicsView(self)
        self.view.setScene(self.scene)
        self.view.verticalScrollBar().setSliderPosition(1)
        self.view.horizontalScrollBar().setSliderPosition(1)
        self.layout.addWidget(self.view)
