import typing as T

from qtpy import QtWidgets, QtGui, QtCore


class GraphView(QtWidgets.QGraphicsView):
    def __init__(
            self,
            scene: QtWidgets.QGraphicsScene,
            parent: T.Optional[QtWidgets.QWidget]=None):
        super().__init__(parent)
        self.setScene(scene)
        self.verticalScrollBar().setSliderPosition(1)
        self.horizontalScrollBar().setSliderPosition(1)
        self.setRenderHint(
            QtGui.QPainter.Antialiasing |
            QtGui.QPainter.TextAntialiasing |
            QtGui.QPainter.SmoothPixmapTransform
        )
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
