import typing as T
import json

from qtpy import QtWidgets, QtCore, QtGui
import textdistance

from ..utils import hex_color_add_alpha

if T.TYPE_CHECKING:
    from easynode.node_factory import NodeFactoryTable, NodeFactory


class ListItem(QtWidgets.QWidget):
    def __init__(self, node_factory: "NodeFactory", parent=None):
        super().__init__(parent=parent)
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
            f"font-size: 15px;"
            "padding: 5px;"
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


class NodeList(QtWidgets.QWidget):
    def __init__(
            self, node_factory_table: "NodeFactoryTable",
            parent=None):
        super().__init__(parent=parent)
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
                len(
                    textdistance.lcsseq(
                        search_text.lower(), factory.type_name().lower())
                )
                for factory in self.node_factory_table.table.values()
            ]
            return [
                factory for _, factory in sorted(
                    zip(lcs_lengeth, self.node_factory_table.table.values()),
                    key=lambda x: x[0],
                    reverse=True
                )
            ]

    def update_list(self):
        # clear list
        for i in reversed(range(self.list_layout.count())):
            self.list_layout.itemAt(i).widget().setParent(None)
        for node_factory in self.get_ordered_node_factories():
            list_item = ListItem(node_factory=node_factory)
            self.list_layout.addWidget(list_item)

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.setStyleSheet(
            "background-color: #EE111111;"
        )
        m = 4
        layout.setContentsMargins(m, m, m, m)
        layout.setSpacing(0)

        self.search_line_edit = QtWidgets.QLineEdit()
        self.search_line_edit.setPlaceholderText("Search for node...")
        self.search_line_edit.setStyleSheet(
            "background-color: #EE222222;"
            "font-size: 15px;"
            "height: 25px;"
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
            "background-color: #EE111111;"
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
