import typing as T
from qtpy import QtWidgets

if T.TYPE_CHECKING:
    from ..model.port import DataPort


class TextPortWidget(QtWidgets.QLineEdit):
    def __init__(
            self,
            port: "DataPort",
            parent: T.Optional[QtWidgets.QWidget] = None,
            **kwargs,
            ) -> None:
        super().__init__(parent, **kwargs)
        self.port = port
        self.setting = port.setting.widget_setting
        self.setFixedHeight(int(self.setting.height))
        self.setFixedWidth(int(self.setting.width))
        if port.data_default is not None:
            assert isinstance(port.data_default, str)
            self.setText(port.data_default)


class IntPortWidget(QtWidgets.QSpinBox):
    def __init__(
            self,
            port: "DataPort",
            parent: T.Optional[QtWidgets.QWidget] = None,
            **kwargs,
            ) -> None:
        super().__init__(parent, **kwargs)
        self.port = port
        self.setting = port.setting.widget_setting
        self.setFixedHeight(int(self.setting.height))
        self.setFixedWidth(int(self.setting.width))
        if port.data_default is not None:
            assert isinstance(port.data_default, int)
            self.setValue(port.data_default)
        if port.data_range is not None:
            assert isinstance(port.data_range, tuple)
            self.setRange(port.data_range[0], port.data_range[1])
        else:
            max_int = 2 ** 31 - 1
            self.setRange(-max_int, max_int)


class FloatPortWidget(QtWidgets.QDoubleSpinBox):
    def __init__(
            self,
            port: "DataPort",
            parent: T.Optional[QtWidgets.QWidget] = None,
            **kwargs,
            ) -> None:
        super().__init__(parent, **kwargs)
        self.port = port
        self.setting = port.setting.widget_setting
        self.setFixedHeight(int(self.setting.height))
        self.setFixedWidth(int(self.setting.width))
        if port.data_default is not None:
            assert isinstance(port.data_default, float)
            self.setValue(port.data_default)
        if port.data_range is not None:
            assert isinstance(port.data_range, tuple)
            self.setRange(port.data_range[0], port.data_range[1])
        else:
            self.setRange(-float('inf'), float('inf'))
