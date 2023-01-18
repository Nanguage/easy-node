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

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        else:
            return super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event: QtGui.QMouseEvent):
        fake_release_midele = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
            QtCore.Qt.MiddleButton, QtCore.Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(fake_release_midele)
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        fake_press_left = QtGui.QMouseEvent(
            event.type(), event.localPos(), event.screenPos(),
            QtCore.Qt.LeftButton, QtCore.Qt.NoButton, event.modifiers())
        super().mousePressEvent(fake_press_left)

    def middleMouseButtonRelease(self, event: QtGui.QMouseEvent):
        fake_release_left = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
            QtCore.Qt.LeftButton, QtCore.Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(fake_release_left)
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
