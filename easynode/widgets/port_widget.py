import typing as T
from qtpy import QtWidgets

if T.TYPE_CHECKING:
    from ..model.port import DataPort


class TextPortWidget(QtWidgets.QLineEdit):
    def __init__(
            self,
            port: "DataPort",
            parent: T.Optional[QtWidgets.QWidget] = None,
            ) -> None:
        super().__init__(parent)
        self.setting = port.setting.widget_setting
        self.setFixedHeight(int(self.setting.height))
        self.setFixedWidth(int(self.setting.width))
        self.setStyleSheet("background-color: white;")
        if port.data_default is not None:
            assert isinstance(port.data_default, str)
            self.setText(port.data_default)
