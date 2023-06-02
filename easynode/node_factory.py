import typing as T

from qtpy import QtWidgets

from .model import Node, Port
from .setting import NodeItemSetting


class NodeFactory(object):
    _count = 0
    theme_color = "#000000"
    input_ports: T.List[Port] = []
    output_ports: T.List[Port] = []

    def __init__(self):
        pass

    @classmethod
    def type_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_widget(cls) -> T.Optional[QtWidgets.QWidget]:
        return None

    @classmethod
    def create_node(cls) -> Node:
        cls._count += 1
        input_ports = [
            port.blueprint_copy() for port in cls.input_ports
        ]
        output_ports = [
            port.blueprint_copy() for port in cls.output_ports
        ]
        return Node(
            name=str(cls._count),
            type_name=cls.type_name(),
            input_ports=input_ports,
            output_ports=output_ports,
            widget=cls.get_widget(),
            item_setting=NodeItemSetting(
                title_area_color=cls.theme_color
            )
        )


class NodeFactoryTable(object):
    def __init__(self) -> None:
        self.table: T.Dict[str, T.Type[NodeFactory]] = {}

    def register(self, factory: T.Type[NodeFactory]) -> None:
        self.table[factory.type_name()] = factory
