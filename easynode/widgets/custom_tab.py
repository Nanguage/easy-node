"""
reference:
    https://stackoverflow.com/a/8718039/8500469
"""

from qtpy import QtWidgets
from qtpy import QtCore


class TabBar(QtWidgets.QTabBar):
    def __init__(self, parent):
        super().__init__(parent)
        self._editor = QtWidgets.QLineEdit(self)
        self._editor.setWindowFlags(QtCore.Qt.Popup)
        self._editor.setFocusProxy(self)
        self._editor.setStyleSheet(
            "QLineEdit {color: white;}"
        )
        self._editor.editingFinished.connect(self.handleEditingFinished)
        self._editor.installEventFilter(self)

    def eventFilter(self, widget, event):
        if ((event.type() == QtCore.QEvent.MouseButtonPress and
             not self._editor.geometry().contains(event.globalPos())) or
            (event.type() == QtCore.QEvent.KeyPress and
             event.key() == QtCore.Qt.Key_Escape)):
            self._editor.hide()
            return True
        return super().eventFilter(widget, event)

    def mouseDoubleClickEvent(self, event):
        index = self.tabAt(event.pos())
        if index >= 0:
            self.editTab(index)

    def editTab(self, index):
        rect = self.tabRect(index)
        self._editor.setFixedSize(rect.size())
        add_btn = self.parent().add_btn
        add_btn_width = add_btn.rect().width()
        new_point = self.parent().mapToGlobal(rect.topLeft())
        new_point.setX(new_point.x() + add_btn_width)
        self._editor.move(new_point)
        self._editor.setText(self.tabText(index))
        if not self._editor.isVisible():
            self._editor.show()

    def handleEditingFinished(self):
        index = self.currentIndex()
        if index >= 0:
            self._editor.hide()
            self.setTabText(index, self._editor.text())


tab_widget_style = """
QWidget {
    font-size: 16px;
}

QPushButton {
    font-size: 20px;
    font-weight: bold;
}
"""


class CustomTabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.min_closeable = 1
        self.setStyleSheet(tab_widget_style)
        self.tab_bar = TabBar(self)
        self.tab_bar.setVisible(True)
        self.setTabBar(self.tab_bar)
        self.add_btn = QtWidgets.QPushButton("+")
        self.add_btn.setToolTip("Add script")
        self.setCornerWidget(self.add_btn, QtCore.Qt.Corner.TopLeftCorner)
        self.setMovable(True)
        self.setTabsClosable(True)

    def removeTab(self, index):
        super().removeTab(index)
        if self.count() <= self.min_closeable:
            self.setTabsClosable(False)
            self.setMovable(False)

    def addTab(self, *args, **kwargs):
        if self.count() >= 1:
            self.setTabsClosable(True)
            self.setMovable(True)
        return super().addTab(*args, **kwargs)
