import typing as T
import json
from functools import lru_cache

from qtpy import QtWidgets, QtCore, QtGui
import textdistance

from ..setting import NodeListWidgetSetting

if T.TYPE_CHECKING:
    from easynode.node_factory import NodeFactoryTable, NodeFactory


@lru_cache(maxsize=None)
def lcs_length(s1: str, s2: str):
    return len(textdistance.lcsseq(s1, s2))


class NodeListView(QtWidgets.QListView):
    item_clicked = QtCore.Signal(str)

    def __init__(
            self,
            parent: T.Optional[QtWidgets.QWidget] = None):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.drag_item_name: T.Optional[str] = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            item = self.indexAt(event.pos())
            self.drag_item_name = item.data()
            self.item_clicked.emit(item.data())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drag_item_name is not None:
            mime_data = QtCore.QMimeData()
            data = {
                'node_factory_type': self.drag_item_name
            }
            mime_data.setData(
                'application/easynode-node-factory',
                bytes(json.dumps(data), encoding='utf-8')
            )
            drag = QtGui.QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec_(QtCore.Qt.MoveAction)
            self.drag_item_name = None


class SearchLine(QtWidgets.QLineEdit):
    def __init__(
            self,
            parent: "NodeList"):
        setting = parent.setting
        super().__init__(parent=parent)
        self.setPlaceholderText("Search for node...")
        sl_background_color = setting.search_line_edit_background_color
        self.setStyleSheet(
            f"background-color: {sl_background_color};"
            f"font-size: {setting.search_line_edit_font_size}px;"
            f"height: {setting.search_line_edit_height}px;"
        )
        self.textChanged.connect(  # type: ignore
            lambda: parent.update_list())

    def contextMenuEvent(self, event) -> None:
        pass


class NodeList(QtWidgets.QWidget):
    def __init__(
            self, node_factory_table: "NodeFactoryTable",
            setting: T.Optional["NodeListWidgetSetting"] = None,
            parent=None):
        super().__init__(parent=parent)
        if setting is None:
            setting = NodeListWidgetSetting()
        self.setting = setting
        self._init_ui()
        self.node_factory_table = node_factory_table
        self.update_list()

    def _get_ordered_node_factories(
            self, thresh_ratio: float = 0.5
            ) -> T.List[T.Type["NodeFactory"]]:
        search_text = self.search_line_edit.text()
        if search_text == "":
            return sorted(
                self.node_factory_table.table.values(),
                key=lambda x: x.type_name()
            )
        else:
            # sort by similarity with search text
            factories = []
            lens_lcs = []
            for factory in self.node_factory_table.table.values():
                len_lcs = lcs_length(
                    search_text.lower(), factory.type_name().lower())
                if (len_lcs / len(search_text)) > thresh_ratio:
                    lens_lcs.append(len_lcs)
                    factories.append(factory)
            if len(factories) == 0:
                return []
            lens_lcs, factories = zip(*sorted(
                zip(lens_lcs, factories),
                key=lambda x: x[0],
                reverse=True,
            ))
            return list(factories)

    def update_list(self) -> None:
        model: QtGui.QStandardItemModel = self.list.model()
        model.clear()
        for node_factory in self._get_ordered_node_factories():
            item = QtGui.QStandardItem()
            item.setText(node_factory.type_name())
            # set color
            item.setData(
                QtGui.QColor(node_factory.theme_color),
                QtCore.Qt.ForegroundRole,  # type: ignore
            )
            item.setFont(
                QtGui.QFont(
                    self.setting.item_setting.font_family,
                    self.setting.item_setting.font_size,
                )
            )
            item.setEditable(False)
            item.setSelectable(False)
            model.appendRow(item)

    def _init_ui(self):
        background_color = self.setting.background_color
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.setStyleSheet(
            f"background-color: {background_color};"
        )
        m = 4
        layout.setContentsMargins(m, m, m, m)
        layout.setSpacing(0)

        self.search_line_edit = SearchLine(self)
        layout.addWidget(self.search_line_edit)

        self.list = NodeListView()
        self.list.setModel(QtGui.QStandardItemModel())
        self.list.setStyleSheet(
            """
            QListView::item {{
                padding: {padding}px;
            }}
            QListView::item:hover {{
                padding: {padding}px;
            }}
            QListView {{
                border: none;
            }}
            """.format(
                padding=self.setting.item_setting.padding,
            )
        )
        layout.addWidget(self.list)
