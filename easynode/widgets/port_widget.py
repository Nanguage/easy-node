import typing as T
from qtpy import QtWidgets, QtCore
from qtpy.QtCore import Qt

if T.TYPE_CHECKING:
    from ..model.port import DataPort


class PortWidget(QtWidgets.QWidget):
    value_changed = QtCore.Signal(object)

    def __init__(
            self, port: "DataPort",
            parent: T.Optional[QtWidgets.QWidget] = None,
            widget_args: T.Optional[T.Dict[str, T.Any]] = None,
            ) -> None:
        super().__init__(parent)
        self.port = port
        self.setting = port.setting.widget_setting
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.widget = self.get_widget(**(widget_args or {}))
        self.layout().addWidget(self.widget)
        self.setFixedHeight(int(self.setting.height))
        self.setFixedWidth(int(self.setting.width))

    def get_widget(self, **kwargs) -> QtWidgets.QWidget:  # type: ignore
        pass

    @property
    def value(self) -> T.Any:
        pass

    @value.setter
    def value(self, value: T.Any):
        pass


class TextPortWidget(PortWidget):
    def __init__(
            self,
            port: "DataPort",
            widget_args: T.Optional[T.Dict[str, T.Any]] = None,
            parent: T.Optional[QtWidgets.QWidget] = None,
            ) -> None:
        super().__init__(port, parent=parent, widget_args=widget_args)
        self.widget: QtWidgets.QLineEdit

    def get_widget(self, **kwargs) -> QtWidgets.QLineEdit:
        widget = QtWidgets.QLineEdit(**kwargs)
        widget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.NoContextMenu)
        widget.editingFinished.connect(  # type: ignore
            self.on_editing_finished)
        if self.port.data_default is not None:
            assert isinstance(self.port.data_default, str)
            widget.setText(self.port.data_default)
        return widget

    def on_editing_finished(self):
        self.value_changed.emit(self.value)

    @property
    def value(self) -> str:
        return self.widget.text()

    @value.setter
    def value(self, value: str):
        self.widget.setText(value)


class IntPortWidget(PortWidget):
    def __init__(
            self,
            port: "DataPort",
            widget_args: T.Optional[T.Dict[str, T.Any]] = None,
            parent: T.Optional[QtWidgets.QWidget] = None,
            ) -> None:
        super().__init__(port, parent=parent, widget_args=widget_args)
        self.widget: QtWidgets.QSpinBox

    def get_widget(self, **kwargs) -> QtWidgets.QSpinBox:
        widget = QtWidgets.QSpinBox(**kwargs)
        widget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.NoContextMenu)
        if self.port.data_default is not None:
            assert isinstance(self.port.data_default, int)
            widget.setValue(self.port.data_default)
        if self.port.data_range is not None:
            data_range = self.port.data_range
            assert isinstance(data_range, tuple)
            widget.setRange(data_range[0], data_range[1])
        else:
            max_int = 2 ** 31 - 1
            widget.setRange(-max_int, max_int)
        widget.valueChanged.connect(  # type: ignore
            self.value_changed.emit)
        return widget

    @property
    def value(self) -> int:
        return self.widget.value()

    @value.setter
    def value(self, value: int):
        self.widget.setValue(value)


class FloatPortWidget(PortWidget):
    def __init__(
            self,
            port: "DataPort",
            widget_args: T.Optional[T.Dict[str, T.Any]] = None,
            parent: T.Optional[QtWidgets.QWidget] = None,
            ) -> None:
        super().__init__(port, parent=parent, widget_args=widget_args)
        self.widget: QtWidgets.QDoubleSpinBox

    def get_widget(self, **kwargs) -> QtWidgets.QDoubleSpinBox:
        widget = QtWidgets.QDoubleSpinBox(**kwargs)
        widget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.NoContextMenu)
        if self.port.data_default is not None:
            assert isinstance(self.port.data_default, float)
            widget.setValue(self.port.data_default)
        if self.port.data_range is not None:
            data_range = self.port.data_range
            assert isinstance(data_range, tuple)
            widget.setRange(data_range[0], data_range[1])
        else:
            widget.setRange(float("-inf"), float("inf"))
        widget.valueChanged.connect(  # type: ignore
            self.value_changed.emit)
        return widget

    @property
    def value(self) -> float:
        return self.widget.value()

    @value.setter
    def value(self, value: float):
        self.widget.setValue(value)
