import typing as T
import json
from functools import lru_cache

from qtpy import QtWidgets, QtCore, QtGui
import textdistance

from ..utils import hex_color_add_alpha
from ..setting import NodeListItemSetting, NodeListWidgetSetting

if T.TYPE_CHECKING:
    from easynode.node_factory import NodeFactoryTable, NodeFactory


class ListItem(QtWidgets.QWidget):
    def __init__(
            self, node_factory: "NodeFactory",
            setting: T.Optional["NodeListItemSetting"] = None,
            parent=None):
        super().__init__(parent=parent)
        if setting is None:
            setting = NodeListItemSetting()
        self.setting = setting
        self.node_factory = node_factory
        self.init_ui()
        self.start_drag = False

    def init_ui(self):
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title_label = QtWidgets.QLabel(self.node_factory.type_name())
        theme_color = self.node_factory.theme_color
        theme_color_with_alpha = hex_color_add_alpha(theme_color, 80)
        self.title_label.setStyleSheet(
            "QLabel {"
            f"color: {theme_color};"
            f"font-size: {self.setting.font_size}px;"
            f"padding: {self.setting.padding}px;"
            "}"
            "QLabel:hover {"
            f"background-color: {theme_color_with_alpha};"
            "}"
        )
        layout.addWidget(self.title_label)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.start_drag = True

    def mouseMoveEvent(self, event):
        if self.start_drag:
            mime_data = QtCore.QMimeData()
            data = {
                'node_factory_type': self.node_factory.type_name()
            }
            mime_data.setData(
                'application/easynode-node-factory',
                bytes(json.dumps(data), encoding='utf-8')
            )
            drag = QtGui.QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec_(QtCore.Qt.MoveAction)
            self.start_drag = False

    def mouseReleaseEvent(self, event):
        self.start_drag = False


@lru_cache(maxsize=None)
def lcs_length(s1: str, s2: str):
    return len(textdistance.lcsseq(s1, s2))


class NodeList(QtWidgets.QWidget):
    def __init__(
            self, node_factory_table: "NodeFactoryTable",
            setting: T.Optional["NodeListWidgetSetting"] = None,
            parent=None):
        super().__init__(parent=parent)
        if setting is None:
            setting = NodeListWidgetSetting()
        self.setting = setting
        self.init_ui()
        self.node_factory_table = node_factory_table
        self.update_list()

    def get_ordered_node_factories(self) -> T.List[T.Type["NodeFactory"]]:
        search_text = self.search_line_edit.text()
        if search_text == "":
            return sorted(
                self.node_factory_table.table.values(),
                key=lambda x: x.type_name()
            )
        else:
            # sort by similarity with search text
            lcs_lengeth = [
                lcs_length(
                    search_text.lower(), factory.type_name().lower())
                for factory in self.node_factory_table.table.values()
            ]
            return [
                factory for len, factory in sorted(
                    zip(lcs_lengeth, self.node_factory_table.table.values()),
                    key=lambda x: x[0],
                    reverse=True
                )
                if len > 0
            ]

    def update_list(self):
        # clear list
        for i in reversed(range(self.list_layout.count())):
            self.list_layout.itemAt(i).widget().setParent(None)
        for node_factory in self.get_ordered_node_factories():
            list_item = ListItem(node_factory=node_factory)
            self.list_layout.addWidget(list_item)

    def init_ui(self):
        background_color = self.setting.background_color
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.setStyleSheet(
            f"background-color: {background_color};"
        )
        m = 4
        layout.setContentsMargins(m, m, m, m)
        layout.setSpacing(0)

        self.search_line_edit = QtWidgets.QLineEdit()
        self.search_line_edit.setPlaceholderText("Search for node...")
        sl_background_color = self.setting.search_line_edit_background_color
        self.search_line_edit.setStyleSheet(
            f"background-color: {sl_background_color};"
            f"font-size: {self.setting.search_line_edit_font_size}px;"
            f"height: {self.setting.search_line_edit_height}px;"
        )
        self.search_line_edit.textChanged.connect(
            lambda: self.update_list())
        layout.addWidget(self.search_line_edit)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setStyleSheet(
            "border: 0px;"
            f"background-color: {background_color};"
        )

        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_widget.setContentsMargins(0, 0, 0, 0)
        self.scroll_widget.setStyleSheet("border: 0px;")
        self.scroll_area.setWidget(self.scroll_widget)

        self.list_layout = QtWidgets.QVBoxLayout()
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_widget.setLayout(self.list_layout)
        layout.addWidget(self.scroll_area)
