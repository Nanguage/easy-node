import typing as T
from qtpy import QtWidgets, QtCore

if T.TYPE_CHECKING:
    from ..model.port import DataPort


class TextPortWidget(QtWidgets.QLineEdit):
    value_changed = QtCore.Signal(str)

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
        self.editingFinished.connect(self.on_editing_finished)  # type: ignore

    def on_editing_finished(self):
        self.value_changed.emit(self.text())


class IntPortWidget(QtWidgets.QSpinBox):
    value_changed = QtCore.Signal(int)

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
        self.valueChanged.connect(self.value_changed.emit)  # type: ignore


class FloatPortWidget(QtWidgets.QDoubleSpinBox):
    value_changed = QtCore.Signal(float)

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
        self.valueChanged.connect(self.value_changed.emit)  # type: ignore
