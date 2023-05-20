import typing as T

from qtpy import QtWidgets, QtGui, QtCore
from ..setting import GraphicsViewSetting  # type: ignore
from .port_item import PortItem
from .edge_item import EdgeDragItem, EdgeItemSetting


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(
            self,
            scene: QtWidgets.QGraphicsScene,
            parent: T.Optional[QtWidgets.QWidget] = None,
            setting: T.Optional[GraphicsViewSetting] = None,
            edge_item_setting: T.Optional["EdgeItemSetting"] = None,
            ) -> None:
        super().__init__(parent)
        if setting is None:
            setting = GraphicsViewSetting()
        self.setting = setting
        if edge_item_setting is None:
            edge_item_setting = EdgeItemSetting()
        self.edge_item_setting = edge_item_setting
        self.setScene(scene)
        self.setup_layout()
        self.current_zoom = 5
        self.zoom_mode = False
        self.edge_drag_mode = False
        self._edge_drag_item: T.Optional[EdgeDragItem] = None

    def setup_layout(self):
        x, y = self.setting.default_slider_position
        self.verticalScrollBar().setSliderPosition(y)
        self.horizontalScrollBar().setSliderPosition(x)
        if self.setting.antialiasing:
            self.setRenderHints(
                QtGui.QPainter.Antialiasing |
                QtGui.QPainter.TextAntialiasing |
                QtGui.QPainter.SmoothPixmapTransform
            )
        if self.setting.full_view_update:
            self.setViewportUpdateMode(
                QtWidgets.QGraphicsView.FullViewportUpdate)
        if self.setting.hidden_sliders:
            self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.MiddleButton:  # type: ignore
            self.middle_mouse_button_press(event)
        elif event.button() == QtCore.Qt.LeftButton:  # type: ignore
            self.left_mouse_button_press(event)
        elif event.button() == QtCore.Qt.RightButton:  # type: ignore
            self.right_mouse_button_press(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.MiddleButton:  # type: ignore
            self.middle_mouse_button_release(event)
        elif event.button() == QtCore.Qt.LeftButton:  # type: ignore
            self.left_mouse_button_release(event)
        elif event.button() == QtCore.Qt.RightButton:  # type: ignore
            self.right_mouse_button_release(event)
        else:
            return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.edge_drag_mode:
            assert self._edge_drag_item is not None
            pos = self.mapToScene(event.pos())
            self._edge_drag_item.movable_pos = pos
            self.scene().update()
        return super().mouseMoveEvent(event)

    def left_mouse_button_press(self, event: QtGui.QMouseEvent):
        item = self.get_item_at_click(event)
        if isinstance(item, PortItem):
            self.edge_drag_mode = True
            self._edge_drag_item = EdgeDragItem(
                item.port, None, self.edge_item_setting)
            self.scene().addItem(self._edge_drag_item)
        super().mousePressEvent(event)

    def left_mouse_button_release(self, event: QtGui.QMouseEvent):
        if self.edge_drag_mode:
            self.edge_drag_mode = False
            assert self._edge_drag_item is not None
            self.scene().removeItem(self._edge_drag_item)
            self._edge_drag_item = None
        super().mouseReleaseEvent(event)

    def right_mouse_button_press(self, event: QtGui.QMouseEvent):
        super().mousePressEvent(event)

    def right_mouse_button_release(self, event: QtGui.QMouseEvent):
        super().mouseReleaseEvent(event)

    def middle_mouse_button_press(self, event: QtGui.QMouseEvent):
        fake_release_midele = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonRelease, event.localPos(),  # type: ignore
            event.screenPos(), QtCore.Qt.MiddleButton,  # type: ignore
            QtCore.Qt.NoButton, event.modifiers())  # type: ignore
        super().mouseReleaseEvent(fake_release_midele)
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        fake_press_left = QtGui.QMouseEvent(
            event.type(), event.localPos(), event.screenPos(),
            QtCore.Qt.LeftButton, QtCore.Qt.NoButton,  # type: ignore
            event.modifiers())
        super().mousePressEvent(fake_press_left)

    def middle_mouse_button_release(self, event: QtGui.QMouseEvent):
        fake_release_left = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonRelease, event.localPos(),  # type: ignore
            event.screenPos(), QtCore.Qt.LeftButton,  # type: ignore
            QtCore.Qt.NoButton, event.modifiers())  # type: ignore
        super().mouseReleaseEvent(fake_release_left)
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

    def get_item_at_click(
            self, event: QtGui.QMouseEvent
            ) -> T.Optional[QtWidgets.QGraphicsItem]:
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Control:  # type: ignore
            self.zoom_mode = True
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Control:  # type: ignore
            self.zoom_mode = False
        super().keyReleaseEvent(event)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if not self.zoom_mode:
            return super().wheelEvent(event)
        zoom_range = self.setting.zoom_range
        if event.angleDelta().y() > 0:
            zoom_factor = self.setting.zoom_in_factor
            self.current_zoom += self.setting.zoom_step
        else:
            zoom_factor = 1 / self.setting.zoom_in_factor
            self.current_zoom -= self.setting.zoom_step
        clamped = False
        if self.current_zoom < zoom_range[0]:
            self.current_zoom, clamped = zoom_range[0], True
        if self.current_zoom > zoom_range[1]:
            self.current_zoom, clamped = zoom_range[1], True
        if not clamped:
            self.scale(zoom_factor, zoom_factor)
