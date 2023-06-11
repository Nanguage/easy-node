import typing as T
from dataclasses import dataclass, field


@dataclass
class GraphicsSceneSetting:
    width: int = 8000
    height: int = 8000
    background_color: str = "#393939"
    draw_grid: bool = True
    grid_size: int = 25
    grid_color_dense: str = "#2f2f2f"
    grid_color_loose: str = "#191919"
    grid_loose_per_dense: int = 4


@dataclass
class GraphicsViewSetting:
    antialiasing: bool = True
    open_gl: bool = False
    default_slider_position: T.Tuple[int, int] = (1, 1)
    hidden_sliders: bool = True
    full_view_update: bool = False
    zoom_in_factor: float = 1.25
    zoom_step: int = 1
    zoom_range: T.Tuple[int, int] = (0, 10)
    node_list_widget_height: int = 300
    undo_limit: int = 100


@dataclass
class PortItemSetting:
    radius: int = 6
    color_background: str = "#E057AEFF"
    color_background_connected: str = "#FFFF8800"
    color_background_hover: str = "#FFFFF637"
    outline_width: int = 2
    color_outline: str = "#FF000000"


@dataclass
class PortWidgetSetting:
    width: int = 70
    height: int = 25


@dataclass
class PortSetting:
    item_setting: PortItemSetting = PortItemSetting()
    widget_setting: PortWidgetSetting = PortWidgetSetting()
    height: int = 30
    label_font_family: str = "Arial"
    label_font_size: int = 11
    space_between_in_and_out: int = 20


@dataclass
class NodeItemSetting:
    title_color: str = "#FFFFFF"
    title_font_size: int = 10
    title_font_family: str = "Arial"
    title_padding: int = 5
    title_area_height: int = 24
    title_area_color: str = "#F0000000"
    status_bar_height: int = 3
    status_to_color: T.Dict[str, str] = field(
        default_factory=lambda: {
            "normal": "#E057AEFF",
            "running": "#E0FFA500",
            "error": "#E0FF0000",
        })
    background_color: str = "#E0222222"
    default_width: int = 200
    outline_radius: int = 0
    outline_width: int = 2
    outline_color: str = "#7F000000"  # alpha, R, G, B
    outline_color_selected: str = "#FFFFA637"
    port_setting: PortSetting = PortSetting()
    space_between_title_and_content: int = 4


@dataclass
class EdgeItemSetting:
    color: str = "#FFFFFFFF"
    color_selected: str = "#FFFFA637"
    style: str = "dotted"  # solid, dashed, dotted
    style_selected: str = "solid"
    width: int = 2
    width_selected: int = 2
    bazel: bool = True


@dataclass
class NodeListItemSetting:
    font_family: str = "Arial"
    font_size: int = 12
    padding: int = 6


@dataclass
class NodeListWidgetSetting:
    item_setting: NodeListItemSetting = NodeListItemSetting()
    background_color: str = "#EE111111"
    margin: int = 4
    search_line_edit_height: int = 25
    search_line_edit_background_color: str = "#EE222222"
    search_line_edit_font_size: int = 18


@dataclass
class EditorSetting:
    graphics_scene_setting: GraphicsSceneSetting = GraphicsSceneSetting()
    graphics_view_setting: GraphicsViewSetting = GraphicsViewSetting()
    node_item_setting: NodeItemSetting = NodeItemSetting()
    edge_item_setting: EdgeItemSetting = EdgeItemSetting()
    edge_drag_item_setting: EdgeItemSetting = EdgeItemSetting()
