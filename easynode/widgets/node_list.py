import typing as T
from qtpy import QtWidgets, QtCore

from ..utils import hex_color_add_alpha

if T.TYPE_CHECKING:
    from easynode.node_factory import NodeFactoryTable, NodeFactory


class ListItem(QtWidgets.QWidget):
    def __init__(self, node_factory: "NodeFactory", parent=None):
        super().__init__(parent=parent)
        self.node_factory = node_factory
        self.init_ui()

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
            f"font-size: 15px;"
            "padding: 5px;"
            "}"
            "QLabel:hover {"
            f"background-color: {theme_color_with_alpha};"
            "}"
        )
        layout.addWidget(self.title_label)


class NodeList(QtWidgets.QWidget):
    def __init__(
            self, node_factory_table: "NodeFactoryTable",
            parent=None):
        super().__init__(parent=parent)
        self.init_ui()
        self.node_factory_table = node_factory_table
        self.update_list()

    def update_list(self):
        for node_factory in self.node_factory_table.table.values():
            list_item = ListItem(node_factory=node_factory)
            self.list_layout.addWidget(list_item)

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.search_line_edit = QtWidgets.QLineEdit()
        self.search_line_edit.setPlaceholderText("Search for node...")
        layout.addWidget(self.search_line_edit)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setStyleSheet("border: 0px;")

        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_widget.setContentsMargins(0, 0, 0, 0)
        self.scroll_widget.setStyleSheet("border: 0px;")
        self.scroll_area.setWidget(self.scroll_widget)

        self.list_layout = QtWidgets.QVBoxLayout()
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_widget.setLayout(self.list_layout)
        layout.addWidget(self.scroll_area)
