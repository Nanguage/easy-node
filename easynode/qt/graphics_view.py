import typing as T
from dataclasses import dataclass

from qtpy import QtWidgets, QtGui, QtCore


@dataclass
class GraphicsViewSetting:
    antialiasing: bool = True
    default_slider_position: T.Tuple[int, int] = (1, 1)
    hidden_sliders: bool = True
    full_view_update: bool = True
    zoom_in_factor: float = 1.25
    zoom_step: int = 1
    zoom_range: T.Tuple[int, int] = (0, 10)


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(
            self,
            scene: QtWidgets.QGraphicsScene,
            parent: T.Optional[QtWidgets.QWidget]=None,
            setting: T.Optional[GraphicsViewSetting]=None):
        super().__init__(parent)
        if setting is None:
            setting = GraphicsViewSetting()
        self.setting = setting
        self.setScene(scene)
        self.setup_layout()
        self.current_zoom = 5
        self.zoom_mode = False

    def setup_layout(self):
        x, y = self.setting.default_slider_position
        self.verticalScrollBar().setSliderPosition(y)
        self.horizontalScrollBar().setSliderPosition(x)
        if self.setting.antialiasing:
            self.setRenderHint(
                QtGui.QPainter.Antialiasing |
                QtGui.QPainter.TextAntialiasing |
                QtGui.QPainter.SmoothPixmapTransform
            )
        if self.setting.full_view_update:
            self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        if self.setting.hidden_sliders:
            self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

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

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Control:
            self.zoom_mode = True
        super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Control:
            self.zoom_mode = False
        super().keyReleaseEvent(event)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if self.zoom_mode == False:
            return super().wheelEvent(event)
        zoom_out_factor = 1 / self.setting.zoom_in_factor
        zoom_range = self.setting.zoom_range
        if event.angleDelta().y() > 0:
            zoom_factor = self.setting.zoom_in_factor
            self.current_zoom += self.setting.zoom_step
        else:
            zoom_factor = zoom_out_factor
            self.current_zoom -= self.setting.zoom_step
        clamped = False
        if self.current_zoom < zoom_range[0]:
            self.current_zoom, clamped = zoom_range[0], True
        if self.current_zoom > zoom_range[1]:
            self.current_zoom, clamped = zoom_range[1], True
        if not clamped:
            self.scale(zoom_factor, zoom_factor)

