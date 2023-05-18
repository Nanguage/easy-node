import typing as T
from dataclasses import dataclass


@dataclass
class NodeViewSetting:
    title_color: str = "#ffffff"
    title_font_size: float = 10
    title_padding: float = 5.0
    title_area_height: float = 24.0
    title_area_color: str = "#FF33363"
    background_color: str = "#E0222222"
    default_width: float = 200.0
    outline_radius: float = 10.0
    outline_width: float = 2.0
    outline_color: str = "#7F000000"  # alpha, R, G, B
    outline_color_selected: str = "#FFFFA637"


@dataclass
class GraphicsViewSetting:
    antialiasing: bool = True
    default_slider_position: T.Tuple[int, int] = (1, 1)
    hidden_sliders: bool = True
    full_view_update: bool = True
    zoom_in_factor: float = 1.25
    zoom_step: int = 1
    zoom_range: T.Tuple[int, int] = (0, 10)


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
