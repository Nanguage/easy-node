
class Port():
    def __init__(self, name: str) -> None:
        self.name = name


class DataPort(Port):
    def __init__(
            self, name: str,
            data_type: type = object,
            data_range: object = None,
            data_default: object = None) -> None:
        super().__init__(name)
        self.data_type = data_type
        self.data_range = data_range
        self.data_default = data_default
