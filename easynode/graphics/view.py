import typing as T
import json

from qtpy import QtWidgets, QtGui, QtCore
from .port_item import PortItem
from .edge_item import EdgeDragItem
from .edge_item import EdgeItem
from .node_item import NodeItem

try:
    from qtpy.QtWidgets import QUndoStack
except ImportError:
    from qtpy.QtGui import QUndoStack  # type: ignore

if T.TYPE_CHECKING:
    from .scene import GraphicsScene


class GraphicsView(QtWidgets.QGraphicsView):
    selected_node_items_moved = QtCore.Signal(QtCore.QPointF)

    def __init__(
            self,
            scene: "GraphicsScene",
            parent: T.Optional[QtWidgets.QWidget] = None,
            ) -> None:
        super().__init__(parent)
        self.setting = scene.editor.setting.graphics_view_setting
        self.setScene(scene)
        self._current_zoom = 5
        self._zoom_mode = False
        self._edge_drag_mode = False
        self._edge_drag_item: T.Optional[EdgeDragItem] = None
        self._clicked_port_item: T.Optional[PortItem] = None
        self._right_clicked_pos: T.Optional[QtCore.QPointF] = None
        self._setup_layout()
        self._init_node_list()
        self._init_undo_stack()
        self._init_shortcuts()
        self._wire_signals()

    def scene(self) -> "GraphicsScene":
        return super().scene()  # type: ignore

    @property
    def _edge_drag_mode(self) -> bool:
        return self.__edge_drag_mode

    @_edge_drag_mode.setter
    def _edge_drag_mode(self, value: bool) -> None:
        self.__edge_drag_mode = value
        if value:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        else:
            self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

    def _setup_layout(self):
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
        if self.setting.open_gl:
            self.setViewport(QtWidgets.QOpenGLWidget())
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def _init_node_list(self):
        factory_table = self.scene().editor.factory_table
        self.node_list_widget = factory_table.create_node_list_widget()
        self.node_list_widget.setFixedHeight(
            self.setting.node_list_widget_height)
        self.node_list_widget.list.item_clicked.connect(
            self.create_node_by_click)
        self.node_list_widget_proxy = QtWidgets.QGraphicsProxyWidget()
        self.node_list_widget_proxy.setWidget(self.node_list_widget)
        self.node_list_widget_proxy.setZValue(1000)
        self.scene().addItem(self.node_list_widget_proxy)
        self.hide_node_list_widget()

    def _init_undo_stack(self):
        self.undo_stack = QUndoStack()
        self.undo_stack.setUndoLimit(self.setting.undo_limit)

    def _init_shortcuts(self):
        undo_shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+Z"), self)
        undo_shortcut.activated.connect(self._on_undo)
        redo_shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+R"), self)
        redo_shortcut.activated.connect(self._on_redo)

    def _on_undo(self):
        self.undo_stack.undo()
        self.viewport().update()

    def _on_redo(self):
        self.undo_stack.redo()
        self.viewport().update()

    def _wire_signals(self):
        self.selected_node_items_moved.connect(
            self._on_selected_node_items_moved)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.MiddleButton:  # type: ignore
            self._middle_mouse_button_press(event)
        elif event.button() == QtCore.Qt.LeftButton:  # type: ignore
            self._left_mouse_button_press(event)
        elif event.button() == QtCore.Qt.RightButton:  # type: ignore
            self._right_mouse_button_press(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.MiddleButton:  # type: ignore
            self._middle_mouse_button_release(event)
        elif event.button() == QtCore.Qt.LeftButton:  # type: ignore
            self._left_mouse_button_release(event)
        elif event.button() == QtCore.Qt.RightButton:  # type: ignore
            self._right_mouse_button_release(event)
        else:
            return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self._edge_drag_mode:
            if self._edge_drag_item is None:
                item = self._clicked_port_item
                assert item is not None
                self._edge_drag_item = EdgeDragItem(
                    item.port, None,
                    self.scene().editor.setting.edge_drag_item_setting)
                self.scene().addItem(self._edge_drag_item)
            else:
                pos = event.pos()
                scene_pos = self.mapToScene(pos)
                self._edge_drag_item.movable_pos = scene_pos
                self.scene().update()
        else:
            if self._clicked_port_item is not None:
                self._edge_drag_mode = True
        return super().mouseMoveEvent(event)

    def _left_mouse_button_press(self, event: QtGui.QMouseEvent):
        item = self.itemAt(event.pos())
        if isinstance(item, PortItem):
            self._clicked_port_item = item
        if (self.node_list_widget_proxy.isVisible()) and \
           (item is not self.node_list_widget_proxy):
            self.hide_node_list_widget()
        super().mousePressEvent(event)

    def _left_mouse_button_release(self, event: QtGui.QMouseEvent):
        if self._clicked_port_item is not None:
            self._clicked_port_item = None
        if self._edge_drag_mode:
            self._edge_drag_mode = False
            assert self._edge_drag_item is not None
            stop_item = self.itemAt(event.pos())
            if isinstance(stop_item, PortItem):
                from ..command import CreateEdgeCommand  # type: ignore
                try:
                    new_edge = self._edge_drag_item.create_edge(stop_item.port)
                    self.scene().graph.add_edge(new_edge)
                    self.undo_stack.push(
                        CreateEdgeCommand(self, new_edge))
                except Exception as e:
                    print(e)
            self.scene().removeItem(self._edge_drag_item)
            self._edge_drag_item = None
        super().mouseReleaseEvent(event)

    def _right_mouse_button_press(self, event: QtGui.QMouseEvent):
        item = self.itemAt(event.pos())
        if item is None:
            self._right_clicked_pos = event.pos()
            self.show_node_list_widget(event)
        super().mousePressEvent(event)

    def show_node_list_widget(self, event: QtGui.QMouseEvent):
        self.node_list_widget.update_list()
        pos = self.mapToScene(event.pos())
        self.node_list_widget_proxy.setPos(pos)
        self.node_list_widget_proxy.show()

    def hide_node_list_widget(self):
        self.node_list_widget_proxy.hide()

    def create_node_by_click(self, factory_type_name: str):
        if factory_type_name == '':
            return
        if self._right_clicked_pos is not None:
            self.create_node(
                factory_type_name,
                self.mapToScene(self._right_clicked_pos))
            self.hide_node_list_widget()

    def create_node(self, factory_type_name: str, pos: QtCore.QPointF):
        factory = self.scene().editor.factory_table.table[factory_type_name]
        node = factory.create_node()
        self.scene().graph.add_node(node)
        assert node.item is not None
        node.item.content_widget.setFocus()
        node.item.setPos(pos)
        from ..command import CreateNodeCommand  # type: ignore
        self.undo_stack.push(CreateNodeCommand(self, node))

    def _right_mouse_button_release(self, event: QtGui.QMouseEvent):
        super().mouseReleaseEvent(event)

    def _middle_mouse_button_press(self, event: QtGui.QMouseEvent):
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

    def _middle_mouse_button_release(self, event: QtGui.QMouseEvent):
        fake_release_left = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonRelease, event.localPos(),  # type: ignore
            event.screenPos(), QtCore.Qt.LeftButton,  # type: ignore
            QtCore.Qt.NoButton, event.modifiers())  # type: ignore
        super().mouseReleaseEvent(fake_release_left)
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Control:  # type: ignore
            self._zoom_mode = True
        if event.key() == QtCore.Qt.Key_Delete:  # type: ignore
            self.remove_selected_items()
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Control:  # type: ignore
            self._zoom_mode = False
        super().keyReleaseEvent(event)

    def remove_selected_items(self):
        from ..command import RemoveItemsCommand  # type: ignore
        graph = self.scene().graph
        deleted_items = set()  # remove deleted items
        items = self.scene().selectedItems()
        for item in items:
            if isinstance(item, NodeItem):
                node = item.node
                for edge in node.input_edges + node.output_edges:
                    # mark connected edges
                    deleted_items.add(edge.item)
                deleted_items.add(node.item)
                graph.remove_node(node)
            elif isinstance(item, EdgeItem):
                edge = item.edge
                deleted_items.add(edge.item)
                graph.remove_edge(edge)
        deleted_items = list(deleted_items)
        self.undo_stack.push(
            RemoveItemsCommand(self, deleted_items))

    def _on_selected_node_items_moved(self, diff: QtCore.QPointF):
        from ..command import NodeItemsMoveCommand  # type: ignore
        items = [
            item for item in self.scene().selectedItems()
            if isinstance(item, NodeItem)
        ]
        command = NodeItemsMoveCommand(self, items, diff)
        self.undo_stack.push(command)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if not self._zoom_mode:
            item = self.itemAt(event.pos())
            if isinstance(item, QtWidgets.QGraphicsProxyWidget):
                from ..widgets.node_list import NodeList  # type: ignore
                widget = item.widget()
                if isinstance(widget, NodeList):
                    widget.list.wheelEvent(event)
                else:
                    super().wheelEvent(event)
            else:
                super().wheelEvent(event)
        else:
            zoom_range = self.setting.zoom_range
            if event.angleDelta().y() > 0:
                zoom_factor = self.setting.zoom_in_factor
                self._current_zoom += self.setting.zoom_step
            else:
                zoom_factor = 1 / self.setting.zoom_in_factor
                self._current_zoom -= self.setting.zoom_step
            clamped = False
            if self._current_zoom < zoom_range[0]:
                self._current_zoom, clamped = zoom_range[0], True
            if self._current_zoom > zoom_range[1]:
                self._current_zoom, clamped = zoom_range[1], True
            if not clamped:
                self.scale(zoom_factor, zoom_factor)

    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasFormat('application/easynode-node-factory'):
            event.acceptProposedAction()

    def dragMoveEvent(self, event) -> None:
        if event.mimeData().hasFormat('application/easynode-node-factory'):
            event.acceptProposedAction()

    def dropEvent(self, event) -> None:
        if event.mimeData().hasFormat('application/easynode-node-factory'):
            data = event.mimeData().data(
                'application/easynode-node-factory')
            data = json.loads(bytes(data).decode())
            node_factory_type = data['node_factory_type']
            self.create_node(
                node_factory_type,
                self.mapToScene(event.pos()))
            event.acceptProposedAction()
