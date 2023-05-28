import typing as T
import os.path as osp

from qtpy import QtWidgets

from .widgets.scene import GraphicsScene
from .widgets.view import GraphicsView
from .setting import EditorSetting


HERE = osp.dirname(osp.abspath(__file__))
DEFAULT_STYLE_SHEET = osp.join(HERE, "qss/default.qss")


class NodeEditor(QtWidgets.QWidget):
    def __init__(
            self,
            parent: T.Optional[QtWidgets.QWidget] = None,
            setting: T.Optional[EditorSetting] = None,
            style_sheet: T.Optional[str] = None,
            ) -> None:
        super().__init__(parent)
        if setting is None:
            setting = EditorSetting()
        self.setting = setting
        self.init_layout()
        if style_sheet is None:
            style_sheet = DEFAULT_STYLE_SHEET
        self.load_style_sheet(style_sheet)

    def init_layout(self):
        self.resize(800, 600)
        self.setWindowTitle("EasyNode")

        self.scene = GraphicsScene(self)
        self.scene.editor = self

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.view = GraphicsView(self.scene, self)
        self.layout.addWidget(self.view)

    def load_style_sheet(self, path: str):
        with open(path, "r") as f:
            app = QtWidgets.QApplication.instance()
            app.setStyleSheet(f.read())  # type: ignore
